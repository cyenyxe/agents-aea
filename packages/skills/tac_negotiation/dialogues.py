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

"""
This module contains the classes required for dialogue management.

- Dialogues: The dialogues class keeps track of all dialogues.
"""

import sys
from typing import TYPE_CHECKING

from aea.skills.base import SharedClass

if TYPE_CHECKING or "pytest" in sys.modules:
    from packages.protocols.fipa.dialogues import FIPADialogues
else:
    from fipa_protocol.dialogues import FIPADialogues


class Dialogues(SharedClass, FIPADialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs) -> None:
        """
        Initialize dialogues.

        :return: None
        """
        SharedClass.__init__(self, **kwargs)
        FIPADialogues.__init__(self)