from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

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
def index():
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    db.close()

    return render_template("index.html", tasks=tasks)

# add task route 
@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method =="POST":
        task_name = request.form.get("task-name")
        db = get_db()
        db.execute("INSERT INTO tasks(title) VALUES(?)", (task_name,))
        db.commit()
        db.close()
        return redirect("/")
    return render_template("add-task.html")

# function to complete the task (check box), dosn't need correspodning HTML.
# It shows in index.html, and it worked with home.js
@app.route('/complete-task', methods=['POST'])
def complete_task():
    data = request.json or {}
    task_id = data.get("id")
    completed = 1 if data.get("completed") else 0
    if not task_id:
        return "Error", 400
    
    db = get_db()
    db.execute("UPDATE tasks SET complete = ? WHERE id = ?", (completed, task_id))
    db.commit()
    db.close()

    return "", 204

@app.route('/delete-task', methods=["POST"])
def delete_task():
    data = request.json or {}
    task_id = data.get("id")
    if not task_id:
        return "Error", 400
    
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    db.close()

    return "", 204

@app.route('/edit-task', methods= ["POST"])
def edit_task():
    data = request.json or {}
    task_id = data.get("id")
    new_title = data.get("title")

    if not task_id or not new_title:
        return "Error", 400
    
    db = get_db()
    db.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    db.commit()
    db.close()

    return "",204