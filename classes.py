import database

class Task_Manager():
    def __init__(self, username):
        self.task_list = []
        tasks = database.get_task_by_username(username)
        for task in tasks:
            self.task_list.append(Task(task[0], task[1], task[2], task[3], task[4], task[5], task[6]))
    
    def get_tasks(self):
        tasks = []
        for x in self.task_list:
            tasks.append(x.get_information())
        return tasks

    def get_task_by_id(self, id):
        for x in self.task_list:
            if x.get_id == id:
                return x.get_information()
        return

class Task():
    def __init__(self, id, description, completed, category, due_date, set_date, username):
        self.id = id
        self.description = description
        self.completed = completed
        self.category = category
        self.due_date = due_date
        self.set_date = set_date
        self.username = username
    
    def get_information(self):
        return [self.id, self.description, self.completed, self.category, self.due_date, self.set_date, self.username]

    def mark_task_complete(self):
        self.completed = True
    
    def get_id(self):
        return self.id

class Timetable():
    def __init__(self) -> None:
        self.week = {
            "Monday": Day(),
            "Tuesday": Day(),
            "Wednesday": Day(),
            "Thursday": Day(),
            "Friday": Day(),
            "Saturday": Day(),
            "Sunday": Day()
        }

    def add_task_to_day(self, day, task_id):
        self.week[day].add_task(task_id)                                 
    
    def display(self):
        result = []
        for key in self.week:
            list_of_tasks = self.week[key].get_tasks()
            if list_of_tasks:
                print(key + ":")
                for task in list_of_tasks:
                    print(f"    ➟ {task[3]}")
                print("__________________")
                result.append(f"{key}: {list_of_tasks}")
            else:
                continue
        return result
        

class Day():
    def __init__(self) -> None:
        self.tasks_today = []

    def add_task(self, task_id):
        self.tasks_today.append(task_id)

    def remove_task(self, task_id):
        self.tasks_today.remove(task_id)

    def get_tasks(self):
        tasks = []
        for x in self.tasks_today:
            tasks.append(database.get_task_by_id(x))
        return tasks


if __name__ == "__main__":
    week = Timetable()
    for x in week.week:
        for y in range(1, 5, 1):
            week.add_task_to_day(x, y)
    week.display()
