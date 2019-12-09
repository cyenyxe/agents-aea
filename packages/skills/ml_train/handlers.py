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

"""This module contains the handler for the 'ml_train' skill."""
import logging
import sys
from typing import cast, TYPE_CHECKING, Any, Dict, Optional, List, Tuple

import numpy as np

from aea.configurations.base import ProtocolId
from aea.decision_maker.messages.transaction import TransactionMessage
from aea.protocols.base import Message
from aea.protocols.oef.message import OEFMessage
from aea.protocols.oef.models import Description
from aea.skills.base import Handler

if TYPE_CHECKING or "pytest" in sys.modules:
    from packages.protocols.ml_trade.message import MLTradeMessage
    from packages.protocols.ml_trade.serialization import MLTradeSerializer
    from packages.skills.ml_train.strategy import Strategy
    from packages.skills.ml_train.tasks import MLTrainTask
    # from packages.skills.ml_train.tasks import MLTask
else:
    from ml_trade_protocol.message import MLTradeMessage
    from ml_trade_protocol.serialization import MLTradeSerializer
    from ml_train_skill.strategy import Strategy
    from ml_train_skill.tasks import MLTrainTask

logger = logging.getLogger("aea.ml_train_skill")

DUMMY_DIGEST = 'dummy_digest'


class TrainHandler(Handler):
    """Train handler."""

    SUPPORTED_PROTOCOL = "ml_trade"

    def __init__(self, **kwargs):
        """Initialize the handler."""
        super().__init__(**kwargs)

    def setup(self) -> None:
        """
        Set up the handler.

        :return: None
        """
        logger.debug("Train handler: setup method called.")

    def handle(self, message: Message, sender: str) -> None:
        """
        Handle messages.

        :param message: the message
        :param sender: the sender
        :return: None
        """
        ml_msg = cast(MLTradeMessage, message)
        ml_msg_performative = MLTradeMessage.Performative(ml_msg.get("performative"))
        if ml_msg_performative == MLTradeMessage.Performative.TERMS:
            self._handle_terms(ml_msg, sender)
        elif ml_msg_performative == MLTradeMessage.Performative.DATA:
            self._handle_data(ml_msg, sender)

    def _handle_terms(self, ml_trade_msg: MLTradeMessage, sender: str) -> None:
        """
        Handle the terms of the request.

        :param ml_trade_msg: the ml trade message
        :param sender: the sender
        :return: None
        """
        terms = cast(Description, ml_trade_msg.get("terms"))
        logger.info("Received terms message from {}: terms={}".format(sender[-5:], terms.values))

        strategy = cast(Strategy, self.context.strategy)
        acceptable = strategy.is_acceptable_terms(terms)
        affordable = strategy.is_affordable_terms(terms)
        if not acceptable and affordable:
            logger.info("[{}]: rejecting, terms are not acceptable and/or affordable".format(self.context.agent_name))
            return

        if strategy.is_ledger_tx:
            # propose the transaction to the decision maker for settlement on the ledger
            tx_msg = TransactionMessage(performative=TransactionMessage.Performative.PROPOSE,
                                        skill_ids=['ml_train'],
                                        transaction_id=strategy.get_next_transition_id(),
                                        sender=self.context.agent_public_keys[terms.values["ledger_id"]],
                                        counterparty=terms.values["address"],
                                        is_sender_buyer=True,
                                        currency_pbk=terms.values['currency_pbk'],
                                        amount=terms.values["price"],
                                        sender_tx_fee=terms.values["buyer_tx_fee"],
                                        counterparty_tx_fee=terms.values["seller_tx_fee"],
                                        ledger_id=terms.values["ledger_id"],
                                        info={'terms': terms, 'counterparty_pbk': sender})  # this is used to send the terms later - because the seller is stateless and must know what terms have been accepted
            self.context.decision_maker_message_queue.put_nowait(tx_msg)
            logger.info("[{}]: proposing the transaction to the decision maker. Waiting for confirmation ...".format(self.context.agent_name))
        else:
            # accept directly with a dummy transaction digest, no settlement
            ml_accept = MLTradeMessage(performative=MLTradeMessage.Performative.ACCEPT,
                                       tx_digest=DUMMY_DIGEST,
                                       terms=terms)
            self.context.outbox.put_message(to=sender,
                                            sender=self.context.agent_public_key,
                                            protocol_id=MLTradeMessage.protocol_id,
                                            message=MLTradeSerializer().encode(ml_accept))
            logger.info("[{}]: sending dummy transaction digest ...".format(self.context.agent_name))

    def _handle_data(self, ml_trade_msg: MLTradeMessage, sender: str) -> None:
        """
        Handle the data.

        :param ml_trade_msg: the ml trade message
        :param sender: the sender
        :return: None
        """
        terms = cast(Description, ml_trade_msg.get("terms"))
        data = cast(Tuple[np.ndarray, np.ndarray], ml_trade_msg.get("data"))
        if data is None:
            logger.info("Received data message with no data from {}".format(sender[-5:]))
        else:
            logger.info("Received data message from {}: data shape={}, terms={}".format(sender[-5:], data[0].shape, terms.values))
            training_task = MLTrainTask(data, skill_context=self.context)
            self.context.task_queue.put(training_task)

    def teardown(self) -> None:
        """
        Teardown the handler.

        :return: None
        """
        logger.debug("Train handler: teardown method called.")


