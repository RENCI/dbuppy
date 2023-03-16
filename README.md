# dbuppy
dbuppy is a tool written in python that automates deployment of changes to PostgreSQL databases.
It tracks list of SQL scripts that have been executed and runs those that are needed to bring your database up to date.

## **How it works**

If you have an existing database that you want to add versioning, then you need to group your SQL scripts in 2 folders: CREATE and UPDATE

![230308_111459.png](readme%2F230308_111459.png)

**CREATE** folder contains files that are needed to recreate your database schema and necessary data. This folder is used when you need to adopt dbuppy for projects with existing databases. Typically it is expected to run only once after fresh your application installation.  

**UPDATE** folder contains all scripts that need to be tracked and executed to bring your database up to date. dbuppy expects that you keep scripts intact and make all your changes by adding new scripts, NOT modifying existing or removing.


**FILENAMING**

dbuppy relies on ordered files to execute your scripts in correct order.
Suggested naming format for files: 

_**YYYYMMDD_HHMM_ScriptName.sql**_

where YYYY - year

MM - month

DD - day

HH - hours (24h format)

MM - minutes

for example: 

_**20230308_1310_AddNewColumn**_

dbuppy creates a table **_dbuppy_** inside your database.
![230308_110029.png](readme%2F230308_110029.png)
It contains:

**_scriptname_** - name of the file containing your SQL code.

**_haderror_** - true/false value indicates if executions of your script resulted in errors.

_**created**_ - timestamp that shows when this script has been executed.

**NOTE dbuppy ignores all files that start with underscore!**


## **Usage**

`main.py -host localhost -port 5455 -dbname postgres -username postgres -password 121212 -path "./path/to/sqlfiles" -action update`



## **Dependencies**:

psycopg2

python 3.11
