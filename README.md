# bo

## overview
imaginary e-shop. Your task is to create an endpoint that, for a given date, will return a report that will contain the following metrics.
* The total number of items sold on that day.
* The total number of customers that made an order that day.
* The total amount of discount given that day.
* The average discount rate applied to the items sold that day.
* The average order total for that day
* The total amount of commissions generated that day.
* The average amount of commissions per order for that day.
* The total amount of commissions earned per promotion that day.

written with Python 3.7.6, Flask 1.1.1, Werkzeug 1.0.0 & SQLite version 3.28.0 
## Assumptions
* i am assuming you are running on a mac with catalina with python installed and sqlite3 installed
## database creation & importing the data
* run the initdb - this will create directory instances
* at the command line cd into instances - there will be a file bo.sqlite
* run sqlite3 to get the prompt sqlite>
* then run the following
* sqlite> .open bo.sqlite
* sqlite> .tables
    * this will give you a list of the created tables
* sqlite> .mode csv
    * to tell sqlite you are importing csv files
* sqlite> .import /path-to-working-dir/file-name.csv tablename
    * on my system it looks like this
    * sqlite> .import /Users/jmhowitt/PycharmProjects/suade/csvdata/promotions.csv promotions
* do this for all six tables
    * commissions
    * orders
    * products
    * order_lines
    * product_promotions
    * promotions
* n.b. this method imports all the line even if the first line are the column header. because of this with the sample data i have removed the column heads.
* 
* 

## tests
There are four basic tests for the main code, one basic api call and two for the database connections
## how to use
/bonjour
just gives you a reply to make sure the api is functioning

/bo?date=yyyy-mm-dd
passing a date in the yyyy-mm-dd between 2019-08-01 and 2019-09-29 will return a json report

## if i had had more time/production environment
• would have used sqlalchemy for obvious reasons and i would have used Alembic to manage  the tables development.
• i would have written and import routine for the databases to import the csv's
* would have solit the code out to more modules
* would have used gRPC and protobuf instead of REST
* was just running out of time