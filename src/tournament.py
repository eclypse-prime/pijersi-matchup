import argparse
import json
import math
import random
from tqdm import tqdm

from game import Game
from utils import elo_difference, elo_incertitude


class Tournament:
    def __init__(self, options):
        self.options = options
        self.game = Game(options['engines'][0]['path'], options['engines'][1]
                         ['path'], options['engines'][0]['name'], options['engines'][1]['name'])
        self.game.mode = f"{self.options['controls']['mode']} {
            self.options['controls']['value']}"
        self.scores = [0, 0]
        self.starting_player = 0
        self.game.initialize_engines()
        with open(self.options['openings']['path']) as file:
            self.openings = file.readlines()
            for i, opening in enumerate(self.openings):
                self.openings[i] = opening.strip()
            random.shuffle(self.openings)

    def play(self):
        n_games = self.options['tournament']['games']
        loop = tqdm(range(n_games))
        for i in loop:
            self.game.startpos = self.openings[(i//2) % len(self.openings)]
            self.game.reset(self.starting_player)
            winner = self.game.play_until_end()
            if winner != -1:
                self.scores[winner] += 1
            self.starting_player = 1 - self.starting_player
            loop.set_description(
                f"{self.scores[0]}-{self.scores[1]}-{i+1-self.scores[0]-self.scores[1]}")
        n_draws = n_games - sum(self.scores)
        print(f"Controls: {self.game.mode}")
        print(f"Engine 1: {self.game.engines[0].name}")
        print(f"Engine 2: {self.game.engines[1].name}")
        print(f"Scores: {self.scores[0]}-{self.scores[1]}-{n_draws}")
        print(f"ELO: {elo_difference(self.scores[1], n_draws, n_games):.2f} ± {
              elo_incertitude(self.scores[1], self.scores[0], n_draws):.2f}")


if __name__ == '__main__':
    with open("config.json") as file:
        options = json.load(file)
    tournament = Tournament(options)
    tournament.play()
