from importlib.resources import files

def load_prompts() -> dict:
    res = {}
    prompt_folder = files('llm_cli.system_prompts')
    for prompt in prompt_folder.iterdir():
        res[prompt.stem] = prompt.read_text()
    return res
