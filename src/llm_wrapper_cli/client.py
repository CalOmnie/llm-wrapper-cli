import argparse
from typing import Optional

import smolagents
from smolagents import HfApiModel, OpenAIServerModel, CodeAgent

from llm_wrapper_cli.tools import AddTest
from llm_wrapper_cli.session import Session


def load_client(args: argparse.Namespace, system_prompt: str) -> "Model":
    base_model = None
    match args.provider:
        case "huggingface":
            base_model = load_hf_client(args.hf_token, args.hf_model_url)
        case "openai":
            base_model = load_openai_client(
                args.openai_url, args.openai_key, args.openai_model
            )
        case _:
            raise ValueError(f"Invalid provider {args.provider}")

    if args.agent:
        return Agent(args, base_model, system_prompt)
    else:
        return ChatBot(base_model, args.cont, system_prompt)


def load_hf_client(hf_token: str, model_url: str) -> HfApiModel:
    return HfApiModel(model_url, token=hf_token)


def load_openai_client(api_url: str, api_key: str, model: str) -> OpenAIServerModel:
    return OpenAIServerModel(model_id=model, api_base=api_url, api_key=api_key)


class Model:
    def send_query(self):
        raise NotImplementedError()


class ChatBot(Model):
    def __init__(
        self, base: smolagents.Model, continue_session: bool, system_prompt: str = ""
    ):
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
    def __init__(
        self, args: argparse.Namespace, base: smolagents.Model, agent_template: Optional[dict] = None
    ):
        self.base = CodeAgent(
            model=base,
            tools=[
                AddTest(
                    run_cmd=args.agent_test_cmd,
                    test_format_string=args.agent_test_format,
                    coverage_regexp=args.agent_coverage_regexp,
                ),
            ],
            prompt_templates = agent_template,
            additional_authorized_imports=["*"],
        )

    def send_query(self, query: str) -> str:
        res = self.base.run(query)
        return str(res)
