from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import database, datetime, functions, json

#configurations
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/sign_in")
    name = session.get("name")
    session["tasks"] = database.get_tasks_by_username(session["username"])
    return render_template("home.html", user=name, tasks = session["tasks"])

@app.route("/sign_in", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username").upper()
        session["username"] = username
        name, password = database.get_username_and_password(username)
        if name and password == functions.hash(request.form.get("password")):
            session["name"] = name
            session["timetable"] = functions.initialise_timetable(database.get_timetable(session["username"]))
            session["revision_list_data"] = functions.initialise_revision(session["username"])
            return redirect("/")    
        else:
            message="Incorrect username or password"
    return render_template("sign_in.html", message=message)

@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    if request.method == "POST":
        if database.check_for_email(request.form.get("email")):
            return render_template("create_account.html", message="Error - Account already exists!")
        elif database.check_for_username(request.form.get("username")):
            return render_template("create_account.html", message="Username taken")
        elif request.form.get("password") != request.form.get("password_check"):
            return render_template("create_account.html", message="Error - Passwords do not match!")
        else:
            database.insert((request.form.get("username").upper(), request.form.get("first_name"), request.form.get("last_name"), request.form.get("email"), functions.hash(request.form.get("password"))))
            return redirect("/")
    return render_template("create_account.html")

@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        subejcts = database.get_subjects()
        return render_template("tasks.html", list_of_tasks = session.get("tasks"), subjects = subejcts)
    if request.method == "POST":
        description = request.form.get("paragraph_text")
        completed = False
        category = request.form.get("category")
        due_date = request.form.get("due_date")    
        set_date = datetime.date.today()    
        database.create_task((description, completed, category, due_date, set_date, session.get("username")))
        return redirect("/tasks")

@app.route("/tasks/<int:number>", methods=["POST", "GET"])
def show_task(number):
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        if session.get("username") == database.get_task_by_id(number)[6]:
            message = database.get_task_by_id(number)
        else:
            message = "Not your task"
        return render_template("tasks.html", message=message, list_of_tasks = session.get("tasks"), subjects = database.get_subjects())
    if request.method == "POST":
        database.mark_as_done(number)
        return redirect(f"/tasks/{number}")

@app.route("/reorder_tasks", methods=["POST", "GET"])
def reorder():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        order_by = request.form.get("order")
        if order_by == "0":
            functions.merge_sort(4, session.get("tasks"))
        elif order_by == "1":
            functions.merge_sort(5, session.get("tasks"))
        elif order_by == "2":
            functions.merge_sort(3, session.get("tasks"))
        return redirect("/tasks")

@app.route("/revision", methods = ["POST", "GET"])
def revision():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        print(session.get("revision_list_data"))
        revision = []
        for x in session.get("revision_list_data"):
            revision.append(x)
        return render_template("revision.html", revision = revision)
    if request.method == "POST":
        term = request.form.get("term")
        definition = request.form.get("definition")
        card_set = request.form.get("set_to_add_card")
        new_cards = request.form.get("title")
        if term and definition and card_set:
            if not card_set:
                card_set = next(iter(session.get("revision_list_data")))
            session["revision_list_data"][card_set][term] = definition
        elif new_cards:
            session["revision_list_data"][new_cards] = {}
        with open ("static/revision.json", "w") as outfile:
            json.dump(session["revision_list_data"], outfile)
        print(session.get("revision_list_data"))
        return redirect("/revision")

@app.route("/timetable", methods=["POST", "GET"])
def timetable():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        week = session.get("timetable").display()
        return render_template("timetable.html", message = week, tasks = database.get_tasks_by_username(session["username"]), days = [x for x in session["timetable"].week] )
    if request.method == "POST":
        day = request.form.get("day")
        task = request.form.get("task")
        remove = request.form.get("remove")
        add = request.form.get("add")
        if add:
            session["timetable"].add_task_to_day(day, task)
        if remove:
            if session["timetable"].remove_task_from_day(day, task):
                return redirect("/timetable")
        week = session.get("timetable").display()   
        return render_template("timetable.html", error = "Task not in day!", message=week, tasks = database.get_tasks_by_username(session["username"]), days = [x for x in session["timetable"].week])

@app.route("/account")
def account():
    if not session.get("name"):
        return redirect("/sign_in")
    if request.method == "GET":
        username, first_name, last_name, email, password = database.get_user_details(session.get("username"))
        number_of_tasks = len(database.get_tasks_by_username("H"))
        revision_set_numer = len(session.get("revision_list_data"))
        tasks_in_timetable = session.get("timetable").get_length()
        return render_template("account.html", name=first_name, username = username, last_name = last_name, email = email, password = password, revision_set_numer=revision_set_numer, tasks_in_timetable = tasks_in_timetable, number_of_tasks = number_of_tasks)

@app.route("/logout")
def logout():
    functions.save_timetable(session["timetable"].get_timetable_data(), session["username"])
    functions.save_revision(session["revision_list_data"], session["username"])
    session["name"] = None
    session["username"] = None
    session["revision_list_data"] = None
    session["timetable"] = None
    session["tasks"] = None
    return redirect("/")