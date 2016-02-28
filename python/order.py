BUY = 'buy'
SELL = 'sell'
OPEN = 'open'

#action: buy/sell
class Order(object):
    def __init__(self, scope, log=None):
        self.log = log
        self.scope = scope
        self.open_cost = float()
        self.close_profit = float()
        self.profit = float()
        
    def open_order(self, action, quote, volume):
        self.action = action
        self.volume = volume
        self.open_cost = quote*volume
        self.logger.info('{action} opened by {agent} in {scope}.'\
                           .format(action=action, agent=self, scope=self.scope))

    def close_order(self, action, quote):
        self.close_profit = quote*volume
        self.profit = self.close_profit - self.open_cost
        self.logger.info('{action} closed by {agent} in {scope}. '\
                         'Profit = ${profit}.'.format(action=action, agent=self,
                                             scope=self.scope, profit=self.profit))
        
    def get_profit(self):
        return self.profit

    
        
    


