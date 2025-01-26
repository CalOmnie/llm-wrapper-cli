#!/usr/bin/env python

"""Tests for `llm_cli` package."""


import pytest
from unittest.mock import patch, MagicMock
from llm_cli.__main__ import load_prompts

def test_load_prompts():
    mock_files = MagicMock()
    mock_prompt_folder = MagicMock()
    mock_file1 = MagicMock()
    mock_file2 = MagicMock()

    mock_files.return_value = mock_prompt_folder
    mock_prompt_folder.iterdir.return_value = [mock_file1, mock_file2]
    mock_file1.stem = 'prompt1'
    mock_file1.read_text.return_value = 'Content of prompt1'
    mock_file2.stem = 'prompt2'
    mock_file2.read_text.return_value = 'Content of prompt2'

    with patch('llm_cli.__main__.files', mock_files):
        result = load_prompts()

    assert result == {'prompt1': 'Content of prompt1', 'prompt2': 'Content of prompt2'}
