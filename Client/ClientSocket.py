import threading

import socket
import json

from Client.Components.Error import Error
from Client.config.utils import client_print
from Client.Components.BaseState import StateManager

class ClientSocket:
    def __init__(self, config: dict, state_manager: StateManager):
        self.client_socket = socket.socket()
        self.config = config
        self.client_socket.settimeout(int(self.config["SOCKET"]["CONNECTION_TIMEOUT"]))

        self.state_manager = state_manager
        self.error_box = []

    def connect(self):
        try:
            self.client_socket.connect((self.config["SOCKET"]["SERVER_ADDRESS"], int(self.config["SOCKET"]["SERVER_PORT"])))
            self.client_socket.settimeout(None)
            threading.Thread(target=self.handle_server).start()
            return True
        except Exception as e:
            client_print(str(e))
            return False

    def send_request(self, data: dict):
        try:
            self.client_socket.send(json.dumps(data).encode())
        except Exception as e:
            client_print(str(e))

    def handle_server(self):
        try:
            while True:
                data = json.loads(self.client_socket.recv(1024).decode())

                if 'code' not in data.keys():
                    continue

                if int(int(data["code"]) / 100) == 4:
                    self.error_box.append(Error(int(data["code"]), data["event"], data["msg"]))

                else:
                    if data["code"] == 200 and data["event"] == "login complete":
                        self.state_manager.remove_state(0)
        except Exception as e:
            client_print(str(e))
