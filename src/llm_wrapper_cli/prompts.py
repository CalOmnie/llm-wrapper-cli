import os
from importlib.resources import files
from pathlib import Path

USER_PROMPT_FOLDER = Path(os.path.expanduser("~")) / ".llmc" / "prompts"


def load_prompts() -> dict:
    res = {}
    prompt_folder = files("llm_wrapper_cli.system_prompts")
    for prompt in prompt_folder.iterdir():
        res[prompt.stem] = prompt.read_text()

    if USER_PROMPT_FOLDER.exists() and USER_PROMPT_FOLDER.is_dir():
        for prompt in USER_PROMPT_FOLDER.iterdir():
            res[prompt.stem] = prompt.read_text()

    return res
