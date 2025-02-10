
from smolagents import Tool

class FileReaderTool(Tool):
    name = "read_file"
    description = """
    This is a tool reading a file passed as argument, it returns the content of the file
    """
    inputs = {
        "path": {
            "type": "string",
            "description": "the path to the file",
        }
    }
    output_type = "string"

    def forward(self, path: str):
        with open(path, "rt") as f:
            return f.read()

class FileWriteTool(Tool):
    name = "write_file"
    description = """
    This is a tool writing a file after asking for user confirmation, if the file exists, it prints the diff.
    """
    inputs = {
        "path": {
            "type": "string",
            "description": "the path to the file",
        },
        "content": {
            "type": "string",
            "description": "Content to write in the file"
        }
    }
    output_type = "null"

    def forward(self, path: str, content: str) -> None:
        from pathlib import Path
        print(content)
        print(f"file path: {path}")
        user_val = input("Do you want to write this file? 'y' for yes, "
                         "anything else for no, anythig you typed is fed to the next step.")
        if user_val != "y":
            raise ValueError(f"User did not validate this change because of: {user_val}")
        p = Path(path)
        with p.open("wt") as f:
            f.write(content)
