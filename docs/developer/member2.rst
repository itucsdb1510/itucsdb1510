Parts Implemented by Nurefşan Sertbaş
=====================================

TABLES
======

- In our code all create table queries creatse a table if not exists. Also, they are triggered by /initdb.
- Admin, basic user and professional user classes are implemented by this developer.
  There exists two main tables in database for this purpose and also 2 helper tables.


Admin Table
-----------

- Admin has the following attributes.
- Here role attribute is used for assisting the redirections according to being user or admin.
- There exists no any foreign key to any table.

  CREATE TABLE IF NOT EXISTS ADMIN (
             |   ID SERIAL PRIMARY KEY,
             |   NAME VARCHAR(30) NOT NULL,
             |   SURNAME VARCHAR(30),
             |   USERNAME VARCHAR(30) UNIQUE NOT NULL,
             |   EMAIL VARCHAR(30) NOT NULL,
             |   PASSWORD VARCHAR(6) NOT NULL,
             |   ROLE VARCHAR(20),
             |   YEAR NUMERIC(4)
             |   )


Member Table
------------

- Both professional and basic members have the following attributes.
- Here role attribute is again used for assisting the redirections according to being user or admin.
- In basic member
            - TEAMID column is inserted as NULL
            - MEMBERTYPE column is inserted as 0 for repersenting it is basic member
- In professional member
            - TEAMID refers to the team table
            - MEMBERTYPE column is inserted as 1 for repersenting it is professional member

  CREATE TABLE IF NOT EXISTS MEMBERS (
            |  MEMBERID SERIAL PRIMARY KEY,
            |  NAME VARCHAR(30) NOT NULL,
            |  SURNAME VARCHAR(30),
            |  USERNAME VARCHAR(30) UNIQUE NOT NULL ,
            |  GENDER VARCHAR(10) ,
            |  MEMBERTYPE NUMERIC(1) DEFAULT 0,
            |  EMAIL VARCHAR(30) NOT NULL,
            |  PASSWORD VARCHAR(6) NOT NULL,
            |  CITY VARCHAR(30),
            |  INTERESTS VARCHAR(30),
            |  SCORE INTEGER DEFAULT 0,
            |  YEAR NUMERIC(4),
            |  LASTLOGIN VARCHAR(20),
            |  REGTIME VARCHAR(20),
            |  ROLE VARCHAR(20),
            |  TEAMID INTEGER REFERENCES TEAM
            |  ON DELETE RESTRICT
            |  )


Additional Tables
-----------------
- In our structure both members could get different awards such as Gold, Silver or Bronze. So that we hold the memberid in our table. Here memberid column is foreign key to the same column in members table.

  CREATE TABLE IF NOT EXISTS AWARDS (
            |  AWARDID SERIAL PRIMARY KEY,
            |  numofGOLD INTEGER,
            |  numofBRONZE INTEGER,
            |  numofSILVER INTEGER,
            |  DATE DATE,
            |  MEMBERID INTEGER REFERENCES MEMBERS
            |  ON DELETE CASCADE
            |  )

- The admin_check table is created to check wheter it possible to be an admin or not. 

  CREATE TABLE IF NOT EXISTS ADMINCHECK (
            |  ID SERIAL PRIMARY KEY,
            |  EMAIL VARCHAR(30) NOT NULL,
            |  PASSWORD VARCHAR(6) NOT NULL
            | )
              

SOFTWARE DESIGN
================

- In order to realization of the three main component of the project, admin, basic member, professional member and admin, python classes are also implemented. They are used in add-delete-update-list operations which are implemented by using database.

- Here contents of the python files are briefly given as:

  - basicmember.py, professionalmember.py and admin.py includes definitions and constructors of the 3 main class.

    - In interface implementation following pages are created:
    
        - Basicmember      
            - basicmember.html, basicmembers.html, basicmember_edit.html
            
        - Professionalmember  
            - professionalmember.html, professionalmembers.html, professionalmember_edit.html
            
        - Admin               
            - admin.html, admins.html, admin_edit.html
  
  - basicmember_view.py, professionalmember_view.py and admin_view.py includes functions which use html files to realization of the  database operations.

- In order to explain the missions of the above files python classes are explained below only for an admin. 
  
  
* admin_view.py :
  
