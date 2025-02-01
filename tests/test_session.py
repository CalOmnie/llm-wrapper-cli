import pytest
from unittest.mock import patch, mock_open
from llm_cli.session import Session
import json
import tempfile
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def mock_session_file():
    with tempfile.NamedTemporaryFile("w+t", delete=False) as mock_file:
        with patch('llm_cli.session.SESSION_PATH', Path(mock_file.name)):
            yield mock_file

def test_session_continue_chat_true():
    with mock_session_file() as mock_file:
        mock_data = [{"role": "user", "content": "previous message"}]
        json.dump(mock_data, mock_file)
        mock_file.seek(0)
        s = Session(continue_chat=True)

        assert s.get() == mock_data

def test_session_continue_chat_false():
    with mock_session_file() as mock_file:
        with patch('builtins.open', mock_open(read_data=json.dumps([]))):
            s = Session(continue_chat=False)
        assert s.get() == []

def test_add_multiple_messages():
    with mock_session_file() as mock_file:
        s = Session(continue_chat=False)
        s.add_message("user", "first message")
        s.add_message("assistant", "second message")
        assert s.get() == [{"role": "user", "content": "first message"}, {"role": "assistant", "content": "second message"}]

def test_session_save():
    msg = {"role": "user", "content": "test"}
    with mock_session_file() as mock_file:
        s = Session(continue_chat=False)
        s.add_message(**msg)
        s.save()

        mock_file.seek(0)
        assert json.load(mock_file) == [msg]

def test_session_save_no_messages():
    with mock_session_file() as mock_file:
        s = Session(continue_chat=False)
        s.save()
        mock_file.seek(0)
        r = mock_file.read()
        assert r == "[]"

def test_session_file_not_found():
    with patch('llm_cli.session.SESSION_PATH', Path("Inexisting file")):
        s = Session(continue_chat=True)
        assert s.get() == []

def test_get_session():
    with mock_session_file() as mock_file:
        s = Session(continue_chat=False)
        s.add_message("user", "test")
        assert s.get() == [{"role": "user", "content": "test"}]

def test_session_file_empty():
    with mock_session_file() as mock_file:
        with pytest.raises(json.decoder.JSONDecodeError):
            s = Session(continue_chat=True)

def test_session_file_invalid_json():
    with mock_session_file() as mock_file:
        mock_file.write("invalid JSON")
        mock_file.seek(0)
        with pytest.raises(ValueError):
            s = Session(continue_chat=True)

def test_session_load_and_save():
    with mock_session_file() as mock_file:
        s1 = Session(continue_chat=False)
        s1.add_message("user", "test")
        s1.save()
        s2 = Session(continue_chat=True)
        assert s2.get() == [{"role": "user", "content": "test"}]