class OEFHandler(Handler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = OEFMessage.protocol_id  # type: Optional[ProtocolId]

    def setup(self) -> None:
        """Call to setup the handler."""
        pass

    def handle(self, message: Message, sender: str) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :param sender: the sender
        :return: None
        """
        # convenience representations
        oef_msg = cast(OEFMessage, message)
        oef_msg_type = OEFMessage.Type(oef_msg.get("type"))

        if oef_msg_type is OEFMessage.Type.SEARCH_RESULT:
            agents = cast(List[str], oef_msg.get("agents"))
            self._handle_search(agents)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass

    def _handle_search(self, agents: List[str]) -> None:
        """
        Handle the search response.

        :param agents: the agents returned by the search
        :return: None
        """
        if len(agents) == 0:
            logger.info("[{}]: found no agents, continue searching.".format(self.context.agent_name))
            return

        logger.info("[{}]: found agents={}, stopping search.".format(self.context.agent_name, list(map(lambda x: x[-5:], agents))))
        strategy = cast(Strategy, self.context.strategy)
        strategy.is_searching = False
        query = strategy.get_service_query()
        for opponent_pbk in agents:
            logger.info("[{}]: sending CFT to agent={}".format(self.context.agent_name, opponent_pbk[-5:]))
            cft_msg = MLTradeMessage(performative=MLTradeMessage.Performative.CFT, query=query)
            self.context.outbox.put_message(to=opponent_pbk,
                                            sender=self.context.agent_public_key,
                                            protocol_id=MLTradeMessage.protocol_id,
                                            message=MLTradeSerializer().encode(cft_msg))


class MyTransactionHandler(Handler):
    """Implement the transaction handler."""

    SUPPORTED_PROTOCOL = TransactionMessage.protocol_id  # type: Optional[ProtocolId]

    def setup(self) -> None:
        """Implement the setup for the handler."""
        pass

    def handle(self, message: Message, sender: str) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :param sender: the sender
        :return: None
        """
        tx_msg_response = cast(TransactionMessage, message)
        if TransactionMessage.Performative(tx_msg_response.get("performative")) == TransactionMessage.Performative.ACCEPT:
            logger.info("[{}]: transaction was successful.".format(self.context.agent_name))
            transaction_digest = cast(str, tx_msg_response.get("transaction_digest"))
            info = cast(Dict[str, Any], tx_msg_response.get("info"))
            terms = cast(Description, info.get("terms"))
            counterparty_pbk = cast(str, info.get("counterparty_pbk"))
            ml_accept = MLTradeMessage(performative=MLTradeMessage.Performative.ACCEPT,
                                       tx_digest=transaction_digest,
                                       terms=terms)
            self.context.outbox.put_message(to=counterparty_pbk,
                                            sender=self.context.agent_public_key,
                                            protocol_id=MLTradeMessage.protocol_id,
                                            message=MLTradeSerializer().encode(ml_accept))
            logger.info("[{}]: Sending accept to counterparty={} with transaction digest={} and terms={}."
                        .format(self.context.agent_name, counterparty_pbk[-5:], transaction_digest, terms.values))
        else:
            logger.info("[{}]: transaction was not successful.".format(self.context.agent_name))

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass