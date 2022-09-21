import re
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import database, classes
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/sign_in")
    name = session.get("name")
    session["tasks"] = database.get_task_by_username(session["username"])
    return render_template("home.html", user=name, tasks = session["tasks"])

@app.route("/sign_in", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username").upper()
        session["username"] = username
        name, password = database.get_username_and_password(username)
        if name and password == database.hash(request.form.get("password")):
            session["name"] = name
            if not session.get("timetable"):
                session["timetable"] = classes.Timetable()
            return redirect("/")
        else:
            message="Incorrect username or password"
    return render_template("sign_in.html", message=message)

@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    if request.method == "POST":
        if database.check_for_password(request.form.get("email")):
            return render_template("create_account.html", message="Error - Account already exists!")
        elif request.form.get("password") != request.form.get("password_check"):
            return render_template("create_account.html", message="Error - Passwords do not match!")
        else:
            database.insert((request.form.get("username").upper(), request.form.get("first_name"), request.form.get("last_name"), request.form.get("email"), database.hash(request.form.get("password"))))
            return redirect("/")
    return render_template("create_account.html")

@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        return render_template("tasks.html")
    if request.method == "POST":
        description = request.form.get("description")
        category = request.form.get("category")
        due_date = request.form.get("due_date")
        print(description, category, due_date)
        return redirect("/tasks")

@app.route("/tasks/<int:number>")
def show_task(number):
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        if session.get("username") == database.get_task_by_id(number)[6]:
            message = database.get_task_by_id(number)
        else:
            message = "Not your task"
        return render_template("tasks.html", message=message)
    
@app.route("/revision")
def revision():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        return render_template("revision.html")

@app.route("/timetable", methods=["POST", "GET"])
def timetable():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        return render_template("timetable.html", message = session.get("timetable").display())
    if request.method == "POST":
        session["timetable"] = classes.Timetable()
        return redirect("/timetable")

@app.route("/account")
def account():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        username, first_name, last_name, email, password = database.get_user_details(session.get("username"))
        return render_template("account.html", name=first_name, username = username, last_name = last_name, email = email, password = password)

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")