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

    def __repr__(self):
        return self.file + str(self.number)

class GamePiece:
    def __init__(self, pos: GamePosition, game_board: list):
        print(pos.get_file_index())
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

        if pos.get_file_index() > 0 and GamePosition(f"{pos.add_to_file(-1)}{pos.number + 1}", game_board).piece.pid != -1 and GamePosition(f"{pos.add_to_file(-1)}{pos.number + 1}", game_board).piece.side != pos.piece.side:
            all_possible_moves[f"{pos.add_to_file(-1)}{pos.number + 1}"] = 1

        if pos.get_file_index() < 7 and GamePosition(f"{pos.add_to_file(1)}{pos.number + 1}", game_board).piece.pid != -1 and GamePosition(f"{pos.add_to_file(1)}{pos.number + 1}", game_board).piece.side != pos.piece.side:
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

    truely_possible_moves = {}

    for key in all_possible_moves:
        if all_possible_moves[key] == 1:
            mv = GamePosition(key, game_board)
            if mv.piece.side != pos.piece.side:
                truely_possible_moves[key] = all_possible_moves[key]
        else:
            truely_possible_moves[key] = all_possible_moves[key]

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

def from_cords(cords: tuple, game_board) -> GamePosition:
    return GamePosition(f"{chr(cords[0] + 97)}{cords[1]}", game_board)