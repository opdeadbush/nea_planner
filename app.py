from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import database
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/sign_in")
    name = session.get("name")
    return render_template("home.html", user=name, subject_list=["maths", "physics", "art", "biology", "chemistry", "computing", "english", "geography", "history", "psychology"])

@app.route("/sign_in", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        name, password = database.get_user_details(username)
        print(name, password, username)
        if name and password == database.hash(request.form.get("password")):
            session["name"] = name
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

@app.route("/tasks")
def tasks():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        return render_template("tasks.html")
    

@app.route("/revision")
def revision():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        return render_template("revision.html")

@app.route("/timetable")
def timetable():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        return render_template("timetable.html")

@app.route("/account")
def account():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        return render_template("account.html", name=session.get("name"))

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")