- Note that, basicmember_view and professionalmember_view files has the same concept with admin_view. So we will just overview admin_view ::
  
  @app.route('/admins', methods=['GET', 'POST'])
  def admins_page() 
  
- If the method is GET to access the page defined by html files this function returns the 'admins .html' with admins and lists all admins in the page ::
 
      if request.method == 'GET':
        admins = app.store.get_admins()
        now = datetime.datetime.now()
        return render_template('admins.html', admins=admins,
                               current_time=now.ctime())
                                   
- If the method is POST in related page and if delete button is clicked, the marked checkboxes are taken from the admins list in 'admins.html' and delete operation is performed::
 
      elif  'admins_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('admins_to_delete')
            for key in keys:
                app.store.delete_admin(int(key))
            return redirect(url_for('admins_page'))
            
- If search button is clicked, the keyword in search line is taken and list of related results are returned to the same page ::
  
        elif  request.form['submit'] == 'search' :
            keyword=request.form['search']
            admins = app.store.search_admin(keyword)
            now = datetime.datetime.now()
            return render_template('admins.html', admins=admins,
                               current_time=now.ctime())  
            
- If submit button is clicked new row is added to table. Attributes of this row are taken from the form in 'admin_edit.html' ::
  
    else:
        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        year = request.form['year']

        now = str((datetime.datetime.now()));
        now = now[:-7]
        if (app.store.check_admin(email,password)):
            role = 'admin'
        else:
            role = 'user'

        admin = Admin(name, surname, username, email,password, year,role)
        app.store.add_admin(admin)
        return redirect(url_for('admin_page', key=app.store.admin_last_key))
  
  Then ::
  
      @app.route('/admin/<int:key>', methods=['GET', 'POST'])
      def admin_page(key)
   
- If the username of the admin is clicked in '/admins' path,  related admin class object is returned ::
  
      if request.method == 'GET':
        admin = app.store.get_admin(key)
        now = datetime.datetime.now()
        return render_template('admin.html', admin=admin,
                               current_time=now.ctime())
                               
- If the edit button is clicked in the admin.html, the attributes of form in admin_edit html is taken and admin_page is returned      with updated attributes ::
  
      else:
        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        year = request.form['year']
        role='admin'
        app.store.update_admin(key,name, surname, username, email,password, year,role)
        return redirect(url_for('admin_page', key=key))
 
            
            
  Then ::
  
    @app.route('/admins/add')
    @app.route('/admin/<int:key>/edit')
    def admin_edit_page(key=None)
 
- If the 'Add Admin' button in adminpanel is clicked, admin_edit.html is returned with blank form or if edit button in                  admin.html are clicked, the edit_admin.html with attributes of related object is returned ::
 
    admin = app.store.get_admin(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('admin_edit.html', admin=admin, current_time=now.ctime())
  
 
DATABASE OPERATIONS 
========================

Admin Functions
-----------------

- Add Admin:

- It takes the object from admin class by html form. Then it executes the below query to add admin to the database ::
 
    "INSERT INTO ADMIN (NAME, SURNAME, USERNAME, EMAIL, PASSWORD, YEAR, ROLE) VALUES (%s, %s, %s, %s, %s, %s,%s) RETURNING ADMIN.ID"
 
- It adds the record to the table and returns with the id of the current record.
  

* Delete Admin:

- It takes the key, index, of the related admin by the form.
- Then it executes the below query to delete admin to the database::

   "DELETE FROM ADMIN WHERE (ID = %s)"
  
- It deletes the record which is selected by its index in html.


* Get Admin:

- It takes the key, index, of the related admin by the form.
- Then it executes the below query to get admin to the database ::

   "SELECT NAME, SURNAME, USERNAME, EMAIL, PASSWORD, YEAR FROM ADMIN WHERE (ID = %s)"
  
- It gets one row from the database whose id is key.



* Get Admins:

- It executes the below query to get admins in each row in table ::

   "SELECT * FROM ADMIN ORDER BY ID"

- It gets one row from the database in each iteration. It continues until covering all rows.



* Update Admin:

- It takes the key, index, of the related admin and new object from admin class with updated information.
- Then it executes the below query to update the existing admin in the database ::

   "UPDATE ADMIN SET NAME=%s, SURNAME=%s, USERNAME=%s, EMAIL=%s, PASSWORD=%s, YEAR=%s, ROLE=%s  WHERE (ID = %s)"
  
- It updates the related row in the database whose id is key.


* Search Admin:

- It takes the name or username of the admin to search his/her in database.
- Then it executes the below query to search an admin with name/username from database ::

   "SELECT * FROM ADMIN WHERE (NAME ILIKE %s OR USERNAME ILIKE%s ) ORDER BY ID"
  
- It returns an admin object whose fields are filled with the result of the database query.



Basic Member Functions
------------------------

- Basic member database operations has the same concept with admins' functions which are stated above.
- Note that in each operation it just fills/retrieves the basic member related columns.


Professional Member Functions
-------------------------------

* Add Professional Member:

- One of the main difference between basic and professional member is joining a team.
- In below query random team id is generated ::
  
   "SELECT id FROM team ORDER BY RANDOM()LIMIT 1"
  
- Then, new row to members table with information in professional member type object and generated team id is ::

   "INSERT INTO MEMBERS 
      |(NAME, SURNAME, USERNAME, GENDER,EMAIL,PASSWORD, CITY, YEAR, INTERESTS,MEMBERTYPE,LASTLOGIN, REGTIME, ROLE ,TEAMID )
      | VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s,%s,%s) RETURNING MEMBERS.MEMBERID"
  
