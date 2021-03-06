# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This test module contains the tests for the `aea generate protocol` sub-command."""

import json
import os
import shutil
import tempfile
import unittest.mock
from pathlib import Path

import jsonschema
from jsonschema import Draft4Validator, ValidationError

import yaml

import aea.cli.common
import aea.configurations.base
from aea.cli import cli
from aea.configurations.base import DEFAULT_PROTOCOL_CONFIG_FILE

from ...common.click_testing import CliRunner
from ...conftest import (
    CLI_LOG_OPTION,
    CONFIGURATION_SCHEMA_DIR,
    CUR_PATH,
    PROTOCOL_CONFIGURATION_SCHEMA,
)


class TestGenerateProtocol:
    """Test that the command 'aea generate protocol' works correctly in correct preconditions."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        shutil.copyfile(
            Path(CUR_PATH, "data", "sample_specification.yaml"),
            Path(cls.t, "sample_specification.yaml"),
        )
        cls.path_to_specification = str(Path("..", "sample_specification.yaml"))
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        cls.schema = json.load(open(PROTOCOL_CONFIGURATION_SCHEMA))
        cls.resolver = jsonschema.RefResolver(
            "file://{}/".format(Path(CONFIGURATION_SCHEMA_DIR).absolute()), cls.schema
        )
        cls.validator = Draft4Validator(cls.schema, resolver=cls.resolver)

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0
        os.chdir(cls.agent_name)
        # generate protocol
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "generate", "protocol", cls.path_to_specification],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_0(self):
        """Test that the exit code is equal to 0."""
        assert self.result.exit_code == 0

    # def test_resource_folder_contains_module_message(self):
    #     """Test that the protocol folder contains message.py module."""
    #     p = Path(
    #         self.t, self.agent_name, "protocols", "two_party_negotiation", "message.py"
    #     )
    #     original = Path(
    #         CUR_PATH,
    #         "..",
    #         "examples",
    #         "protocol_specification_ex",
    #         "output",
    #         "two_party_negotiation",
    #         "message.py",
    #     )
    #     assert filecmp.cmp(p, original)

    # def test_resource_folder_contains_module_serialization(self):
    #     """Test that the protocol folder contains serialization.py module."""
    #     p = Path(
    #         self.t,
    #         self.agent_name,
    #         "protocols",
    #         "two_party_negotiation",
    #         "serialization.py",
    #     )
    #     original = Path(
    #         CUR_PATH,
    #         "..",
    #         "examples",
    #         "protocol_specification_ex",
    #         "output",
    #         "two_party_negotiation",
    #         "serialization.py",
    #     )
    #     assert filecmp.cmp(p, original)

    def test_resource_folder_contains_configuration_file(self):
        """Test that the protocol folder contains a structurally valid configuration file."""
        p = Path(
            self.t,
            self.agent_name,
            "protocols",
            "two_party_negotiation",
            DEFAULT_PROTOCOL_CONFIG_FILE,
        )
        config_file = yaml.safe_load(open(p))
        self.validator.validate(instance=config_file)

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestGenerateProtocolFailsWhenDirectoryAlreadyExists:
    """Test that the command 'aea generate protocol' fails when a directory with the same name as the name of the protocol being generated already exists."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.protocol_name = "two_party_negotiation"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        shutil.copyfile(
            Path(CUR_PATH, "data", "sample_specification.yaml"),
            Path(cls.t, "sample_specification.yaml"),
        )
        cls.path_to_specification = str(Path("..", "sample_specification.yaml"))
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0
        os.chdir(cls.agent_name)
        # create a dummy 'myprotocol' folder
        Path(cls.t, cls.agent_name, "protocols", cls.protocol_name).mkdir(
            exist_ok=False, parents=True
        )
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "generate", "protocol", cls.path_to_specification],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_error_message_protocol_already_existing(self):
        """Test that the log error message is fixed.

        The expected message is: 'A protocol with name '{protocol_name}' already exists. Aborting...'
        """
        s = "A directory with name '{}' already exists. Aborting...".format(
            self.protocol_name
        )
        self.mocked_logger_error.assert_called_once_with(s)

    def test_resource_directory_exists(self):
        """Test that the resource directory still exists.

        This means that after every failure, we make sure we restore the previous state.
        """
        assert Path(self.t, self.agent_name, "protocols", self.protocol_name).exists()

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestGenerateProtocolFailsWhenProtocolAlreadyExists:
    """Test that the command 'aea add protocol' fails when the protocol already exists."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        shutil.copyfile(
            Path(CUR_PATH, "data", "sample_specification.yaml"),
            Path(cls.t, "sample_specification.yaml"),
        )
        cls.path_to_specification = str(Path("..", "sample_specification.yaml"))
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0
        os.chdir(cls.agent_name)
        # add protocol first time
        result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "generate", "protocol", cls.path_to_specification],
            standalone_mode=False,
        )
        assert result.exit_code == 0
        # generate protocol with the same protocol name
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "generate", "protocol", cls.path_to_specification],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_error_message_protocol_already_existing(self):
        """Test that the log error message is fixed.

        The expected message is: 'A protocol with name '{protocol_name}' already exists. Aborting...'
        """
        s = "A protocol with name 'two_party_negotiation' already exists. Aborting..."
        self.mocked_logger_error.assert_called_once_with(s)

    def test_resource_directory_exists(self):
        """Test that the resource directory still exists.

        This means that after every failure, we make sure we restore the previous state.
        """
        assert Path(
            self.t, self.agent_name, "protocols", "two_party_negotiation"
        ).exists()

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestGenerateProtocolFailsWhenConfigFileIsNotCompliant:
    """Test that the command 'aea generate protocol' fails when the configuration file is not compliant with the schema."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        shutil.copyfile(
            Path(CUR_PATH, "data", "sample_specification.yaml"),
            Path(cls.t, "sample_specification.yaml"),
        )
        cls.path_to_specification = str(Path("..", "sample_specification.yaml"))
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0

        # change the dumping of yaml module to raise an exception.
        cls.patch = unittest.mock.patch(
            "yaml.safe_dump", side_effect=ValidationError("test error message")
        )
        cls.patch.__enter__()

        os.chdir(cls.agent_name)
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "generate", "protocol", cls.path_to_specification],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    # def test_configuration_file_not_valid(self):
    #     """Test that the log error message is fixed.
    #
    #     The expected message is: 'Cannot find protocol: '{protocol_name}'
    #     """
    #     self.mocked_logger_error.assert_called_once_with("test error message")

    def test_resource_directory_does_not_exists(self):
        """Test that the resource directory does not exist.

        This means that after every failure, we make sure we restore the previous state.
        """
        assert not Path(
            self.t, self.agent_name, "protocols", "two_party_negotiation"
        ).exists()

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        cls.patch.__exit__()
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestGenerateProtocolFailsWhenExceptionOccurs:
    """Test that the command 'aea generate protocol' fails when the configuration file is not compliant with the schema."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        cls.path_to_specification = str(Path("..", "sample_specification.yaml"))

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0

        cls.patch = unittest.mock.patch(
            "shutil.copytree", side_effect=Exception("unknwon exception")
        )
        cls.patch.__enter__()

        os.chdir(cls.agent_name)
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "generate", "protocol", cls.path_to_specification],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_resource_directory_does_not_exists(self):
        """Test that the resource directory does not exist.

        This means that after every failure, we make sure we restore the previous state.
        """
        assert not Path(
            self.t, self.agent_name, "protocols", "two_party_negotiation"
        ).exists()

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        cls.patch.__exit__()
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass
