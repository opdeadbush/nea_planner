import database
        
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

    def remove_task_from_day(self, day: str, task_id: int) -> bool:
        if self.week[day].remove_task(task_id):
            return True
        return False

    def display(self) -> list:
        result = []
        for key in self.week:
            list_of_tasks = self.week[key].get_tasks()
            result.append([key, list_of_tasks])
        return result
        
    def get_length(self) -> int:
        result = 0
        for key in self.week:
            result += len(self.week[key].get_task_ids())
        return result
        
class Day:
    def __init__(self) -> None:
        self.tasks_today = []

    def add_task(self, task_id: int) -> None:
        self.tasks_today.append(task_id)
        return

    def remove_task(self, task_id: int) -> bool:
        if task_id in self.tasks_today:
            self.tasks_today.remove(task_id)
            return True
        return False
    
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