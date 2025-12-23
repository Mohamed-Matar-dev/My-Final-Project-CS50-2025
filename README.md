# To-Do list Web Application

#### Video Demo: 

## This project is a web-based to-do list appliction that allow users to create, complete, edit, and delete tasks. it was build as a CS50 final project to practic full-stack web development using Flask, JavaScript and SQLite

## Features
- Add new tasks
- Mark tasks as completed or uncompleted
- Edit existing tasks
- Delete tasks
- Task presist using SQLite
- Dynamic UI update using JavaScript (no page reload)

## Technologies used
- Python (Flask)
- SQLite
- HTML (Jinja2 templates)
- CSS (Bootstrap)
- JavaScript (Fetch API)

## How to Run
1. Install Python 3
2. Install Flask
3. Run 'python app.py'
4. Open browser and go to http://127.0.0.1:5000

## File Structure
- app.py: Main Flask application and routes
- templates/: HTML templates rendered by Flask
- templates/layout.html: Web appliction layout to avoid repetition
- templates/index.html: Web appliction Home page
- templates/add-task.html: Add tasks to To-Do list
- static/home.js: JavaScript For Handling checkbox, edit and delete actions
- static/home.css: Custom styles
- todo.db: SQLite database storing tasks

