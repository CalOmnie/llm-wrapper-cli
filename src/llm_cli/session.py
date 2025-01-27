from pathlib import Path
import tempfile
import json

SESSION_PATH = Path(tempfile.gettempdir()) / "llmc_session.json"

class Session:

    def __init__(self, continue_chat: bool):
        self.session = []
        if continue_chat:
            self.load_session()

    def load_session(self):
        if (SESSION_PATH.exists() and SESSION_PATH.is_file()):
            with SESSION_PATH.open("rt") as f:
                self.session = json.load(f)

    def add_message(self, role: str, content: str):
        self.session.append({"role": role, "content": content})

    def get(self):
        return self.session

    def save(self):
        with SESSION_PATH.open("wt") as f:
            json.dump(self.session, f)
