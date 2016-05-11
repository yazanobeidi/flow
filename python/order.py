"""Flow - Algorithmic HF trader

   Copyright 2016, Yazan Obeidi

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__author__ = 'matthew/yazan'

BUY = 'buy'
SELL = 'sell'
OPEN = 'open'
ACTIONS = [1, -1, 0] # BUY, SELL, DO_NOTHING

#action: buy/sell
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
        self.action = action
        self.volume = volume
        self.open_cost = quote*volume
        self.bankroll.transaction(-self.open_cost)
        self.logger.info('{volume} {action} opened by {agent} in {scope}.'\
                                        .format(action=action, volume=volume,
                                                  agent=self, scope=self.scope))

    def close_order(self, action, quote):
        self.close_profit = quote*self.volume
        self.bankroll.transaction(self.close_profit)
        self.profit = self.close_profit - self.open_cost
        self.logger.info('{volume} {action} closed by {agent} in {scope}. '\
                         'Profit = ${profit}.'.format(action=action, agent=self,
                      volume=self.volume, scope=self.scope, profit=self.profit))        
    def get_profit(self):
        return self.profit

    
        
    


