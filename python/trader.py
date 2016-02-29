from learning import Learning
from indicators import Indicators
from order import Order, BUY, SELL, OPEN, ACTIONS

class Scope(object):
    def __init__(self, scope, q, alpha, reward, discount, quotes, 
                                                                 bankroll, all_profit, log):
        self.scope = scope
        self.logger = log
        self.quotes = self.quotes(quotes, scope)
        self.agents = [Agent(self.scope, q, alpha, reward, discount, self.quotes, 
                                                         bankroll, all_profit, self.logger)]

    def add_agent(self, q, alpha, reward, discount, quotes, bankroll, all_profit, log):
        self.agents.append(Agent(self.scope, q, alpha, reward, discount, 
                                                 self.quotes, bankroll, all_profit, self.logger))

    def get_agents(self):
        return self.agents

    def update(self, quote):
        for agent in self.agents:
            agent.update(quote)

    @staticmethod
    def quotes(quotes, sampling=1):
        return quotes[0::sampling]


class Agent(Learning, Indicators, Order):
    def __init__(self, scope, q, alpha, reward, discount, quotes, bankroll, all_profit, 
                                                                      log=None):
        self.logger = log
        self.actions = ACTIONS # BUY, SELL, DO_NOTHING
        Indicators.__init__(self, log)
        #Learning.__init__(self, q, alpha, reward, discount, self.state, \
        #                                                           self.actions)
        Order.__init__(self, scope, bankroll, all_profit, log)
        self.num_trades = 0
        self.performance = 1
        self.volume = max(self.performance, 5000)
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
        #response = self.learn()
        i=0
        g=0
        p = 0
        response = 0
        self.prev_states = self.states
        self.states = self.get_states(self.quotes)
        for p in range(9):
            if self.states[p] == 1:
                i += 1
            elif self.states[p] == -1:
                g += 1
        if i == 0 and g > 1:
            #print g
            response = -1
        elif g == 0 and i > 1:
            #print i 
            response = 1
        else: response = 0

        if response != 0:
            self.logger.debug('{agent} response is {response}'.format(agent=self, 
                                                            response=response))
        if response is 1:
            if self.status['status'] is not OPEN:
                self.open_position(order=BUY)
            elif self.status['action'] is SELL:
                self.close_position()
                self.open_position(order=BUY)
        elif response is -1:
            if self.status['status'] is not OPEN:
                self.open_position(order=SELL)
            elif self.status['action'] is BUY:
                self.close_position()
                self.open_position(order=SELL)

    def open_position(self, order):
        if len(self.quotes) > 0:
            self.open_order(order, self.quotes[-1], self.volume)
            self.status['status'] = OPEN
            self.status['action'] = order
            self.num_trades = +1

    def close_position(self):
        self.close_order(self.status['action'], self.quotes[-1])
        profit = self.get_profit()
        self.all_profit.append(profit)
        #self.learnQ(self.states, self.status['action'], self.prev_states, profit)
        self.update_performance(profit)
        self.status['status'] = ''
        self.logger.debug('Bankroll: {}'.format(self.bankroll.get_bankroll()))
        self.logger.debug('Ave. Profit: {}'.format(sum(self.all_profit)/len(self.all_profit)))

    def update_performance(self, profit):
        self.performance += profit / self.volume * self.num_trades

    def update(self, quote):
        self.quotes.append(quote)