![publishing](https://github.com/CalOmnie/llm_cli/actions/workflows/publish_to_pypi.yml/badge.svg)
![Tests](https://github.com/CalOmnie/llm_cli/actions/workflows/test_python.yml/badge.svg)

# LLM Wrapper CLI

LLM Wrapper CLI is a powerful tool designed to simplify interactions with language models API like Hugging Face and OpenAI. Whether you need to execute code snippets, analyze documents, or generate content, LLM Wrapper CLI provides a seamless command-line interface. Key features include:
- **Custom System Prompts**: Quickly configure language model outputs with custom prompts.
- **File and URL Processing**: Process files and URLs to generate insightful outputs.
- **Self-Hosting Support**: Easily connect to self-hosted language models using Ollama or similar services.
- **Flexible Configuration**: Configure settings either through command-line arguments, configuration files, or environment variables.

## Quick Examples

Here are a few examples to give you a taste of what you can do with LLM Wrapper CLI:
```
# Convert date string to datetime object
$ llmc python convert "29 June, 1895" to datetime
from datetime import datetime
dt = datetime.strptime('29 June, 1895', '%d %B, %Y')

# Grep for Python files in a directory hierarchy
$ llmc bash grep only python files in folder hierarchy
grep -r --include "*.py" "pattern" folder/

# Explain the functionality of this package
$ llmc explain what this package does in 2 sentences -i $(find src -name "*.py")
This package provides a command-line interface for interacting with language models
like Hugging Face and OpenAI. It supports managing chat sessions,
loading custom prompts, and performing file operations via a code agent.
```

## Features

### Seamless system prompts

The first word of the query is used to check against the available prompts,
this allows for easy configuration of the llm output, without the need to maintain multiple sessions:

```
$ cat ~/.llmc/prompts/bash.md
You are a helpful chatbot, expert in shell commands, you answer queries
about shell with only the commands, without markdown backticks or explanations,
unless specifically requested for instance:

User: Give me a command that list the size of all files in a folder.
You: du -sh folder/*

$ llmc bash ssh into a docker container
docker exec -it container_id_or_name /bin/bash
```

### Providing files and URLs

You can provide files or URLs using the `-i` option, those inputs are converted
to markdown thanks to Microsoft's `markitdown` package, which handles a truly impressive amount of format.

#### Examples
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
To pass all python files in the src folder: `llmc -i $(find src -name "*.py")`

Summarizing youtube videos
```
$ llmc summarize in a few words -i https://www.youtube.com/watch\?v\=BKorP55Aqvg
Short, humorous comedy sketch satirizing corporate meeting dynamics and an engineer's frustration with ambiguous instructions.
```

## Prerequisites

This project sends its queries to a REST API, there are several options to gain
access or host such an API, such as:

### Huggingface
This is the default option due to it being very generous with its free API calls.
this API usually requires a huggingface token to use. To create such a token,
follow the instructions [here](https://huggingface.co/docs/api-inference/en/getting-started).
You can then export your token in your shell `export HF_TOKEN=[...]`

### Self hosted with Ollama
Arguably the easiest way to run self hosted LLMs, just run:
```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
```
Then configure `llmc` to use an openai API (which ollama implements) and you're good to go.

## Quickstart

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ llm-wrapper-cli
export HF_TOKEN=[...] # Token generated in the above step
llmc Tell me a joke
```

## Connecting to OpenAI APIs

To use `llmc` with OpenAI APIs (Chatgpt, Ollama, llama.cpp...), you need to fill in the `openai_*` parameters e.g.

```
$ ollama pull llama3.2
$ llmc --provider openai --openai-url "http://localhost:11434/v1" --openai-model "llama3.2" "Tell me a joke"
```

## Configuration

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


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter-pypackage)
and the [CalOmnie/cookiecutter-pypackage](https://github.com/CalOmnie/cookiecutter) project template.
