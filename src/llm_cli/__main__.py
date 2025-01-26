import argparse
import sys
import time
from importlib.resources import files
import os

from smolagents import HfApiModel, CodeAgent, ToolCallingAgent, tool

from llm_cli.session import Session

def load_prompts():
    res = {}
    prompt_folder = files('llm_cli.prompts')
    for prompt in prompt_folder.iterdir():
        res[prompt.stem] = prompt.read_text()
    return res

PROMPTS = load_prompts()

def run(args):
    """Console script for llm_cli."""
    agent = HfApiModel(
        token = os.getenv("HF_TOKEN"),
    )
    session = Session(args.new)
    if args.query and args.query[0] in PROMPTS:
        prompt = PROMPTS[args.query[0]]
        session.add_message("system", prompt)

    query = " ".join(args.query)
    if args.input:
        for f in args.input:
            query += f"# {str(f.name)}\n"
            query += "```\n"
            query += f.read()
            query += "\n```\n"

    session.add_message("user", query)
    res = agent(session.get())
    session.add_message(res.role, res.content or "")
    print(res.content)
    session.save()
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=argparse.FileType("r"), nargs="+")
    parser.add_argument("--new", action="store_true", help="Whether to create a new session")
    parser.add_argument("query", nargs="*", type=str)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    sys.exit(main())
