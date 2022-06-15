from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, Response, session
app = Flask(__name__)

import pyodbc 
import sys
import db
import mysql.connector
from mysql.connector import Error
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from forms import LoginForm
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import LETS

key = 'AAAACCCC'
c_con, c_curs = db.connect_db()
global switch2
switch2 = False

config = {
    "SECRET_KEY": "6d8ed540960d1085d183d8e5d236f2da",
    "TEMPLATES_AUTO_RELOAD": True,
    "MYSQL_HOST": "10.90.1.110",
    "MYSQL_USER": "stefan",
    "MYSQL_PASSWORD": "Start2020!",
    "MYSQL_DB": "LETS"
}

mysql = MySQL(app)
bcrypt = Bcrypt(app)
app.config.from_mapping(config)

# c_curs.execute("SELECT id FROM users WHERE id='{}'".format(1))
# print(c_curs.fetchone(), file=sys.stdout)
    
#was ist user id? wie kann ich aus der datenbank user abrufen? SELECT * FROM users WHERE user='admin'

def insert_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    c_curs.execute("INSERT INTO users(user, password) VALUES ('{}', '{}');".format(username, hashed_password))
    c_curs.execute("SELECT * FROM users")
    record = c_curs.fetchall()
    print(record, file=sys.stdout)
    c_con.commit()

# insert_user('admin1', 'king')

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            
            
            print(switch2, file=sys.stderr)
            print('This is standard output', file=sys.stdout)
        elif  request.form.get('action2') == 'VALUE2':
            
            insert_user("fakeadm", "goodpw")
            print(switch2, file=sys.stderr)
            print('This is standard output', file=sys.stdout)
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('home.html', form=request.form)
    
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        c_curs.execute('SELECT user FROM users WHERE user = "{}"'.format(username))
        if c_curs.fetchone() is not None:
            c_curs.execute('SELECT password FROM users WHERE user = "{}"'.format(username))
            hashed_pw = c_curs.fetchone()[0]
            print(hashed_pw, file=sys.stdout)
            pw_check = bcrypt.check_password_hash(hashed_pw, password)
            print(pw_check, file=sys.stdout)

            c_curs.execute('SELECT id, user FROM users WHERE user = "{}"'.format(username))
            account = c_curs.fetchone()
            print(account, file=sys.stdout)
            if account and pw_check:
                session['loggedin'] = True
                session['id'] = account[0]
                # print(account['id'], file=sys.stdout)
                # print(account['user'], file=sys.stdout)
                session['username'] = account[1]
                print(session, file=sys.stdout)
                return redirect('/home')
            else:
                print(session, file=sys.stdout)
                msg = 'Incorrect username/password!'
        else:
            print(session, file=sys.stdout)
    return render_template('login.html', title='Login', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('home'))

@app.route("/covid_test", methods=['GET', 'POST'])
def covid_test():
    if 'loggedin' in session:
        if request.method == 'POST' and 'nfccard' in request.form.to_dict():
            default_value = '0'
            data = request.form.to_dict(flat=False)
            data = data.get('nfccard')
            print(data, file=sys.stdout)  
            print(LETS.map_serial_to_emp_number(data))
            print(data, file=sys.stdout)  
        return render_template('covid_test.html')
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=False)


        # {% if current_user.is_authenticated %}
        # Currently logged in as <b>{{ current_user.username }}</b>
        # <b><a href="{{ url_for('home') }}">Home</a></b> |
        # <b><a href="{{ url_for('editscreens') }}">Videos</a></b> |
        # <b><a href="{{ url_for('logout') }}">Logout</a></b>
        # {% else %}
        # <b><a href="{{ url_for('home') }}">Home</a></b> |
        # <b><a href="{{ url_for('login') }}">Login</a></b> |
        # <b><a href="{{ url_for('register') }}">Register</a></b>
        # {% endif %}
        # </div>