- It inserts a new row into table for a professional member.



* Delete Professional Member:

- It is similar to other delete operations.


* Get Professional Member:

- First it retrieves the numbers of awards in each group for the user then it gets the personal information from the members table
as a result it combines these into html form to show.
- Following queries should be executed ::

   "SELECT sum(numofGOLD),sum(numofBRONZE), sum(numofSILVER) FROM MEMBERS, AWARDS 
          |WHERE( (members.memberid=awards.memberid) and members.memberid=%s )"
   "SELECT NAME, SURNAME, USERNAME, GENDER, MEMBERTYPE,EMAIL, PASSWORD, CITY, INTERESTS,SCORE,YEAR, LASTLOGIN, REGTIME, ROLE, TEAMID           |FROM MEMBERS WHERE (MEMBERID =%s)"



* Get Professional Members:

- It is similar to other gets operations.


* Search Professional Member:

- It is similar to other search operations.


* Update Professional Member:

- It is similar to other update operations.
- Note  that there is no award update because it is only done at the end of team races and en the end of the week by experiences of the users.


ADDITIONAL FUNCTIONS
====================

* Find Member:

- It takes an email and password as a key which are entered at login page by the user.
- Then it executes the below query to check existencty of the user in database ::
  
   SELECT NAME FROM MEMBERS WHERE ((email=%s)and (password=%s)) UNION SELECT NAME FROM ADMIN WHERE ((email=%s)and (password=%s))"

- It gets one row from the database which has matched email and password.
- Note that above query searches on both members and admin tables.
- If there exists any record with related email and password it returns 1 else it returns 0. Returning 0 means record has not found.


* Check Admin:

- It gets an email and password.
- Actually it is not an database operation it just returns whether the record is available for becoming an admin or not.
- If the user may be an admin it will return 1 else it will return 0.


* Get Top 5 Team:

- It select 5 teams from the team table which have the higher scores.
- For this purpose, it executes below query ::
  
   "select * from team order by score desc limit 5"
  
- It returns with 5 object from the team class.
- Note that it is not guaranteed that all of them is different from none.


* Get Top 5 Member:

- It select 5 members from the members table which have the higher scores.
- For this purpose, it executes below query ::

   "select * from members where membertype=1 order by score desc limit 5"
  
- It returns with 5 object from the member class.
- Note that it is not guaranteed that all of them is different from none.


* Get Num of Basic/Professional Members:

- In database professional and basic members are hold in the same table which is named as 'members'.
- They can be differ by 'membertype' column which is 0 for basic members and 1 for professional members.
- So that,

    - for basic members ::
        
        "select count(memberid) from members where membertype=0"
      
    - for professional members ::
      
        "select count(memberid) from members where membertype=1"


* Get Num of Admins:

- By the help of below query we can obtain the number of admins in the database ::

   "select count(id) from admin"


* Get My Experiences:

- It gets the name of the member to list his/her experiences in his/her home page.
- For this purpose it executes the following query::

   "SELECT * FROM EXPERIENCE where (username=%s)"
  
- Note that it can return with multiple rows or none.

----------------------------------------------------------------------------------------------------
