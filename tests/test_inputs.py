import pytest
from unittest.mock import Mock, patch
from llm_cli.inputs import read_inputs, extract_markdown, read_file, URL_REGEX

def test_read_inputs_url():
    with patch('llm_cli.inputs.extract_markdown', return_value='Markdown content'):
        result = read_inputs(['https://example.com'])
    assert result == 'Markdown content'

def test_read_inputs_file():
    file_path = '/path/to/file.txt'
    with patch('llm_cli.inputs.Path') as MockPath:
        mock_path = MockPath.return_value
        mock_path.exists.return_value = True
        mock_path.open.return_value.__enter__.return_value.read.return_value = 'File content'
        mock_path.__str__.return_value = file_path
        result = read_inputs([file_path])
    assert result == f"\n# {file_path}\n```\nFile content\n```\n"

def test_read_inputs_invalid_input():
    with pytest.raises(ValueError) as e:
        read_inputs(['invalid_input'])
    assert str(e.value) == 'Invalid input invalid_input'

def test_read_file():
    file_path = '/path/to/file.txt'
    with patch('llm_cli.inputs.Path') as MockPath:
        mock_path = MockPath.return_value
        mock_path.open.return_value.__enter__.return_value.read.return_value = 'File content'
        result = read_file(mock_path)
    assert result == 'File content'
