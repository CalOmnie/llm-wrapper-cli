
from pathlib import Path
import tempfile
import json

SESSION_PATH = Path(tempfile.gettempdir()) / "llmc_session.json"

class Session:
    """
    A class to manage chat sessions, load, add and save messages.
    """

    def __init__(self, continue_chat: bool, path: Path = SESSION_PATH):
        """
        Initializes a new session, loading an existing one if continue_chat is True.
        """
        self.session = []
        if continue_chat:
            self.load_session()

    def load_session(self):
        """
        Loads the session from a file if it exists.
        """
        if (SESSION_PATH.exists() and SESSION_PATH.is_file()):
            with SESSION_PATH.open("rt") as f:
                self.session = json.load(f)

    def add_message(self, role: str, content: str):
        """
        Adds a message to the session.
        """
        self.session.append({"role": role, "content": content})

    def get(self):
        """
        Returns the current session.
        """
        return self.session

    def save(self):
        """
        Saves the current session to a file.
        """
        with SESSION_PATH.open("wt") as f:
            json.dump(self.session, f)
