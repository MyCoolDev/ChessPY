from DataStructures.connections import Connection, Status
from logic import Game

from typing import List

import json

class GameManager:
    def __init__(self):
        self.queue: List[Connection] = []
        self.active_games = {}

    def remove_from_queue(self, value):
        if self.queue.count(value) > 0:
            self.queue.remove(value)

    def add_to_queue(self, con: Connection):
        if len(self.queue) > 0:
            # create a new match
            player = self.queue.pop(0)
            con.connection.send(json.dumps({'code': 200, 'event': 'match found', "msg": "we found a match for you!", "data": {"opponent": player.data["username"]}}).encode())
            con.status = Status.InGame
            player.connection.send(json.dumps({'code': 200, 'event': 'match found', "msg": "we found a match for you!", "data": {"opponent": con.data["username"]}}).encode())
            player.status = Status.InGame

            # create game object
            game = Game(con, player, 60 * 10)

            # add to each player his interface to the game
            # for now just giving them the game object

            con.data['current_game'], player.data['current_game'] = game, game

        self.queue.append(con)
