import os
from importlib.resources import files
from pathlib import Path
import yaml

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

def load_agent_templates() -> dict:
    res = {}
    templates_folder = files("llm_wrapper_cli.agent_templates")
    for template in templates_folder.iterdir():
        res[template.stem] = yaml.safe_load(template.read_text())
    return res
