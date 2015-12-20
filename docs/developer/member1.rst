Parts Implemented by Miyase Tekpınar
================================

Tables
======

- All queries create a table if not exists that holds id as a primary key and username that reference to username of members table,
only if a user trigger to "/intdb".


**CycRoute Table**
-------------------


CREATE TABLE IF NOT EXISTS CYCROUTE (
                ID SERIAL PRIMARY KEY,
                TITLE VARCHAR(40) UNIQUE,
                USERNAME VARCHAR(40),
                START VARCHAR(40),
                FINISH VARCHAR(10),
                LENGTH FLOAT,
                DATE DATE DEFAULT current_timestamp)


ALTER TABLE CYCROUTE ADD  FOREIGN KEY(USERNAME) REFERENCES MEMBERS(USERNAME) ON DELETE CASCADE

Bike Table
-----------


CREATE TABLE IF NOT EXISTS BIKE (
                ID SERIAL PRIMARY KEY,
                MODEL VARCHAR(40),
                BRAND VARCHAR(40),
                TYPE VARCHAR(40),
                SIZE VARCHAR(10),
                YEAR VARCHAR(10),
                PRICE FLOAT,
                USERNAME VARCHAR(40) unique ,
                DATE DATE DEFAULT current_timestamp
                )
                
ALTER TABLE BIKE ADD  FOREIGN KEY(USERNAME) REFERENCES MEMBERS(USERNAME) ON DELETE CASCADE 

Experience Table
----------------

CREATE TABLE IF NOT EXISTS EXPERIENCE (
                ID SERIAL PRIMARY KEY,
                TITLE VARCHAR(40),
                USERNAME VARCHAR(40),
                START VARCHAR(40),
                FINISH VARCHAR(10),
                PERIOD FLOAT,
                LENGTH FLOAT,
                USERID INTEGER,
                DATE DATE DEFAULT current_timestamp
                )
                
ALTER TABLE EXPERIENCE ADD  FOREIGN KEY(USERNAME) REFERENCES MEMBERS(USERNAME) ON DELETE CASCADE

-TOPMEMBERS table holds best five users.
CREATE TABLE IF NOT EXISTS TOPMEMBERS (ID SERIAL PRIMARY KEY,USERID INTEGER,COUNT INTEGER)

Software Design
===================

- For all tables, a class created.
- cycroute.py, bike.py and experience.py includes definitions of constructors.
- cycroute_view.py,bike_view.py and experience_view.py includes functions that link html files and database.
- 'session' library are imported to hold current user and 'redirect', 'render_template', 'request' and 'url_for' libraries are imported from flask for connection of html files. 

  cycroute_view.py
  ----------------
  
  
  

Database Operations
===================
Theese operations are defined in 'store.py' for all related tables.

- add_nameofclass(self, nameofclass): Add functions get a object  as a parameter and include that query:
  INSERT INTO NAMEOFCLASS (COLUMN1,COLUMN2,..) VALUES (ATTRIBUTE1, ATTRIBUTE2,...) RETURNING NAMEOFCLASS.ID
  This query's parameters are attributes of the object and it add a new row to related table.
  
- delete_nameofclass(self, key): Delete functions get a id as a parameter an include that query:
  DELETE FROM NAMEOFCLASS WHERE (ID = key)

- get_nameofclass(self,key): This function gets a id as a parameter and returns a object that is created by using selected attributes.
  SELECT [ATTRIBUTE1, ATTRIBUTE2,...] FROM EXPERIENCE WHERE (ID = key)
  
- get_(nameofclass)s(self) : This function returns a list of related objects by creating a array from table using that query:
  SELECT * FROM NAMEOFCLASS ORDER BY ID
  
-update_activity(self, key, attribute1, attribute2,..):This function gets attributes of related object and update related row in table.UPDATE NAMEOFCLASS SET ATTRIBUTE1 =attribute1, ATTRIBUTE2 = attribute2,.. WHERE (ID = key)
  
-search_nameofclass(self,keyword): This function searches keyword into related table and returns a list of results of that query:
 SELECT * FROM NAMEOFCLASS WHERE (ATTRIBUTE1 ILIKE '%'+keyword+'%' OR ATTRIBUTE2 ILIKE '%'+keyword+'%' OR ..)
  






