__author__ = 'matthew/yazan'

BUY = 'buy'
SELL = 'sell'
OPEN = 'open'
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
        self.close_profit = float()
        self.profit = float()
        
    def open_order(self, action, quote, volume):
        """
        Opens an order and commits cost to bankroll and log.
        :param: action: position type (BUY or SELL)
        :param: quote: current openening price
        :param: volume: order size
        """
        self.action = action
        self.volume = volume
        self.open_cost = quote*volume
        self.bankroll.transaction(-self.open_cost)
        self.logger.info('{volume} {action} opened by {agent} in {scope}.'\
                                        .format(action=action, volume=volume,
                                                  agent=self, scope=self.scope))

    def close_order(self, action, quote):
        """
        Closes an order, commits transaction to bankroll and returns signed 
            profit generated.
        :param: action: position type (BUY or SELL)
        :param: quote: current closing price
        """
        self.close_profit = quote*self.volume
        self.bankroll.transaction(self.close_profit)
        self.profit = self.close_profit - self.open_cost
        self.logger.info('{volume} {action} closed by {agent} in {scope}. '\
                         'Profit = ${profit}.'.format(action=action, agent=self,
                      volume=self.volume, scope=self.scope, profit=self.profit))        
        return self.profit
    
        
    


