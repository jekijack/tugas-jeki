from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import mysql.connector

app = Flask(_name_)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="user",
    password=""
)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/aksi_login', methods=["POST"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("SELECT * FROM project x WHERE username = %s AND password = %s")
    data = (request.form['username'], request.form['password'])
    cursor.execute(query, data)
    value = cursor.fetchone()

    if value:
        session["user"] = request.form['username']
        return redirect(url_for('admin'))
    else:
        return "Salah !!!"


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route('/admin')
def admin():
    if session.get("user"):
        return render_template("admin.html")
    else:
        return redirect(url_for("home"))


if _name_ == "_main_":
    app.run(debug=True)