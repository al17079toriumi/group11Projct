import os

from flask import *
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'kenpa'
app.config['MYSQL_PASSWORD'] = 'qazwsx'
app.config['MYSQL_DB'] = 'USERDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = os.urandom(24)

mysql = MySQL(app)

auth_code = "NMXGfD0hgon3nD717qoW4DfwP26I0u7I"

@app.route('/home')
def hello_world():
    return render_template('w5.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('w2.html',messages=None)
    else:
        cur = mysql.connection.cursor()
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        permission = int(request.form['permission'])

        if permission == 1:
            input_code = request.form['code']
            if input_code != auth_code:
                print("認証不可")
                flash("Error!Authorization code is not vaild.","Error")
                return redirect(url_for("register"))

        if not username or not password:
            print("UserName or Password is null.")
            flash("Error!UserName or Password is null.","Error")
            return redirect(url_for("register"))
        select_stmt = 'SELECT * FROM users WHERE username = "%s"' %username
        cur.execute(select_stmt)
        users = cur.fetchall()
        if users:
            flash("UserID already in used.","Error")
            cur.close()
            return redirect(url_for("register"))
        else:
            hash_password = bcrypt.hashpw(password,bcrypt.gensalt())
            if len(username) > 255 or len(password) > 255:
                flash("No No 255", "Error")
                return redirect(url_for("register"))
            cur.execute('INSERT IGNORE INTO users(username,password,permission) VALUES (%s,%s,%s)',(username,hash_password,permission))
            mysql.connection.commit()
            session['username'] = request.form['username']
            session['permission'] = int(request.form['permission'])
            cur.close()
            return redirect(url_for("hello_world"))
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('w1.html')
    else:
        username = request.form['username']
        password  = request.form['password'].encode('utf-8')
        if not username or not password:
            print("UserName or Password is null.")
            flash("Error!UserName or Password is null.","Error")
            return redirect(url_for("login"))
        if len(username) > 255 or len(password) > 255:
            flash("No No 255","Error")
            print("No No 255")
            return redirect(url_for("login"))
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username=%s',(username,))
        user = cur.fetchone()
        cur.close()
        print(user)
        print("True" if user else "False")
        if user:
            if bcrypt.hashpw(password,user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['username'] = username
                session['password'] = password
                session['permission'] = user['permission']
                return redirect(url_for('hello_world'))
            else:
                flash('Error! Password and UserId not match.','Error')
                return redirect(url_for('login'))
        else:
            flash('Error! User not found.','Error')
            return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
