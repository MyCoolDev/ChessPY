import random
import pygame
import os
import math

from .MonoBehaviour import MonoBehaviour

class ChessBoard:
    def __init__(self, base_pos: pygame.Vector2, size: int, theme=((80, 59, 54), (220, 213, 197)), show_pieces=False):
        self.box_size = size / 8
        self.base_pos = base_pos

        self.theme = theme

        self.show_pieces = show_pieces

        self.board = []
        self.game_board = [["R", "N", "B", "Q", "K", "B", "N", "R"],
                             ["P", "P", "P", "P", "P", "P", "P", "P"],
                             ["", "", "", "", "", "", "", ""],
                             ["", "", "", "", "", "", "", ""],
                             ["", "", "", "", "", "", "", ""],
                             ["", "", "", "", "", "", "", ""],
                             ["p", "p", "p", "p", "p", "p", "p", "p"],
                             ["r", "n", "b", "q", "k", "b", "n", "r"]]

        if show_pieces:
            self.__load_pieces_images()

        self.__create_board()

    def __create_board(self):
        self.board = []

        for i in range(0, 8):
            self.board.append([])
            for j in range(0, 8):
                if (j + i) % 2 == 0:
                    color = self.theme[0]
                else:
                    color = self.theme[1]

                self.board[i].append(MonoBehaviour(pygame.Vector2(self.box_size, self.box_size), self.base_pos + pygame.Vector2(j * self.box_size, i * self.box_size), color))

        self.board[0][0].update_border(border_top_left_radius=10)
        self.board[0][-1].update_border(border_top_right_radius=10)
        self.board[-1][0].update_border(border_bottom_left_radius=10)
        self.board[-1][-1].update_border(border_bottom_right_radius=10)

    def __load_pieces_images(self):
        self.wp = pygame.image.load(os.path.join('Images', "wp.png")).convert_alpha()
        self.wp = pygame.transform.scale(self.wp, (self.box_size, self.box_size))

        self.bp = pygame.image.load(os.path.join('Images', "bp.png")).convert_alpha()
        self.bp = pygame.transform.scale(self.bp, (self.box_size, self.box_size))

        self.wr = pygame.image.load(os.path.join('Images', "wr.png")).convert_alpha()
        self.wr = pygame.transform.scale(self.wr, (self.box_size, self.box_size))

        self.br = pygame.image.load(os.path.join('Images', "br.png")).convert_alpha()
        self.br = pygame.transform.scale(self.br, (self.box_size, self.box_size))

        self.wn = pygame.image.load(os.path.join('Images', "wn.png")).convert_alpha()
        self.wn = pygame.transform.scale(self.wn, (self.box_size, self.box_size))

        self.bn = pygame.image.load(os.path.join('Images', "bn.png")).convert_alpha()
        self.bn = pygame.transform.scale(self.bn, (self.box_size, self.box_size))

        self.wb = pygame.image.load(os.path.join('Images', "wb.png")).convert_alpha()
        self.wb = pygame.transform.scale(self.wb, (self.box_size, self.box_size))

        self.bb = pygame.image.load(os.path.join('Images', "bb.png")).convert_alpha()
        self.bb = pygame.transform.scale(self.bb, (self.box_size, self.box_size))

        self.wq = pygame.image.load(os.path.join('Images', "wq.png")).convert_alpha()
        self.wq = pygame.transform.scale(self.wq, (self.box_size, self.box_size))

        self.bq = pygame.image.load(os.path.join('Images', "bq.png")).convert_alpha()
        self.bq = pygame.transform.scale(self.bq, (self.box_size, self.box_size))

        self.wk = pygame.image.load(os.path.join('Images', "wk.png")).convert_alpha()
        self.wk = pygame.transform.scale(self.wk, (self.box_size, self.box_size))

        self.bk = pygame.image.load(os.path.join('Images', "bk.png")).convert_alpha()
        self.bk = pygame.transform.scale(self.bk, (self.box_size, self.box_size))

    def update_theme(self, theme: tuple):
        self.theme = theme

        self.__create_board()

    def mark_blocks(self, screen: pygame.Surface, cords: tuple):
        pygame.draw.circle(screen, (122, 122, 122, 0.5), self.base_pos + ((cords[0] - 0.5) * self.box_size, (cords[1] - 0.5) * self.box_size), self.box_size / 3)

    def update(self, dt: float, events: list):
        pass

    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0 < pygame.mouse.get_pos()[0] - self.base_pos.x < self.box_size * 8 and 0 < pygame.mouse.get_pos()[1] - self.base_pos.y < self.box_size * 8:
                    return True

        return False

    def find_chess_pieces(self, events):
        if not self.is_clicked(events):
            return -1, -1

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                index_pos = (1 / self.box_size) * (pygame.Vector2(pos[0], pos[1]) - self.base_pos)
                index_pos = (math.floor(index_pos[0]), math.floor(index_pos[1]))

                return index_pos

    def render(self, screen: pygame.Surface):
        for i in range(0, 8):
            for j in range(0, 8):
                self.board[i][j].render(screen)

        if self.show_pieces:
            for j in range(0, 8):
                screen.blit(self.wp, self.base_pos + pygame.Vector2(j * self.box_size, 6 * self.box_size))
                screen.blit(self.bp, self.base_pos + pygame.Vector2(j * self.box_size, self.box_size))

            for j in range(0, 2):
                screen.blit(self.wr, self.base_pos + pygame.Vector2(j * self.box_size * 7, 7 * self.box_size))
                screen.blit(self.br, self.base_pos + pygame.Vector2(j * self.box_size * 7, 0))

                if j == 0:
                    screen.blit(self.wn, self.base_pos + pygame.Vector2((j + 1) * self.box_size, 7 * self.box_size))
                    screen.blit(self.bn, self.base_pos + pygame.Vector2((j + 1) * self.box_size, 0))

                    screen.blit(self.wb, self.base_pos + pygame.Vector2((j + 2) * self.box_size, 7 * self.box_size))
                    screen.blit(self.bb, self.base_pos + pygame.Vector2((j + 2) * self.box_size, 0))
                else:
                    screen.blit(self.wn, self.base_pos + pygame.Vector2((7 - 1) * self.box_size, 7 * self.box_size))
                    screen.blit(self.bn, self.base_pos + pygame.Vector2((7 - 1) * self.box_size, 0))

                    screen.blit(self.wb, self.base_pos + pygame.Vector2((7 - 2) * self.box_size, 7 * self.box_size))
                    screen.blit(self.bb, self.base_pos + pygame.Vector2((7 - 2) * self.box_size, 0))

            screen.blit(self.wq, self.base_pos + pygame.Vector2(3 * self.box_size, 7 * self.box_size))
            screen.blit(self.bq, self.base_pos + pygame.Vector2(3 * self.box_size, 0))

            screen.blit(self.wk, self.base_pos + pygame.Vector2(4 * self.box_size, 7 * self.box_size))
            screen.blit(self.bk, self.base_pos + pygame.Vector2(4 * self.box_size, 0))
