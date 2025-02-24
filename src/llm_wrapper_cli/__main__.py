import argparse
import sys
import os
from pathlib import Path
from typing import Any

import yaml

from llm_wrapper_cli.inputs import read_inputs
from llm_wrapper_cli.prompts import load_prompts, load_agent_templates
from llm_wrapper_cli.client import load_client
from llm_wrapper_cli.tools import TEST_RUN_CMD, TEST_FORMAT_STRING

PROMPTS = load_prompts()
AGENT_TEMPLATES = load_agent_templates()

USER_CONFIG_FOLDER_PATH = Path(os.path.expanduser("~")) / ".llmc" / "conf.yml"

PROVIDERS = {"hf_api", "openai_api"}


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        nargs="+",
        help="Path to file or URL to append to the query",
    )
    parser.add_argument(
        "-c",
        "--continue",
        dest="cont",
        action="store_true",
        help="Whether to use the response to continue the chat",
    )
    parser.add_argument("query", nargs="*", type=str)

    add_argument(
        parser,
        "provider",
        default_val="huggingface",
        choices=list(PROVIDERS),
        help="Which model provider to use.",
    )
    add_argument(
        parser,
        "agent",
        default_val=False,
        action="store_true",
        help="Whether to use a code agent",
    )
    add_argument(parser, "tee", default_val="", help="Which file to save to")

    group = parser.add_argument_group("HuggingFace API parameters")
    add_argument(group, "hf_token", help="Used to connect to huggingface api")
    add_argument(
        group,
        "hf_model_url",
        default_val="Qwen/Qwen2.5-Coder-32B-Instruct",
        help="Model URL, can also be a localhost URL for self hosted models",
    )
    # add_argument(group, "hf_model_url", default_val="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", help="Model URL, can also be a localhost URL for self hosted models")

    group = parser.add_argument_group("OpenAI API parameters")
    add_argument(group, "openai_url", help="Base URL to the OpenAI-compatible API")
    add_argument(
        group, "openai_key", default_val="no-key", help="API key to provide the URL"
    )
    add_argument(group, "openai_model", help="Name of the model to use")

    group = parser.add_argument_group("Code Agent parameters")
    add_argument(
        group,
        "agent_test_cmd",
        help="Command use by the agent to run tests e.g. `pytest`",
        default_val=TEST_RUN_CMD,
    )
    add_argument(
        group,
        "agent_test_format",
        help="Format string used by the agent to run specific function in the test file e.g. '{test_path}::{test_name}'",
        default_val=TEST_FORMAT_STRING,
    )
    add_argument(
        group,
        "agent_coverage_regexp",
        help="If set, checks whether the generated test increases coverage before adding",
    )

    return parser


def add_argument(
    parser: argparse.ArgumentParser, name: str, default_val: Any = "", **kwargs
) -> None:
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


def run(args):
    """Console script for llm_wrapper_cli."""
    system_prompt = ""
    if args.agent and args.query and args.query[0] in AGENT_TEMPLATES:
        system_prompt = AGENT_TEMPLATES[args.query[0]]
        args.query = args.query[1:]
    if args.query and args.query[0] in PROMPTS:
        system_prompt = PROMPTS[args.query[0]]
        args.query = args.query[1:]
    client = load_client(args, system_prompt)

    query = " ".join(args.query)
    if args.input:
        query += read_inputs(args.input)

    res = client.send_query(query)
    print(res)
    if args.tee:
        with open(args.tee, "wt") as f:
            f.write(res)
    return 0


def main():
    parser = create_parser()
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    sys.exit(main())
