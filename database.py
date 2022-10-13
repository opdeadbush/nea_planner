import sqlite3

def execute(query: str, arguments: tuple) -> None:
    connection = sqlite3.connect("./nea_database.db")
    connection.execute(query, arguments).fetchall()
    connection.commit()
    connection.close()
    return

def execute_and_return(query: str, arguments: tuple) -> list:
    details = []
    connection = sqlite3.connect("./nea_database.db")
    cursor = connection.execute(query, arguments).fetchall()
    for x in cursor:
        details.append(x)
    connection.commit()
    connection.close()
    return details

def get_username_and_password(username) -> tuple:
    username=username.upper()
    value = execute_and_return("SELECT first_name, password_hash FROM user_info WHERE username = ?", (username,))
    if value:    
        details = value[0]
    else:
        details = ('','')
    return details

def get_user_details(username):
    value = execute_and_return("SELECT * FROM user_info where username = ?", (username, ))
    if value:
        details = value[0]
    else:
        details = ("", "", "", "", "")
    return details

def check_for_email(email):
    cursor = execute_and_return("SELECT email FROM user_info WHERE email = ?", (email,))
    result = False
    if cursor:
        result = True
    return result

def check_for_username(username):
    cursor = execute_and_return("SELECT username FROM user_info WHERE username = ?", (username, ))
    result = False
    if cursor:
        result = True
    return result

def get_task_by_id(id):
    details = execute_and_return("SELECT * FROM tasks WHERE task_id = ?", (id, ))[0]
    return details

def get_tasks_by_username(username):
    value = execute_and_return("SELECT * FROM tasks JOIN subjects ON tasks.category = subjects.subject WHERE tasks.username = ?", (username, ))
    details = []
    for x in value:
        details.append(x)
    return details

def get_subjects():
    connection = sqlite3.connect("./nea_database.db")
    cursor = connection.execute("SELECT * FROM subjects")
    details = []
    for x in cursor:
        details.append(x)
    connection.commit()
    connection.close()
    return details

def get_timetable(user):
    value = execute_and_return("SELECT * FROM timetable WHERE user = ?", (user, ))
    if not value:
        execute("INSERT INTO timetable (contents, user) VALUES (?, ?)", (str({"Monday": "", "Tuesday": "", "Wednesday": "", "Thursday": "", "Friday": "", "Saturday": "", "Sunday": ""}), user))
        return get_timetable(user)
    return eval(value[0][0])

def insert_timetable(contents, user):
    execute("UPDATE timetable SET contents = ? WHERE user = ?", (contents, user))

def mark_as_done(task):
    execute("UPDATE tasks SET completed = True WHERE task_id = ?", (task, ))
    return 

def insert(attributes):
    query="""
    INSERT INTO user_info
    VALUES (?, ?, ?, ?, ?)
    """
    execute(query, attributes)
    return

def create_task(attributes):
    query = """
    INSERT INTO tasks (description, completed, category, due_date, set_date, username)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    execute(query, attributes)
    return

if __name__ == "__main__":
    insert_timetable("", "H")