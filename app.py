from flask import Flask, render_template, request, redirect
import functions
app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/sign_in")

@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    return render_template("sign_in.html")

@app.route("/home", methods=["POST", "GET"])
def home():
    user = request.form.get("user")
    if not user:
        return redirect("/sign_in")
    return render_template("home.html", user=user, subject_list=["maths", "art", "computing", "biology", "english", "history", "physics"])

FIELDS={"username":"Username", "first_name":"First name", "last_name": "Last name", "email": "Email", "password": "Password"}

@app.route("/create_account")
def create_account():
    return render_template("create_account.html", fields=FIELDS)

@app.route("/check_account", methods=["POST", "GET"])
def check_account():
    username = request.form.get("username")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    password_check = request.form.get("password_check")
    return render_template("sign_in.html", message=username)
