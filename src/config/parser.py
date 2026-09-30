import json
import os


class Parser:
    """a remplir"""

    def build_config(self, filepath: str) -> dict:
        """a remplir"""
        return self.load_json(filepath)

    def load_json(self, filepath: str) -> dict:
        """a remplir"""
        if not os.path.exists(filepath):
            print(f"WARNING, {filepath} don't exist")
            return {}

        with open(filepath, 'r') as f:
            lines = f.readlines()

        cleaned = "".join([
            line for line in lines
            if not line.strip().startswith("#")
        ])

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"WARNING, json syntax error :{e}")
            return {}
        except Exception as e:
            print(f"WARNING, an error occured :{e}")
            return {}
