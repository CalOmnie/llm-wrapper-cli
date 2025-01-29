from pathlib import Path
import re

from markitdown import MarkItDown

URL_REGEX = re.compile(r'^https?://[^\s]+$')
MARKDOWN_SUFFIX = {"pdf"}

def read_inputs(inputs: list[str]) -> str:
    res = ""
    for inp in inputs:
        if URL_REGEX.match(inp):
            res += extract_markdown(inp)
        elif not (path := Path(inp)).exists():
            raise ValueErrror(f"Invalid input {inp}")
        else:
            if should_markdown(path.suffix):
                res += extract_markdown(path)
            else:
                res += "\n```\n" + read_file(path) + "\n```\n"
    return res

def extract_markdown(target: str) -> str:
    md = MarkItDown()
    result = md.convert(target)
    return result.text_content

def read_file(path: Path) -> str:
    with path.open("rt") as f:
        return f.read()

def should_markdown(suffix: str) -> bool:
    return suffix in MARKDOWN_SUFFIX
