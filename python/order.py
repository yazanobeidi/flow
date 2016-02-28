
#action: buy/sell
class Order():
    def __init__(self):
        self.log = log
        self.open_cost = []
        self.close_profit = []
        self.profit = []
        
    def open_order(self, action, quote, volume):
        self.action = action
        self.volume = volume
        self.open_cost = quote*volume
        self.logger.info('{action} opened by {agent} in {scope} learning.'.format(
                                                      action=action, agent=self, scope=scope))

    def close_order(self, quote):
        self.close_profit = quote*volume
        self.profit = self.close_profit - self.open_cost
        self.logger.info('{action} closed by {agent} in {scope} learning. Profit = ${profit}.'.format(
                                                      action=action, agent=self, scope=scope, profit = self.profit))
        
    def get_profit(self):
        return self.profit

    
        
    


