from smolagents import Tool
from typing import Callable

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


class AddTest(Tool):
    name = "add_test"
    description = """
    This is a tool appending a test to a test file, running sais test,
    and removing it from the file if it fails.
    """
    inputs = {
        "path": {
            "type": "string",
            "description": "The path to the test file.",
        },
        "test_function": {
            "type": "object",
            "description": "The test function to add to the file."
        }
    }
    output_type = "null"

    def __init__(self, run_cmd: str, *args, **kwargs):
        self.run_cmd = run_cmd
        super().__init__(*args, **kwargs)

    def forward(self, path: str, test_function: object):
        fun_name = self.add_test(path, test_function)
        output, returncode = self.run_test(path)
        if returncode != 0:
            self.delete_test(path, fun_name)
        return output

    def add_test(self, path: str, test_function: object) -> str:
        import ast
        fun_code, fun_name = "", ""
        for param in test_function.__closure__:
            content = param.cell_contents
            if isinstance(content, ast.FunctionDef):
                fun_code = ast.unparse(content)
                fun_name = content.name
        with open(path, "at") as f:
            f.write("\n\n")
            f.write(fun_code)
        return fun_name

    def run_test(self, path: str):
        import subprocess
        full_cmd = f"{self.run_cmd} {path}".split()
        res = subprocess.run(full_cmd, check=False, stdout=subprocess.PIPE)
        output = res.stdout.decode()
        returncode = res.returncode
        return output, returncode

    def delete_test(self, path: str, fun_name: str):
        import ast
        with open(path, "rt+") as f:
            tree = ast.parse(f.read(), filename=path)
            body = filter(lambda node: not (isinstance(node, ast.FunctionDef) and node.name == fun_name), tree.body)
            tree.body = list(body)
            f.seek(0)
            f.write(ast.unparse(tree))
            f.truncate()

class RunTestFile(Tool):
    name = "run_test_file"
    description = """
    This tool runs a test file and returns the test output.
    """
    inputs = {
        "path": {
            "type": "string",
            "description": "Path to the test file."
        }
    }
    output_type = "string"

    def __init__(self, run_cmd: str, *args, **kwargs):
        self.run_cmd = run_cmd
        super().__init__(*args, **kwargs)

    def forward(self, path: str) -> str:
        import subprocess
        full_cmd = f"{self.run_cmd} {path}".split()
        res = subprocess.run(full_cmd, check=False, stdout=subprocess.PIPE).stdout.decode()
        return res
