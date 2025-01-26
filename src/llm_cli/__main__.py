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
    if args.query and args.query[0] in PROMPTS:
        prompt = PROMPTS[args.query[0]]
        msg.append({"role": "system", "content": prompt})

    query = " ".join(args.query)
    if args.input:
        for f in args.input:
            query += f"# {str(f.name)}\n"
            query += f.read()

    msg.append({"role": "user", "content": query})
    res = model(msg)
    print(res.content)
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=argparse.FileType("r"), nargs="+")
    parser.add_argument("query", nargs="*", type=str)
    args = parser.parse_args()
    print(args)
    run(args)


if __name__ == "__main__":
    sys.exit(main())
