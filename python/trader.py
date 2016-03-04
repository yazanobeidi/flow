from random import random

from learning import Learning
from indicators import Indicators
from order import Order, BUY, SELL, OPEN, ACTIONS

PERFORMANCE = 0.0 # Value between 0 and 1, 0 agent will always be fired, 1 never

__author__ = 'yazan/matthew'

class Scope(object):
    """
    CONSIDER : RATHER THAN MANY SCOPES AND SINGLE AGENTS WITH SINGLE POSITIONS
               Agents (scopes) with many positions. 
                    This would have an effect on the learning, and performance rating
    A scope is a resolution in time of quotes and has a collection of agents.
    #TODO: ways to visualize agent behaviour and trends, starting with logs
    #CONSIDER: update_limit() using sum of all agent performances / num agents
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
        self.limit = limit # max number of agents
        self.performances = [1] # initial value of default performance
        self.agents = [Agent(self.scope, q, alpha, reward, discount, quotes, 
                                                         bankroll, self.logger)]

    def add_agent(self):
        """
        Adds a new idle agent to the scope.
        """
        self.logger.info('Adding agent to {}'.format(self.scope))
        self.agents.append(Agent(self.scope, self.q, self.alpha, self.reward, 
                     self.discount, self.quotes, self.bankroll, self.logger))

    def get_agents(self):
        """
        Returns the list of all agents.
        """
        return self.agents

    def trade(self):
        """
        Iterates through all agents within a scope instance and 
            begins trading.
        """
        for agent in self.agents:
            agent.trade()

    def refresh(self, new_quote):
        """
        Performs pre-trade actions to update scope state on a new hop:
            - Update quotes: Agent.update(new_quote)
            - Fire agents with poor performance: agents.remove()
            - Spawn new agent if none are idle: self.add_agent
            - Evaluates lowest performance at current hop
        """
        none_are_idle = True
        for agent in self.agents[:]:
            agent.update_quote(new_quote)

            self.performances.append(agent.performance)

            if agent.status['status'] is 'idle':
                if self.needs_to_be_fired(agent):
                    self.logger.info('Firing {}, status: {}'.format(agent, 
                                                        agent.status['status']))
                    self.agents.remove(agent)
                else: none_are_idle = False

        if none_are_idle and len(self.agents) < self.limit:
            self.add_agent()

        self.logger.info('{} agents active'.format(len(self.agents)))

    @staticmethod
    def needs_to_be_fired(agent):
        """
        Evaluation of whether agent needs to be cut.
        """
        return (agent.num_good_trades / agent.num_trades) < PERFORMANCE if \
                                                agent.num_trades is not 0 else False

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
        self.num_trades = 0
        self.num_good_trades = 0
        self.age = 0
        self.close_attempts = 0
        self.performance = 1.00001 #initial performance
        self.volume = 1 #initial volume
        self.logger = log
        self.status = {'status':'idle','action':''}
        self.quotes = quotes # Agent receives most up-to-date quote list
        self.states = None
        Indicators.__init__(self, log)
        Order.__init__(self, scope, bankroll, log)
        Learning.__init__(self, q, alpha, reward, discount, self.state, \
                                                                   self.actions)

    def learn(self):
        """
        Interface between Indicators and Learning.
        Returns best possible action after agent's first state transition.
        """
        self.logger.debug('{agent} in {scope} is learning'.format(
                                                  agent=self, scope=self.scope))
        self.prev_states = self.states
        self.states = self.get_current_state(self.quotes)
        return self.get_action(self.states) if self.prev_states is not None \
                                                                       else None

    def trade(self):
        """
        Defines the tasks an agent performs on a given hop.
        #TODO: Need a way to make agent hold position if potential loss too high
        #TODO: Refactor position logic to a probability distribution function
        #CONSIDER: maybe ^ should respond to the agent's performance
        """
        response = self.learn()
        self.logger.info('{scope} {agent} response: {action} age: {age} '\
                         'trades: {trades}'.format(
                         scope=self.scope, agent=self, age=self.age, 
                         action=response, trades=self.num_trades))
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

        self.age += 1

    def open_position(self, order):
        """
        The steps needed to open a positon.
        :param: order: Order type, can be BUY or SELL
        """
        self.open_order(order, self.quotes[-1], self.volume)
        self.status['status'] = OPEN
        self.status['action'] = order
        self.num_trades += 1

    def close_position(self):
        """
        This function closes agent's open position.
        We introduce randomness so that the agent has the opportunity to learn.
        #TODO: do not close position if potential profit is too low!
        """
        potential = self.potential_profit(self.quotes[-1])
        self.logger.info('{attempt}CLOSE attempt: {val}'.format(val=potential,
                                                                    attempt=self.close_attempts))
        if random() < 0.01 or potential > 0: #(self.performance * self.num_trades / self.age):
            profit = self.close_order(self.status['action'], self.quotes[-1])
            self.learnQ(self.states, self.status['action'], self.prev_states, profit)
            self.update_performance(profit)
            self.update_volume()
            if profit > 0: self.num_good_trades += 1
            self.status['status'] = 'idle'
        else: self.close_attempts += 1

    def update_performance(self, profit):
        """
        This function updates an agent's performance rating and is currently
        called each time a trade is closed.
        :param: profit: signed integer defining profit achieved in closed pos.
        """
        #self.performance = pow(self.performance, ((profit / self.volume) * (self.num_good_trades / self.num_trades)))
        self.performance += ((profit / self.volume) * (self.num_good_trades / self.num_trades))
        self.logger.info('{agent} performance: {perf}'.format(
                            agent=self, perf=self.performance))

    def update_volume(self):
        self.volume = max(int(self.performance), 1)

    def update_quote(self, new_quote):
        """
        This function adds the new_quote for the current hop to its quotes list.
        """
        self.quotes.append(new_quote)
