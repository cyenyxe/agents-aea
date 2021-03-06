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

"""This test module contains the tests for the `aea add connection` sub-command."""

import os
import shutil
import tempfile
import unittest.mock
from pathlib import Path

from jsonschema import ValidationError

import yaml

import aea.configurations.base
from aea.cli import cli
from aea.configurations.base import DEFAULT_CONNECTION_CONFIG_FILE

from ...common.click_testing import CliRunner
from ...conftest import CLI_LOG_OPTION, CUR_PATH


class TestAddConnectionFailsWhenConnectionAlreadyExists:
    """Test that the command 'aea add connection' fails when the connection already exists."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        cls.connection_name = "local"
        cls.connection_author = "fetchai"
        cls.connection_version = "0.1.0"
        cls.connection_id = (
            cls.connection_author
            + "/"
            + cls.connection_name
            + ":"
            + cls.connection_version
        )
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        # copy the 'packages' directory in the parent of the agent folder.
        shutil.copytree(Path(CUR_PATH, "..", "packages"), Path(cls.t, "packages"))

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0
        os.chdir(cls.agent_name)
        # add connection first time
        result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "connection", cls.connection_id],
            standalone_mode=False,
        )
        assert result.exit_code == 0
        # add connection again
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "connection", cls.connection_id],
            standalone_mode=False,
        )

    @unittest.mock.patch("aea.cli.add.fetch_package")
    def test_add_connection_from_registry_positive(self, fetch_package_mock):
        """Test add from registry positive result."""
        public_id = aea.configurations.base.PublicId("author", "name", "0.1.0")
        obj_type = "connection"
        result = self.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "--registry", obj_type, str(public_id)],
            standalone_mode=False,
        )
        assert result.exit_code == 0
        fetch_package_mock.assert_called_once_with(
            obj_type, public_id=public_id, cwd="."
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_error_message_connection_already_existing(self):
        """Test that the log error message is fixed.

        The expected message is: 'A connection with id '{connection_id}' already exists. Aborting...'
        """
        s = "A connection with id '{}/{}' already exists. Aborting...".format(
            self.connection_author, self.connection_name
        )
        self.mocked_logger_error.assert_called_once_with(s)

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestAddConnectionFailsWhenConnectionWithSameAuthorAndNameButDifferentVersion:
    """Test that 'aea add connection' fails when the connection with different version already exists."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        cls.connection_name = "local"
        cls.connection_author = "fetchai"
        cls.connection_version = "0.1.0"
        cls.connection_id = (
            cls.connection_author
            + "/"
            + cls.connection_name
            + ":"
            + cls.connection_version
        )
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        # copy the 'packages' directory in the parent of the agent folder.
        shutil.copytree(Path(CUR_PATH, "..", "packages"), Path(cls.t, "packages"))

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0
        os.chdir(cls.agent_name)
        # add connection first time
        result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "connection", cls.connection_id],
            standalone_mode=False,
        )
        assert result.exit_code == 0

        # add connection again, but with different version number
        # first, change version number to package
        different_version = "0.1.1"
        different_id = (
            cls.connection_author + "/" + cls.connection_name + ":" + different_version
        )
        config_path = Path(
            cls.t,
            "packages",
            cls.connection_author,
            "connections",
            cls.connection_name,
            DEFAULT_CONNECTION_CONFIG_FILE,
        )
        config = yaml.safe_load(config_path.open())
        config["version"] = different_version
        yaml.safe_dump(config, config_path.open(mode="w"))
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "connection", different_id],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_error_message_connection_already_existing(self):
        """Test that the log error message is fixed.

        The expected message is: 'A connection with id '{connection_id}' already exists. Aborting...'
        """
        s = "A connection with id '{}' already exists. Aborting...".format(
            self.connection_author + "/" + self.connection_name
        )
        self.mocked_logger_error.assert_called_once_with(s)

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestAddConnectionFailsWhenConnectionNotInRegistry:
    """Test that the command 'aea add connection' fails when the connection is not in the registry."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        cls.connection_id = "author/unknown_connection:0.1.0"
        cls.connection_name = "unknown_connection"
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        # copy the 'packages' directory in the parent of the agent folder.
        shutil.copytree(Path(CUR_PATH, "..", "packages"), Path(cls.t, "packages"))

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0
        os.chdir(cls.agent_name)
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "connection", cls.connection_id],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_error_message_connection_already_existing(self):
        """Test that the log error message is fixed.

        The expected message is: 'Cannot find connection: '{connection_name}''
        """
        s = "Cannot find connection: '{}'.".format(self.connection_id)
        self.mocked_logger_error.assert_called_once_with(s)

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestAddConnectionFailsWhenDifferentPublicId:
    """Test that the command 'aea add connection' fails when the connection has not the same public id."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        cls.connection_id = "different_author/local:0.1.0"
        cls.connection_name = "unknown_connection"
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        # copy the 'packages' directory in the parent of the agent folder.
        shutil.copytree(Path(CUR_PATH, "..", "packages"), Path(cls.t, "packages"))

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0
        os.chdir(cls.agent_name)
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "connection", cls.connection_id],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_error_message_connection_wrong_public_id(self):
        """Test that the log error message is fixed."""
        s = "Cannot find connection: '{}'.".format(self.connection_id)
        self.mocked_logger_error.assert_called_once_with(s)

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestAddConnectionFailsWhenConfigFileIsNotCompliant:
    """Test that the command 'aea add connection' fails when the configuration file is not compliant with the schema."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        cls.connection_id = "fetchai/local:0.1.0"
        cls.connection_name = "local"
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        # copy the 'packages' directory in the parent of the agent folder.
        shutil.copytree(Path(CUR_PATH, "..", "packages"), Path(cls.t, "packages"))

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0

        # change the serialization of the AgentConfig class so to make the parsing to fail.
        cls.patch = unittest.mock.patch.object(
            aea.configurations.base.ConnectionConfig,
            "from_json",
            side_effect=ValidationError("test error message"),
        )
        cls.patch.__enter__()

        os.chdir(cls.agent_name)
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "connection", cls.connection_id],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_configuration_file_not_valid(self):
        """Test that the log error message is fixed.

        The expected message is: 'Cannot find connection: '{connection_name}''
        """
        self.mocked_logger_error.assert_called_once_with(
            "Connection configuration file not valid: test error message"
        )

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        cls.patch.__exit__()
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass


class TestAddConnectionFailsWhenDirectoryAlreadyExists:
    """Test that the command 'aea add connection' fails when the destination directory already exists."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        cls.runner = CliRunner()
        cls.agent_name = "myagent"
        cls.cwd = os.getcwd()
        cls.t = tempfile.mkdtemp()
        cls.connection_id = "fetchai/local:0.1.0"
        cls.connection_name = "local"
        cls.patch = unittest.mock.patch.object(aea.cli.common.logger, "error")
        cls.mocked_logger_error = cls.patch.__enter__()

        # copy the 'packages' directory in the parent of the agent folder.
        shutil.copytree(Path(CUR_PATH, "..", "packages"), Path(cls.t, "packages"))

        os.chdir(cls.t)
        result = cls.runner.invoke(
            cli, [*CLI_LOG_OPTION, "create", cls.agent_name], standalone_mode=False
        )
        assert result.exit_code == 0

        os.chdir(cls.agent_name)
        Path(
            cls.t,
            cls.agent_name,
            "vendor",
            "fetchai",
            "connections",
            cls.connection_name,
        ).mkdir(parents=True, exist_ok=True)
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "add", "connection", cls.connection_id],
            standalone_mode=False,
        )

    def test_exit_code_equal_to_1(self):
        """Test that the exit code is equal to 1 (i.e. catchall for general errors)."""
        assert self.result.exit_code == 1

    def test_file_exists_error(self):
        """Test that the log error message is fixed.

        The expected message is: 'Cannot find connection: '{connection_name}''
        """
        s = "[Errno 17] File exists: './vendor/fetchai/connections/{}'".format(
            self.connection_name
        )
        self.mocked_logger_error.assert_called_once_with(s)

    @classmethod
    def teardown_class(cls):
        """Tear the test down."""
        os.chdir(cls.cwd)
        try:
            shutil.rmtree(cls.t)
        except (OSError, IOError):
            pass
