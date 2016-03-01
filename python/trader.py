from learning import Learning
from indicators import Indicators
from order import Order, BUY, SELL, OPEN, ACTIONS

__author__ = 'yazan/matthew'

class Scope(object):
    """
    A scope is a resolution in time of quotes and has a collection of agents.
    """
    def __init__(self, scope, q, alpha, reward, discount, quotes, 
                                                                 bankroll, log):
        self.scope = scope
        self.logger = log
        self.quotes = quotes
        self.agents = [Agent(self.scope, q, alpha, reward, discount, quotes, 
                                                         bankroll, self.logger)]

    def add_agent(self, q, alpha, reward, discount, quotes, bankroll, log):
        self.agents.append(Agent(self.scope, q, alpha, reward, discount, 
                                                 quotes, bankroll, self.logger))

    def get_agents(self):
        return self.agents

    def update(self, quote):
        for agent in self.agents:
            agent.update(quote)


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
        self.status = {'status':'','action':''}
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
            elif self.status['action'] is BUY:
                self.close_position()
        elif response is -1:
            if self.status['status'] is not OPEN:
                self.open_position(order=SELL)
            elif self.status['action'] is SELL:
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
        self.status['status'] = ''

    def update_performance(self, profit):
        self.logger.info(self.performance)
        self.performance += profit / self.volume * self.num_trades

    def update(self, quote):
        self.quotes.append(quote)