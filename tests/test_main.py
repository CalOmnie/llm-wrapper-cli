import pytest
from unittest.mock import patch, MagicMock
import argparse
import os
from pathlib import Path
from llm_wrapper_cli import __main__ as main_module
import yaml


class TestParser:
    def write_conf_to_file(self, conf_path: Path, conf: dict):
        with conf_path.open("wt") as f:
            yaml.safe_dump(conf, f)

    def test_conf_provider(self, tmp_path):
        conf_path = tmp_path / "conf.yml"
        self.write_conf_to_file(conf_path, {"provider": "openai"})
        with patch("llm_wrapper_cli.__main__.USER_CONFIG_FOLDER_PATH", conf_path):
            parser = main_module.create_parser()
            args = parser.parse_args([])
            assert args.provider == "openai"

    def test_default_provider(self, tmp_path):
        conf_path = tmp_path / "conf.yml"
        with patch("llm_wrapper_cli.__main__.USER_CONFIG_FOLDER_PATH", conf_path):
            parser = main_module.create_parser()
            args = parser.parse_args([])
            assert args.provider == "huggingface"

    def test_env_provider(self):
        with patch.dict(os.environ, {"PROVIDER": "env_provider"}):
            parser = main_module.create_parser()
            args = parser.parse_args([])
            assert args.provider == "env_provider"

    def test_cli_provider(self):
        parser = main_module.create_parser()
        args = parser.parse_args(["--provider", "openai_api"])
        assert args.provider == "openai_api"

    def test_default_agent(self):
        parser = main_module.create_parser()
        args = parser.parse_args([])
        assert not args.agent

    def test_env_agent(self):
        with patch.dict(os.environ, {"AGENT": "true"}):
            parser = main_module.create_parser()
            args = parser.parse_args([])
            assert args.agent

    def test_cli_agent(self):
        parser = main_module.create_parser()
        args = parser.parse_args(["--agent"])
        assert args.agent

    def test_cli_tee(self, tmp_path):
        conf_path = tmp_path / "conf.yml"
        with patch("llm_wrapper_cli.__main__.USER_CONFIG_FOLDER_PATH", conf_path):
            parser = main_module.create_parser()
            args = parser.parse_args("--tee a.out".split())
            assert args.tee == "a.out"

    def test_command_line_query(self):
        parser = main_module.create_parser()
        args = parser.parse_args(["hello", "world"])
        assert args.query == ["hello", "world"]

    def test_command_line_input(self):
        parser = main_module.create_parser()
        args = parser.parse_args(["-i", "input.txt"])
        assert args.input == ["input.txt"]

    def test_continue_flag(self):
        parser = main_module.create_parser()
        args = parser.parse_args(["-c"])
        assert args.cont

    def test_combined_arguments(self, tmp_path):
        parser = main_module.create_parser()
        conf_path = tmp_path / "conf.yml"
        self.write_conf_to_file(conf_path, {"provider": "openai", "tee": True})
        with patch("llm_wrapper_cli.__main__.USER_CONFIG_FOLDER_PATH", conf_path):
            with patch.dict(os.environ, {"AGENT": "true"}):
                args = parser.parse_args(
                    [
                        "--provider",
                        "openai_api",
                        "--agent",
                        "--tee",
                        "foo",
                        "bar",
                        "-i",
                        "input.txt",
                        "-c",
                    ]
                )
                assert args.provider == "openai_api"
                assert args.agent
                assert args.tee == "foo"
                assert args.query == ["bar"]
                assert args.input == ["input.txt"]
                assert args.cont

    def test_empty_query(self):
        parser = main_module.create_parser()
        args = parser.parse_args([])
        assert args.query == []

    def test_multiple_inputs(self):
        parser = main_module.create_parser()
        args = parser.parse_args(["-i", "input1.txt", "input2.txt"])
        assert args.input == ["input1.txt", "input2.txt"]
