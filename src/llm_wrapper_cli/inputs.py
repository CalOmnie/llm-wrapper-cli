from pathlib import Path
import re

from markitdown import MarkItDown

URL_REGEX = re.compile(r'^https?://[^\s]+$')

def read_inputs(inputs: list[str]) -> str:
    """Reads a list of inputs that can be URLs or file paths.

    For URLs, it extracts markdown content.
    For file paths, it reads the file and converts it to markdown if possible.
    If the file cannot be converted to markdown, it reads the file content as text.

    Args:
        inputs (list[str]): A list of URLs or file paths.

    Returns:
        str: A concatenated string of markdown content extracted from inputs.

    Raises:
        ValueError: If an input is neither a valid URL nor a valid file path.
    """
    res = ""
    for inp in inputs:
        if URL_REGEX.match(inp):
            res += extract_markdown(inp)
        elif not (path := Path(inp)).exists():
            raise ValueError(f"Invalid input {inp}")
        else:
            res += f"\n# {str(path)}"
            try:
                res += extract_markdown(path)
            except Exception:
                res += "\n```\n" + read_file(path) + "\n```\n"
    return res

def extract_markdown(target: str) -> str:
    md = MarkItDown()
    result = md.convert(target)
    return result.text_content

def read_file(path: Path) -> str:
    with path.open("rt") as f:
        return f.read()
