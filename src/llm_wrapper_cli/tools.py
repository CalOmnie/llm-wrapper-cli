from smolagents import Tool

TEST_RUN_CMD = "pytest"
TEST_FORMAT_STRING = "{test_file}::{test_name}"

class AddTest(Tool):
    name = "add_test"
    description = """
    This is a tool appending a test to a test file, running said test,
    and removing it from the file if it fails.
    This tool does 3 things:
        - Add the test function to the test file at position `path`
        - Run the test function, checking for results
        - Revert the file to its original state if the test function fails
    """
    inputs = {
        "path": {
            "type": "string",
            "description": "The path to the test file.",
        },
        "test_function": {
            "type": "object",
            "description": (
                "The test function to add to the file. "
                "This is the actual function object, **not** a string"
            ),
        },
    }
    output_type = "string"

    def __init__(
        self,
        *args,
        run_cmd: str = TEST_RUN_CMD,
        test_format_string=TEST_FORMAT_STRING,
        coverage_regexp="",
    ):
        self.run_cmd = run_cmd
        self.test_format_string = test_format_string
        self.coverage_regexp = coverage_regexp
        super().__init__()

    def forward(self, path: str, test_function: object):
        from pathlib import Path
        path = Path(path)
        fun_def = self._get_function_def(test_function)
        path_ast = self.__parse_py_file(path)

        if self.coverage_regexp:
            output = self.add_with_coverage(path, path_ast, fun_def)
        else:
            # Add test
            self.add_test(path, path_ast, fun_def)
            output, returncode = self.run_test(path, fun_def)
            if returncode != 0:
                self.delete_test(path, fun_def)
                raise ValueError(f"test failed with output:\n{output}")
        return self._generate_output(output, fun_def)

    def add_with_coverage(self, path, path_ast, fun_def):
        import re

        output, returncode = self.run_test(path, fun_def)
        # Return code 5 is when no test ran
        if returncode != 0 and returncode != 5:
            raise ValueError(
                f"Test file does not pass before adding the tests, returncode:\n{output}"
            )

        base_coverage = float(
            re.search(self.coverage_regexp, output, re.MULTILINE).group(1)
        )
        # Add test
        self.add_test(path, path_ast, fun_def)
        output, returncode = self.run_test(path, fun_def)
        if returncode != 0:
            self.delete_test(path, fun_def)
            raise ValueError(f"Test failed with output:\n{output}")
        new_coverage = float(
            re.search(self.coverage_regexp, output, re.MULTILINE).group(1)
        )
        if new_coverage <= base_coverage:
            self.delete_test(path, fun_def)
            raise ValueError(f"Test did not increase coverage, full output:\n{output}")
        return output

    def add_test(self, path, path_ast, fun_def) -> None:
        import ast

        for member in path_ast.body:
            if getattr(member, "name", "") == fun_def.name:
                raise ValueError(f"A file already has a member called {fun_def.name}")
        with open(path, "at") as f:
            f.write(f"\n{ast.unparse(fun_def)}\n")

    def run_test(self, path, fun_def):
        import subprocess

        test_str = self.test_format_string.format(
            test_file=path, test_name=fun_def.name
        )
        full_cmd = f"{self.run_cmd} {test_str}".split()
        res = subprocess.run(full_cmd, check=False, stdout=subprocess.PIPE)
        output = res.stdout.decode()
        returncode = res.returncode
        return output, returncode

    def delete_test(self, path: str, fun_def):
        with path.open("rt+") as f:
            pos = f.tell()
            while line := f.readline():
                if f"def {fun_def.name}" in line:
                    f.seek(pos)
                    f.truncate()
                    break
                pos = f.tell()

    def _get_function_def(self, function: object):
        import ast
        import inspect
        import textwrap

        if getattr(function, "__closure__", None) is not None:
            for param in function.__closure__:
                content = param.cell_contents
                if isinstance(content, ast.FunctionDef):
                    return content
        fun_source = textwrap.dedent(inspect.getsource(function))
        return ast.parse(fun_source).body[0]

    def _generate_output(self, output, fun_def):
        import ast
        return (f"Test added succesfully.\n"
               f"# Test run Output\n{output}\n"
               f"# Test function\n{ast.unparse(fun_def)}")

    def __parse_py_file(self, path: str):
        import ast

        return ast.parse(path.read_text(), filename=path)
