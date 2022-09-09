import hashlib
import sqlite3
from tabnanny import check
from webbrowser import get

def get_user_details(username):
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

def check_for_password(password_hash):
    connection = sqlite3.connect("./nea_database.db")
    query="""
    SELECT password_hash FROM user_info WHERE password_hash = ?
    """
    cursor = connection.execute(query, (password_hash,)).fetchall()
    if cursor:
        print(cursor[0])
    else:
        print(cursor)
    connection.commit()
    connection.close()
    return

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

if __name__ == "__main__":
    check_for_password(hash("asd"))