
from llm_cli.session import Session
import json

def test_session_init_new(tmp_path):
    session_path = tmp_path / "test_session.json"
    session = Session(continue_chat=False, path=session_path)
    assert session.session == []
    assert session.session_path == session_path

def test_session_load_existing(tmp_path):
    session_path = tmp_path / "test_session.json"
    test_session_data = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
    session_path.write_text(json.dumps(test_session_data))
    session = Session(continue_chat=True, path=session_path)
    assert session.session == test_session_data

def test_session_add_message(tmp_path):
    session_path = tmp_path / "test_session.json"
    session = Session(continue_chat=False, path=session_path)
    session.add_message("user", "Hello")
    session.add_message("assistant", "Hi")
    assert session.session == [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]

def test_session_get(tmp_path):
    session_path = tmp_path / "test_session.json"
    session = Session(continue_chat=False, path=session_path)
    session.add_message("user", "Hello")
    assert session.get() == [{"role": "user", "content": "Hello"}]

def test_session_save(tmp_path):
    session_path = tmp_path / "test_session.json"
    session = Session(continue_chat=False, path=session_path)
    session.add_message("user", "Hello")
    session.save()
    saved_data = json.loads(session_path.read_text())
    assert saved_data == [{"role": "user", "content": "Hello"}]
