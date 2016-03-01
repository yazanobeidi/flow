import logging

__author__ = 'yazan'

class Bankroll(object):
    """
    This class bookkeeps transactions and maintains funds.
    To access real time log output of bankroll:
    $ tail -f -n 40 logs/bankroll.log
    """
    def __init__(self, vault, funds):
        self.init_logging(vault)
        self.bankroll = funds
        self.transactions = 0
        self.logger.info('Bankroll initialized with $ {}'.format(funds))

    def transaction(self, val):
        self.bankroll += val
        self.transactions += 1
        self.logger.info('Transaction {id}: $ {val} added to bankroll: $ {br}'\
                    .format(id=self.transactions, val=val, br=self.bankroll))
        if self.bankroll < 0:
            raise Exception('We ran out of money')

    def get_bankroll(self):
        return self.bankroll

    def init_logging(self, log_file):
        self.logger = logging.getLogger('bankroll')
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_file, mode='w')
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '\
                                                                '- %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)