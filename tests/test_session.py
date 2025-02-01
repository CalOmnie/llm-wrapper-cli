import pytest
from unittest.mock import patch
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

def test_session_continue_chat_true(tmp_path):
    tmp_session = tmp_path / "session.json"
    with patch('llm_cli.session.SESSION_PATH', tmp_session):
        with open(tmp_session, "wt") as f:
            mock_data = [{"role": "user", "content": "previous message"}]
            json.dump(mock_data, f)
        s = Session(continue_chat=True)

        assert s.get() == mock_data

def test_session_continue_chat_false():
    s = Session(continue_chat=False)
    assert s.get() == []

def test_add_multiple_messages():
    s = Session(continue_chat=False)
    s.add_message("user", "first message")
    s.add_message("assistant", "second message")
    assert s.get() == [{"role": "user", "content": "first message"}, {"role": "assistant", "content": "second message"}]

def test_session_save(tmp_path):
    msg = {"role": "user", "content": "test"}
    tmp_session = tmp_path / "session.json"
    with patch('llm_cli.session.SESSION_PATH', tmp_session):
        s = Session(continue_chat=False)
        s.add_message(**msg)
        s.save()

        with open(tmp_session) as f:
            assert json.load(f) == [msg]

def test_session_save_no_messages(tmp_path):
    tmp_session = tmp_path / "session.json"
    with patch('llm_cli.session.SESSION_PATH', tmp_session):
        s = Session(continue_chat=False)
        s.save()
        with open(tmp_session) as f:
            assert json.load(f) == []

def test_session_file_not_found():
    with patch('llm_cli.session.SESSION_PATH', Path("Inexisting file")):
        s = Session(continue_chat=True)
        assert s.get() == []

def test_get_session():
    s = Session(continue_chat=False)
    s.add_message("user", "test")
    assert s.get() == [{"role": "user", "content": "test"}]

def test_session_file_empty(tmp_path):
    tmp_session = tmp_path / "session.json"
    with patch('llm_cli.session.SESSION_PATH', tmp_session):
        tmp_session.touch()
        with pytest.raises(json.decoder.JSONDecodeError):
            Session(continue_chat=True)

def test_session_file_invalid_json(tmp_path):
    tmp_session = tmp_path / "session.json"
    with patch('llm_cli.session.SESSION_PATH', tmp_session):
        with open(tmp_session, "wt") as f:
            f.write("invalid JSON")
        with pytest.raises(ValueError):
            Session(continue_chat=True)

def test_session_load_and_save(tmp_path):
    tmp_session = tmp_path / "session.json"
    with patch('llm_cli.session.SESSION_PATH', tmp_session):
        s1 = Session(continue_chat=False)
        s1.add_message("user", "test")
        s1.save()
        s2 = Session(continue_chat=True)
        assert s2.get() == [{"role": "user", "content": "test"}]

