# To-Do List Web Application

#### Video Demo:

---

## Project Description

This project is a web-based **To-Do List application** built as my final project for **CS50**.  
The application allows users to create an account, log in securely, and manage their own personal list of tasks. Each user can add new tasks, mark them as completed, edit task titles, and delete tasks. Tasks are private and tied to the logged-in user, ensuring that each account only sees its own data.

The main goal of this project was to apply the concepts learned throughout CS50, including backend development with Flask, database management using SQLite, session handling, user authentication, and frontend interaction using HTML, CSS, JavaScript, and Bootstrap.

This project goes beyond a simple static website by implementing full CRUD functionality, user authentication, and dynamic updates without requiring full page reloads for certain actions.

---

## Features

- User registration and login system with password hashing
- Session-based authentication
- Create, read, update, and delete tasks (CRUD)
- Mark tasks as completed using checkboxes
- User-specific tasks (each user sees only their own tasks)
- Responsive design using Bootstrap
- Clean and simple user interface
- Protection against unauthorized access using a custom `login_required` decorator

---

## File Structure and Explanation

### `app.py`

This is the main Flask application file. It contains:
- All route definitions
- Database connection logic
- User authentication (login, logout, signup)
- Task-related operations (add, edit, delete, complete)
- Session configuration using `Flask-Session`
- Response headers that disable caching to ensure changes appear immediately

Each route is carefully designed to either render a template or return a response suitable for JavaScript-based requests (such as task completion and deletion).

---

### `helper.py`

This file contains a custom `login_required` decorator.  
It ensures that certain routes can only be accessed by authenticated users. If a user tries to access a protected route without being logged in, they are redirected to the login page. This helps keep the application secure and prevents unauthorized access to user data.

---

### Templates (`templates/` folder)

- **`layout.html`**  
  The base template shared by all pages. It includes:
  - Navigation bar
  - Bootstrap integration
  - Conditional navigation links based on login status  
  Other templates extend this file to maintain a consistent layout.

- **`index.html`**  
  Displays the list of tasks for the logged-in user.  
  Tasks can be marked as completed, edited, or deleted using JavaScript interactions.

- **`add-task.html`**  
  Contains a form for adding new tasks.

- **`login.html`**  
  Allows existing users to log in.

- **`sign-up.html`**  
  Allows new users to create an account.

Flash messages are used in the authentication templates to display errors such as missing fields or invalid credentials.

---

### Static Files (`static/` folder)

- **Bootstrap files** for styling and responsive layout
- **`home.css`** for custom styles
- **JavaScript files** that handle asynchronous task updates (edit, delete, complete) without refreshing the page

---

### Database (`todo.db`)

The application uses **SQLite** as its database.  
It contains two main tables:

- **`users`**
  - `id`
  - `username`
  - `email`
  - `hash` (hashed password)

- **`tasks`**
  - `id`
  - `title`
  - `complete`
  - `user_id`

Tasks are linked to users using a foreign key relationship.

---

## Design Decisions

One important design choice was implementing **user authentication** instead of making the to-do list global. This makes the application more realistic and secure, as each user has a private workspace.

Another key decision was handling task updates (completion, editing, deletion) using **JavaScript and POST requests** instead of full page reloads. This improves user experience and makes the application feel more dynamic.

I also chose to disable browser caching using response headers to avoid confusion during development, where changes would not immediately appear unless the page was refreshed manually.

Bootstrap was used to speed up UI development while still allowing customization through CSS.

---

## How to Run
1. Clone the repository:
    ```
     git clone <repo url> 
    ```
2. Navigate into the project folder:
   ```
    cd <project-folder>
   ``` 
3. (Optional) Create a virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate # Linux/Mac
    venv\Scripts\activate # Windows
    ```
4. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Create the `todo.db` database:
  - Schema:
  ```
    CREATE TABLE users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      hash TEXT NOT NULL
      );
  ```
  ```
    CREATE TABLE tasks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      complete INTEGER DEFAULT 0,
      user_id INTEGER NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
  ```

6. Run the Flask app:
    ```
    python app.py
    ```
7. Open your browser and go to:
    ```
    http://127.0.0.1:5000
    ```
8. Sign up and log in to start using your personal to-do list!

---
## Requirements
This project uses the following Python packages:
- Flask
- Flask_Session
- Werkzeug

All dependencies are listed in requirements.txt

---
## Author:
- **Name**: Mohamed Matar
- **Course**: CS50
- **Project**: Final Project
- **Year**: 2025