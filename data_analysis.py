#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: data_analysis
# Version: 0.1a8
# Owner: Ruslan Korniichuk

import argparse
import json
import os
import sys

from loguru import logger
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table

import pypandas
import pys3


def convert(o):
    if isinstance(o, np.int64):
        return int(o)
    raise TypeError


if __name__ == '__main__':
    # Load arguments
    description = 'Data Analysis script'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--db', required=True, action='store', help='Database string')
    parser.add_argument(
        '--s3_bucket', required=True, action='store', metavar='BUCKET',
        help='Amazon S3 bucket bucket')
    args = parser.parse_args()
    db = args.db
    s3_bucket = args.s3_bucket

    try:
        # Configure logging
        fmt = '{time}\t{level}\t{module}\t{message}'
        logger.remove()
        logger.add(sys.stderr, format=fmt, level='DEBUG')  # DEBUG | INFO
        script_filename = os.path.basename(__file__)
        log_filename = os.path.splitext(script_filename)[0] + '.log'
        log_path = '/var/log/pb/{}'.format(log_filename)
        logger.add(log_path, format=fmt, level='INFO')  # DEBUG | INFO

        text = 'postgresql+psycopg2://{}'
        db_url = text.format(db)

        engine = create_engine(db_url)
        metadata = MetaData()
        products = Table('products', metadata, autoload=True,
                         autoload_with=engine)
        suppliers = Table('suppliers', metadata, autoload=True,
                          autoload_with=engine)
        employees = Table('employees', metadata, autoload=True,
                          autoload_with=engine)
        orders = Table('orders', metadata, autoload=True,
                       autoload_with=engine)
        order_details = Table('order_details', metadata, autoload=True,
                              autoload_with=engine)
        categories = Table('categories', metadata, autoload=True,
                           autoload_with=engine)

        data = {}
        # Total number of units in inventory
        num = pypandas.units_num(engine)
        data['units_number'] = num
        # Total price of units in inventory
        total_price = pypandas.units_total_price(engine)
        data['units_total_price'] = total_price
        # Number of suppliers
        num = pypandas.suppliers_num(engine)
        data['suppliers_number'] = num
        # Number of employees
        num = pypandas.employees_num(engine)
        data['employees_number'] = num
        # Top 5 selling countries, sales per country
        result = pypandas.top_countries(engine, limit=5)
        data['top_5_selling_countries'] = result
        # Create 'company_overview.json' file
        file_name = 'company_overview.json'
        file_path = '/tmp/{}'.format(file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f, default=convert)
        # Upload 'company_overview.json' file to S3
        result = pys3.upload_file(s3_bucket, file_path, file_name,
                                  logger=logger)

        data = {}
        # Total sales per region
        result = pypandas.sales_num_per_region(engine)
        data['sales_num_per_region'] = result
        # Sales per category
        result = pypandas.sales_num_per_category(engine)
        data['sales_num_per_category'] = result
        # Top 3 sale representatives, total sales volume, total discount given
        result = pypandas.top_sale_representatives(engine, limit=3)
        data['top_3_sale_representatives'] = result
        # Create 'sales_details.json' file
        file_name = 'sales_details.json'
        file_path = '/tmp/{}'.format(file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f, default=convert)
        # Upload 'sales_details.json' file to S3
        result = pys3.upload_file(s3_bucket, file_path, file_name,
                                  logger=logger)

        data = pypandas.statistics_per_year(engine)
        # Create 'sales_overview.csv' file
        file_name = 'sales_overview.csv'
        file_path = '/tmp/{}'.format(file_name)
        df = pd.DataFrame.from_dict(data)
        df.to_csv(file_path, index=False)
        # Upload 'sales_overview.csv' file to S3
        result = pys3.upload_file(s3_bucket, file_path, file_name,
                                  logger=logger)

        # SQLAlchemy engine disposal
        engine.dispose()
    except BaseException as e:
        logger.error(e)
        # Log 'FAILURE' status
        logger.error('Status: FAILURE')
        logger.error('Exit status: 1')
        sys.exit(1)
    else:
        # Log 'SUCCESS' status
        logger.info('Status: SUCCESS')
        logger.info('Exit status: 0')
        sys.exit(0)
