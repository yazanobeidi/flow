import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import logging

__author__ = 'yazan'

class Bankroll(object):
    """
    This class bookkeeps transactions and maintains funds.
    To access real time log output of bankroll:
    $ tail -f -n 40 logs/bankroll.log
    """
    def __init__(self, vault, funds, resolution):
        self.init_logging(vault)
        self.bankroll = [funds]
        self.transactions = [0]
        self.logger.info('Bankroll initialized with $ {}'.format(funds))
        self.xlim = 3000
        self.Hud = HUD(self.transactions[-1], self.bankroll[-1], resolution)

    def transaction(self, val, t=''):
        """
        Commits and logs a transaction.
        :param: val: amount to transact
        :param: t: type of transaction (withdrawal or deposit)
        """
        self.bankroll.append(self.get_bankroll() + val)
        self.transactions.append(self.transactions[-1] + 1)
        self.Hud.update_plot(self.transactions, self.get_full_bankroll())
        self.logger.info('{kind} transaction {id}:\t$ {val} added to '\
                        'bankroll:\t$ {br}'.format(id=self.transactions, 
                            val=val, br=self.get_bankroll(), kind=t))
        if self.bankroll < 0:
            raise Exception('We ran out of money')

    def get_bankroll(self):
        """
        Returns current value of bankroll.
        """
        return self.bankroll[-1]

    def get_full_bankroll(self):
        return self.bankroll

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


class HUD(object):
    def __init__(self, x, y, resolution):
        self.resolution = resolution
        self.resize_factor = 2
        self.init_plot(x, y)

    def init_plot(self, x, y):
        #plt.ion()
        self.fig = plt.figure()
        plt.xlabel('Transactions')
        plt.ylabel('Funds')
        plt.ylim(0, 2000)
        plt.xlim(0, self.resolution)
        plt.hold(True)
        plt.show(False)
        plt.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        self.lines = plt.plot(x, y, 'o')[0]

    def update_plot(self, x, y):
        """
        Work in progress
        Updates plot on each transaction.
        #TODO: solid line graph
        #TODO: scroll once transaction > self.xlim if not already by default
        """
        if x[-1] % self.resolution == 0:
            plt.xlim(0, self.resolution * self.resize_factor)
            plt.draw()
            self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
            self.resize_factor += 1
        #self.ax.set_xlim(0, self.xlim)
        self.lines.set_data(x, y)
        #self.line.set_data(self.transactions, self.get_bankroll())
        #self.points.set_data(self.transactions, self.bankroll)
        self.fig.canvas.restore_region(self.background)
        #self.ax.draw_artist(self.lines)
        self.fig.draw_artist(self.lines)
        self.fig.canvas.blit(self.fig.bbox)
        #self.fig.canvas.draw()