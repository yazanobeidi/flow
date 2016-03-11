import logging
from utils.plotter import Plotter
from utils.exceptions import Bankruptcy

__author__ = 'yazan'

class Bankroll(object):
    """
    This class bookkeeps transactions and maintains funds.
    To access real time log output of bankroll:
        $ tail -f -n 40 logs/bankroll.log
    :param: vault: file path of desired Bankroll output.
    :param: funds: initial bankroll funds.
    :param: plot: Bool, whether or not you want to see a plot of Bankroll.
    :param: resolution: desired upper x limit of initial bankroll plot.
    """
    def __init__(self, vault, funds, plot=False, resolution=None):
        self.init_logging(vault)
        self.bankroll, self.transactions = [funds], [0]
        self.logger.info('{} initialized with $ {}'.format(self, funds))
        self.plot = plot
        if plot: self.Plot = Plotter(self.num_transactions(), 
                                     self.get_bankroll(), resolution)

    def transaction(self, val, _type=''):
        """
        Commits and logs a transaction.
        :param: val: amount to transact
        :param: _type: type of transaction (withdrawal or deposit)
        """
        self.bankroll.append(self.get_bankroll() + val)
        # Add increment to list of number of transactions (plot x axis):
        self.transactions.append(self.transactions[-1] + 1)
        if self.plot: self.Plot.update_plot(self.transactions, self.bankroll)
        self.logger.info('{kind} transaction {id}:\t$ {val} added to '\
                         'bankroll:\t$ {br}'.format(id=self.num_transactions(), 
                                   val=val, br=self.get_bankroll(), kind=_type))
        if self.get_bankroll() < 0:
            raise Bankruptcy

    def get_bankroll(self):
        """
        Returns current value of bankroll.
        """
        return self.bankroll[-1]

    def num_transactions(self):
        """
        Returns the number of transactions made so far.
        """
        return self.transactions[-1]

    def init_logging(self, log_file):
        """
        Logger initialization and boilerplate.
        """
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