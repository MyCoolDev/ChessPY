import random
import socket
import time

import DataStructures.connections as connections

from typing import List


class GameManager:
    def __init__(self):
        self.queue: List[connections] = []
        self.games = []

    def search_match(self):
        while True:
            if len(self.queue) > 1:
                player1 = self.queue.pop(0)
                player2 = self.queue.pop(0)
                game = Game(player1.data["username"], player2.data["username"], 10 * 60 * 1000)
                player1.data["game"] = game
                player1.data["game"] = game

    def remove_from_queue(self, value):
        if self.queue.count(value) > 0:
            self.queue.remove(value)

    def add_to_queue(self, con):
        self.queue.append(con)


# GAME GLOBAL PIECES VALUES
PIECES_VALUES = {
    900: "Q",
    90: "K",
    30.5: "B",
    30: "N",
    50: "R",
    10: ""
}


class Game:
    def __init__(self, p1: str, p2: str, duration: int):
        self.last_move = 0
        self.players = {p1: duration, p2: duration}
        self.turn = random.randint(0, 1) # white = 0 : black = 1
        self.winner = None
        self.game_history = []
        self.game_board = [["R", "N", "B", "Q", "K", "B", "K", "R"],
                            ["P", "P", "P", "P", "P", "P", "P", "P"],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["p", "p", "p", "p", "p", "p", "p", "p"],
                            ["r", "n", "b", "q", "k", "b", "k", "r"]]

    def check_if_move_legal(self, move: str, side: bool) -> bool:
        if side not in [0, 1]:
            return False

        if move[0].islower():
            return self.is_valid_pawn_move(move, side)

    def is_valid_pawn_move(self, move: str, side: bool) -> bool:
        # Implement pawn move validation
        try:
            file = ord(move[0]) - ord('a')
            if file < 0 or file > 7:
                return False

            if side:
                if move[1] == "2":
                    return False

                if move[1] != 'x' and move[1] != '=':
                    rank = int(move[1]) - 1
                    if rank < 0 or rank > 7:
                        return False

                    if self.game_board[file][1] != "P":
                        if self.game_board[file][rank - 1] != "P":
                            return False
                        if self.game_board[file][rank] != "":
                            return False
                    else:
                        if self.game_board[file][rank - 1] != "P" and self.game_board[file][rank - 2] != "P":
                            return False
                        if self.game_board[file][rank] != "" or self.game_board[file][rank - 1] != "":
                            return False

                if move[1] == 'x':
                    eat_file = ord(move[2]) - ord('a')

                    if eat_file < 0 or eat_file > 7:
                        return False

                    eat_rank = int(move[3]) - 1

                    if eat_rank < 0 or eat_rank > 7:
                        return False

                    if self.game_board[file][eat_rank - 1] != "P":
                        return False

                    if self.game_board[eat_file][eat_rank] == "" or self.game_board[eat_file][eat_rank].isupper():
                        return False

                    if move[4] == '=':
                        if eat_rank != 7:
                            return False

                if move[1] == "=":
                    if self.game_board[file][6] != "P" or self.game_board[file][7] != "":
                        return False

            else:
                if move[1] == "7":
                    return False

                if move[1] != 'x' and move[1] != '=':
                    rank = int(move[1]) - 1
                    if self.game_board[file][1] != "P":
                        if self.game_board[file][rank] != "P":
                            return False
                        if self.game_board[file][rank] != "":
                            return False
                    else:
                        if self.game_board[file][rank + 1] != "P" and self.game_board[file][rank + 2] != "P":
                            return False
                        if self.game_board[file][rank] != "" or self.game_board[file][rank + 1] != "":
                            return False

                if move[1] == 'x':
                    eat_file = ord(move[2]) - ord('a')
                    if eat_file < 0 or eat_file > 7:
                        return False
                    eat_rank = int(move[3]) - 1
                    if eat_rank < 0 or eat_rank > 7:
                        return False
                    if self.game_board[file][eat_rank + 1] != "p":
                        return False
                    if self.game_board[eat_file][eat_rank] == "" or self.game_board[eat_file][eat_rank].islower():
                        return False
                    if move[4] == '=':
                        if eat_rank != 1:
                            return False

                if move[1] == "=":
                    if self.game_board[file][1] != "p" or self.game_board[file][0] != "":
                        return False

            return True
        finally:
            return False

    def is_valid_knight_move(self, move: str):
        # Implement knight move validation
        pass

    def is_valid_bishop_move(self, move: str):
        # Implement bishop move validation
        return self.check_diagonal(self, move)

    def check_diagonal(self, move: str):
        piece = move[0]
        if move[1] != 'x':
            file = ord(move[1]) - ord('a')
            rank = int(move[2]) - 1
        else:
            file = ord(move[2]) - ord('a')
            rank = int(move[3]) - 1

        return self.actually_check_diagonal(self, file, rank, piece)

    def actually_check_diagonal(self, File, Rank, piece):
        found = False
        file = File + 1
        rank = Rank + 1
        while file in range(0, 8) and rank in range(0, 8):
            if self.game_board[file][rank].upper() != piece and self.game_board[file][rank].upper() != "":
                break
            if self.game_board[file][rank].upper() == piece:
                return True

            rank += 1
            file += 1

        file = File + 1
        rank = Rank - 1
        while file in range(0, 8) and rank in range(0, 8):
            if self.game_board[file][rank].upper() != piece and self.game_board[file][rank].upper() != "":
                break
            if self.game_board[file][rank].upper() == piece:
                return True

            rank -= 1
            file += 1

        file = File - 1
        rank = Rank - 1
        while file in range(0, 8) and rank in range(0, 8):
            if self.game_board[file][rank].upper() != piece and self.game_board[file][rank].upper() != "":
                break
            if self.game_board[file][rank].upper() == piece:
                return True

            rank -= 1
            file -= 1

        file = File - 1
        rank = Rank + 1
        while file in range(0, 8) and rank in range(0, 8):
            if self.game_board[file][rank].upper() != piece and self.game_board[file][rank].upper() != "":
                break
            if self.game_board[file][rank].upper() == piece:
                return True

            rank += 1
            file -= 1

        return False

    def is_valid_rook_move(self, move: str):
        # Implement rook move validation
        pass

    def is_valid_queen_move(self, move: str, side: bool):
        # Implement queen move validation
        if side:
            before_file = 0
            for play in self.game_history[::2]:
                if play[0] == "Q":
                    if play[1] != "x":
                        before_file = ord(play[1]) - ord('a')
                    else:
                        before_file = ord(play[2]) - ord('a')

            if move[1] != "x":
                file = ord(move[1]) - ord('a')
            else:
                file = ord(move[2]) - ord('a')

        else:
            before_file = 7
            for play in self.game_history[1::2]:
                if play[0] == "Q":
                    if play[1] != "x":
                        before_file = ord(play[1]) - ord('a')
                    else:
                        before_file = ord(play[2]) - ord('a')

            if move[1] != "x":
                file = ord(move[1]) - ord('a')
            else:
                file = ord(move[2]) - ord('a')

        if before_file != file: # צריך לבדוק גם את הרנק
            return self.check_diagonal(self, move)

    def is_valid_king_move(self, move: str):
        # Implement king move validation
        pass

    # 0 - turn is not yours, 1 - illegal move, 2 - move confirmed.
    def do_turn(self, username: str, move: str) -> int:
        if username != self.players.keys()[self.turn]:
            return 0

        if not self.check_if_move_legal(move):
            pass
