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

"""Training environment for multi armed bandit."""

from gym.env import BanditNArmedRandom
from proxy.env import ProxyEnv
from rl.agent import RLAgent


if __name__ == "__main__":
    NB_GOODS = 10
    NB_PRICES_PER_GOOD = 100
    NB_STEPS = 4000

    gym_env = BanditNArmedRandom(nb_bandits=NB_GOODS, nb_prices_per_bandit=NB_PRICES_PER_GOOD)
    proxy_env = ProxyEnv(gym_env)

    """Launch the agent."""
    rl_agent = RLAgent(nb_goods=NB_GOODS)
    rl_agent.fit(proxy_env, nb_steps=NB_STEPS)
