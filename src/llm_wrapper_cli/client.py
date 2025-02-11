import argparse

import smolagents
from smolagents import HfApiModel, OpenAIServerModel, CodeAgent

from llm_wrapper_cli.tools import FileReaderTool, FileWriteTool
from llm_wrapper_cli.session import Session

def load_client(args: argparse.Namespace, system_prompt: str) -> "Model":
    base_model = None
    match args.provider:
        case "huggingface":
            base_model = load_hf_client(args.hf_token, args.hf_model_url)
        case "openai":
            base_model = load_openai_client(args.openai_url, args.openai_key, args.openai_model)
        case _:
            raise ValueError(f"Invalid provider {args.provider}")

    if args.agent:
        return Agent(base_model, system_prompt)
    else:
        return ChatBot(base_model, args.cont, system_prompt)

def load_hf_client(hf_token: str, model_url: str) -> HfApiModel:
    return HfApiModel(model_url, token=hf_token)

def load_openai_client(api_url: str, api_key: str, model: str) -> OpenAIServerModel:
    return OpenAIServerModel(
        model_id=model,
        api_base=api_url,
        api_key=api_key
    )


class Model:
    def send_query(self):
        raise NotImplementedError()

class ChatBot(Model):
    def __init__(self, base: smolagents.Model, continue_session: bool, system_prompt: str = ""):
        self.base = base
        self.session = Session(continue_session)
        if system_prompt:
            self.session.add_message(role="system", content=system_prompt)

    def send_query(self, query: str) -> str:
        self.session.add_message("user", query)
        res = self.base(self.session.get())
        self.session.add_message(res.role, res.content or "")
        self.session.save()
        return res.content

class Agent(Model):
    def __init__(self, base: smolagents.Model, system_prompt: str = ""):
        self.base = CodeAgent(
            model=base,
            add_base_tools=True,
            tools=[FileReaderTool(), FileWriteTool()],
            additional_authorized_imports=["*"],
        )
        self.system_prompt = system_prompt

    def send_query(self, query: str) -> str:
        full_query = f"{self.system_prompt}\n{query}"
        res = self.base.run(full_query)
        return str(res)
