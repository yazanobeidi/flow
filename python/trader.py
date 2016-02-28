from learning import Learning
from indicators import Indicators
from order import Order, BUY, SELL, OPEN, ACTIONS

class Scope(object):
    def __init__(self, scope, q, alpha, reward, discount, quotes, 
                                                                 bankroll, log):
        self.scope = scope
        self.logger = log
        self.quotes = self.quotes(quotes)
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

    @staticmethod
    def quotes(quotes, sampling=1):
        return quotes[0::sampling]


class Agent(Learning, Indicators, Order):
    def __init__(self, scope, q, alpha, reward, discount, quotes, bankroll, 
                                                                      log=None):
        self.logger = log
        self.actions = ACTIONS # BUY, SELL, DO_NOTHING
        Indicators.__init__(self, log)
        Learning.__init__(self, q, alpha, reward, discount, self.state, \
                                                                   self.actions)
        Order.__init__(self, scope, bankroll, log)
        self.num_trades = 0
        self.performance = 1
        self.volume = max(self.performance, 1)
        self.logger = log
        self.status = {'status':'','action':''}
        self.quotes = quotes
        self.states = None

    def learn(self):
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
        self.performance += profit / self.volume * self.num_trades

    def update(self, quote):
        self.quotes.append(quote)