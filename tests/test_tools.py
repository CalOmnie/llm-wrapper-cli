from unittest.mock import patch, mock_open
from llm_wrapper_cli.tools import FileWriteTool, AddTest
from smolagents.local_python_executor import LocalPythonInterpreter
import pytest



def test_write_file_confirmed(tmp_path):
    path = tmp_path / "testfile.txt"
    content = "Hello, world!"
    tool = FileWriteTool()
    with patch("builtins.input", return_value="y"):
        tool.forward(str(path), content)
    assert path.read_text() == content


def test_write_file_rejected(tmp_path):
    path = tmp_path / "testfile.txt"
    content = "Hello, world!"
    tool = FileWriteTool()
    with patch("builtins.input", return_value="n"):
        try:
            tool.forward(str(path), content)
        except ValueError as e:
            assert str(e) == "User did not validate this change because of: n"
    assert not path.exists()


def test_write_file_existing_confirmed(tmp_path):
    path = tmp_path / "testfile.txt"
    path.write_text("Initial content")
    content = "Hello, world!"
    tool = FileWriteTool()
    with patch("builtins.input", return_value="y"):
        tool.forward(str(path), content)
    assert path.read_text() == content


def test_write_file_existing_rejected(tmp_path):
    path = tmp_path / "testfile.txt"
    path.write_text("Initial content")
    content = "Hello, world!"
    tool = FileWriteTool()
    with patch("builtins.input", return_value="n"):
        try:
            tool.forward(str(path), content)
        except ValueError as e:
            assert str(e) == "User did not validate this change because of: n"
    assert path.read_text() == "Initial content"


@pytest.fixture
def mock_add_test():
    res = AddTest(run_cmd="pytest")
    return res


@pytest.fixture
def valid_test_function():
    def test_something():
        print("testing")

    return test_something


@pytest.fixture
def failing_test_function():
    def test_failing():
        assert False

    return test_failing


def test_add_valid_test(tmp_path, mock_add_test, valid_test_function):
    test_path = tmp_path / "test.py"
    test_path.touch()
    mock_add_test.forward(test_path, valid_test_function)
    with open(test_path, "rt") as f:
        assert "def test_something():" in f.read()


def test_add_failing_test(tmp_path, mock_add_test, failing_test_function):
    test_path = tmp_path / "test.py"
    test_path.touch()
    try:
        mock_add_test.forward(str(test_path), failing_test_function)
    except Exception as e:
        with open(test_path, "rt") as f:
            content = f.read()
            print(content)
        assert "def failing_test_function():" not in content
        print(f"Exception raised as expected: {e}")
    else:
        assert False, "No exception raised for failing test"


def test_add_test_same_function_twice(mock_add_test, valid_test_function, tmp_path):
    test_path = tmp_path / "test.py"
    test_path.touch()
    mock_add_test.forward(test_path, valid_test_function)
    with open(test_path, "rt") as f:
        content = f.read()
        assert "def test_something():" in content, "First addition failed"
    try:
        mock_add_test.forward(test_path, valid_test_function)
    except ValueError as e:
        with open(test_path, "rt") as f:
            content = f.read()
            assert "def test_something():" in content, (
                "Content changed after second addition"
            )
        assert str(e) == "A file already has a member called test_something", (
            f"Unexpected exception message: {e}"
        )
    else:
        assert False, "No exception raised when adding the same function twice"


def test_add_test_local_python_interpreter_valid(tmp_path):
    test_path = tmp_path / "test.py"
    test_path.touch()
    runner = LocalPythonInterpreter(
        tools={"add_test": AddTest("pytest")}, additional_authorized_imports=["*"]
    )
    code = f'def test_thingy():\n    print("testing")\n\nadd_test(path="{test_path}", test_function=test_thingy)'
    runner(code, {})


def test_add_test_with_empty_content(tmp_path, mock_add_test):
    test_path = tmp_path / "test_empty.py"
    test_path.write_text("")

    def test_empty():
        assert True

    mock_add_test.forward(test_path, test_empty)
    with open(test_path, "rt") as f:
        content = f.read()
        assert "def test_empty():" in content, (
            "Test was not added to the empty file correctly"
        )


def test_add_test_with_coverage_increase(tmp_path, mock_add_test):
    test_path = tmp_path / 'test_coverage.py'
    test_path.touch()

    def test_new_coverage():
        assert True
    old_coverage_output = "0%"
    new_coverage_output = "100%"
    coverage_regexp = "(\\d+)%"
    mock_add_test.coverage_regexp = coverage_regexp
    with patch.object(mock_add_test, 'run_test', side_effect=[(old_coverage_output, 0), (new_coverage_output, 0)]):
        mock_add_test.forward(test_path, test_new_coverage)
    with open(test_path, 'rt') as f:
        content = f.read()
        assert 'def test_new_coverage():' in content



def test_add_test_with_coverage_failing(tmp_path):
    test_path = tmp_path / 'test.py'
    test_path.write_text(
        """
def test_fail():
    raise ValueError('Failing test')
        """
    )

    tester = AddTest(coverage_regexp = "(.*)")
    def test_new():
        assert True
    with pytest.raises(ValueError, match="Test file does not pass before adding the tests"):
        tester.forward(test_path, test_new)

def test_add_test_with_no_coverage_increase(tmp_path, mock_add_test):
    test_path = tmp_path / 'test_no_coverage.py'
    test_path.touch()

    def test_existing():
        assert True

    def test_new_no_coverage():
        pass
    mock_add_test.coverage_regexp = '(\\d+)%'
    with patch.object(mock_add_test, 'run_test', side_effect=[('0%', 0), ('100%', 0)]):
        mock_add_test.forward(test_path, test_existing)
    with patch.object(mock_add_test, 'run_test', side_effect=[('100%', 0), ('100%', 0)]):
        try:
            mock_add_test.forward(test_path, test_new_no_coverage)
        except ValueError as e:
            assert str(e) == 'Test did not increase coverage, full output:\n100%'
        else:
            assert False, 'No exception raised when adding a test that does not increase coverage'



