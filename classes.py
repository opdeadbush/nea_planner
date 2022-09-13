from dataclasses import dataclass
import datetime
import database

class Task_Manager():
    def __init__(self, username):
        self.task_list = []
        tasks = database.get_task_by_username(username)
        for task in tasks:
            self.task_list.append(Task(task[0], task[1], task[2], task[3], task[4], task[5], task[6]))
    
    def list_tasks(self):
        y = self.task_list[0].get_information()
        return y

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

if __name__ == "__main__":
    tasks = Task_Manager("H")
    print(tasks.list_tasks())