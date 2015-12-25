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

   ALTER TABLE TEAM ADD  FOREIGN KEY(FOUNDER) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE

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

   | ALTER TABLE RACE ADD  FOREIGN KEY(FOUNDERID) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE
   | ALTER TABLE RACE ADD  FOREIGN KEY(CYCROUTEID) REFERENCES CYCROUTE(TITLE) ON DELETE CASCADE

Race Results Table
------------------

   ID attribute holds the primary key of the race table.
   | MEMBERID attribute references to the ID attribute in the MEMBERS table.
   | RACEID attribute references to the ID attribute in the RACE table.

  CREATE TABLE RACE_RESULTS (
       | ID SERIAL PRIMARY KEY,
       | MEMBERID INTEGER ,
       | RACEID INTEGER,
       | ORD INTEGER
       | )

   | ALTER TABLE RACE_RESULTS ADD  FOREIGN KEY(MEMBERID) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE
   | ALTER TABLE RACE_RESULTS ADD  FOREIGN KEY(RACEID) REFERENCES RACE(ID) ON DELETE CASCADE

Activity Table
--------------

   ID attribute holds the primary key of the activity table.
   | FOUNDERID attribute references to the ID attribute in the MEMBERS table.

   CREATE TABLE ACTIVITY (
      | ID SERIAL PRIMARY KEY,
      | TITLE VARCHAR(40),
      | ACTIVITY_TYPE VARCHAR(40),
      | FOUNDERID INTEGER ,
      | PARTICIPANT_COUNT INTEGER,
      | TIME VARCHAR(40),
      | PLACE VARCHAR(40),
      | ACTIVITY_INFO VARCHAR(150)
      | )

    ALTER TABLE ACTIVITY ADD  FOREIGN KEY(FOUNDERID) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE

Activity Members Table
----------------------

   ID attribute holds the primary key of the race table.
   | MEMBERID attribute references to the ID attribute in the MEMBERS table.
   | ACTIVITYID attribute references to the ID attribute in the ACTIVITY table.

   CREATE TABLE ACTIVITY_MEMBERS (
         | ID SERIAL PRIMARY KEY,
         | MEMBERID INTEGER,
         | ACTIVITYID INTEGER
          )

   | ALTER TABLE ACTIVITY_MEMBERS ADD  FOREIGN KEY(MEMBERID) REFERENCES MEMBERS(MEMBERID) ON DELETE CASCADE
   | ALTER TABLE ACTIVITY_MEMBERS ADD  FOREIGN KEY(ACTIVITYID) REFERENCES ACTIVITY(ID) ON DELETE CASCADE

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

team_views.py ::
-------------

   @app.route('/teams', methods=['GET', 'POST'])
   def teams_page():
- If the method is GET to access the page defined by html files this function returns the 'teams .html' with teams and list all         members of the team in the page ::
      if 'username' in session:
         if request.method == 'GET':
            teams = app.store.get_teams()
            now = datetime.datetime.now()
            return render_template('teams.html', teams=teams,
                                   current_time=now.ctime())
- If the method is POST in related page and if delete button is clicked, the marked checkboxes are taken from 'teams.html' and delete   operation are called, if search button is clicked, the keyword in search line is taken is returned the same page ::
      elif  'teams_to_delete' in request.form or 'search' in request.form:
            if request.form['submit'] == 'Delete':
                keys = request.form.getlist('teams_to_delete')
                for key in keys:
                    app.store.delete_team(int(key))
                return redirect(url_for('teams_page'))
            elif  request.form['submit'] == 'Search' :
                search_name=request.form['search']
                teams = app.store.search_team(search_name)
                now = datetime.datetime.now()
                return render_template('teams.html', teams=teams,
                                   current_time=now.ctime())
 - If submit button is clicked in team_edit.html, in the route defined by '@app.route('/teams/add')' , a new row is added to teams       table. Attributes of this row are pulled from the form in 'team_edit.html'::
 
        else:
            title = request.form['title']
            score = request.form['score']
            year = request.form['year']
            team_type = request.form.get('team_type')
            location = request.form['location']
            if 'username' in session:
                name = session['username']
                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
                    founder = cursor.fetchone()
                    founder=founder[0]
                    connection.commit()
                member_count = 1
                team = Team(title, score, founder, member_count, year, team_type, location)
                app.store.add_team(team)
                image=request.files['file']
                if image:
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/image/teams/' + str(app.store.team_last_key) + '.jpg'))
                return redirect(url_for('team_page', key=app.store.team_last_key))

   |
   |
   
   @app.route('/team/<int:key>', methods=['GET', 'POST'])
   def team_page(key):
