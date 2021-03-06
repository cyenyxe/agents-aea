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
"""This test module contains the tests for CLI Registry fetch methods."""

from unittest import TestCase, mock

from click import ClickException

from aea.cli.registry.fetch import fetch_agent

from tests.test_cli.tools_for_testing import ContextMock, PublicIdMock


def _raise_exception():
    raise Exception()


@mock.patch("aea.cli.registry.fetch.PublicId", PublicIdMock)
@mock.patch("aea.cli.registry.fetch.download_file", return_value="filepath")
@mock.patch("aea.cli.registry.fetch.extract")
class TestFetchAgent(TestCase):
    """Test case for fetch_package method."""

    @mock.patch(
        "aea.cli.registry.fetch.request_api",
        return_value={"file": "url", "connections": [], "protocols": [], "skills": []},
    )
    def test_fetch_agent_positive(
        self, request_api_mock, extract_mock, download_file_mock,
    ):
        """Test for fetch_agent method positive result."""
        fetch_agent(ContextMock(), PublicIdMock())
        request_api_mock.assert_called_with(
            "GET", "/agents/author/name/{}".format(PublicIdMock.DEFAULT_VERSION)
        )
        download_file_mock.assert_called_once_with("url", "cwd")
        extract_mock.assert_called_once_with("filepath", "cwd/name")

    @mock.patch("aea.cli.registry.fetch.fetch_package")
    @mock.patch(
        "aea.cli.registry.fetch.request_api",
        return_value={
            "file": "url",
            "connections": ["public/id:{}".format(PublicIdMock.DEFAULT_VERSION)],
            "protocols": ["public/id:{}".format(PublicIdMock.DEFAULT_VERSION)],
            "skills": ["public/id:{}".format(PublicIdMock.DEFAULT_VERSION)],
        },
    )
    def test_fetch_agent_with_dependencies_positive(
        self, request_api_mock, fetch_package_mock, extract_mock, download_file_mock,
    ):
        """Test for fetch_agent method with dependencies positive result."""
        fetch_agent(ContextMock(), PublicIdMock())
        request_api_mock.assert_called_with(
            "GET", "/agents/author/name/{}".format(PublicIdMock.DEFAULT_VERSION)
        )
        download_file_mock.assert_called_once_with("url", "cwd")
        extract_mock.assert_called_once_with("filepath", "cwd/name")
        fetch_package_mock.assert_called()

    @mock.patch("aea.cli.registry.fetch.fetch_package", _raise_exception)
    @mock.patch(
        "aea.cli.registry.fetch.request_api",
        return_value={
            "file": "url",
            "connections": ["public/id:{}".format(PublicIdMock.DEFAULT_VERSION)],
            "protocols": [],
            "skills": [],
        },
    )
    @mock.patch("aea.cli.registry.fetch.rmtree")
    def test_fetch_agent_with_dependencies_unable_to_fetch(self, *mocks):
        """Test for fetch_agent method positive result."""
        with self.assertRaises(ClickException):
            fetch_agent(ContextMock(), PublicIdMock())
