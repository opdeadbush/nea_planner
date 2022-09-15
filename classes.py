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

if __name__ == "__main__":
    tasks = Task_Manager("H")
    x = tasks.get_task_by_id(1)
    print(x)