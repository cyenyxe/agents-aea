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

"""This module contains the tasks for the 'gym' skill."""

import logging
from queue import Queue
from threading import Thread

from aea.skills.base import SkillContext
from aea.skills.tasks import Task

from packages.fetchai.skills.gym.helpers import ProxyEnv
from packages.fetchai.skills.gym.rl_agent import DEFAULT_NB_STEPS, MyRLAgent, NB_GOODS

logger = logging.getLogger("aea.gym_skill")


class GymTask(Task):
    """Gym task."""

    def __init__(self, skill_context: SkillContext, nb_steps: int = DEFAULT_NB_STEPS):
        """Initialize the task."""
        logger.info("GymTask.__init__: arguments: nb_steps={}".format(nb_steps))
        super().__init__()
        self._rl_agent = MyRLAgent(NB_GOODS)
        self._proxy_env = ProxyEnv(skill_context)
        self.nb_steps = nb_steps
        self._rl_agent_training_thread = Thread(
            target=self._fit, args=[self._proxy_env, self.nb_steps]
        )
        self.is_rl_agent_training = False

    def _fit(self, proxy_env: ProxyEnv, nb_steps: int):
        """Fit the RL agent."""
        self._rl_agent.fit(proxy_env, nb_steps)
        logger.info("Training finished. You can exit now via CTRL+C.")

    @property
    def proxy_env_queue(self) -> Queue:
        """Get the queue."""
        return self._proxy_env.queue

    def setup(self) -> None:
        """Set up the task."""
        logger.info("Gym task: setup method called.")

    def execute(self, *args, **kwargs) -> None:
        """Execute the task."""
        if not self._proxy_env.is_rl_agent_trained and not self.is_rl_agent_training:
            self._start_training()
        if self._proxy_env.is_rl_agent_trained and self.is_rl_agent_training:
            self._stop_training()

    def teardown(self) -> None:
        """Teardown the task."""
        logger.info("Gym Task: teardown method called.")
        if self.is_rl_agent_training:
            self._stop_training()

    def _start_training(self) -> None:
        """Start training the RL agent."""
        logger.info("Training starting ...")
        self.is_rl_agent_training = True
        self._rl_agent_training_thread.start()

    def _stop_training(self) -> None:
        """Stop training the RL agent."""
        self.is_rl_agent_training = False
        self._proxy_env.close()
        self._rl_agent_training_thread.join()
