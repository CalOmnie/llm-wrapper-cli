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
    This is a tool appending a test to a test file, running said test,
    and removing it from the file if it fails.
    This tool does 3 things:
        - Add the test function to the test file at position `path`
        - Run the rest file, checking for results
        - Revert the file to its original state if the test fails
    """
    inputs = {
        "path": {
            "type": "string",
            "description": "The path to the test file.",
        },
        "test_function": {
            "type": "object",
            "description": ("The test function to add to the file. "
                            "This is the actual function object, **not** a string")
        }
    }
    output_type = "null"

    def __init__(self, run_cmd: str, *args, **kwargs):
        self.run_cmd = run_cmd
        super().__init__(*args, **kwargs)

    def forward(self, path: str, test_function: object):
        import ast
        fun_def = self.__get_function_def(test_function)
        path_ast = self.__parse_py_file(path)

        # Add test
        self.add_test(path_ast, fun_def)
        output, returncode = self.run_test(path, path_ast)
        if returncode != 0:
            self.delete_test(path, path_ast)
        return output

    def add_test(self, path_ast, fun_def) -> None:
        for member in path_ast.body:
            if getattr(member, "name", "") == fun_def.name:
                raise ValueError(f"A file already has a member called {fun_def.name}")
        path_ast.body.append(fun_def)

    def run_test(self, path: str, path_ast):
        import subprocess
        import ast
        with open(path, "wt") as f:
            f.write(ast.unparse(path_ast))

        full_cmd = f"{self.run_cmd} {path}".split()
        res = subprocess.run(full_cmd, check=False, stdout=subprocess.PIPE)
        output = res.stdout.decode()
        returncode = res.returncode
        return output, returncode

    def delete_test(self, path: str, path_ast):
        import ast
        with open(path, "wt") as f:
            path_ast.body = list(path_ast.body)[:-1]
            f.write(ast.unparse(path_ast))

    def __get_function_def(self, function: object):
        import ast
        for param in function.__closure__:
            content = param.cell_contents
            if isinstance(content, ast.FunctionDef):
                return content
        raise ValueError("Could not find the function definition, "
                         "was this tool called through `smolagents.local_python_intepreter`?")

    def __parse_py_file(self, path: str):
        import ast
        with open(path, "rt") as f:
            return ast.parse(f.read(), filename=path)


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
