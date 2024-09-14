import pygame

from Components.BaseState import BaseState, StateManager


class InGame(BaseState):
    def __init__(self, state_manager: StateManager, screen: pygame.Surface, client_socket):
        BaseState.__init__(self, state_manager)

        self.client_socket = client_socket
        self.__init_vars(screen)

    def __init_vars(self, screen: pygame.Surface = None, *args, **kwargs):
        pass

    def update(self, dt: float, events: list, *args, **kwargs):
        pass

    def render(self, screen: pygame.Surface, *args, **kwargs):
        pass
