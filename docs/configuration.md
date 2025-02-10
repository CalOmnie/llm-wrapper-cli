# Configuration

Configuration in `llm_cli` is done "a la" pip, meaning that options can be passed:
- In the command line directly: `llmc --my-argument foo`
- Through environment variables: `export MY_ARGUMENT=foo ; llmc`
- In a config file located in `~/.llmc/conf.yml`: `my_argument: foo`

In case the arguments are provided in multiple fashion, the priority is as follow:
`CLI>Environment>Config file`.

## Example - handling multiple providers
A simple use case for this method is to easily switch between different providers:

`~/.llmc/conf.yml`
```
provider: hf_api
hf_token: gf_XXX
openai_url: http://XXX
openai_key: XXX
openai_model: XXX
```

Usage:
```shell
# Using huggingface api
$ llmc $PROMPT $QUERY

# Using openai api
$ llmc --provider openai_api $PROMPT $QUERY
```