__author__ = 'matthew/yazan'

BUY = 'buy'
SELL = 'sell'
OPEN = 'open'
WITHDRAW = 'withdraw'
DEPOSIT = 'deposit'
ACTIONS = [1, -1, 0] # BUY, SELL, DO_NOTHING

class Order(object):
    """
    This class defines a single order and records details to bankroll and log.
    """
    def __init__(self, scope, bankroll, log=None):
        self.bankroll = bankroll
        self.log = log
        self.scope = scope
        self.open_cost = float()
        self.closing_value = float()
        self.profit = float()
        
    def open_order(self, action, price, volume):
        """
        Opens an order and commits cost to bankroll and log.
        :param: action: position type (BUY or SELL)
        :param: price: current opening price
        :param: volume: order size
        """
        self.action = action
        self.volume = volume
        self.open_cost = -price*volume
        self.bankroll.transaction(self.open_cost, WITHDRAW)
        self.logger.info('{volume} {action} opened by {agent} in {scope}. '\
                        'Cost {cost}.'.format(action=action, volume=volume,
                            agent=self, scope=self.scope, cost=self.open_cost))

    def close_order(self, action, price):
        """
        Closes an order, commits transaction to bankroll and returns signed 
            profit generated.
        :param: action: position type (BUY or SELL)
        :param: price: current closing price
        """
        self.closing_value = price*self.volume
        self.bankroll.transaction(self.closing_value, DEPOSIT)
        self.profit = self.closing_value + self.open_cost
        self.logger.info('{volume} {action} closed by {agent} in {scope}. '\
                         'Profit = ${profit}.'.format(action=action, agent=self,
                      volume=self.volume, scope=self.scope, profit=self.profit))        
        return self.profit
    
    def potential_profit(self, price):
        """
        Returns amount of profit closing an order would produce
        """
        return (price * self.volume) + self.open_cost