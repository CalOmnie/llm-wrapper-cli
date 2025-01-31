# tests/test_tools.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
from llm_cli.tools import FileReaderTool, FileWriteTool

def test_file_reader_tool():
    m = mock_open(read_data="test content")
    with patch('builtins.open', m):
        tool = FileReaderTool()
        assert tool.forward("test.txt") == "test content"

def test_write_file_confirmed(tmp_path):
    path = tmp_path / "testfile.txt"
    content = "Hello, world!"
    tool = FileWriteTool()
    with patch('builtins.input', return_value='y'):
        tool.forward(str(path), content)
    assert path.read_text() == content

def test_write_file_rejected(tmp_path):
    path = tmp_path / "testfile.txt"
    content = "Hello, world!"
    tool = FileWriteTool()
    with patch('builtins.input', return_value='n'):
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
    with patch('builtins.input', return_value='y'):
        tool.forward(str(path), content)
    assert path.read_text() == content

def test_write_file_existing_rejected(tmp_path):
    path = tmp_path / "testfile.txt"
    path.write_text("Initial content")
    content = "Hello, world!"
    tool = FileWriteTool()
    with patch('builtins.input', return_value='n'):
        try:
            tool.forward(str(path), content)
        except ValueError as e:
            assert str(e) == "User did not validate this change because of: n"
    assert path.read_text() == "Initial content"
