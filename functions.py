import classes, database, hashlib, json

def initialise_timetable(timetable_data):
    timetable = classes.Timetable()
    for item in timetable_data:
        if timetable_data[item]:
            for task_id in timetable_data[item]:
                timetable.add_task_to_day(item, task_id)
    return timetable

def save_timetable(timetable_data, user):
    database.insert_timetable(str(timetable_data), user)

def initialise_revision(user):
    data = eval(database.get_revision(user)[0])
    with open ("./static/revision.json", "w") as outfile:
        json.dump(data, outfile)
    return data

def save_revision(data, user):
    database.insert_revision(data, user)

def hash(string):
    x = hashlib.sha256(str.encode(string))
    return(x.hexdigest())