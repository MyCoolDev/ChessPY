import socket
import enum

class Status(enum.IntEnum):
    Wait = 0,
    Live = 1
    Queue = 2
    Matched = 3
    InGame = 4

class Connection:
    def __init__(self, address: str, con: socket.socket):
        self.connection = con
        self.status: Status = Status.Wait
        self.data = {'address': address}
