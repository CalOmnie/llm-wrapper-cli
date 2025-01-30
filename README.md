# LLM Wrapper CLI

Yet another LLM wrapper, this one used to access LLM APIs in the CLI.
The main goal of this project is to provide a faster answer to simple queries
than current solutions. The main things this project aims to provide are:

- A fast and easy way to send queries e.g. `llmc tell me a joke`
- The possibility to provide complex prompts without having to type them every time (see Prompts section)
- The ability to handle files and web pages: `llmc summarize in one line -i https://www.youtube.com/watch\?v\=BKorP55Aqvg`

* Free software: MIT license
* Documentation: https://llm-cli.readthedocs.io.

# Prerequisites

This project sends its queries to a REST API, there are several options to gain
access or host such an API, such as:

## Huggingface
This is the default option due to it being very generous with its free API calls.
this API usually requires a huggingface token to use. To create such a token,
follow the instructions [here](https://huggingface.co/docs/api-inference/en/getting-started).
You can then export your token in your shell `export HF_TOKEN=[...]`

## Self hosted with Ollama
Arguably the easiest way to run self hosted LLMs, just run:
```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
```
Then configure `llmc` to use an openai API (which ollama implements) and you're good to go.

# Quickstart

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ llm-wrapper-cli
export HF_TOKEN=[...] # Token generated in the above step
llmc Tell me a joke
```

# Connecting to OpenAI APIs

To use `llmc` with OpenAI APIs (Chatgpt, Ollama, llama.cpp...), you need to fill in the `openai_*` parameters e.g.

```
$ ollama pull llama3.2
$ llmc --provider openai --openai-url "http://localhost:11434/v1" --openai-model "llama3.2" "Tell me a joke"
```

# Configuration

Every argument, besides `-i` and `-c` can be provided either through a configuration file located
at `~/.llmc/conf.yml`, or an env file, which means that the previous example could also be configured like so:

```
$ cat ~/.llmc/conf.yml
provider: openai
openai_url: "http://localhost:11434/v1"
openai_model: llama3.2
$ llmc "Tell me a joke"
```

```
$ export PROVIDER=openai
$ export OPENAI_URL="http://localhost:11434/v1"
$ export OPENAI_MODEL="llama3.2"
$ llmc Tell me a joke
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
