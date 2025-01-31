# tests/test_session.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
from llm_cli.session import Session

def test_session():
    s = Session(continue_chat=False)
    s.add_message("user", "test")
    assert s.get() == [{"role": "user", "content": "test"}]
    s.save()
