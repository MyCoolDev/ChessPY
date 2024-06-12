import threading

from typing import List
import json


class DatabaseManager:
    def __init__(self):
        self.thread = threading.Thread(target=self.__TaskChecker)
        self.tasks: List[Task] = []
        self.thread.start()

    @staticmethod
    def __add_data(database_name: str, key, value):
        with open("./Database/" + database_name + ".json", 'r+') as db:
            data = json.loads(db.read())
            db.seek(0)
            data[key] = value
            db.write(json.dumps(data))

    def add_data(self, database_name: str, key, value):
        self.tasks.append(Task("AddData", database_name, [key, value]))

    @staticmethod
    def verify_data(database_name: str, key, value) -> bool:
        with open("./Database/" + database_name + ".json", 'r') as db:
            data = json.load(db)
            if data[f"{key}"] == str(value):
                return True

        return False

    @staticmethod
    def is_exists(database_name: str, key) -> bool:
        with open("./Database/" + database_name + ".json", 'r') as db:
            data = json.load(db)

            return key in data

    @staticmethod
    def hash(string: str, p: int, m: int) -> int:
        hash_number = 0

        for i in range(0, len(string)):
            hash_number += ord(string[i]) * pow(int(p), i)

        return hash_number % int(m)

    def __TaskChecker(self):
        while True:
            if len(self.tasks) > 0:
                task = self.tasks.pop(0)

                if task.job == "AddData":
                    self.__add_data(task.db_name, *task.args)


class Task:
    def __init__(self, job: str, db_name: str, args: list):
        self.job = job
        self.db_name = db_name
        self.args = args
