# -*- coding: utf-8 -*-
# Name: pypandas
# Version: 0.1a3
# Owner: Ruslan Korniichuk

import pandas as pd


def employees_num(engine):
    """Get number of employees"""

    df = pd.read_sql_table('employees', con=engine)
    num = df.employee_id.count()
    return num


def sales_num_per_category(engine):
    """Get sales per category"""

    df1 = pd.read_sql_table('order_details', con=engine)
    df1 = df1[['order_id', 'product_id']]
    df2 = pd.read_sql_table('products', con=engine)
    df2 = df2[['product_id', 'category_id']]
    df3 = pd.merge(df1, df2, on='product_id', how='outer')
    df4 = pd.read_sql_table('categories', con=engine)
    df4 = df4[['category_id', 'category_name']]
    df5 = pd.merge(df3, df4, on='category_id', how='outer')
    df5 = df5[['order_id', 'category_name']].drop_duplicates()
    tmp = df5.groupby(['category_name']).count()['order_id']
    tmp = tmp.to_frame(name='orders').sort_values(['orders'], ascending=False)
    result = tmp.to_dict()['orders']
    return result


def sales_num_per_region(engine):
    """Get total sales per region"""

    df = pd.read_sql_table('orders', con=engine)
    tmp = df.groupby(['ship_region']).count()['order_id']
    tmp = tmp.to_frame(name='orders').sort_values(['orders'], ascending=False)
    result = tmp.to_dict()['orders']
    return result


def statistics_per_year(engine):
    """Get sales_overview for each year.

    Total sales, total products sold, best customer country,
    best selling category.
    """

    data = {}
    data['year'] = []
    data['sales_num'] = []
    data['products_num_sold'] = []
    data['top_country'] = []
    data['top_category'] = []

    df1 = pd.read_sql_table('order_details', con=engine)
    df2 = pd.read_sql_table('orders', con=engine)
    df3 = pd.merge(df1, df2, on='order_id', how='outer')
    df4 = pd.read_sql_table('products', con=engine)
    df5 = pd.merge(df3, df4, on='product_id', how='outer')
    df6 = pd.read_sql_table('categories', con=engine)
    df7 = pd.merge(df5, df6, on='category_id', how='outer')
    df7 = df7[['order_id', 'order_date', 'quantity', 'unit_price_x',
               'ship_country', 'category_name']]
    df7['year'] = df7.order_date.dt.year

    years = sorted(df7.year.unique())
    for year in years:
        data['year'].append(year)
        num = len(df7[df7.year == year]['order_id'].unique())
        data['sales_num'].append(num)
        num = df7[df7.year == year].quantity.sum()
        data['products_num_sold'].append(num)
        value = df7[df7.year == year].groupby(['ship_country']) \
            .count()['order_id'].to_frame(name='orders') \
            .sort_values(['orders'], ascending=False).head(1).index[0]
        data['top_country'].append(value)
        value = df7[df7.year == year].groupby(['category_name']) \
            .count()['order_id'].to_frame(name='orders') \
            .sort_values(['orders'], ascending=False).head(1).index[0]
        data['top_category'].append(value)
    return data


def suppliers_num(engine):
    """Get number of suppliers"""

    df = pd.read_sql_table('suppliers', con=engine)
    num = df.supplier_id.count()
    return num


def top_countries(engine, limit=5):
    """Get top selling countries, sales per country"""

    df = pd.read_sql_table('orders', con=engine)
    tmp = df.groupby(['ship_country']).count()['order_id']
    tmp = tmp.to_frame(name='orders').sort_values(['orders'], ascending=False)
    tmp = tmp.head(limit)
    result = tmp.to_dict()['orders']
    return result


def top_sale_representatives(engine, limit=3):
    """Get top sale representatives.

     Total sales volume, total discount given.
    """

    df1 = pd.read_sql_table('order_details', con=engine)
    df1 = df1[['order_id', 'unit_price', 'quantity', 'discount']]
    df2 = pd.read_sql_table('orders', con=engine)
    df2 = df2[['order_id', 'employee_id']]
    df3 = pd.merge(df1, df2, on='order_id', how='outer')
    df4 = pd.read_sql_table('employees', con=engine)
    df4 = df4[['employee_id', 'last_name']]
    df5 = pd.merge(df3, df4, on='employee_id', how='outer')
    df5['sales_volume'] = df5.unit_price * df5.quantity * (1 - df5.discount)
    df5['discount_volume'] = df5.unit_price * df5.quantity * df5.discount
    df5 = df5.round(2)
    tmp = df5.groupby(['last_name']).sum()[['sales_volume', 'discount_volume']]
    tmp = tmp.sort_values(['sales_volume'], ascending=False).head(limit)
    result = tmp.round(2).to_dict('index')
    return result


def units_num(engine):
    """Get total number of units in inventory"""

    df = pd.read_sql_table('products', con=engine)
    num = df.units_in_stock.sum()
    return num


def units_total_price(engine):
    """Get total price of units in inventory"""

    df = pd.read_sql_table('products', con=engine)
    df['price'] = df.unit_price * df.units_in_stock
    total_price = df.price.sum()
    return total_price
