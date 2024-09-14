import string

import random

import threading

from typing import List
import json

import hashlib

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
            if data[f"{key}"][0] == value:
                return True

        return False

    @staticmethod
    def verify_user_data(key, value) -> bool:
        with open("./Database/users.json", 'r') as db:
            data = json.load(db)
            if data[f"{key}"][0] == DatabaseManager.hash_with_salt(value, data[f"{key}"][1]):
                return True

        return False

    @staticmethod
    def is_exists(database_name: str, key) -> bool:
        with open("./Database/" + database_name + ".json", 'r') as db:
            data = json.load(db)

            return key in data

    @staticmethod
    def hash(pre_encrypted_data: str) -> (str, str):
        chrs = string.hexdigits
        salt = ""

        # generate the salt
        for _ in range(random.randint(9, 12)):
            salt += random.choice(chrs)

        encrypted_data = (salt + pre_encrypted_data).encode()

        for _ in range(3):
            encrypted_data = hashlib.sha256(encrypted_data).hexdigest().encode()

        return encrypted_data.decode(), salt

    @staticmethod
    def hash_with_salt(pre_encrypted_data: str, salt: str) -> str:
        encrypted_data = (salt + pre_encrypted_data).encode()

        for _ in range(3):
            encrypted_data = hashlib.sha256(encrypted_data).hexdigest().encode()

        return encrypted_data.decode()

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
