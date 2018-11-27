# Log Analysis - Udacity #

## System requirement and how to run it##
This project reuires a Python including a _psycopg2_ library and SQL and data in the file _newsdata.sql_ must be added to the databse and all installed on machine running ubuntu.

To run the project the user needs to run _App.py_ file and the uoutput will be displayed.

### Creating Views: ###
Because the app need to create Views we need to make sure that there are no VIEWS in the database that have the same name to prevent conflicts from happening, so we should first delete the VIEWS form the db, second create the VIEWS.

#### Deleting Views from DB ####
```SQL
DROP VIEW error_status_view
DROP VIEW percentage_view
DROP VIEW percentage_view

```

#### Creating Views ####
```SQL
CREATE OR REPLACE VIEW error_status_view	
AS
SELECT date(time),count(*) as error_views 
FROM log 
WHERE status = '404 NOT FOUND' GROUP BY 1;

CREATE OR REPLACE VIEW all_status_view 
AS 
SELECT date(time),count(*) as all_views 
FROM log 
GROUP BY 1;

CREATE OR REPLACE VIEW percentage_view 
AS 
SELECT all_status_view.date, (1.0*error_status_view.error_views / all_status_view.all_views)*100.0 AS percentage_value 
FROM error_status_view,all_status_view 
WHERE all_status_view.date = error_status_view.date 
GROUP BY 1,2
```

### What this project does ? ###
This project answers the questions in _Log Analysis_ Project with a retrived data from the _news_ database.

### References: ###
In addition to Udacity's great materials I refered to some other websites follwoing is a link to it:

- https://www.w3schools.com/
- https://www.python.org/