import pygame

class BaseState:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def __init_vars(self):
        pass

    def restart_state(self):
        self.__init_vars()

    def update(self, dt: float, events: list):
        pass

    def render(self, screen: pygame.Surface):
        pass

class StateManager:
    def __init__(self):
        self.__states = []

    def add_state(self, state: BaseState):
        self.__states.append(state)

    def insert_state(self, state: BaseState):
        self.__states.insert(0, state)

    def remove_state(self, index: int) -> bool:
        if index < len(self.__states):
            self.__states.pop(index)
            return True

        return False

    def get_current_state(self):
        if len(self.__states) >= 0:
            return self.__states[0]

        return None

    def update(self, dt: float, events: list):
        self.__states[0].update(dt, events)

    def render(self, screen: pygame.Surface):
        self.__states[0].render(screen)
