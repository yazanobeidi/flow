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
        Order.__init__(self, scope, log)
        self.volume = 5
        self.logger = log
        self.status = ''
        self.quotes = quotes
        self.actions = [None, None, None] # BUY, SELL, DO_NOTHING

    def learn(self):
        states = self.get_states(self.quotes)
        return self.qlearn(states, self.actions)

    def trade(self):
        response = self.learn()
        if response > 0:
            if self.status is not OPEN:
                self.open_position(order=BUY)
            elif self.status is BUY:
                self.close_position()
        elif response < 0:
            if self.status is not OPEN:
                self.open_position(order=SELL)
            elif self.status is SELL:
                self.close_position()

    def open_position(self, order):
        self.open_order(order, self.quotes[-1], self.volume)
        self.status = OPEN

    def close_position(self, order):
        self.close_order()
        self.status = ''

    def update(self, quote):
        self.quotes.append(quote)