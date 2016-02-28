from learning import Learning
from indicators import Indicators

class Scope(object):
    def __init__(self, scope, q, alpha, reward, discount):
        self.scope = scope
        self.agents = [Agent(self.scope, q, alpha, reward, discount)]

    def add_agent(self, scope, q, alpha, reward, discount):
        self.agents.append(Agent(scope, q, alpha, reward, discount))

    def get_agents(self):
        return self.agents


class Agent(Learning, Indicators):
    def __init__(self, scope, q, alpha, reward, discount, quotes, log=None):
        Learning.__init__(q, alpha, reward, discount)
        Indicators.__init__(quotes)
        self.status = ''
        self.quotes = quotes

    def start_learning(self, states):
        response = self.learn(states)
        if response > 0
            open_position(self, order)


    def open_position(self, type):
        pass

    def close_position(self):
        pass

    def update(self, quote):
        self.quotes.append(quote)