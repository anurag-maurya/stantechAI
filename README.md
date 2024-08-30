# stantechAI
This is StantechAI python assignment solution

Assignment 1: SQL Assignment
sql_assignment.sql file contain the query for this assignment solution.

Assignment 2: Python Assignment
data-> data folder has 2 files products.csv and summary_report.csv
products.csv has dummy data and summary_report.csv is the solution summary report


Django web framework is used to solve this assignment.

database used: SQLite3(default databse of Django)
ORM used: Django built in ORM
task 1: user signup and login endpoints:
users app is created to complete this task and 2 endpoints /api/signup, /api/login is created in the same app

signup:
method: POST
url: /api/signup
request body:
{
    "username": "testuser2",
    "password": "testpassword2"
}

response:
{
    "message": "User created successfully"
}

login:
method: POST
url: /api/login
request body:
{
    "username": "testuser2",
    "password": "testpassword2"
}
response:
{
    "refresh": "eyJhbGciOixxxxxxxxxx",
    "access": "eyJhbGciOiJxxxxxxxxxx"
}

Task 2: load data from products.csv | sanitize data | dump into database | create summary_report
2 endpoints are created to solve this task

loaddata:
Method: POST
url: /api/products/loaddata
it will get the products.csv fro /data/products.csv file and create dataframe from it,
it will sanitize and add missing values and write the data into Product table

createsummary:
Method: GET
url: /api/products/createsummary
it will get the data from product table and generate summary from that data and write into summary_report.csv inside data folder

connect to me to get more about it:
myanurag0202@gmail.com