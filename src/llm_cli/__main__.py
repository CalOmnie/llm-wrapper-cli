import argparse
import sys
import time
from importlib.resources import files
import os
from pathlib import Path
from typing import Any

import yaml
from smolagents import HfApiModel, CodeAgent, OpenAIServerModel

from llm_cli.session import Session
from llm_cli.inputs import read_inputs
from llm_cli.prompts import load_prompts

PROMPTS = load_prompts()

USER_CONFIG_FOLDER_PATH = Path(os.path.expanduser("~")) / ".llmc" / "conf.yml"

PROVIDERS = {"hf_api", "openai_api"}

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, nargs="+", help="Path to file or URL to append to the query")
    parser.add_argument("-c", "--continue", dest="cont", action="store_true", help="Whether to use the response to continue the chat")
    parser.add_argument("query", nargs="*", type=str)

    add_argument(parser, "provider", default_val="huggingface", choices=list(PROVIDERS), help="Which model provider to use.")

    group = parser.add_argument_group('HuggingFace API parameters')
    add_argument(group, "hf_token", help="Used to connect to huggingface api")
    add_argument(group, "hf_model_url", default_val="Qwen/Qwen2.5-Coder-32B-Instruct", help="Model URL, can also be a localhost URL for self hosted models")

    group = parser.add_argument_group('OpenAI API parameters')
    add_argument(group, "openai_url", help="Base URL to the OpenAI-compatible API")
    add_argument(group, "openai_key", default_val="no-key", help="API key to provide the URL")
    add_argument(group, "openai_model", help="Name of the model to use")

    return parser


def add_argument(parser: argparse.ArgumentParser, name: str, default_val: Any="", **kwargs) -> None:
    default = get_default(name, default_val)
    arg_name = f"--{name.replace('_', '-')}"
    parser.add_argument(arg_name, default=default, **kwargs)


def get_default(arg_name: str, default: Any) -> Any:
    file_val = ""
    if USER_CONFIG_FOLDER_PATH.exists():
        with USER_CONFIG_FOLDER_PATH.open("rt") as file_conf:
            file_val = yaml.safe_load(file_conf).get(arg_name, "")
    env_val = os.getenv(arg_name.upper(), "")
    return env_val or file_val or default

def load_model(args: argparse.Namespace):
    match args.provider:
        case "huggingface":
            return load_hf_model(args.hf_token, args.hf_model_url)
        case "openai":
            return load_openai_model(args.openai_url, args.openai_key, args.openai_model)
        case _:
            raise ValueError(f"Invalid provider {args.provider}")

def load_hf_model(hf_token: str, model_url: str) -> HfApiModel:
    return HfApiModel(model_url, token=hf_token)

def load_openai_model(api_url: str, api_key: str, model: str) -> OpenAIServerModel:
    return OpenAIServerModel(
        model_id=model,
        api_base=api_url,
        api_key=api_key
    )

def run(args):
    """Console script for llm_cli."""
    agent = load_model(args)
    session = Session(args.cont)
    if args.query and args.query[0] in PROMPTS:
        prompt = PROMPTS[args.query[0]]
        session.add_message("system", prompt)

    query = " ".join(args.query)
    if args.input:
        query += read_inputs(args.input)

    session.add_message("user", query)
    res = agent(session.get())
    session.add_message(res.role, res.content or "")
    print(res.content)
    session.save()
    return 0


def main():
    parser = create_parser()
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    sys.exit(main())
