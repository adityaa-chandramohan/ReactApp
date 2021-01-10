from flask import Flask, jsonify,request,Response
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from psycopg2 import connect
import json
import os
import psycopg2
import re
import datetime

from psycopg2 import sql, extensions

app = Flask(__name__)
bcrypt = Bcrypt(app)

connection = None
try:
    connection = connect(dbname="ApplicationDB",user="user",password="test",host="database",port="5432")
    cursor = connection.cursor()
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    cursor.execute("SELECT version();")
    record = cursor.fetchone()

except(Exception, psycopg2.Error) as error:
    connection = None
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    connection.set_isolation_level(autocommit)

table_name_1 = "users"
create_table_1 = "CREATE TABLE IF NOT EXISTS {} (id serial PRIMARY KEY,user_name TEXT NOT NULL,email_address TEXT NOT NULL,Password TEXT);"
cursor.execute(sql.SQL(
    create_table_1
).format(sql.Identifier(table_name_1)))

table_name_2 = "login_attempts"
create_table_2 = "CREATE TABLE IF NOT EXISTS {} (serialid SERIAL PRIMARY KEY,id INT,ip inet,login_attempt TEXT CHECK (login_attempt='SUCCESS' OR login_attempt='FAILURE'),lastaccessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP, CONSTRAINT fk_users FOREIGN KEY(id) REFERENCES users(id));"
cursor.execute(sql.SQL(
    create_table_2
).format(sql.Identifier(table_name_2)))


cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
def checkEmailFormat(email):
    match=re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",email)
    if match:
        return True
    else:
        return False

def checkPasswordFormat(password):
    match=re.search(r"[A-Za-z0-9@!#?=$^*-_]",password)
    if match:
        return True
    else:
        return False

@app.route("/api/register", methods = ['POST'])
def register():
    if request.method == 'POST':
        req_data = request.get_json()
        if not(req_data['name']) or not(req_data['email']) or not(req_data['password']):
            return Response("Please enter all details.", status=403, mimetype='application/json')
        if not(checkEmailFormat(req_data['email'])):
            return Response("Please enter valid email.", status=403, mimetype='application/json')
        if len(req_data['password']) <= 8:
            return Response("Password length should be minimum 8.", status=403, mimetype='application/json')
        if not(checkPasswordFormat(req_data['password'])):
            return Response("Password is invalid. Password should have 1 Uppercase character, 1 lower case character , 1 number and 1 special character out of @,!,#,$,^,*,-,_", status=403, mimeype='application/json')


        getUserID = "SELECT id FROM users WHERE user_name = %(usname)s AND email_address = %(emailaddr)s ;"

        userexists = False
        cursor.execute(getUserID,{"usname":req_data['name'],"emailaddr":req_data['email']})
        usersval = cursor.fetchall()

        if usersval:
            userexists = True

        if (userexists):
            return jsonify("There is a serverside problem"),500
        else:
            pw_hash = bcrypt.generate_password_hash(req_data['password'])

            insertUser = """INSERT INTO users (user_name, email_address, Password) VALUES (%s,%s,%s)"""
            inserted_values = (req_data['name'],req_data['email'],str(pw_hash.decode('utf8')))
            cursor.execute(insertUser, inserted_values)
            connection.commit()

            getUserID = "SELECT id FROM users WHERE email_address = %(emailaddr)s ;"
            cursor.execute(getUserID,{"emailaddr":req_data['email']})
            userID = cursor.fetchall()
            if len(userID) > 0:
                ID = userID[0]
            else:
                ID = 0
            insertLoginAttempt = """INSERT INTO login_attempts (id, ip, login_attempt) VALUES (%s,%s,%s)"""
            inserted_values = (ID,request.remote_addr,'SUCCESS')
            cursor.execute(insertLoginAttempt, inserted_values)


            count = cursor.rowcount
            fetchUser = "SELECT id,user_name,email_address FROM users WHERE user_name = %(usname)s AND email_address = %(emailaddr)s ;"
            cursor.execute(fetchUser,{"usname":req_data['name'],"emailaddr":req_data['email']})

            usersval = cursor.fetchall()

            for row in usersval:
                userData = {
                "id": row[0],
                "name": row[1],
                "email": row[2]
                }

            return jsonify(userData),200

@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        req_data = request.get_json()
        if not(req_data['email']) or not(req_data['password']):
            return Response("Please enter all details.", status=403, mimetype='application/json')
        if not(checkEmailFormat(req_data['email'])):
            return Response("Please enter valid email.", status=403, mimetype='application/json')

        getUserID = "SELECT id FROM users WHERE email_address = %(emailaddr)s ;"
        cursor.execute(getUserID,{"emailaddr":req_data['email']})
        userID = cursor.fetchall()
        if len(userID) > 0:
            ID = userID[0]
        else:
            ID = 0

        userexists = False

        if ID != 0:
            userexists = True
        else:
            return jsonify('Username or password is incorrect.'),400

        if userexists:
            cursor.execute("SELECT password FROM users WHERE email_address = %(emailaddr)s", {"emailaddr":req_data['email']})
            row = cursor.fetchone()

            if row:
                saltpassword = row[0]
            else:
                insertLoginAttempt = """INSERT INTO login_attempts (id, ip, login_attempt) VALUES (%s,%s,%s)"""
                inserted_values = (ID,request.remote_addr,'FAILURE')
                cursor.execute(insertLoginAttempt, inserted_values)
                return jsonify('Username or Password is incorrect'),400

            validuser = False
            if bcrypt.check_password_hash(bytes(saltpassword, 'utf-8'), req_data['password']):
                validuser=True

            if (validuser):

                insertLoginAttempt = """INSERT INTO login_attempts (id, ip, login_attempt) VALUES (%s,%s,%s)"""
                inserted_values = (ID,request.remote_addr,'SUCCESS')
                cursor.execute(insertLoginAttempt, inserted_values)

                fetchUser = "SELECT id,user_name,email_address FROM users WHERE email_address = %(emailaddr)s ;"
                cursor.execute(fetchUser,{"emailaddr":req_data['email']})

                usersval = cursor.fetchall()

                for row in usersval:
                    userData = {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2]
                    }

                return jsonify(userData),200

            else:
                insertLoginAttempt = """INSERT INTO login_attempts (id, ip, login_attempt) VALUES (%s,%s,%s)"""
                inserted_values = (ID,request.remote_addr,'FAILURE')
                cursor.execute(insertLoginAttempt, inserted_values)
                return jsonify('Username or Password is incorrect'),400

@app.route('/api/login_attempt/<int:i>', methods=['GET'])
def login_attempt(i):
    if request.method == 'GET':
        getCurrentLoginAttempt = "select id,ip,lastaccessed from login_attempts where id = %(userID)s and login_attempt='SUCCESS' order by lastaccessed DESC limit 1 ;"
        cursor.execute(getCurrentLoginAttempt,{"userID":i})
        loginAttemptDetail = cursor.fetchall()

        if len(loginAttemptDetail) > 0:
            for row in loginAttemptDetail:
                userData = {
                "id": row[0],
                "ip": row[1],
                "lastaccessed": row[2]
                }

            return jsonify(userData),200
        else:
            return Response("Invalid request.", status=400, mimetype='application/json')

    else:
        return Response("Invalid request.", status=400, mimetype='application/json')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
