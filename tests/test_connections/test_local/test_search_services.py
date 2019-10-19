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

"""This module contains the tests for the search feature of the local OEF node."""
import pytest

from aea.connections.local.connection import LocalNode, OEFLocalConnection
from aea.mail.base import MailBox, Envelope
from aea.protocols.fipa.message import FIPAMessage
from aea.protocols.fipa.serialization import FIPASerializer
from aea.protocols.oef.message import OEFMessage
from aea.protocols.oef.models import Query, DataModel, Description
from aea.protocols.oef.serialization import DEFAULT_OEF, OEFSerializer


class TestEmptySearch:
    """Test that the search request returns an empty search result."""

    @classmethod
    def setup_class(cls):
        """Set up the test."""
        cls.node = LocalNode()

        cls.public_key_1 = "mailbox1"
        cls.mailbox1 = MailBox(OEFLocalConnection(cls.public_key_1, cls.node))

        cls.mailbox1.connect()

    def test_empty_search_result(self):
        """Test that at the beginning, the search request returns an empty search result."""
        request_id = 1
        query = Query(constraints=[], model=None)

        # build and send the request
        search_services_request = OEFMessage(oef_type=OEFMessage.Type.SEARCH_SERVICES, id=request_id, query=query)
        msg_bytes = OEFSerializer().encode(search_services_request)
        envelope = Envelope(to=DEFAULT_OEF, sender=self.public_key_1, protocol_id=OEFMessage.protocol_id,
                            message=msg_bytes)
        self.mailbox1.send(envelope)

        # check the result
        response_envelope = self.mailbox1.inbox.get(block=True, timeout=2.0)
        assert response_envelope.protocol_id == OEFMessage.protocol_id
        assert response_envelope.to == self.public_key_1
        assert response_envelope.sender == DEFAULT_OEF
        search_result = OEFSerializer().decode(response_envelope.message)
        assert search_result.get("type") == OEFMessage.Type.SEARCH_RESULT
        assert search_result.get("agents") == []

        # build and send the request
        search_agents_request = OEFMessage(oef_type=OEFMessage.Type.SEARCH_AGENTS, id=request_id, query=query)
        msg_bytes = OEFSerializer().encode(search_agents_request)
        envelope = Envelope(to=DEFAULT_OEF, sender=self.public_key_1, protocol_id=OEFMessage.protocol_id,
                            message=msg_bytes)
        self.mailbox1.send(envelope)

        # check the result
        response_envelope = self.mailbox1.inbox.get(block=True, timeout=5.0)
        assert response_envelope.protocol_id == OEFMessage.protocol_id
        assert response_envelope.sender == DEFAULT_OEF
        search_result = OEFSerializer().decode(response_envelope.message)
        assert search_result.get("type") == OEFMessage.Type.SEARCH_RESULT
        assert search_result.get("agents") == []

    @classmethod
    def teardown_class(cls):
        """Teardown the test."""
        cls.mailbox1.disconnect()


class TestSimpleSearchResult:
    """Test that a simple search result return the expected result."""

    @classmethod
    def setup_class(cls):
        """Set up the test."""
        cls.node = LocalNode()

        cls.public_key_1 = "mailbox1"
        cls.mailbox1 = MailBox(OEFLocalConnection(cls.public_key_1, cls.node))

        cls.mailbox1.connect()

        # register a service.
        request_id = 1
        service_id = ''
        cls.data_model = DataModel("foobar", attributes=[])
        service_description = Description({"foo": 1, "bar": "baz"}, data_model=cls.data_model)
        register_service_request = OEFMessage(oef_type=OEFMessage.Type.REGISTER_SERVICE, id=request_id,
                                              service_description=service_description, service_id=service_id)
        msg_bytes = OEFSerializer().encode(register_service_request)
        envelope = Envelope(to=DEFAULT_OEF, sender=cls.public_key_1, protocol_id=OEFMessage.protocol_id,
                            message=msg_bytes)
        cls.mailbox1.send(envelope)

    def test_not_empty_search_result(self):
        """Test that the search result contains one entry after a successful registration."""
        request_id = 1
        query = Query(constraints=[], model=self.data_model)

        # build and send the request
        search_services_request = OEFMessage(oef_type=OEFMessage.Type.SEARCH_SERVICES, id=request_id, query=query)
        msg_bytes = OEFSerializer().encode(search_services_request)
        envelope = Envelope(to=DEFAULT_OEF, sender=self.public_key_1, protocol_id=OEFMessage.protocol_id,
                            message=msg_bytes)
        self.mailbox1.send(envelope)

        # check the result
        response_envelope = self.mailbox1.inbox.get(block=True, timeout=2.0)
        assert response_envelope.protocol_id == OEFMessage.protocol_id
        assert response_envelope.to == self.public_key_1
        assert response_envelope.sender == DEFAULT_OEF
        search_result = OEFSerializer().decode(response_envelope.message)
        assert search_result.get("type") == OEFMessage.Type.SEARCH_RESULT
        assert search_result.get("agents") == [self.public_key_1]

    @classmethod
    def teardown_class(cls):
        """Teardown the test."""
        cls.mailbox1.disconnect()


