import threading

import pygame

import socket
import json

from Client.StoppableThread import StoppableThread

from Client.Components.Error import Error
from Client.config.utils import client_print
from Client.Components.BaseState import StateManager

from Client.GameStates.Queueing import Queueing

class ClientSocket:
    def __init__(self, config: dict, state_manager: StateManager, screen: pygame.Surface):
        self.client_socket = socket.socket()
        self.config = config
        self.client_socket.settimeout(int(self.config["SOCKET"]["CONNECTION_TIMEOUT"]))
        self.screen = screen

        self.__init_server_thread()

        self.state_manager = state_manager
        self.error_box = []

    def __init_server_thread(self):
        self.thread = StoppableThread(target=self.handle_server)
        self.thread.start()

    def connect(self):
        try:
            self.client_socket.connect((self.config["SOCKET"]["SERVER_ADDRESS"], int(self.config["SOCKET"]["SERVER_PORT"])))
            self.client_socket.settimeout(None)

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
            while self.thread.isAlive():
                data = json.loads(self.client_socket.recv(1024).decode())

                print(data)

                if 'code' not in data.keys():
                    continue

                if int(int(data["code"]) / 100) == 4:
                    self.error_box.append(Error(int(data["code"]), data["event"], data["msg"]))

                elif data["code"] == 200:
                    if data["event"] == "login complete":
                        self.state_manager.remove_state(0)
                    if data["event"] == "queue stated":
                        self.state_manager.insert_state(Queueing(self.state_manager, self.screen, self))
        except Exception as e:
            client_print(str(e))
            self.thread.stop()
            self.client_socket.detach()
            self.client_socket.close()
