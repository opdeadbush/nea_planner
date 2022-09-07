import datetime

class Task():
    def __init__(self, name):
        self.name = name
        self.set_date = datetime.date.today()


class Homework(Task):
    def __init__(self):
        super().__init__(self)
        pass

class Timetable():
    def __init__(self):
        pass

def main():
    pass

if __name__ == "__main__":
    main()