# class TestFilteredSearchResult:
#     """Test that the query system of the search gives the expected result."""
#
#     @classmethod
#     def setup_class(cls):
#         """Set up the test."""
#         cls.node = LocalNode()
#
#         cls.public_key_1 = "mailbox1"
#         cls.public_key_2 = "mailbox2"
#         cls.mailbox1 = MailBox(OEFLocalConnection(cls.public_key_1, cls.node))
#         cls.mailbox2 = MailBox(OEFLocalConnection(cls.public_key_2, cls.node))
#         cls.mailbox1.connect()
#         cls.mailbox2.connect()
#
#         # register 'mailbox2' as a service 'foobar'.
#         request_id = 1
#         service_id = ''
#         cls.data_model_foobar = DataModel("foobar", attributes=[])
#         service_description = Description({"foo": 1, "bar": "baz"}, data_model=cls.data_model_foobar)
#         register_service_request = OEFMessage(oef_type=OEFMessage.Type.REGISTER_SERVICE, id=request_id,
#                                               service_description=service_description, service_id=service_id)
#         msg_bytes = OEFSerializer().encode(register_service_request)
#         envelope = Envelope(to=DEFAULT_OEF, sender=cls.public_key_1, protocol_id=OEFMessage.protocol_id,
#                             message=msg_bytes)
#         cls.mailbox1.send(envelope)
#
#         time.sleep(2.0)
#
#         # register 'mailbox2' as a service 'barfoo'.
#         cls.data_model_barfoo = DataModel("barfoo", attributes=[])
#         service_description = Description({"foo": 1, "bar": "baz"}, data_model=cls.data_model_barfoo)
#         register_service_request = OEFMessage(oef_type=OEFMessage.Type.REGISTER_SERVICE, id=request_id,
#                                               service_description=service_description, service_id=service_id)
#         msg_bytes = OEFSerializer().encode(register_service_request)
#         envelope = Envelope(to=DEFAULT_OEF, sender=cls.public_key_2, protocol_id=OEFMessage.protocol_id,
#                             message=msg_bytes)
#         cls.mailbox2.send(envelope)
#
#         data_model = DataModel("foobar", attributes=[])
#         service_description = Description({"foo": 1, "bar": "baz"}, data_model=data_model)
#         msg = OEFMessage(oef_type=OEFMessage.Type.UNREGISTER_SERVICE, id=0, service_description=service_description,
#                          service_id="Test_service")
#         msg_bytes = OEFSerializer().encode(msg)
#         envelope = Envelope(to="mailbox2", sender="mailbox1", protocol_id=OEFMessage.protocol_id, message=msg_bytes)
#         cls.mailbox1.send(envelope)
#
#     def test_filtered_search_result(self):
#         """Test that the search result contains only the entries matching the query."""
#         request_id = 1
#         query = Query(constraints=[], model=self.data_model_barfoo)
#
#         # build and send the request
#         search_services_request = OEFMessage(oef_type=OEFMessage.Type.SEARCH_SERVICES, id=request_id, query=query)
#         msg_bytes = OEFSerializer().encode(search_services_request)
#         envelope = Envelope(to=DEFAULT_OEF, sender=self.public_key_1, protocol_id=OEFMessage.protocol_id,
#                             message=msg_bytes)
#         self.mailbox1.send(envelope)
#
#         # check the result
#         response_envelope = self.mailbox1.inbox.get(block=True, timeout=5.0)
#         assert response_envelope.protocol_id == OEFMessage.protocol_id
#         assert response_envelope.to == self.public_key_1
#         assert response_envelope.sender == DEFAULT_OEF
#         search_result = OEFSerializer().decode(response_envelope.message)
#         assert search_result.get("type") == OEFMessage.Type.SEARCH_RESULT
#         assert search_result.get("agents") == [self.public_key_2]
#
#     def test_filtered_search_agents(self):
#         """Test that the search result contains only the entries matching the query."""
#         request_id = 1
#
#         query = Query(constraints=[], model=self.data_model_foobar)
#         # build and send the request
#         search_agents_request = OEFMessage(oef_type=OEFMessage.Type.SEARCH_AGENTS, id=request_id, query=query)
#         msg_bytes = OEFSerializer().encode(search_agents_request)
#         envelope = Envelope(to=DEFAULT_OEF, sender=self.public_key_1, protocol_id=OEFMessage.protocol_id,
#                             message=msg_bytes)
#         self.mailbox1.send(envelope)
#
#         # check the result
#         response_envelope = self.mailbox1.inbox.get(block=True, timeout=5.0)
#         assert response_envelope.protocol_id == OEFMessage.protocol_id
#         assert response_envelope.sender == DEFAULT_OEF
#         search_result = OEFSerializer().decode(response_envelope.message)
#         assert search_result.get("type") == OEFMessage.Type.SEARCH_RESULT
#         assert search_result.get("agents") == []
#
#     @classmethod
#     def teardown_class(cls):
#         """Teardown the test."""
#         cls.mailbox1.disconnect()
#         cls.mailbox2.disconnect()


