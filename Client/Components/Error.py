import pygame

from Client.Components.UI.ErrorBox import ErrorBox

class Error:
    def __init__(self, code: int, event: str, description: str):
        self.code = code
        self.event = event
        self.description = description
        self.error_box = None

    def update(self, dt: float, events: list):
        if self.error_box is not None:
            return self.error_box.update(dt, events)

        return False

    def create_error_box(self, bottom_pos: int, screen: pygame.Surface) -> ErrorBox:
        self.error_box = ErrorBox(bottom_pos, screen, self.code, self.event, self.description)
        return self.error_box
