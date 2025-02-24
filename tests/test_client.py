import pytest
from unittest.mock import Mock
import argparse
from smolagents import HfApiModel, OpenAIServerModel
from llm_wrapper_cli.client import (
    load_openai_client,
    load_hf_client,
    load_client,
    ChatBot,
    Agent,
)


@pytest.fixture
def mock_args():
    args = argparse.Namespace()
    args.provider = "huggingface"
    args.hf_token = "fake_token"
    args.hf_model_url = "http://fakeurl"
    args.openai_url = None
    args.openai_key = None
    args.openai_model = None
    args.agent = False
    args.cont = False
    args.agent_test_cmd = "pytest"
    args.agent_test_format = "{test_file}::{test_name}"
    args.agent_coverage_regexp = ""
    return args


def test_load_hf_client():
    client = load_hf_client("fake_token", "http://fakeurl")
    assert isinstance(client, HfApiModel)
    assert client.model_id == "http://fakeurl"


def test_load_openai_client():
    client = load_openai_client(
        api_url="http://apiurl", api_key="api_key", model="model"
    )
    assert isinstance(client, OpenAIServerModel)
    assert client.model_id == "model"


def test_load_client_hf(mock_args):
    mock_args.provider = "huggingface"
    model = load_client(mock_args, "system prompt")
    assert isinstance(model, ChatBot)


def test_load_client_openai(mock_args):
    mock_args.provider = "openai"
    mock_args.openai_key = "api_key"
    model = load_client(mock_args, "system prompt")
    assert isinstance(model, ChatBot)


def test_load_client_agent(mock_args):
    mock_args.agent = True
    model = load_client(mock_args, None)
    assert isinstance(model, Agent)


def test_chatbot_send_query():
    base_model = Mock()
    response = Mock(role="assistant", content="response")
    base_model.return_value = response
    chatbot = ChatBot(base_model, False, "system prompt")
    result = chatbot.send_query("user query")
    assert result == "response"
