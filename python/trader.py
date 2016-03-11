from learning import Learning
from indicators import Indicators
from order import Order, BUY, SELL, OPEN, ACTIONS, S, M, L


class Scope(object):

    def __init__(self, scope, q, alpha, reward, discount, asks, bids,
                 bankroll, all_profit, log):
        self.scope = scope
        self.logger = log
        self.q = q
        self.alpha = alpha
        self.reward = reward
        self.all_profit = all_profit
        self.discount = discount
        self.bankroll = bankroll
        self.activate = False
        self.asks = self.quotes(asks, scope)
        self.bids = self.quotes(bids, scope)
        self.agents = [Agent(self.scope, self.q, self.alpha, self.reward,
                             self.discount, self.asks, self.bids,
                             bankroll, self.all_profit, self.logger)]

    def add_agent(self):
        self.agents.append(Agent(self.scope, self.q, self.alpha,
                                 self.reward, self.discount,
                                 self.asks, self.bids, self.bankroll,
                                 self.all_profit, self.logger))
        self.logger.debug('Adding agent to {}'.format(self.scope))
        return self.agents[-1]

    def get_agents(self):
        return self.agents

    def update(self, ask, bid):
        for agent in self.agents:
            agent.update(ask, bid)

    @staticmethod
    def quotes(quotes, sampling=1):
        return quotes[0::sampling]


class Agent(Learning, Indicators, Order):

    def __init__(self, scope, q, alpha, reward, discount, asks,
                 bids, bankroll, all_profit, log=None):
        self.logger = log
        self.actions = ACTIONS  # BUY, SELL, DO_NOTHING
        Indicators.__init__(self, log)
        # Learning.__init__(self, q, alpha, reward, discount,
        # self.state, self.actions)
        Order.__init__(self, scope, bankroll, all_profit, log)
        self.num_trades = 0
        self.performance = 1
        self.volume = max(self.performance, 5000)
        self.logger = log
        self.status = {'status': '', 'action': '', 'type': ''}
        self.asks = asks
        self.bids = bids
        self.states = (0, 0, 0, 0)

    def learn(self):
        self.prev_states = self.states
        self.states = self.get_states(self.asks)
        if self.prev_states is not None:
            return self.get_action(self.states)
        return None

    def trade(self, ticks, scopeclass):
        # response = self.learn()
        i = 0
        g = 0
        p = 0
        response = 0
        level = 0
        self.states = self.get_states(self.asks)
        scopenum = scopeclass.scope
        level = ticks/scopeclass.scope
        # determining which indicators to count
        state_level = 0
        if level >= 7 and level < 20:
            state_level = 2
        elif level >= 20 and level < 30:
            state_level = 5
        elif level >= 30:
            state_level = 7

        self.agent_logic(level)

        '''
        old method
        # start at max info
        if ticks < 3000:
            state_level = 0

        for p in range(state_level):
            if self.states[p] == 1:
                i += 1
            elif self.states[p] == -1:
                g += 1
        if state_level >= 1:
            if float(g)/float(state_level) > 0.7:
                response = -1
                self.volume = round(float(g)/float(state_level)*5000)
            elif float(i)/float(state_level) > 0.9:
                response = 1
                self.volume = round(float(i)/float(state_level)*5000)
            else:
                response = 0
        else:
            response = 0
        '''

        if response != 0:
            self.logger.debug('{agent} response is {response}'
                              .format(agent=self, response=response))

        # also adds agent if others are busy. that functionality should be
        # implemented somewhere else tho.
        '''
        if response is 1:
            if self.status['status'] is not OPEN:
                self.open_position(order=BUY)
            elif self.status['action'] is SELL:
                self.close_position()
                self.open_position(order=BUY)
            elif len(scopeclass.get_agents()) < 1:
                new = scopeclass.add_agent()
                new.open_position(order=BUY)
        elif response is -1:
            if self.status['status'] is not OPEN:
                self.open_position(order=SELL)
            elif self.status['action'] is BUY:
                self.close_position()
                self.open_position(order=SELL)
            elif len(scopeclass.get_agents()) < 1:
                new = scopeclass.add_agent()
                new.open_position(order=SELL)
        '''

    def agent_logic(self, level):
        if self.status['status'] is OPEN:
            if self.status['action'] is BUY:
                if (self.states[0] == -1) or \
                    self.states[3] == -1:
                    self.close_position()
            elif (self.states[0] == 1) or \
                self.states[3] == -1:
                self.close_position()
        else: 
            if self.states[1] == 1 and self.states[0] == 1:
                self.open_position(order=BUY, ord_type=M)
            elif self.states[1] == -1 and self.states[0] == -1:
                self.open_position(order=SELL, ord_type=M)

        '''
        if self.status['status'] is OPEN:
            if self.status['action'] is BUY:
                varcheck = 1
            else:
                varcheck = -1
            if self.status['type'] is S:
                dim1 = 0
                dim2 = 1
            elif self.status['type'] is M:
                dim1 = 2
                dim2 = 3
            else:
                dim1 = 5
                dim2 = 6
            if self.states[dim1] != self.states[dim2] or self.states[4] == \
                    -varcheck or self.states[dim1] != varcheck:
                    #self.logger.info('Statements: {one}, {two}, {three}'.format(one=(self.states[dim1] != self.states[dim2]), two=(self.states[4] == -varcheck), three=(self.states[dim1] != varcheck)
                    self.close_position()
        else:
            if self.states[0] == self.states[1] and \
                -self.states[0] != self.states[4]:
                # if self.states[0] == 1:
                    # self.open_position(order=BUY, ord_type=S)

                pass
                # else: self.open_position(order=SELL, ord_type=S)
            elif self.states[2] == self.states[3] and \
                -self.states[2] != self.states[4]:
                if self.states[2] == 1:
                    self.open_position(order=BUY, ord_type=M)
                else: self.open_position(order=SELL, ord_type=M)
            elif self.states[5] == self.states[6] and \
                -self.states[5] != self.states[4]:
                if self.states[5] == 1:
                    self.open_position(order=BUY, ord_type=L)
                else: self.open_position(order=SELL, ord_type=L)
        '''


    def open_position(self, order, ord_type):
        if len(self.asks) > 0:
            if order == BUY:
                cost=self.asks[-1]
                self.open_order(order, cost, self.volume)
            if order == SELL:
                cost=self.bids[-1]
                self.open_order(order, cost, self.volume)
            self.status['status']=OPEN
            self.status['action']=order
            self.status['type']=ord_type
            self.num_trades += 1
            self.logger.debug(
                '{type} {order} opened at: {cost}'.format(type=ord_type, order=order, cost=cost))

    def close_position(self):
        if self.status['action'] == BUY:
            cost=self.bids[-1]
            self.close_order(self.status['action'], cost)
        elif self.status['action'] == SELL:
            cost=self.asks[-1]
            self.close_order(self.status['action'], cost)
        profit=self.get_profit()
        self.all_profit.append(profit)
        # self.learnQ(self.states, self.status['action'],
        # self.prev_states, profit)
        self.update_performance(profit)
        self.logger.debug(
            '{order} closed at: {cost}'.format(order=self.status['action'],
                                               cost=cost))
        self.status['status']=''
        self.status['type']=''
        self.logger.info('Bankroll: {}'.format(self.bankroll.get_bankroll()))
        self.logger.debug(
            'Ave. Profit: {}'.format(sum(self.all_profit) /
                                     len(self.all_profit)))

    def update_performance(self, profit):
        self.performance += profit / self.volume * self.num_trades

    def update(self, ask, bid):
        self.asks.append(ask)
        self.bids.append(bid)
