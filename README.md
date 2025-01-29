# LLM Wrapper CLI

Yet another LLM wrapper, this one used to access LLM output in CLI

* Free software: MIT license
* Documentation: https://llm-cli.readthedocs.io.

# Quickstart

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ llm-wrapper-cli
export HF_TOKEN=[...] # Optional
llmc Tell me a joke
```

# Features

## System prompts

The first word of your query is checked against the prompts in `llm_cli.system_prompts`,
available prompts are:

## bash prompt
```
You are a helpful chatbot, expert in shell commands, you answer queries
about shell with only the commands, without markdown backticks or explanations,
unless specifically requested for instance:

User: Give me a command that list the size of all files in a folder.
You: du -sh folder/*
```

### Example
```
$ llmc bash find a substring in all python files of a hierarchy
grep -r "substring" . --include "*.py"
```

## python
```
You are a helpful chatbot, expert in python, you answer queries
about python with only code, without explanations,
unless specifically requested. The code you provide should emphasize conciseness.
If you are asked for tests, you should provide results using the pytest library.
Do not use markdown formatting in your responses.
```

### Example
```
$ llmc python histogram of a list
from collections import Counter

def histogram(lst):
    return Counter(lst)

lst = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
histogram(lst)
```

## naming
```
You are a helpful chatbot and an expert at naming variables, modules, library, and scripts.
When asked a query your goal is to find the best name to represent what is described in the query.
You should adhere to the python code style. e.g. variables, functions and method are snake_case,
classes and modules are CamelCase, scripts are snake_case.
You should empahsize conciseness, and always provides at least 5 options and up to 10.
Pay attention to waht the user asks, if he asks for a function, do not propose file names.

### Examples:

User: A module handling both encoding and decoding of files
You:
    - codec.py
    - encode_decode.py
    - file_codec.py

```

### Example
```
$ llmc naming function reading both files and URLs and merging their contents
Sure, here are some naming suggestions for a function that reads both files and URLs and merges their contents:

- `merge_file_url_contents`
- `combine_file_url_data`
- `read_and_merge_sources`
- `fetch_and_merge_resources`
- `integrate_file_url_content`
- `gather_and_merge_data`
- `merge_data_from_files_and_urls`
- `consolidate_file_url_contents`
- `unify_file_url_data`
- `aggregate_file_url_content`
```

## Providing files and URLs

You can provide files or URLs using the `-i` option, those inputs are handled like so:

- `.pdf` and URLs files are converted to markdown using `markitdown`
- other files are just read in the query with them path prepended
- youtube URLs are handled by extracting the transcript and converting it to markdown

### Example:
Passing code files
```
$ llmc python histogram of a list >> hist.py
$ llmc python test histogram function -i hist.py
def test_histogram():
    assert histogram([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]) == {1: 1, 2: 2, 3: 3, 4: 4}
    assert histogram(['a', 'b', 'a', 'c', 'b', 'c', 'c']) == {'a': 2, 'b': 2, 'c': 3}
    assert histogram([]) == {}
    assert histogram([1]) == {1: 1}
    assert histogram([1, 1, 1, 1]) == {1: 4}

test_histogram()
```

Summarizing youtube videos
```
$ llmc summarize in a few words -i https://www.youtube.com/watch\?v\=BKorP55Aqvg
Short, humorous comedy sketch satirizing corporate meeting dynamics and an engineer's frustration with ambiguous instructions.
```

## Continuing conversation

Use the `-c` to continue the conversation and ask for modifications
```
$ llmc python write tests -i hist.py
def test_histogram():
    assert histogram([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]) == {1: 1, 2: 2, 3: 3, 4: 4}
    assert histogram([]) == {}
    assert histogram([1]) == {1: 1}
    assert histogram([1, 1, 1, 1]) == {1: 4}
    assert histogram([1, 2, 3, 4, 5]) == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}

$ llmc -c write one function per test
def test_histogram_with_multiple_elements():
    assert histogram([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]) == {1: 1, 2: 2, 3: 3, 4: 4}

def test_histogram_with_empty_list():
    assert histogram([]) == {}

def test_histogram_with_single_element():
    assert histogram([1]) == {1: 1}

def test_histogram_with_identical_elements():
    assert histogram([1, 1, 1, 1]) == {1: 4}

def test_histogram_with_unique_elements():
    assert histogram([1, 2, 3, 4, 5]) == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
```

# Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter-pypackage)
and the [CalOmnie/cookiecutter-pypackage](https://github.com/CalOmnie/cookiecutter) project template.
