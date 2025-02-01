import pytest
from unittest.mock import patch, MagicMock
from llm_cli.prompts import load_prompts, USER_PROMPT_FOLDER

@pytest.fixture
def mock_files(monkeypatch):
    mock_package = MagicMock()
    mock_resource = MagicMock()
    mock_package.iterdir.return_value = [MagicMock(stem='test1', read_text=lambda: 'content1')]
    monkeypatch.setattr('llm_cli.prompts.files', MagicMock(return_value=mock_package))
    return mock_resource

def test_load_prompts_no_user_folder(mock_files, monkeypatch):
    mock_folder = MagicMock(exists=lambda: False)
    monkeypatch.setattr('llm_cli.prompts.USER_PROMPT_FOLDER', mock_folder)
    prompts = load_prompts()
    assert prompts == {'test1': 'content1'}

def test_load_prompts_with_user_folder(mock_files, monkeypatch, tmp_path):
    user_prompt_path = tmp_path / "test2.txt"
    user_prompt_path.write_text("content2")
    mock_folder = MagicMock(iterdir= lambda: [user_prompt_path])
    monkeypatch.setattr('llm_cli.prompts.USER_PROMPT_FOLDER', mock_folder)
    prompts = load_prompts()
    assert prompts == {'test1': 'content1', 'test2': 'content2'}
