import argparse
import sys
import time
from importlib.resources import files
import os

from smolagents import HfApiModel

def load_prompts():
    res = {}
    prompt_folder = files('llm_cli.prompts')
    for prompt in prompt_folder.iterdir():
        res[prompt.stem] = prompt.read_text()
    return res

PROMPTS = load_prompts()

def run(args):
    """Console script for llm_cli."""
    model = HfApiModel(
        token = os.getenv("HF_TOKEN")
    )
    msg = []
    if args.query and args.prompt:
        prompt = PROMPTS[args.prompt[0]]
        msg.append({"role": "system", "content": prompt})

    query = args.query or args.prompt
    if args.input:
        query += args.input.read()

    msg.append({"role": "user", "content": query})
    res = model(msg)
    print(res.content)
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=argparse.FileType("r"))
    parser.add_argument("prompt", nargs=1, type=str)
    parser.add_argument("query", nargs="?", type=str)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    sys.exit(main())
