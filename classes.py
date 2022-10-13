from sqlite3 import Time
import database, functions

class Revision_Set:
    def __init__(self, name: str) -> None:
        self.name = name
        self.note_bundle = {}

    def create_revision_note(self, name: str, contents: str="Default Notes"):
        self.note_bundle[name] = (Note(self.name, name, contents))
        return
  
    def get_details(self) -> str:
        return self.name

class Note:
    def __init__(self, parent: str, name: str, contents) -> None:
        self.parent = parent
        self.name = name
        self.contents = contents
    
    def rewrite_note(self, new_contents: str) -> None:
        self.contents = new_contents
        return
    
    def display_note(self):
        print(f"{self.name} --> {self.contents} | Belongs to {self.parent}")
        
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
    
    def get_timetable_data(self):
        details = {}
        for x in self.week:
            details[x] = self.week[x].get_task_ids()
        return details

    def add_task_to_day(self, day: str, task_id: int) -> None:
        self.week[day].add_task(task_id)  
        return                               
    
    def display(self) -> list:
        result = []
        for key in self.week:
            list_of_tasks = self.week[key].get_tasks()
            if list_of_tasks:
                # print(key + ":")
                # for task in list_of_tasks:
                #     print(f"    ➟ {task[3]}")
                # print("__________________")
                result.append([key, list_of_tasks])
            else:
                continue
        return result
        
class Day:
    def __init__(self) -> None:
        self.tasks_today = []

    def add_task(self, task_id: int) -> None:
        self.tasks_today.append(task_id)
        return

    def remove_task(self, task_id: int) -> None:
        self.tasks_today.remove(task_id)
        return
    
    def reorder_day(self, swap_from_id: int, swap_to_id: int) -> None:
        for x in range(len(self.tasks_today)):
            print(self.tasks_today[x])
            if self.tasks_today[x] == swap_from_id:
                swap_from_idx = x
            elif self.tasks_today[x] == swap_to_id:
                swap_to_idx = x
        self.tasks_today[swap_to_idx], self.tasks_today[swap_from_idx] = self.tasks_today[swap_from_idx], self.tasks_today[swap_to_idx]
        for x in self.tasks_today:
            print(x)
        return

    def get_tasks(self) -> list:
        tasks = []
        for x in self.tasks_today:
            tasks.append(database.get_task_by_id(x))
        return tasks
    
    def get_task_ids(self):
        details = []
        for x in self.tasks_today:
            details.append(str(x))
        return details

if __name__ == "__main__":
    # revision_set = Revision_Set("Maths")
    # revision_set.create_revision_note("Integration", "Integrate innit")
    # revision_set.display_notes()
    timetable = functions.initialise_timetable(database.get_timetable("H"))
    print(timetable.get_timetable_data())