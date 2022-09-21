import database

class revision:
    def __init__(self, name) -> None:
        self.name = name
        self.note_bundle = []
    
    def create_revision_note(self):
        self.note_bundle += note(self.name)
    
    def display_notes(self):
        pass

class note:
    def __init__(self, parent) -> None:
        self.parent = parent

class Timetable:
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
        
class Day:
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
