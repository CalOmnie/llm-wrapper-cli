from pathlib import Path
import json

SESSION_PATH = Path("/tmp/llmc_session.json")

class Session:

    def __init__(self, new: bool):
        if new:
            SESSION_PATH.unlink(missing_ok=True)
        if (SESSION_PATH.exists() and SESSION_PATH.is_file()):
            with SESSION_PATH.open("rt") as f:
                self.session = json.load(f)
        else:
            self.session = []

    def add_message(self, role: str, content: str):
        self.session.append({"role": role, "content": content})

    def get(self):
        return self.session

    def save(self):
        with SESSION_PATH.open("wt") as f:
            json.dump(self.session, f)
