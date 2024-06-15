import math
import pygame
import socket

import Client.config.utils as utils
from Client.Components.BaseState import StateManager
from Client.GameStates.LoginRegister import LoginRegisterState
from Client.GameStates.MainMenu import MainMenu
from Client.ClientSocket import ClientSocket

class Game:
    def __init__(self):
        self.config = utils.load_config("config/config.ini")

        self.screen = pygame.display.set_mode()
        pygame.display.set_caption("ChessPY")
        self.events = None

        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.state_manager = StateManager()

        self.client_socket = ClientSocket(self.config, self.state_manager, self.screen)
        self.client_socket.connect()

        self.state_manager.add_state(LoginRegisterState(self.state_manager, self.screen, self.client_socket))
        self.state_manager.add_state(MainMenu(self.state_manager, self.screen, self.client_socket))

    def start_game(self):
        try:
            while self.running:
                self.events = pygame.event.get()
                for event in self.events:
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()

                self.screen.fill((46, 46, 46))

                self.state_manager.update(self.dt, self.events)
                self.state_manager.render(self.screen)

                # flip() the display to put your work on screen
                pygame.display.flip()

                # limits FPS to 60
                # dt is delta time in seconds since last frame, used for framerate-
                # independent physics.
                dt = self.clock.tick(60) / 1000
        finally:
            print("Closing Game")
            pygame.quit()
            self.client_socket.thread.stop()

if __name__ == '__main__':
    Game().start_game()
