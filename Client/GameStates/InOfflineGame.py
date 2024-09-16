import pygame

from Components.BaseState import BaseState, StateManager
from Components.ChessBoard import ChessBoard
import Client.Chess.logic as logic

class InOfflineGame(BaseState):
    def __init__(self, state_manager: StateManager, screen: pygame.Surface, client_socket):
        BaseState.__init__(self, state_manager)

        self.client_socket = client_socket
        self.screen = screen
        self.__init_vars(screen)
        self.turn = 0   # 0 - white, 1 - black
        self.focus_piece = (None, [])

    def __init_vars(self, screen: pygame.Surface = None, *args, **kwargs):
        self.chess_board = ChessBoard(pygame.Vector2((screen.get_width() - 480) / 2, (screen.get_height() - 480) / 2), 480, show_pieces=True)

    def update(self, dt: float, events: list, *args, **kwargs):
        cords = self.chess_board.find_chess_pieces(events)

        if cords != (-1, -1):
            print((cords[0], 8 - cords[1]))
            game_pos = logic.from_cords((cords[0], 8 - cords[1]), self.chess_board.game_board)

            if self.focus_piece[0] is not None and game_pos in self.focus_piece[1] and logic.is_move_legal(self.focus_piece[0] + game_pos, self.turn, self.chess_board.game_board):
                pass

            moves = logic.get_all_possible_moves(game_pos, self.chess_board.game_board)
            if len(moves) > 0:
                self.focus_piece = (game_pos, moves)

    def render(self, screen: pygame.Surface, *args, **kwargs):
        self.chess_board.render(screen)
        if self.focus_piece[0] is not None:
            for x in self.focus_piece[1]:
                self.chess_board.mark_blocks(self.screen, (ord(x[0]) - 96, 9 - int(x[1])))
