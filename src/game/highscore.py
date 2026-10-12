import os
import json


class Highscore:

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.scores: list[dict[str, str | int]] = []

    def load_score(self) -> None:
        if not os.path.exists(self.filepath):
            print(f"WARNING: {self.filepath} doesn't exist")
            self.scores = []
            self.save_score()
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

    def save_score(self) -> bool:
        """Save highscores safely to the JSON file."""

        temp_path = self.filepath + ".tmp"

        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(self.scores, file, indent=4)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())

            os.replace(temp_path, self.filepath)
            return True

        except (OSError, TypeError, ValueError) as e:
            print(f"WARNING: cannot save highscores: {e}")
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except OSError:
                pass
            return False

    def add_score(self, name: str, score: int) -> bool:
        """Add a score and save the updated leaderboard."""

        if not isinstance(name, str):
            return False

        if not 1 <= len(name) <= 10:
            return False

        if not all(c.isalnum() or c == " " for c in name):
            return False

        if (
            not isinstance(score, int)
            or isinstance(score, bool)
            or score < 0
        ):
            return False

        previous_scores = self.scores
        updated_scores = previous_scores.copy()
        updated_scores.append({"name": name, "score": score})
        updated_scores.sort(
            key=lambda entry: entry["score"],
            reverse=True,
        )
        updated_scores = updated_scores[:10]

        self.scores = updated_scores

        if not self.save_score():
            self.scores = previous_scores
            return False

        return True

    def top_score(self, n=10):
        return self.scores[:n]
