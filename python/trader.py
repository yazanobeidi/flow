"""Flow - Algorithmic HF trader

   Copyright 2016, Yazan Obeidi

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from learning import Learning
from indicators import Indicators
from order import Order, BUY, SELL, OPEN, ACTIONS

__author__ = 'yazan/matthew'

class Scope(object):
    """
    A scope is a resolution in time of quotes and has a collection of agents.
    """
    def __init__(self, scope, q, alpha, reward, discount, limit, quotes, 
                                                                 bankroll, log):
        self.scope = scope
        self.q = q
        self.alpha = alpha
        self.reward = reward
        self.discount = discount
        self.bankroll = bankroll
        self.logger = log
        self.quotes = quotes
        self.limit = limit
        self.agents = [Agent(self.scope, q, alpha, reward, discount, quotes, 
                                                         bankroll, self.logger)]

    def add_agent(self):
        self.logger.info('Adding agent to {}'.format(self.scope))
        self.agents.append(Agent(self.scope, self.q, self.alpha, self.reward, 
                        self.discount, self.quotes, self.bankroll, self.logger))

    def get_agents(self):
        return self.agents

    def update(self, quote):
        for agent in self.agents:
            agent.update(quote)

    def trade(self):
        for agent in self.agents:
            agent.trade()

    def refresh(self, new_quote):
        """
        Performs actions to update scope state on a new hop:
            Update quotes: Agent.update(new_quote)
            Fire agents with poor performance: Agent.remove()
            Spawn new agent if none are idle: self.add_agent
        """
        none_are_idle = True
        #self.agents[:] = [agent for agent in self.agents if agent.performance < 1]
        # the above line should work but to avoid iterating through self.agents
        # twice I would like to try doing the following:
        for agent in self.agents[:]:
            agent.update(new_quote)
            if agent.status['status'] is 'idle':
                none_are_idle = False
            elif agent.performance < 1:
                self.agents.remove(agent)
        if none_are_idle and len(self.agents) < self.limit:
            self.add_agent()
            self.logger.info('{} agents active'.format(len(self.agents)))

    def free_agents(self):
        """
        Returns true iff at least one agent has no open positions.
        """
        for agent in self.agents:
            if agent.status['status'] is 'idle':
                return True
        return False

class Agent(Learning, Indicators, Order):
    """
    An agent's primarily role is to place good trades and learn from the
        consequences of its actions. A good trade is one that profits, and good
        trades raise the agent's performance. A higher performance results in a
        greater trade volume for the agent. An agent holds at most a single
        position at once.
    """
    def __init__(self, scope, q, alpha, reward, discount, quotes, bankroll, 
                                                                      log=None):
        self.logger = log
        self.scope = scope
        self.actions = ACTIONS
        Indicators.__init__(self, log)
        Order.__init__(self, scope, bankroll, log)
        Learning.__init__(self, q, alpha, reward, discount, self.state, \
                                                                   self.actions)
        self.num_trades = 0
        self.performance = 1
        self.volume = max(self.performance, 1)
        self.logger = log
        self.status = {'status':'idle','action':''}
        self.quotes = quotes
        self.states = None

    def learn(self):
        self.logger.debug('{agent} in {scope} is learning'.format(
                                                  agent=self, scope=self.scope))
        self.prev_states = self.states
        self.states = self.get_states(self.quotes)
        if self.prev_states is not None: 
            return self.get_action(self.states)
        return None

    def trade(self):
        response = self.learn()
        self.logger.debug('{agent} response is {response}'.format(agent=self, 
                                                            response=response))
        if response is 1:
            if self.status['status'] is not OPEN:
                self.open_position(order=BUY)
            elif self.status['action'] is SELL:
                self.close_position()
        elif response is -1:
            if self.status['status'] is not OPEN:
                self.open_position(order=SELL)
            elif self.status['action'] is BUY:
                self.close_position()

    def open_position(self, order):
        self.open_order(order, self.quotes[-1], self.volume)
        self.status['status'] = OPEN
        self.status['action'] = order
        self.num_trades += 1

    def close_position(self):
        self.close_order(self.status['action'], self.quotes[-1])
        profit = self.get_profit()
        self.learnQ(self.states, self.status['action'], self.prev_states, profit)
        self.update_performance(profit)
        self.status['status'] = 'idle'

    def update_performance(self, profit):
        self.performance += profit * self.volume * self.num_trades
        self.logger.info('{p} - {agent} performance:'.format(agent=self, 
                                                            p=self.performance))

    def update(self, quote):
        self.quotes.append(quote)
