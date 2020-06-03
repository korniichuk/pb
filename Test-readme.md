# Test: 

You are provided with a Postgres endpoint containing a sample database of a fictional company, and this S3 bucket. 
Your code should read data from the DB and write summarized results to the S3 bucket - 2 json files, 1 csv file.


## Submission Guidelines: 

* Single zip file, containing code and Dockerfile. The file name should be your name.
* You can use the provided bucket for testing, but at time of submission please make sure only the zip file and this readme are in the bucket.
* The submission criteria is that once the Dockerfile is built and ran (docker run...), the results will appear in the bucket.
* Provide a way to configure the DB and S3 connection details (any way you see fit).


## Results Description:

#### company_overview.json

* total number of units in inventory
* total price of units in inventory
* number of suppliers
* number of employees
* top 5 selling countries, sales per country

#### sales_overview.csv:

Row for each year:

* total sales
* total products sold
* best customer country
* best selling category

#### sales_details.json:

 * total sales per region
 * sales per category
 * top 3 sale representatives, total sales volume, total discount given


## DB Connection Details: 

Endpoint: demo.cluster-ro-c3rno4vis1ue.eu-central-1.rds.amazonaws.com

Port: 5432

User: ruslan

Password: passwd





