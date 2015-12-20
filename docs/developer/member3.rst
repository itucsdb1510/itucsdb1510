Parts Implemented by Esin Ersoğan
=================================

TABLES
======

Team Table
----------
   ID attribute holds the primary key of the team table.
   | FOUNDER attribute references to the ID attribute in the MEMBERS table.

   CREATE TABLE TEAM (
      | ID SERIAL PRIMARY KEY,
      | NAME VARCHAR(80),
      | SCORE INTEGER,
      | FOUNDER INTEGER ,
      | MEMBER_COUNT INTEGER,
      | YEAR INTEGER,
      | TEAMTYPE VARCHAR(80),
      | LOCATION VARCHAR(80)
      | )

   |ALTER TABLE TEAM ADD  FOREIGN KEY(FOUNDER) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE

Race Table
----------

   ID attribute holds the primary key of the race table.
   | FOUNDERID attribute references to the ID attribute in the MEMBERS table.
   | CYCROUTEID attribute references to the TITLE attribute in the CYCROUTE table.

   CREATE TABLE RACE (
       | ID SERIAL PRIMARY KEY,
       | TITLE VARCHAR(40),
       | RACE_TYPE VARCHAR(40),
       | FOUNDERID INTEGER,
       | PARTICIPANT_COUNT INTEGER,
       | TIME VARCHAR(40),
       | CYCROUTEID VARCHAR(40)
       )

   ALTER TABLE RACE ADD  FOREIGN KEY(FOUNDERID) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE
   ALTER TABLE RACE ADD  FOREIGN KEY(CYCROUTEID) REFERENCES CYCROUTE(TITLE) ON DELETE CASCADE

Race Results Table
------------------

   ID attribute holds the primary key of the race table.
   MEMBERID attribute references to the ID attribute in the MEMBERS table.
   RACEID attribute references to the ID attribute in the RACE table.

  CREATE TABLE RACE_RESULTS (
       ID SERIAL PRIMARY KEY,
       MEMBERID INTEGER ,
       RACEID INTEGER,
       ORD INTEGER
       )

   ALTER TABLE RACE_RESULTS ADD  FOREIGN KEY(MEMBERID) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE
   ALTER TABLE RACE_RESULTS ADD  FOREIGN KEY(RACEID) REFERENCES RACE(ID) ON DELETE CASCADE

Activity Table
--------------

   ID attribute holds the primary key of the activity table.
   FOUNDERID attribute references to the ID attribute in the MEMBERS table.

   CREATE TABLE ACTIVITY (
       ID SERIAL PRIMARY KEY,
       TITLE VARCHAR(40),
       ACTIVITY_TYPE VARCHAR(40),
       FOUNDERID INTEGER ,
       PARTICIPANT_COUNT INTEGER,
       TIME VARCHAR(40),
       PLACE VARCHAR(40),
       ACTIVITY_INFO VARCHAR(150)
       )

    ALTER TABLE ACTIVITY ADD  FOREIGN KEY(FOUNDERID) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE

Activity Members Table
----------------------

   ID attribute holds the primary key of the race table.
   MEMBERID attribute references to the ID attribute in the MEMBERS table.
   ACTIVITYID attribute references to the ID attribute in the ACTIVITY table.

   CREATE TABLE ACTIVITY_MEMBERS (
                ID SERIAL PRIMARY KEY,
                MEMBERID INTEGER,
                ACTIVITYID INTEGER
                )

   ALTER TABLE ACTIVITY_MEMBERS ADD  FOREIGN KEY(MEMBERID) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE
   ALTER TABLE ACTIVITY_MEMBERS ADD  FOREIGN KEY(ACTIVITYID) REFERENCES ACTIVITY(ID) ON DELETE CASCADE

SOFTWARE DESIGN
===============

Class Definitions
-----------------

   - For team, race and avtivity classes, class definitions and constructors are implemented as
   team.py, race.py and activity.py.

Interfaces
----------

   - For interfaces,
      -  team.html, teams.html, team_edit.html
      -  race.html, races.html, race_edit.html
      -  activity.html, activities.html, activity_edit.html
      pages are implemented.



DATABASE OPERATIONS
===================

