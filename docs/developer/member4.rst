Parts Implemented by Zehra ÖZER
===============================

TABLES
======

Announcement Table
------------------
   ID attribute holds the primary key of the announcement table.

   CREATE TABLE ANNOUNCEMENT (
      | ID SERIAL PRIMARY KEY,
      | TITLE VARCHAR(40),
      | TEXT VARCHAR(80)
      | )


Category Table
--------------
   ID attribute holds the primary key of the category table.

   CREATE TABLE CATEGORY (
      | ID SERIAL PRIMARY KEY,
      | TITLE VARCHAR(40),
      | TYPEE VARCHAR(30)
      | )

Topic Table
-----------
   ID attribute holds the primary key of the topic table.
   | CATEGORYID attribute references to the ID attribute in the CATEGORY table.

   CREATE TABLE CATEGORY (
      | ID SERIAL PRIMARY KEY,
      | TITLE VARCHAR(40),
      | TEXT VARCHAR(40),
      | CURTIME VARCHAR(20),
      | CATEGORYID INTEGER REFERENCES CATEGORY ON DELETE CASCADE
      | )


SOFTWARE DESIGN
===============

Class Definitions
-----------------

   - For announcement, category and topic classes, class definitions and constructors are implemented as
   announcement.py, category.py and topic.py.

Interfaces
----------

   - For interfaces,
      -  announcement.html, announcements.html, announcement_edit.html
      -  category.html, categories.html, category_edit.html
      -  topic.html, topics.html, topic_edit.html
      pages are implemented.

DATABASE OPERATIONS
===================

Announcement Class Operations
-----------------------------

* Add operation:add_announcement operation takes an announcement object as parameter related to the requested page and
         insert a new row into the announcement table.
         | INSERT INTO ANNOUNCEMENT (TITLE, TEXT) VALUES (%s, %s) RETURNING ANNOUNCEMENT.ID

* Delete operation:delete_announcement operation takes a key as parameter related to the requested page and
         deletes the row from the announcement table that includes the taken key.
         | DELETE FROM ANNOUNCEMENT WHERE (ID = %s)

* Get operation: get_announcement operation takes a key as parameter related to the requested page and
         selects the row from the announcement table that includes the taken key,
         then returns the found announcement to the user.
         | SELECT TITLE, TEXT FROM ANNOUNCEMENT WHERE (ID = %s)

* Get List Operation: get_announcements operation does not take any argument. It selects all rows from the
         announcement table and returns announcements to the user.
         | SELECT * FROM ANNOUNCEMENT ORDER BY ID

* Search Operation:search_announcement operation takes a key as parameter related to the requested page and
         selects the rows from the announcement table that include the key parameter in the
         specified columns.
         | SELECT * FROM ANNOUNCEMENT WHERE (TITLE ILIKE %s OR TEXT ILIKE %s)

* Update Operation:update_announcement operation takes a key and related fields that are wanted to update that is
         related to the requested page. Then, the rows including the key are selected and the requested
         fields are updated in the announcement table.
         | UPDATE ANNOUNCEMENT SET TITLE = %s, TEXT = %s WHERE (ID = %s)


Category Class Operation
------------------------
* Add operation:add_category operation takes a category object as parameter related to the requested page and
         insert a new row into the category table.
         | INSERT INTO CATEGORY (TITLE,TYPEE) VALUES (%s,%s) RETURNING CATEGORY.ID

* Delete operation:delete_category operation takes a key as parameter related to the requested page and
         deletes the row from the category table that includes the taken key.
         | DELETE FROM CATEGORY WHERE (ID = %s)

* Get operation: get_category operation takes a key as parameter related to the requested page and
         selects the row from the category table that includes the taken key,
         then returns the found category to the user.
         | SELECT TITLE,TYPEE FROM CATEGORY WHERE (ID = %s)

* Get List Operation: get_categories operation does not take any argument. It selects all rows from the
         category table and returns categories to the user.
         | SELECT * FROM CATEGORY ORDER BY ID

* Search Operation:search_category operation takes a key as parameter related to the requested page and
         selects the rows from the category table that include the key parameter in the
         specified columns.
         | SELECT * FROM CATEGORY WHERE (TITLE ILIKE %s OR TYPEE ILIKE %s)

* Update Operation:update_category operation takes a key and related fields that are wanted to update that is
         related to the requested page. Then, the rows including the key are selected and the requested
         fields are updated in the category table.
        | UPDATE CATEGORY SET TITLE = %s, TYPEE= %s WHERE (ID = %s))



Topic Class Operation
---------------------
* Add operation:add_topic operation takes a topic object as parameter related to the requested page and
         insert a new row into the topic table.
         | INSERT INTO TOPIC (TITLE,TEXT,CURTIME, CATEGORYID) VALUES (%s,%s,%s,%s) RETURNING TOPIC.ID

* Delete operation:delete_topic operation takes a key as parameter related to the requested page and
         deletes the row from the topic table that includes the taken key.
         | DELETE FROM TOPIC WHERE (ID = %s)

* Get operation: get_topic operation takes a key as parameter related to the requested page and
         selects the row from the topic table that includes the taken key,
         then returns the found topic to the user.
         | SELECT TITLE, TEXT, CURTIME,CATEGORYID FROM TOPIC WHERE (ID = %s)

* Get List Operation: get_topics operation does not take any argument. It selects all rows from the
         topic table and returns topics to the user.
         | SELECT * FROM TOPIC ORDER BY ID

* Search Operation:search_topic operation takes a key as parameter related to the requested page and
         selects the rows from the topic table that include the key parameter in the
         specified columns.
         | SELECT * FROM TOPIC WHERE (TITLE ILIKE %s OR TEXT ILIKE %s)

* Update Operation:update_topic operation takes a key and related fields that are wanted to update that is
         related to the requested page. Then, the rows including the key are selected and the requested
         fields are updated in the topic table.
         | UPDATE TOPIC SET TITLE = %s, TEXT = %s, CURTIME = %s, CATEGORYID = %s WHERE (ID = %s)
