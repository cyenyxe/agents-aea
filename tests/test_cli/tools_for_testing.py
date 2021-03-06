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
"""Tools used for CLI registry testing."""

from typing import List

from click import ClickException

from tests.test_cli.constants import DEFAULT_TESTING_VERSION


def raise_click_exception(*args):
    """Raise ClickException."""
    raise ClickException("Message")


class AgentConfigMock:
    """An object to mock Agent config."""

    registry_path = "registry"
    name = "name"
    author = "author"

    connections: List[str] = []
    protocols: List[str] = []
    skills: List[str] = []


class ContextMock:
    """An object to mock Context."""

    cwd = "cwd"
    agent_config = AgentConfigMock()


class PublicIdMock:
    """An object to mock PublicId."""

    DEFAULT_VERSION = DEFAULT_TESTING_VERSION

    def __init__(self, name="name", author="author", version=DEFAULT_TESTING_VERSION):
        """Init the Public ID mock object."""
        self.name = name
        self.author = author
        self.version = version

    @classmethod
    def from_str(cls, public_id):
        author, name, version = public_id.replace(":", "/").split("/")
        return cls(author, name, version)
