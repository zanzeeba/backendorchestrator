# bo

## overview

## Assumptions
* i am assuming you are running on a mac with catalina 
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

## how to use


## if i had had more time/production environment
• would have used sqlalchemy for obvious reasons and i would have used Alembic to manage  the tables development.
• i would have written and import routine for the databases to import the csv's