- If the title of a route in '/teams ' is clicked, team.html with related team object is returned::
    if request.method == 'GET':
        team = app.store.get_team(key)
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM MEMBERS WHERE teamid='%s';"%key)
            members = [(key, Basicmember(name, surname, username, gender, email, password, byear, city, interests, lastlogin, regtime, role))
                      for key, name, surname, username, gender, membertype, email, password, city, interests, score, byear,teamid, lastlogin, regtime, role in cursor]
            connection.commit()
        now = datetime.datetime.now()
        return render_template('team.html', team=team, members=members,
                           current_time=now.ctime())
- If the edit button is clicked in the team.html, the attributes of form in team_edit html is pulled and team_page is returned with     updated attributes::
    else:
        title = request.form['title']
        score = request.form['score']
        year = request.form['year']
        team_type = request.form.get('team_type')
        location = request.form['location']
        image=request.files['file']
        if image:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/image/teams/' + str(key) + '.jpg'))
        app.store.update_team(key, title, score, year, team_type, location)
        return redirect(url_for('team_page', key=key))

|
|
|

@app.route('/teams/add')
@app.route('/team/<int:key>/edit')
def team_edit_page(key=None):
- If the 'Add Team' button in layout is clicked, team_edit.html is returned with blank form or if edit button in team.html are clicked   the team_edit.html with attributes of related object is returned::
    team = app.store.get_team(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('team_edit.html', team=team,
                           current_time=now.ctime())

|
|
|

@app.route('/team/<int:key>')
@app.route('/team/<int:key>/join')
def team_join_page(key=None):
- If the 'Join Team' button is clicked on the team page, the members of this team are listed in the team's page ::
    if 'username' in session:
        name = session['username']
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
            id = cursor.fetchone()
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = ("UPDATE MEMBERS SET teamid=%s  WHERE (memberid=%s)")
            cursor.execute(query, (key, id))
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT member_count FROM TEAM WHERE id='%s';"%key)
            connection.commit()
            member_count = cursor.fetchone()[0]
            member_count = member_count + 1
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = ("UPDATE TEAM SET member_count=%s  WHERE (id=%s)")
            cursor.execute(query, (member_count, key))
            connection.commit()
            now = datetime.datetime.now()
            return redirect(url_for('team_page', key=key))
- If the current user is not included in the session::
    else:
        team = app.store.get_team(key) if key is not None else None
        now = datetime.datetime.now()
        return redirect(url_for('team_page', key=key))

- race_view and activity_view operations has the same concept with teams’ functions which are stated above. 
- Additionally, races.html has MEMBERS list that is defined in races_page():

@app.route('/race/<int:key>')
@app.route('/race/<int:key>/join')
def race_join_page(key=None):
- If the 'Join Race' button is clicked on the race page, the participants of this race are listed in the race's page::
    if 'username' in session:
        name = session['username']
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
            id = cursor.fetchone()
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = ("INSERT INTO RACE_RESULTS (MEMBERID, RACEID ) VALUES (%s, %s)")
            cursor.execute(query, (id, key))
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT participant_count FROM RACE WHERE id='%s';"%key)
            participant_count = cursor.fetchone()[0]
            participant_count = participant_count + 1
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = ("UPDATE RACE SET participant_count=%s  WHERE (id=%s)")
            cursor.execute(query, (participant_count, key))
            connection.commit()
        now = datetime.datetime.now()
        return redirect(url_for('race_page', key=key))

- If the current user is not included in the session::
    else:
        race = app.store.get_race(key) if key is not None else None
        now = datetime.datetime.now()
        return redirect(url_for('race_page', key=key))

|
|

- Additionally, activities.html has MEMBERS list that is defined in activities_page():

@app.route('/activity/<int:key>')
@app.route('/activity/<int:key>/join')
def activity_join_page(key=None):
- If the 'Join Activity' button is clicked on the activity page, the participants of this activity are listed in the activity's page::
    if 'username' in session:
        name = session['username']
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
                    connection.commit()
        id = cursor.fetchone()
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = ("INSERT INTO ACTIVITY_MEMBERS (MEMBERID, ACTIVITYID ) VALUES (%s, %s)")
                    cursor.execute(query, (id, key))
                    connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT participant_count FROM ACTIVITY WHERE id='%s';"%key)
                    connection.commit()
        participant_count = cursor.fetchone()
        participant_count = participant_count[0]
        participant_count = participant_count + 1
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = ("UPDATE ACTIVITY SET participant_count=%s  WHERE (id=%s)")
                    cursor.execute(query, (participant_count, key))
                    connection.commit()
        now = datetime.datetime.now()
        return redirect(url_for('activity_page', key=key))
        
- If the current user is not included in the session::
    else:
        activity = app.store.get_activity(key) if key is not None else None
        now = datetime.datetime.now()
        return redirect(url_for('activity_page', key=key))





DATABASE OPERATIONS
===================

Basic Operations
----------------

   - The following database operations are implemented for the team, race, and activity classes listed below:
      -Add Operation:
         add_nameofclass operation takes an object as parameter related to the requested page and
         insert a new row into the related object's table.
            | INSERT INTO TEAM (NAME, SCORE, FOUNDER, MEMBER_COUNT, YEAR, TEAMTYPE, LOCATION) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING TEAM.ID
            | INSERT INTO RACE (TITLE, RACE_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, CYCROUTEID) VALUES (%s, %s, %s, %s, %s, %s) RETURNING RACE.ID
            | INSERT INTO ACTIVITY (TITLE, ACTIVITY_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, PLACE, ACTIVITY_INFO) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING ACTIVITY.ID

      -Delete Operation:
         delete_nameofclass operation takes a key as parameter related to the requested page and
         deletes the row from the related object's table that includes the taken key.
            | DELETE FROM TEAM WHERE (ID = %s)
            | DELETE FROM RACE WHERE (ID = %s)
            | DELETE FROM ACTIVITY WHERE (ID = %s)

      -Get Operation:
         get_nameofclass operation takes a key as parameter related to the requested page and
         selects the row from the related object's table that includes the taken key,
         then returns the found object to the user.
            | SELECT NAME, SCORE, FOUNDER, MEMBER_COUNT, YEAR, TEAMTYPE, LOCATION FROM TEAM WHERE (ID = %s)
            | SELECT TITLE, RACE_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, CYCROUTEID FROM RACE WHERE (ID = %s)
            | SELECT TITLE, ACTIVITY_TYPE, FOUNDERID, PARTICIPANT_COUNT,  TIME, PLACE, ACTIVITY_INFO FROM ACTIVITY WHERE (ID = %s)

      -Get List Operation:
         get_nameofclasses operation does not take any argument. It selects all rows from the
         related object's table and returns these objects to the user.
            | SELECT * FROM TEAM ORDER BY ID
            | SELECT * FROM RACE ORDER BY ID
            | SELECT * FROM ACTIVITY ORDER BY ID

      -Search Operation:
         search_nameofclass operation takes a key as parameter related to the requested page and
         selects the rows from the related object's table that include the key parameter in the
         specified columns.
            | SELECT * FROM TEAM WHERE (NAME ILIKE %s OR LOCATION ILIKE %s)
            | SELECT * FROM RACE WHERE (TITLE ILIKE %s OR RACE_TYPE ILIKE %s)
            | SELECT * FROM ACTIVITY WHERE (TITLE ILIKE %s OR ACTIVITY_TYPE ILIKE %s OR PLACE ILIKE %s OR ACTIVITY_INFO ILIKE %s)

      -Update Operation:
         update_nameofclass operation takes a key and related fields that are wanted to update that is
         related to the requested page. Then, the rows including the key are selected and the requested
         fields are updated in the related object's table.
            | UPDATE TEAM SET NAME = %s, SCORE = %s, YEAR = %s, TEAMTYPE = %s, LOCATION = %s WHERE (ID = %s)
            | UPDATE RACE SET TITLE = %s, RACE_TYPE = %s, TIME = %s, CYCROUTEID = %s WHERE (ID = %s)
            | UPDATE ACTIVITY SET TITLE = %s, ACTIVITY_TYPE = %s, TIME = %s, PLACE = %s, ACTIVITY_INFO = %s WHERE (ID = %s)


Operations for Race and Race Results Tables
-------------------------------------------

    - The following database operations are implemented for the race and race_results tables:
      -When a new race is created, the founder of the race is inserted to the race_results table
      to keep the participants of the races using the following queries:
         | SELECT memberid FROM MEMBERS WHERE username='%s';"%name
         | INSERT INTO RACE_RESULTS (MEMBERID, RACEID ) VALUES (%s, %s)

      -When a race page is clicked for open, the following queries are executed
      for obtain the necessary informations of the page from the tables:
         | SELECT memberid FROM RACE_RESULTS WHERE raceid='%s';"%key
         | SELECT * FROM MEMBERS WHERE memberid='%s';"%memberid
         | SELECT DISTINCT RACEID FROM RACE_RESULTS
         | SELECT COUNT(ID) FROM RACE_RESULTS WHERE raceid='%s';"%i
         | SELECT id FROM RACE_RESULTS WHERE raceid='%s';"%i
         | UPDATE RACE_RESULTS SET ord=%s  WHERE (raceid=%s)

      -When a user clicks the join race button, the participant of the race is inserted to the race_results
      table to keep the participants of the races using the following queries:
         | SELECT memberid FROM MEMBERS WHERE username='%s';"%name
         | INSERT INTO RACE_RESULTS (MEMBERID, RACEID ) VALUES (%s, %s)
         | SELECT participant_count FROM RACE WHERE id='%s';"%key
         | UPDATE RACE SET participant_count=%s  WHERE (id=%s)

Operations for Activity and Activity Members Tables
---------------------------------------------------

   - The following database operations are implemented
      -When a new activity is created, the founder of the activity is inserted to the activity_members table
      to keep the participants of the activities using the following queries.
         | SELECT memberid FROM MEMBERS WHERE username='%s';"%name
         | INSERT INTO ACTIVITY_MEMBERS (MEMBERID, ACTIVITYID ) VALUES (%s, %s)

      -When an activity page is clicked for open, the following queries are executed
      for obtain the necessary informations of the page from the tables:
         | SELECT memberid FROM ACTIVITY_MEMBERS WHERE activityid='%s';"%key
         | SELECT * FROM MEMBERS WHERE memberid='%s';"%memberid

      -When a user clicks the join activity button, the participant of the activity is inserted to the
      activity_members table to keep the participants of the activities using the following queries:
         | SELECT memberid FROM MEMBERS WHERE username='%s';"%name
         | INSERT INTO ACTIVITY_MEMBERS (MEMBERID, ACTIVITYID ) VALUES (%s, %s)
         | SELECT participant_count FROM ACTIVITY WHERE id='%s';"%key
         | UPDATE ACTIVITY SET participant_count=%s  WHERE (id=%s)

