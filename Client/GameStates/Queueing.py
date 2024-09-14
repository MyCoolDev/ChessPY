import math

import pygame

from Client.GameStates.GlobalStateImport import *

class Queueing(BaseState):
    def __init__(self, state_manager: StateManager, screen: pygame.Surface, client_socket):
        BaseState.__init__(self, state_manager)

        self.client_socket = client_socket
        self.__init_vars(screen)

    def __init_vars(self, screen: pygame.Surface = None, *args, **kwargs):
        self.alpha = 0

        self.queue_box = MonoBehaviour(pygame.Vector2(min(screen.get_width() / 2, 600), 50), pygame.Vector2((screen.get_width() - min(screen.get_width() / 2, 600)) / 2, (screen.get_height() - 50) / 2), (220, 213, 197), border_radius=6)
        self.queue_box_anim = MonoBehaviour(pygame.Vector2(50, 50), self.queue_box.position + pygame.Vector2((self.queue_box.size.x - 50) / 2 - math.cos(self.alpha) * ((self.queue_box.size.x - 50) / 2), 0), (80, 59, 54), border_radius=6)
        self.title = Text("Searching a match...", "Open Sans", 70, True, pygame.Vector2(screen.get_width() / 2, self.queue_box.position.y - 100), (226, 226, 226), top_mode=True)
        self.stop_button = Button(pygame.Vector2(340, 50), pygame.Vector2((screen.get_width()) / 2, (screen.get_height()) / 2 + 75), (255, 74, 74), "Stop", "Open Sans", 20, (255, 255, 255), border_radius=6)

    def __update_queueing_animation(self):
        self.alpha += 1 / 100
        self.alpha %= 360
        self.queue_box_anim = MonoBehaviour(pygame.Vector2(50, 50), self.queue_box.position + pygame.Vector2((self.queue_box.size.x - 50) / 2 - math.cos(self.alpha) * ((self.queue_box.size.x - 50) / 2), 0), (80, 59, 54), border_radius=6)

    def update(self, dt: float, events: list, *args, **kwargs):
        self.__update_queueing_animation()
        if self.stop_button.update(dt, events):
            self.client_socket.send_request({"event": "stop_queue"})


    def render(self, screen: pygame.Surface, *args, **kwargs):
        self.title.render(screen)
        self.queue_box.render(screen)
        self.queue_box_anim.render(screen)
        self.stop_button.render(screen)
