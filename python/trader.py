from learning import Learning
from indicators import Indicators

BUY = 'buy'
SELL = 'sell'

class Scope(object):
    def __init__(self, scope, q, alpha, reward, discount, quotes, log):
        self.scope = scope
        self.logger = log
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


class Agent(Learning, Indicators):
    def __init__(self, scope, q, alpha, reward, discount, quotes, log=None):
        self.logger = log
        Learning.__init__(self, q, alpha, reward, discount)
        Indicators.__init__(self, log)
        self.logger = log
        self.status = ''
        self.quotes = quotes

    def start_learning(self):
        states = self.get_states(self.quotes)
        response = self.learn(states)
        if response > 0:
            open_position(self, order=BUY)
        elif response < 0:
            open_position(self, order=SELL)

    def open_position(self, type):
        pass

    def close_position(self):
        pass

    def update(self, quote):
        self.quotes.append(quote)