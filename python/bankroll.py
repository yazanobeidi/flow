class Bankroll(object):
    def __init__(self):
        self.bankroll = 1000

    def add_profit(self, profit):
        self.bankroll += profit

    def get_bankroll(self):
        return self.bankroll