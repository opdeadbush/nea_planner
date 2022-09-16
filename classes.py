from dataclasses import dataclass
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
            self.Monday: Day(),
            self.Tuesday: Day(),
            self.Wednesday: Day(),
            self.Thursday: Day(),
            self.Friday: Day(),
            self.Saturday: Day(),
            self.Sunday: Day()
        }
                                        
    def _display(self):
        for key, value in self.week:
            print(key, value)


class Day():
    def __init__(self) -> None:
        self.tasks_today = []

    def add_task(self, task_id):
        self.tasks_today.append(task_id)

if __name__ == "__main__":
    timetable = Timetable()
