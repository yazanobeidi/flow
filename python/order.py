BUY = 'buy'
SELL = 'sell'
OPEN = 'open'
S = 's'
M = 'm'
L = 'l'
ACTIONS = [1, -1, 0] # BUY, SELL, DO_NOTHING

#action: buy/sell
class Order(object):
    def __init__(self, scope, bankroll, all_profit, log=None):
        self.bankroll = bankroll
        self.log = log
        self.scope = scope
        self.open_cost = float()
        self.close_profit = float()
        self.profit = float()
        self.all_profit = all_profit
        self.order_volume = 0
        
    def open_order(self, action, quote, volume):
        self.action = action
        self.order_volume = volume
        self.open_cost = quote*volume
        self.logger.debug('{action} {volume} opened by {agent} in {scope}.'\
                           .format(action=action, volume=volume,
                                                  agent=self, scope=self.scope))

    def close_order(self, action, quote):
        self.close_profit = quote*self.order_volume

        if action == BUY:
            self.profit = self.close_profit - self.open_cost

        else:
            self.profit = self.open_cost - self.close_profit
        self.bankroll.add_profit(self.profit)
        self.logger.debug('{action} closed by {agent} in {scope}. '\
                         'Profit = ${profit}.'.format(action=action, agent=self,
                                          scope=self.scope, profit=self.profit))        
    def get_profit(self):
        return self.profit

    
        
    


