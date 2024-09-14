import pygame

from Components.BaseState import BaseState, StateManager
from Components.Text import Text
from Components.Button import Button
from ClientSocket import ClientSocket

from Components.ChessBoard import ChessBoard

class MainMenu(BaseState):
    def __init__(self, state_manager: StateManager, screen: pygame.Surface, client_socket: ClientSocket):
        BaseState.__init__(self, state_manager)

        self.client_socket = client_socket
        self.__init_vars(screen)

    def __init_vars(self, screen: pygame.Surface = None, *args, **kwargs):
        self.themes = [((80, 59, 54), (220, 213, 197)), ((55, 80, 54), (220, 213, 197)), ((65, 97, 111), (220, 213, 197)), ((163, 76, 76), (220, 213, 197))]
        self.current_theme = 0

        self.chess_board = ChessBoard(pygame.Vector2((screen.get_width() - 480) / 2, (screen.get_height() - 480) / 2), 480, theme=self.themes[self.current_theme], show_pieces=True)
        self.next_chess_board = ChessBoard(self.chess_board.base_pos + pygame.Vector2(self.chess_board.box_size * 8 + 50, self.chess_board.box_size * 2), 240, theme=self.themes[self.current_theme + 1])
        self.back_chess_board = ChessBoard(self.chess_board.base_pos + pygame.Vector2(-self.chess_board.box_size * 4 - 50, self.chess_board.box_size * 2), 240, theme=self.themes[self.current_theme - 1])
        self.credits = Text("By Ron & Itay", "Open Sans", 30, True, pygame.Vector2(screen.get_width() / 2, self.chess_board.base_pos.y - 100), (226, 226, 226), top_mode=True)
        self.title = Text("ChessPY", "Open Sans", 70, True, pygame.Vector2(screen.get_width() / 2, self.credits.position.y - self.credits.text_surface.get_height() - 40), (226, 226, 226), top_mode=True)
        self.start_button = Button(pygame.Vector2(340, 50), pygame.Vector2(screen.get_width() / 2, self.chess_board.base_pos.y + self.chess_board.box_size * 8 + 80), (74, 114, 255), "Start Playing", "Open Sans", 20, (255, 255, 255), border_radius=6)
        self.exit_button = Button(pygame.Vector2(340, 50), pygame.Vector2(screen.get_width() / 2, self.start_button.position.y + self.start_button.size.y + 50), (255, 74, 74), "Exit", "Open Sans", 20, (255, 255, 255), border_radius=6)

    def update(self, dt: float, events: list, *args, **kwargs):
        if self.start_button.update(dt, events):
            self.client_socket.send_request({"event": "start_queue"})
        if self.exit_button.update(dt, events):
            pygame.quit()
        if self.next_chess_board.is_clicked(events):
            self.current_theme += 1
            self.current_theme %= len(self.themes)

            self.chess_board.update_theme(self.themes[self.current_theme])
            self.next_chess_board.update_theme(self.themes[(self.current_theme + 1) % len(self.themes)])
            self.back_chess_board.update_theme(self.themes[self.current_theme - 1])

        if self.back_chess_board.is_clicked(events):
            self.current_theme -= 1

            if self.current_theme == -1:
                self.current_theme += len(self.themes)

            self.chess_board.update_theme(self.themes[self.current_theme])
            self.next_chess_board.update_theme(self.themes[(self.current_theme + 1) % len(self.themes)])
            self.back_chess_board.update_theme(self.themes[self.current_theme - 1])

    def render(self, screen: pygame.Surface, *args, **kwargs):
        self.title.render(screen)
        self.credits.render(screen)
        self.chess_board.render(screen)
        self.next_chess_board.render(screen)
        self.back_chess_board.render(screen)
        self.start_button.render(screen)
        self.exit_button.render(screen)
