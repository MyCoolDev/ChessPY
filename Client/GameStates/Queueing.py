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

    def __update_queueing_animation(self):
        self.alpha += 1 / 100
        self.alpha %= 360
        self.queue_box_anim = MonoBehaviour(pygame.Vector2(50, 50), self.queue_box.position + pygame.Vector2((self.queue_box.size.x - 50) / 2 - math.cos(self.alpha) * ((self.queue_box.size.x - 50) / 2), 0), (80, 59, 54), border_radius=6)

    def update(self, dt: float, events: list, *args, **kwargs):
        self.__update_queueing_animation()

    def render(self, screen: pygame.Surface, *args, **kwargs):
        self.title.render(screen)
        self.queue_box.render(screen)
        self.queue_box_anim.render(screen)
