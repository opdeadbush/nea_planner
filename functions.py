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

def merge_sort(sort_idx, sort_list):
    n = len(sort_list)
    if n < 2:
        return
    else:
        mid = n // 2
        s1 = sort_list[0:mid]
        s2 = sort_list[mid:n]
        merge_sort(sort_idx, s1)
        merge_sort(sort_idx, s2)
        return merge(s1, s2, sort_list, sort_idx)

def merge(s1, s2, s, idx):
    i = j = 0
    while i + j < len(s):
        if (j == len(s2)) or (i < len(s1) and s1[i][idx] < s2[j][idx]):
            s[i + j] = s1[i]
            i = i + 1
        else:
            s[i + j] = s2[j]
            j = j + 1
    return s