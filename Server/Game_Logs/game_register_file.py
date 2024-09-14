import json
import enum
import datetime


# .tlog - test file log
# .log - official file log

class LogType(enum.IntEnum):
    TestLog = 0,
    OfficialLog = 1,


log_type_values = [".tlog", ".log"]


class RegisterFile:
    def __init__(self, log_type: LogType):
        self.file_id = -1
        self.file_type = log_type_values[log_type]

        with open('control.json', 'rw') as json_file:
            data = json.load(json_file)
            self.file_id = data[self.file_type]
            data[self.file_type] += 1
            json_file.seek(0)
            json_file.write(json.dumps(data))

        with open(f'__{self.file_id}.tlog', 'w+') as file:
            file.write(f"[{datetime.datetime.now()}] ({self.file_id}) Chess Game")

    def write_to_file(self, data: str):
        with open(f'__{self.file_id}.tlog', 'a') as file:
            file.write(f"[{datetime.datetime.now()}] " + data)