class TestUnregister:
    """Test that the unregister service results to Error Message."""

    @classmethod
    def setup_class(cls):
        """Set up the test."""
        cls.node = LocalNode()

        cls.public_key_1 = "mailbox1"
        cls.mailbox1 = MailBox(OEFLocalConnection(cls.public_key_1, cls.node))

        cls.mailbox1.connect()

    def test_unregister_service_result(self):
        """Test that at the beginning, the search request returns an empty search result."""
        data_model = DataModel("foobar", attributes=[])
        service_description = Description({"foo": 1, "bar": "baz"}, data_model=data_model)
        msg = OEFMessage(oef_type=OEFMessage.Type.UNREGISTER_SERVICE, id=0, service_description=service_description,
                         service_id="Test_service")
        msg_bytes = OEFSerializer().encode(msg)
        envelope = Envelope(to=DEFAULT_OEF, sender="mailbox1", protocol_id=OEFMessage.protocol_id, message=msg_bytes)
        self.mailbox1.send(envelope)

        # check the result
        response_envelope = self.mailbox1.inbox.get(block=True, timeout=5.0)
        assert response_envelope.protocol_id == OEFMessage.protocol_id
        assert response_envelope.sender == DEFAULT_OEF
        result = OEFSerializer().decode(response_envelope.message)
        assert result.get("type") == OEFMessage.Type.OEF_ERROR

    @classmethod
    def teardown_class(cls):
        """Teardown the test."""
        cls.mailbox1.disconnect()


class TestAgentMessage:
    """Test the the OEF will return Dialogue Error if it doesn't know the public key."""

    @classmethod
    def setup_class(cls):
        """Set up the test."""
        cls.node = LocalNode()

        cls.public_key_1 = "mailbox1"
        cls.mailbox1 = MailBox(OEFLocalConnection(cls.public_key_1, cls.node))

    def test_messages(self):
        """Test that at the beginning, the search request returns an empty search result."""
        msg = FIPAMessage(0, 0, 0, FIPAMessage.Performative.CFP, query=None)
        msg_bytes = FIPASerializer().encode(msg)
        envelope = Envelope(to=DEFAULT_OEF, sender="mailbox1", protocol_id=FIPAMessage.protocol_id, message=msg_bytes)
        with pytest.raises(ConnectionError):
            OEFLocalConnection(self.public_key_1, self.node).send(envelope)

        self.mailbox1.connect()
        msg = FIPAMessage(0, 0, 0, FIPAMessage.Performative.CFP, query=None)
        msg_bytes = FIPASerializer().encode(msg)
        envelope = Envelope(to="mailbox3", sender="mailbox1", protocol_id=FIPAMessage.protocol_id, message=msg_bytes)
        self.mailbox1.send(envelope)

        # check the result
        response_envelope = self.mailbox1.inbox.get(block=True, timeout=5.0)
        assert response_envelope.protocol_id == OEFMessage.protocol_id
        assert response_envelope.sender == DEFAULT_OEF
        result = OEFSerializer().decode(response_envelope.message)
        assert result.get("type") == OEFMessage.Type.DIALOGUE_ERROR

    @classmethod
    def teardown_class(cls):
        """Teardown the test."""
        cls.mailbox1.disconnect()


class TestOEFConnectionFromJson:
    """Test the the OEF will return a connection after reading the .json file."""

    @classmethod
    def setup_class(cls):
        """Set up the test."""
        cls.node = LocalNode()
        cls.public_key_1 = "mailbox1"

    @classmethod
    def teardown_class(cls):
        """Teardown the test."""
        cls.mailbox1.disconnect()