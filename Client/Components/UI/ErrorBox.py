import pygame

from Client.Components.MonoBehaviour import MonoBehaviour
from Client.Components.UI.Text import Text
from Client.Components.UI.Button import Button

class ErrorBox(MonoBehaviour):
    def __init__(self, bottom_pos: int, screen: pygame.Surface, code: int, event: str, description: str):
        self.description_text = Text(description, "Open Sans", 20, False, pygame.Vector2(0, 0), (255, 255, 255), top_left_mode=True)

        base_pos = pygame.Vector2(screen.get_width() - 100 - self.description_text.text_surface.get_width(), bottom_pos - 160)
        super().__init__(pygame.Vector2(self.description_text.text_surface.get_width() + 80, 160), base_pos, (29, 29, 29), border_radius=10)
        self.event_text = Text(event, "Open Sans", 20, True, base_pos + pygame.Vector2(20, 20), (255, 255, 255), top_left_mode=True)
        self.description_text = Text(description, "Open Sans", 20, False, self.event_text.position + pygame.Vector2(0, 30), (255, 255, 255), top_left_mode=True)
        self.code_text = Text(f"Status Code: {code}", "Open Sans", 20, False, base_pos + pygame.Vector2(20, 130), (255, 255, 255), top_left_mode=True)

        self.exit_button = Button(pygame.Vector2(10, 10), base_pos + pygame.Vector2(self.size.x - 15, 15), (255, 55, 55), "", border_radius=10)

    def update(self, dt: float, events: list):
        return self.exit_button.update(dt, events)

    def render(self, surface: pygame.Surface):
        super().render(surface)
        self.event_text.render(surface)
        self.description_text.render(surface)
        self.code_text.render(surface)
        self.exit_button.render(surface)
