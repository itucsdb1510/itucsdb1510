Parts Implemented by Miyase Tekpınar
================================

Tables
======

- All queries create a table if not exists that holds id as a primary key and username that reference to username of members table,
  only if a user trigger to "/intdb".


CycRoute Table 
-------------

- ::                
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
----------
- :: 
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
---------------
- :: 
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

- TOPMEMBERS table holds best five users ::
   CREATE TABLE IF NOT EXISTS TOPMEMBERS (ID SERIAL PRIMARY KEY,USERID INTEGER,COUNT INTEGER)

Software Design
===================

- For all tables, a class created.
- cycroute.py, bike.py and experience.py includes definitions of constructors.
- cycroute_view.py,bike_view.py and experience_view.py includes functions that link html files and database.
- 'session' library are imported to hold current user and 'redirect', 'render_template', 'request' and 'url_for' libraries are
  imported from flask for connection of html files.

 

  cycroute_view.py ::
  ----------------
 
    @app.route('/cycroutes', methods=['GET', 'POST']) 
    def cycroutes_page(): 
 - If the method is GET to access the page defined by html files this function returns the 'cycroutes .html' with cycroutes and list     all routes in the page ::
            if request.method == 'GET': 
            cycroutes = app.store.get_cycroutes() 
            now = datetime.datetime.now() 
            return render_template('cycroutes.html', cycroutes=cycroutes, 
                                    current_time=now.ctime()) 
                                   
 - If the method is POST in related page 
   and if delete button is clicked, the marked checkboxes are taken from 'cycroutes.html' and delete operation are called,
   if search button is clicked, the keyword in search line is taken and list of related routes are returned the same page ::
      elif 'cycroutes_to_delete' in request.form or 'search' in request.form:
            if request.form['submit'] == 'Delete':
                keys = request.form.getlist('cycroutes_to_delete')
                for key in keys:
                    app.store.delete_cycroute(int(key))
                return redirect(url_for('cycroutes_page'))
            elif  request.form['submit'] == 'Search' :
                keyword=request.form['search']
                cycroutes = app.store.search_cycroute(keyword)
                now = datetime.datetime.now()
                return render_template('cycroutes.html', cycroutes=cycroutes,
                                   current_time=now.ctime())
  -If submit button is clicked in cycroute_edit.html, in the route defined by '@app.route('/cycroutes/add')' , 
   a new row is added to cycroutes table. Attributes of this row are pulled from the form in 'cycroute_edit.html'::
    else:
            title = request.form['title']
            start = request.form['start']
            finish = request.form['finish']
            length=request.form['length']
            name = session['username']
            cycroute = Cycroute(title, name, start, finish,length)
            app.store.add_cycroute(cycroute)
            return redirect(url_for('cycroute_page', key=app.store.cycroute_last_key)) 
  
  |
  |
  |
  
  ::
   @app.route('/cycroute/<int:key>', methods=['GET', 'POST'])
   def cycroute_page(key):
   
  - If the title of a route in '/cycroutes ' is clicked, cycroute.html with related cycroute object is returned::
       if request.method == 'GET':
            cycroute = app.store.get_cycroute(key)
            now = datetime.datetime.now()
            return render_template('cycroute.html', cycroute=cycroute,
                                   current_time=now.ctime())
  - If the edit button is clicked in the cycroute.html, the attributes of form in cycroute_edit html is pulled and
    cycroute_page is returned with updated attributes::
        else:
            title = request.form['title']
            start = request.form['start']
            finish = request.form['finish']
            length=request.form['length']
            app.store.update_cycroute(key, title,start, finish,length)
            return redirect(url_for('cycroute_page', key=key))
  |
  |
  |        
            
            
 @app.route('/cycroutes/add')
 @app.route('/cycroute/<int:key>/edit')
 def cycroute_edit_page(key=None):
 
 - If the 'Add Cycroute' button in layout is clicked, cycroute_edit.html is returned with blank form or if edit button in                  cycroute.html are clicked, the edit_cycroute.html with attributes of related object is returned.
   
    cycroute = app.store.get_cycroute(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('cycroute_edit.html',cycroute=cycroute, current_time=now.ctime())
  
  |
  |
  |
- bike_view and experience_view operations has the same concept with cycroutes’ functions which are stated above. 
- Additionally, experiences.html has TOPMEMBERS list that is defined in experiences_page():
- If the method is GET, TOPMEMBERS table is cleaned. Then, from union of experience and members tables, best five members' ids 
  selected  and numbers of members' experiences are taken and topmembers table filled again.Usernames of members in the table is taken   from members table according to id and sended to experiences.html to list::
      if request.method == 'GET':
            experiences = app.store.get_experiences()
            now = datetime.datetime.now()
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM TOPMEMBERS")
                connection.commit()
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("(select userid, count(userid) from members inner join experience on(userid=memberid) group by userid                  limit 5) order by count(userid) desc")
                cr=cursor.fetchall()
                topmembers = [(row[0],row[1] )
                              for row in cr]
                connection.commit()
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                for userid, count in topmembers:
                    query = "INSERT INTO TOPMEMBERS (USERID, COUNT) VALUES ( %s, %s)"
                    cursor.execute(query, (userid, count))
                counter=0
                for userid, count in topmembers:
                    cursor.execute("select username from members where memberid='%s';"%userid)
                    user= cursor.fetchone()
                    topmembers[counter]=user[0],count*10
                    counter=counter+1
                connection.commit()
                return render_template('experiences.html', experiences=experiences,topmembers=topmembers,
                                       current_time=now.ctime())
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""DROP TABLE TOPMEMBERS""")
                connection.commit()



Database Operations
===================
Theese operations are defined in 'store.py' for all related tables.

- add_nameofclass(self, nameofclass): Add functions get a object  as a parameter and include that query ::
     INSERT INTO NAMEOFCLASS (COLUMN1,COLUMN2,..) VALUES (ATTRIBUTE1, ATTRIBUTE2,...) RETURNING NAMEOFCLASS.ID
  This query's parameters are attributes of the object and it add a new row to related table.
| 
  
- delete_nameofclass(self, key): Delete functions get a id as a parameter an include that query ::
    DELETE FROM NAMEOFCLASS WHERE (ID = key)
| 
- get_nameofclass(self,key): This function gets a id as a parameter and returns a object that is created by using selected attributes   ::
    SELECT [ATTRIBUTE1, ATTRIBUTE2,...] FROM EXPERIENCE WHERE (ID = key)
|   
- get_(nameofclass)s(self) : This function returns a list of related objects by creating a array from table using that query::
    SELECT * FROM NAMEOFCLASS ORDER BY ID
|   
- update_activity(self, key, attribute1, attribute2,..):This function gets attributes of related object and update related row in 
  table::
    UPDATE NAMEOFCLASS SET ATTRIBUTE1 =attribute1, ATTRIBUTE2 = attribute2,.. WHERE (ID = key)
|  
- search_nameofclass(self,keyword): This function searches keyword into related table and returns a list of results of that query:
  SELECT * FROM NAMEOFCLASS WHERE (ATTRIBUTE1 ILIKE '%'+keyword+'%' OR ATTRIBUTE2 ILIKE '%'+keyword+'%' OR ..)
  
  
  






