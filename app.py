from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import sqlite3
import database

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/sign_in")
    return redirect("/home")

@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        session["name"] = request.form.get("username")
        return redirect("/")
    return render_template("sign_in.html")

@app.route("/home", methods=["GET"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        user = database.get_name(username)
        if user:
            return render_template("home.html", user=user, subject_list=["psychology", "maths", "english", "chemistry", "computing"])
    return redirect("/sign_in")

FIELDS={"username":"Username", "first_name":"First name", "last_name": "Last name", "email": "Email", "password": "Password"}

@app.route("/create_account")
def create_account():
    return render_template("create_account.html", fields=FIELDS)

@app.route("/check_account", methods=["POST", "GET"])
def check_account():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        hash = database.hash(password)
        connection = sqlite3.connect("nea_database.db")
        return render_template("sign_in.html", message=hash) 
    return render_template("sign_in.html")
