from learning import Learning
from indicators import Indicators
from order import Order, BUY, SELL, OPEN, ACTIONS

__author__ = 'yazan/matthew'

class Scope(object):
    """
    A scope is a resolution in time of quotes and has a collection of agents.
    #TODO: ways to visualize agent behaviour and trends, starting with logs
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

    def update(self, quote):
        """
        Iterates through all agents within a scope instance and 
            provides the newest quote on a hop.
        """
        for agent in self.agents:
            agent.update(quote)

    def trade(self):
        """
        Iterates through all agents within a scope instance and 
            begins trading.
        """
        for agent in self.agents:
            agent.trade()

    def refresh(self, new_quote):
        """
        Performs actions to update scope state on a new hop:
            Update quotes: Agent.update(new_quote)
            Fire agents with poor performance: Agent.remove()
            Spawn new agent if none are idle: self.add_agent
        (We iterate over a slice so that we only need a single loop, and can
        remove agent instances within this single loop.)
        self.agents[:] = [agent for agent in self.agents if agent.performance<1]
            could also work, before the existing loop.
        """
        none_are_idle = True
        for agent in self.agents[:]:
            agent.update(new_quote)

            if agent.status['status'] is 'idle':
                none_are_idle = False
            elif agent.performance < 1:
                self.logger.info('Firing {}'.format(agent))
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
        self.num_trades = 0
        self.performance = 1.00 #initial performance
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
        #CONSIDER: maybe ^ should respond to the agent's 
        """
        response = self.learn()
        self.logger.info('{agent} response is {action}'.format(agent=self, 
                                                            action=response))
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
        #TODO: do not close position if potential profit is too low!
        """
        profit = self.close_order(self.status['action'], self.quotes[-1])
        self.learnQ(self.states, self.status['action'], self.prev_states, profit)
        self.update_performance(profit)
        self.status['status'] = 'idle'

    def update_performance(self, profit):
        """
        This function updates an agent's performance rating and is currently
        called each time a trade is closed.
        :param: profit: signed integer defining profit achieved in closed pos.
        """
        self.performance += pow(self.performance, (profit / self.volume * self.num_trades))
        self.volume = max(int(self.performance), 1)
        self.logger.info('{perf} - {agent} performance:'.format(agent=self, 
                                                        perf=self.performance))

    def update(self, new_quote):
        """
        This function adds the new_quote for the current hop to its quotes list.
        """
        self.quotes.append(new_quote)