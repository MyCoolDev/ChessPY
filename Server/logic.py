import random
import datetime
import string

from DataStructures.connections import Connection
import Game_Logs.game_register_file as regfile

class Game:
    def __init__(self, p1: Connection, p2: Connection, duration: int):
        # game inter vars
        self.__winner = None
        self.__game_history = []
        self.__game_board = [["R", "N", "B", "Q", "K", "B", "N", "R"],
                             ["P", "P", "P", "P", "P", "P", "P", "P"],
                             ["", "", "", "", "", "", "", ""],
                             ["", "", "", "", "", "", "", ""],
                             ["", "", "", "", "", "", "", ""],
                             ["", "", "", "", "", "", "", ""],
                             ["p", "p", "p", "p", "p", "p", "p", "p"],
                             ["r", "n", "b", "q", "k", "b", "n", "r"]]

        # give each player his token in order to make a move
        token1, token2 = self.__generate_tokens()
        p1.data['ident_token'], p2.data['ident_token'] = token1, token2

        # get game meta data
        self.__player_game_time_duration = duration
        self.__players = ((p1, token1), (p2, token2))
        self.turn = random.randint(0, 1)
        self.__game_start_time = datetime.datetime.now()

        # create game register file
        self.__register_file = regfile.RegisterFile(regfile.LogType.TestLog)
        self.__register_file.write_to_file(f"{self.__players[0]} vs {self.__players[1]}")

    @staticmethod
    def __generate_tokens() -> (str, str):
        chrs = string.hexdigits
        token, other_token = "", ""

        # generate a token
        for _ in range(5):
            token += random.choice(chrs)
            other_token += random.choice(chrs)

        while other_token == token:
            # regenerate other token
            other_token = ""

            # generate a token
            for _ in range(5):
                other_token += random.choice(chrs)

        return token, other_token

    def do_turn(self, turn, token):
        is_move_legal(turn, 0 if self.__players[0][1] == token else 1, self.__game_board)

class GamePosition:
    def __init__(self, pos: str, game_board):
        self.pos = pos
        self.file = pos[0]
        self.number = int(pos[1])
        self.piece = GamePiece(self, game_board)

    def get_file_index(self):
        return ord(self.file) - 97

    def add_to_file(self, num) -> str:
        return chr(ord(self.file) + num)

    def get_cords(self) -> tuple:
        return self.get_file_index(), self.number

    def __str__(self):
        return self.pos

class GamePiece:
    def __init__(self, pos: GamePosition, game_board: list):
        self.piece = game_board[len(game_board) - pos.number][pos.get_file_index()]
        self.side = -1 if self.piece == "" else 1 if self.piece.isupper() else 0
        self.pid = -1 if self.piece == "" else self.calc_pid(self.piece)

    @staticmethod
    def calc_pid(piece):
        x = ord(piece.lower()) - 98
        return [0, 9, 12, 14, 15, 16].index(x)

# logic functions

