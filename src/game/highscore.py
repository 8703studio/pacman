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
                    if not isinstance(self.scores, list):
                        print("WARNING contenu invalide")
                        self.scores = []
                except json.JSONDecodeError as e:
                    print(f"WARNING, json syntax error: {e}")
                    self.scores = []

    def save_score(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.scores, f)

    def add_score(self, name, score):
        self.scores.append({"name": name, "score": score})
        self.scores = sorted(self.scores, key=lambda s:
                             s["score"],
                             reverse=True
                             )
        self.scores = self.scores[:10]
        self.save_score()

    def top_score(self, n=10):
        return self.scores[:n]
