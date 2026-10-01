import os
import json


class Highscore:

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.scores = []

    def load_score(self) -> None:
        if not os.path.exists(self.filepath):
            print(f"WARNING: {self.filepath} doesn't exist")
            self.scores = []
            return

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("Invalid highscore format")

            self.scores = []

            for entry in data:
                if (
                    isinstance(entry, dict)
                    and isinstance(entry.get("name"), str)
                    and isinstance(entry.get("score"), int)
                    and not isinstance(entry.get("score"), bool)
                    and 0 <= entry["score"]
                    and 0 < len(entry["name"]) <= 10
                    and all(c.isalnum() or c == " " for c in entry["name"])
                ):
                    self.scores.append(entry)

            self.scores.sort(key=lambda s: s["score"], reverse=True)

            self.scores = self.scores[:10]

        except (json.JSONDecodeError, OSError, ValueError) as e:
            print(f"WARNING: invalid highscore file: {e}")
            self.scores = []

    def save_score(self) -> None:
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.scores, f, indent=4)

        except OSError as e:
            print(f"WARNING: cannot save highscores: {e}")

    def add_score(self, name: str, score: int) -> bool:
        if not isinstance(name, str):
            return False

        if not 1 <= len(name) <= 10:
            return False

        if not all(c.isalnum() or c == " " for c in name):
            return False

        if not isinstance(score, int):
            return False

        if isinstance(score, bool) or score < 0:
            return False

        self.scores.append({"name": name, "score": score})

        self.scores.sort(key=lambda s: s["score"], reverse=True)

        self.scores = self.scores[:10]

        return True

    def top_score(self, n=10):
        return self.scores[:n]
