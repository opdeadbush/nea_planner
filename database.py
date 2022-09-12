import hashlib
import sqlite3
from tabnanny import check
from webbrowser import get

def get_username_and_password(username):
    username=username.upper()
    connection = sqlite3.connect("./nea_database.db")
    value = connection.execute("SELECT first_name, password_hash FROM user_info WHERE username = ?", (username,)).fetchall()
    if value:    
        details = value[0]
    else:
        details = ('','')
    connection.commit()
    connection.close()
    return details

def get_user_details(username):
    connection = sqlite3.connect("./nea_database.db")
    cursor = connection.execute("SELECT * FROM user_info where username = ?", (username, )).fetchall()
    if cursor:
        details = cursor[0]
    else:
        details = ("", "", "", "", "")
    connection.commit()
    connection.close()
    return details

def check_for_password(email):
    connection = sqlite3.connect("./nea_database.db")
    query="""
    SELECT password_hash FROM user_info WHERE email = ?
    """
    cursor = connection.execute(query, (email,)).fetchall()
    if cursor:
        result = True
    else:
        result = False
    connection.commit()
    connection.close()
    return result

def insert(attribute):
    connection = sqlite3.connect("./nea_database.db")
    query="""
    INSERT INTO user_info
    VALUES (?, ?, ?, ?, ?)
    """
    value = connection.execute(query, attribute)
    connection.commit()
    connection.close()

def hash(string):
    x = hashlib.sha256(str.encode(string))
    return(x.hexdigest())

def f(x):
    return (x)

if __name__ == "__main__":
    print(get_user_details("H"))