from os import PathLike
from typing import Union
from engine import Engine


class Game:
    """A class encapsulating a match between two engines communicating with the UGI protocol."""

    def __init__(self, engine_path1: Union[str, bytes, PathLike], engine_path2: Union[str, bytes, PathLike]):
        self.engines = [Engine(engine_path1), Engine(engine_path2)]
        self.current_player = 0
        self.startpos = 'startpos'
        self.mode = 'depth 4'
        self.move_list = []
    
    def initialize_engines(self):
        for engine in self.engines:
            engine.send_command("ugi", "ugiok")
            engine.send_command("isready", "readyok")
            engine.send_command("uginewgame")

    def set_pos(self):
        command = ["position"]
        if self.startpos == 'startpos':
            command += ['startpos']
        else:
            command += ['fen', self.startpos]
        if len(self.move_list) > 0:
            command += ['moves']
            command += self.move_list
        command = ' '.join(command)
        self.engines[self.current_player].send_command(command)

    def play_move(self):
        self.set_pos()
        command = f"go {self.mode}"
        move_info = self.engines[self.current_player].send_command(command, "bestmove")
        bestmove = move_info[-1].split(" ")[-1]
        self.move_list.append(bestmove)
        self.current_player = 1 - self.current_player
    
    def play_until_end(self):
        game_ended = False
        while not game_ended:
            self.play_move()
            command = "query result"
            game_state = self.engines[self.current_player].send_command(command, "response")[-1].split(" ")[-1]
            if game_state != 'none':
                print(game_state)
                game_ended = True