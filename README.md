[![CI](https://github.com/CalOmnie/llm_cli/actions/workflows/publish_to_pypi.yml/badge.svg)](https://github.com/CalOmnie/llm_cli/actions/workflows/publish_to_pypi.yml)
[![Coverage Status](https://coveralls.io/repos/github/CalOmnie/llm_cli/badge.svg?branch=main)](https://coveralls.io/github/CalOmnie/llm_cli?branch=main)

# LLM Wrapper CLI
LLM Wrapper CLI is a powerful tool designed to simplify interactions with language models API like Hugging Face and OpenAI. Whether you need to execute code snippets, analyze documents, or generate content, LLM Wrapper CLI provides a seamless command-line interface. Key features include:
- 📜 **Custom System Prompts**: Quickly configure language model outputs with custom prompts.
- 🌐 **File and URL Processing**: Process files and URLs with various format including youtube vidoes and excel files.
- 🏠 **Self-Hosting Support**: Easily connect to self-hosted language models using Ollama or similar services.
- ⚙️ **Flexible Configuration**: Configure settings either through command-line arguments, configuration files, or environment variables.

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

## Installation

```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ llm-wrapper-cli
```

### Using HuggingFace API

The fastest way to get started with `llmc` is with HuggingFace.
Simply follow [these](https://huggingface.co/docs/api-inference/en/getting-started) instructions to create a token,
then export it in your shell like so:
```
export HF_TOKEN=[...]
```
And you're ready to go

### Using Ollama/OpenAI

If you're already using Ollama, one way to configure `llmc` to use is by creating the following file:
```
$ cat ~/.llmc/conf.yml
provider: openai
openai_url: "http://localhost:11434/v1"
openai_model: llama3.2 # Put your favourite model here
```

You can find more ways to configure `llmc` in the [Configuration](https://github.com/CalOmnie/llm_cli/blob/main/docs/configuration.md) section.

## Features

### Code agent

This projects is based off of Huggingface's [smolagents](FIXME) package, this package allows for LLMs to write their own code, execute it,
and use the result to write further code. In the context of ths project, this can be used for:
- Write code/tests, and debug it on its own.
- Do filesystem operations such as file moving/renaming/editing
- Provide up to date information by querrying the web for information instead of its own memory.

The agent function is activated by using the `--agent` option of `llmc`, for instance:

```bash
$ llmc --agent Write a function computing the histggram of a list as well as tests and writes it to hist.py
[...]
FIXME

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

This prompts and others are provided by default, you can find their definition in the [Prompts](https://github.com/CalOmnie/llm_cli/blob/main/docs/prompts.md) section.

### Providing files and URLs

You can provide files or URLs using the `-i` option, those inputs are converted
to markdown thanks to Microsoft's [markitdown](https://github.com/microsoft/markitdown) package, which handles a truly impressive amount of format.

#### Examples
##### Passing code files
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

##### Summarizing youtube videos
```
$ llmc summarize in a few words -i https://www.youtube.com/watch\?v\=BKorP55Aqvg
Short, humorous comedy sketch satirizing corporate meeting dynamics and an engineer's
frustration with ambiguous instructions.
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter-pypackage)
and the [CalOmnie/cookiecutter-pypackage](https://github.com/CalOmnie/cookiecutter) project template.
