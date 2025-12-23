from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

from helper import login_required

app = Flask(__name__)

app.secret_key = os.urandom(24)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# default route/page showing the tasks
@app.route("/")
@login_required
def index():
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks WHERE user_id=?", (session["user_id"],)).fetchall()
    db.close()

    return render_template("index.html", tasks=tasks)

# add task route 
@app.route("/add-task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method =="POST":
        task_name = request.form.get("task-name")
        db = get_db()
        db.execute("INSERT INTO tasks(title, user_id) VALUES(?, ?)", (task_name, session["user_id"]))
        db.commit()
        db.close()
        return redirect("/")
    return render_template("add-task.html")

# function to complete the task (check box), dosn't need correspodning HTML.
# It shows in index.html, and it worked with home.js
@app.route('/complete-task', methods=['POST'])
@login_required
def complete_task():
    data = request.json or {}
    task_id = data.get("id")
    completed = 1 if data.get("completed") else 0
    if not task_id:
        return "Error", 400
    
    db = get_db()
    db.execute("UPDATE tasks SET complete = ? WHERE id = ? AND user_id = ?", (completed, task_id, session["user_id"]))
    db.commit()
    db.close()

    return "", 204

# function to Delete the task, dosn't need correspodning HTML.
# It shows in index.html, and it worked with home.js
@app.route('/delete-task', methods=["POST"])
@login_required
def delete_task():
    data = request.json or {}
    task_id = data.get("id")
    if not task_id:
        return "Error", 400
    
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, session["user_id"]))
    db.commit()
    db.close()

    return "", 204

# function to Edit the task, dosn't need correspodning HTML.
# It shows in index.html, and it worked with home.js
@app.route('/edit-task', methods= ["POST"])
@login_required
def edit_task():
    data = request.json or {}
    task_id = data.get("id")
    new_title = data.get("title")

    if not task_id or not new_title:
        return "Error", 400
    
    db = get_db()
    db.execute("UPDATE tasks SET title = ? WHERE id = ? AND user_id = ?", (new_title, task_id, session["user_id"]))
    db.commit()
    db.close()

    return "",204

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if session.get("user_id"):
        return redirect("/")
    
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Missing username")
            return redirect("/sign-up")
             
        
        email = request.form.get("email")
        if not email:
            flash("Missing email")
            return redirect("/sign-up")
        
        db = get_db()
        exist = db.execute("SELECT * FROM users WHERE email= ?", (email,)).fetchone()
        if exist:
            flash("user already exist")
            return redirect("/sign-up")
        
        password = request.form.get("password")
        if not password:
            flash("Missing password")
            return redirect("/sign-up")
        
        password_hash = generate_password_hash(password)

        db.execute("INSERT INTO users(username, email, hash) Values(?,?,?)", (username, email, password_hash))
        db.commit()
        db.close()

        return redirect("/login")

    return render_template("sign-up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect("/")
    
    if request.method == "POST":
        email = request.form.get("email")

        if not email:
            flash("Enter email")
            return redirect("/login")
        
        password = request.form.get("password")
        if not password:
            flash("Enter your password")
            return redirect("/login")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email= ?", (email,)).fetchone()
        db.close()
        if not user:
            flash("invalid email and/or password")
            return redirect("/login")
        
        if not check_password_hash(user["hash"], password):
            flash("invalid email and/or password")
            return redirect("/login")
        
        session["user_id"] = user["id"]

        return redirect("/")


    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")