def get_all_possible_moves(pos: GamePosition, game_board: list) -> dict:
    all_possible_moves = {}

    if pos.piece.pid == GamePiece.calc_pid("p"):
        if GamePosition(f"{pos.file}{(pos.number + 1)}", game_board).piece.pid == -1:
            all_possible_moves[f"{pos.file}{(pos.number + 1)}"] = 0

            if GamePosition(f"{pos.file}{(pos.number + 2)}", game_board).piece.pid == -1:
                if pos.number == (pos.piece.side * 5) + 2:
                    all_possible_moves[f"{pos.file}{pos.number + 2}"] = 0

        # taking other player piece - flag 1

        if pos.get_file_index() > 0:
            all_possible_moves[f"{pos.add_to_file(-1)}{pos.number + 1}"] = 1
        if pos.get_file_index() < 7:
            all_possible_moves[f"{pos.add_to_file(1)}{pos.number + 1}"] = 1

    if pos.piece.pid == GamePiece.calc_pid("n"):
        if pos.get_file_index() > 0 and pos.number < 7:
            all_possible_moves[f"{pos.add_to_file(-1)}{pos.number + 2}"] = 0 if GamePosition(
                f"{pos.add_to_file(-1)}{pos.number + 2}", game_board).piece.pid == -1 else 1

        if pos.get_file_index() < 7 and pos.number < 7:
            all_possible_moves[f"{pos.add_to_file(1)}{pos.number + 2}"] = 0 if GamePosition(
                f"{pos.add_to_file(1)}{pos.number + 2}", game_board).piece.pid == -1 else 1

        if pos.get_file_index() > 1 and pos.number < 8:
            all_possible_moves[f"{pos.add_to_file(-2)}{pos.number + 1}"] = 0 if GamePosition(
                f"{pos.add_to_file(-2)}{pos.number + 1}", game_board).piece.pid == -1 else 1

        if pos.get_file_index() < 6 and pos.number < 8:
            all_possible_moves[f"{pos.add_to_file(2)}{pos.number + 1}"] = 0 if GamePosition(
                f"{pos.add_to_file(-2)}{pos.number + 1}", game_board).piece.pid == -1 else 1

        if pos.get_file_index() > 0 and pos.number > 2:
            all_possible_moves[f"{pos.add_to_file(-1)}{pos.number - 2}"] = 0 if GamePosition(
                f"{pos.add_to_file(-1)}{pos.number - 2}", game_board).piece.pid == -1 else 1

        if pos.get_file_index() < 7 and pos.number > 2:
            all_possible_moves[f"{pos.add_to_file(1)}{pos.number - 2}"] = 0 if GamePosition(
                f"{pos.add_to_file(1)}{pos.number - 2}", game_board).piece.pid == -1 else 1

        if pos.get_file_index() > 1 and pos.number > 1:
            all_possible_moves[f"{pos.add_to_file(-2)}{pos.number + 1}"] = 0 if GamePosition(
                f"{pos.add_to_file(-2)}{pos.number + 1}", game_board).piece.pid == -1 else 1

        if pos.get_file_index() < 6 and pos.number > 1:
            all_possible_moves[f"{pos.add_to_file(2)}{pos.number - 1}"] = 0 if GamePosition(
                f"{pos.add_to_file(-2)}{pos.number - 1}", game_board).piece.pid == -1 else 1

    if pos.piece.pid == GamePiece.calc_pid("r") or pos.piece.pid == GamePiece.calc_pid("q"):
        k = 1
        z = 0
        dk = 1
        dz = 0
        flag = False

        while True:
            if not (0 <= pos.get_file_index() + z <= 7 and 1 <= pos.number + k <= 8) or flag:
                flag = False
                if dz == -1:
                    break
                if dz == 1:
                    dz = -1
                elif dk == 1:
                    dk = -1
                else:
                    dk = 0
                    dz = 1

                k = dk
                z = dz
                continue

            mv = GamePosition(f"{pos.add_to_file(z)}{(pos.number + k)}", game_board)
            if mv.piece.side == pos.piece.side:
                flag = False
                if dz == -1:
                    break
                if dz == 1:
                    dz = -1
                elif dk == 1:
                    dk = -1
                else:
                    dk = 0
                    dz = 1

                k = dk
                z = dz
                continue

            if mv.piece.side == -1:
                all_possible_moves[f"{pos.add_to_file(z)}{(pos.number + k)}"] = 0
            else:
                all_possible_moves[f"{pos.add_to_file(z)}{(pos.number + k)}"] = 1
                flag = True

            k += dk
            z += dz

    if pos.piece.pid == GamePiece.calc_pid("b") or pos.piece.pid == GamePiece.calc_pid("q"):
        k = 1
        z = 1
        dk = 1
        dz = 1
        flag = False

        while True:
            if not (0 <= pos.get_file_index() + z <= 7 and 1 <= pos.number + k <= 8) or flag:
                flag = False
                if dz == -1 and dk == -1:
                    break
                if dk == 1 and dz == 1:
                    dz = -1

                elif dk == 1 and dz == -1:
                    dk = -1
                    dz = 1
                else:
                    dk = -1
                    dz = -1

                k = dk
                z = dz
                continue

            mv = GamePosition(f"{pos.add_to_file(z)}{(pos.number + k)}", game_board)
            if mv.piece.side == pos.piece.side:
                flag = False
                if dz == -1 and dk == -1:
                    break
                if dk == 1 and dz == 1:
                    dz = -1

                elif dk == 1 and dz == -1:
                    dk = -1
                    dz = 1
                else:
                    dk = -1
                    dz = -1

                k = dk
                z = dz
                continue

            if mv.piece.side == -1:
                all_possible_moves[f"{pos.add_to_file(z)}{(pos.number + k)}"] = 0
            else:
                all_possible_moves[f"{pos.add_to_file(z)}{(pos.number + k)}"] = 1
                flag = True

            k += dk
            z += dz
    if pos.piece.pid == GamePiece.calc_pid("k"):
        if pos.get_file_index() > 0 and pos.number > 1:
            all_possible_moves[f"{pos.add_to_file(-1)}{pos.number - 1}"] = 0 if GamePosition(
                f"{pos.add_to_file(-1)}{pos.number - 1}", game_board).piece.pid == -1 else 1
        if pos.number > 1:
            all_possible_moves[f"{pos.file}{pos.number - 1}"] = 0 if GamePosition(
                f"{pos.file}{pos.number - 1}", game_board).piece.pid == -1 else 1
        if pos.get_file_index() < 7 and pos.number > 1:
            all_possible_moves[f"{pos.add_to_file(1)}{pos.number - 1}"] = 0 if GamePosition(
                f"{pos.add_to_file(1)}{pos.number - 1}", game_board).piece.pid == -1 else 1
        if pos.get_file_index() < 7:
            all_possible_moves[f"{pos.add_to_file(1)}{pos.number}"] = 0 if GamePosition(
                f"{pos.add_to_file(1)}{pos.number}", game_board).piece.pid == -1 else 1
        if pos.get_file_index() < 7 and pos.number < 8:
            all_possible_moves[f"{pos.add_to_file(1)}{pos.number + 1}"] = 0 if GamePosition(
                f"{pos.add_to_file(1)}{pos.number + 1}", game_board).piece.pid == -1 else 1
        if pos.number < 8:
            all_possible_moves[f"{pos.file}{pos.number + 1}"] = 0 if GamePosition(
                f"{pos.file}{pos.number + 1}", game_board).piece.pid == -1 else 1
        if pos.get_file_index() > 0 and pos.number < 8:
            all_possible_moves[f"{pos.add_to_file(-1)}{pos.number + 1}"] = 0 if GamePosition(
                f"{pos.add_to_file(-1)}{pos.number + 1}", game_board).piece.pid == -1 else 1
        if pos.get_file_index() > 0:
            all_possible_moves[f"{pos.add_to_file(-1)}{pos.number}"] = 0 if GamePosition(
                f"{pos.add_to_file(-1)}{pos.number}", game_board).piece.pid == -1 else 1

    return all_possible_moves

def is_move_legal(move: str, side: int, game_board) -> (bool, tuple):
    if side not in [0, 1]:
        return False, None

    sp = GamePosition(move[:2], game_board)
    ep = GamePosition(move[2:], game_board)

    if sp.piece.side != side:
        return False, None

    all_possible_moves = get_all_possible_moves(sp)

    if ep.pos not in all_possible_moves:
        return False, None

    if all_possible_moves[ep.pos] == 1 and ep.piece.side == sp.piece.side:
        return False, None

    return True, (sp, ep)
