import json
import os


class Parser:
    """Read the configuration file and ignore its comments."""

    def build_config(self, filepath: str) -> dict:
        """Return the configuration read from filepath."""
        return self.load_json(filepath)

    def load_json(self, filepath: str) -> dict:
        """Load a JSON file whose comment lines start with #."""
        if not os.path.exists(filepath):
            print(f"WARNING, {filepath} don't exist")
            return {}

        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except (OSError, UnicodeDecodeError) as e:
            print(f"WARNING, cannot read {filepath} : {e}")
            return {}

        cleaned = "".join([
            line for line in lines
            if not line.strip().startswith("#")
        ])

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"WARNING, json syntax error :{e}")
            return {}
        except Exception as e:
            print(f"WARNING, an error occured :{e}")
            return {}

        if not isinstance(data, dict):
            print("WARNING, the configuration must be a JSON object")
            return {}

        return data
