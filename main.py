from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import functions

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/sign_in")
    name = session.get("name")
    return render_template("home.html", user=name, subject_list=["chemistry", "physics", "maths", "biology", "art"])

@app.route("/sign_in", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        name, password = functions.get_user_details(username)
        print(name, password, username)
        if name and password == functions.hash(request.form.get("password")):
            session["name"] = name
            return redirect("/")
        else:
            message="Incorrect username or password"
    return render_template("sign_in.html", message=message)

@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    FIELDS={"username":"Username", "first_name":"First name", "last_name": "Last name", "email": "Email", "password": "Password"}
    if request.method == "POST":
        for field in FIELDS:
            request.form.get(field)
    return render_template("create_account.html", fields=FIELDS)
    

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")