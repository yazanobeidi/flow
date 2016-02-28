from learning import Learning
from indicators import Indicators
from order import Order, BUY, SELL, OPEN

class Scope(object):
    def __init__(self, scope, q, alpha, reward, discount, quotes, log):
        self.scope = scope
        self.logger = log
        self.quotes = self.quotes(quotes)
        self.agents = [Agent(self.scope, q, alpha, reward, discount, quotes, 
                                                                   self.logger)]

    def add_agent(self, q, alpha, reward, discount, quotes, log):
        self.agents.append(Agent(self.scope, q, alpha, reward, discount, 
                                                           quotes, self.logger))

    def get_agents(self):
        return self.agents

    def update(self, quote):
        for agent in self.agents:
            agent.update(quote)

    @staticmethod
    def quotes(quotes, sampling=1):
        return quotes[0::sampling]


class Agent(Learning, Indicators, Order):
    def __init__(self, scope, q, alpha, reward, discount, quotes, log=None):
        self.logger = log
        Learning.__init__(self, q, alpha, reward, discount)
        Indicators.__init__(self, log)
        Order.__init__(self, log)
        self.logger = log
        self.status = ''
        self.quotes = quotes

    def learn(self):
        states = self.get_states(self.quotes)
        return self.qlearn(states)

    def trade(self):
        response = self.learn()
        if response > 0:
            if status is not OPEN:
                open_position(order=BUY)
            elif status is BUY:
                self.close_position()
        elif response < 0:
            if status is not OPEN:
                open_position(order=SELL)
            elif status is SELL:
                self.close_position()

    def open_position(self, type):
        self.open_order()
        self.status = OPEN

    def close_position(self):
        self.close_order()
        self.status = ''

    def update(self, quote):
        self.quotes.append(quote)