import hashlib
import sqlite3
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

def insert(field, attribute):
    connection = sqlite3.connect("./nea_database.db")
    query="""
    INSERT INTO user_info (%s)
    VALUES (?) 
    """
    value = connection.execute(query % (field), (attribute,))
    connection.commit()
    connection.close()

def hash(string):
    x = hashlib.sha256(str.encode(string))
    return(x.hexdigest())

if __name__ == "__main__":
    print(get_user_details("harvz"))