Basic Operations
----------------

   - The following database operations are implemented for the team, race, and activity classes listed below:
      -Add Operation:
         add_nameofclass operation takes an object as parameter related to the requested page and
         insert a new row into the related object's table.
            INSERT INTO TEAM (NAME, SCORE, FOUNDER, MEMBER_COUNT, YEAR, TEAMTYPE, LOCATION) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING TEAM.ID
            INSERT INTO RACE (TITLE, RACE_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, CYCROUTEID) VALUES (%s, %s, %s, %s, %s, %s) RETURNING RACE.ID
            INSERT INTO ACTIVITY (TITLE, ACTIVITY_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, PLACE, ACTIVITY_INFO) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING ACTIVITY.ID

      -Delete Operation:
         delete_nameofclass operation takes a key as parameter related to the requested page and
         deletes the row from the related object's table that includes the taken key.
            DELETE FROM TEAM WHERE (ID = %s)
            DELETE FROM RACE WHERE (ID = %s)
            DELETE FROM ACTIVITY WHERE (ID = %s)

      -Get Operation:
         get_nameofclass operation takes a key as parameter related to the requested page and
         selects the row from the related object's table that includes the taken key,
         then returns the found object to the user.
            SELECT NAME, SCORE, FOUNDER, MEMBER_COUNT, YEAR, TEAMTYPE, LOCATION FROM TEAM WHERE (ID = %s)
            SELECT TITLE, RACE_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, CYCROUTEID FROM RACE WHERE (ID = %s)
            SELECT TITLE, ACTIVITY_TYPE, FOUNDERID, PARTICIPANT_COUNT,  TIME, PLACE, ACTIVITY_INFO FROM ACTIVITY WHERE (ID = %s)

      -Get List Operation:
         get_nameofclasses operation does not take any argument. It selects all rows from the
         related object's table and returns these objects to the user.
            SELECT * FROM TEAM ORDER BY ID
            SELECT * FROM RACE ORDER BY ID
            SELECT * FROM ACTIVITY ORDER BY ID

      -Search Operation:
         search_nameofclass operation takes a key as parameter related to the requested page and
         selects the rows from the related object's table that include the key parameter in the
         specified columns.
            SELECT * FROM TEAM WHERE (NAME ILIKE %s OR LOCATION ILIKE %s)
            SELECT * FROM RACE WHERE (TITLE ILIKE %s OR RACE_TYPE ILIKE %s)
            SELECT * FROM ACTIVITY WHERE (TITLE ILIKE %s OR ACTIVITY_TYPE ILIKE %s OR PLACE ILIKE %s OR ACTIVITY_INFO ILIKE %s)

      -Update Operation:
         update_nameofclass operation takes a key and related fields that are wanted to update that is
         related to the requested page. Then, the rows including the key are selected and the requested
         fields are updated in the related object's table.
            UPDATE TEAM SET NAME = %s, SCORE = %s, YEAR = %s, TEAMTYPE = %s, LOCATION = %s WHERE (ID = %s)
            UPDATE RACE SET TITLE = %s, RACE_TYPE = %s, TIME = %s, CYCROUTEID = %s WHERE (ID = %s)
            UPDATE ACTIVITY SET TITLE = %s, ACTIVITY_TYPE = %s, TIME = %s, PLACE = %s, ACTIVITY_INFO = %s WHERE (ID = %s)


Operations for Race and Race Results Tables
-------------------------------------------

    - The following database operations are implemented for the race and race_results tables:
      -When a new race is created, the founder of the race is inserted to the race_results table
      to keep the participants of the races using the following queries:
         SELECT memberid FROM MEMBERS WHERE username='%s';"%name
         INSERT INTO RACE_RESULTS (MEMBERID, RACEID ) VALUES (%s, %s)

      -When a race page is clicked for open, the following queries are executed
      for obtain the necessary informations of the page from the tables:
         SELECT memberid FROM RACE_RESULTS WHERE raceid='%s';"%key
         SELECT * FROM MEMBERS WHERE memberid='%s';"%memberid
         SELECT DISTINCT RACEID FROM RACE_RESULTS
         SELECT COUNT(ID) FROM RACE_RESULTS WHERE raceid='%s';"%i
         SELECT id FROM RACE_RESULTS WHERE raceid='%s';"%i
         UPDATE RACE_RESULTS SET ord=%s  WHERE (raceid=%s)

      -When a user clicks the join race button, the participant of the race is inserted to the race_results
      table to keep the participants of the races using the following queries:
         SELECT memberid FROM MEMBERS WHERE username='%s';"%name
         INSERT INTO RACE_RESULTS (MEMBERID, RACEID ) VALUES (%s, %s)
         SELECT participant_count FROM RACE WHERE id='%s';"%key
         UPDATE RACE SET participant_count=%s  WHERE (id=%s)

Operations for Activity and Activity Members Tables
---------------------------------------------------

   - The following database operations are implemented
      -When a new activity is created, the founder of the activity is inserted to the activity_members table
      to keep the participants of the activities using the following queries.
         SELECT memberid FROM MEMBERS WHERE username='%s';"%name
         INSERT INTO ACTIVITY_MEMBERS (MEMBERID, ACTIVITYID ) VALUES (%s, %s)

      -When an activity page is clicked for open, the following queries are executed
      for obtain the necessary informations of the page from the tables:
         SELECT memberid FROM ACTIVITY_MEMBERS WHERE activityid='%s';"%key
         SELECT * FROM MEMBERS WHERE memberid='%s';"%memberid

      -When a user clicks the join activity button, the participant of the activity is inserted to the
      activity_members table to keep the participants of the activities using the following queries:
         SELECT memberid FROM MEMBERS WHERE username='%s';"%name
         INSERT INTO ACTIVITY_MEMBERS (MEMBERID, ACTIVITYID ) VALUES (%s, %s)
         SELECT participant_count FROM ACTIVITY WHERE id='%s';"%key
         UPDATE ACTIVITY SET participant_count=%s  WHERE (id=%s)

