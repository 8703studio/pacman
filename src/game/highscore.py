import os
import json


class Highscore:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.scores = []

    def load_score(self) -> None:
        if not os.path.exists(self.filepath):
            print(f"WARNING, {self.filepath} don't exist")
            self.scores = []
        else:
            with open(self.filepath, 'r') as f:
                try:
                    self.scores = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"WARNING, json syntax error: {e}")
                    self.scores = []

    def save_score(self):
        pass

    def add_score(self):
        pass

    def top_score(self):
        pass
