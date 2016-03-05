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
    def __init__(self, vault, funds):
        self.init_logging(vault)
        self.bankroll = [funds]
        self.transactions = 0
        self.logger.info('Bankroll initialized with $ {}'.format(funds))
        self.xlim = 3000
        self.init_plot()

    def transaction(self, val, t=''):
        """
        Commits and logs a transaction.
        :param: val: amount to transact
        :param: t: type of transaction (withdrawal or deposit)
        """
        self.bankroll.append(self.get_bankroll() + val)
        self.update_plot()
        self.transactions += 1
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

    def init_plot(self):
        plt.ion()
        self.fig, self.ax = plt.subplots(1, 1)
        #self.line = Line2D([], [], color='red', linewidth=2)
        #self.ax.add_line(self.line)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, self.xlim)
        self.ax.set_ylim(0, self.get_bankroll() * 2)
        plt.xlabel('Transactions')
        plt.ylabel('Funds')
        self.ax.hold(True)
        plt.show(False)
        plt.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        #self.line, = self.ax.plot(self.transactions+10, self.get_bankroll(), '--r')
        #self.points = self.ax.plot(self.transactions, self.bankroll, 'o')[0]
        self.lines, = self.ax.plot(self.transactions, self.get_bankroll(), 'o')

    def update_plot(self):
        """
        Work in progress
        Updates plot on each transaction.
        #TODO: solid line graph
        #TODO: scroll once transaction > self.xlim if not already by default
        """
        self.xlim += 1
        #self.ax.set_xlim(0, self.xlim)
        self.lines.set_data(self.transactions, self.get_full_bankroll())
        #self.line.set_data(self.transactions, self.get_bankroll())
        #self.points.set_data(self.transactions, self.bankroll)
        self.fig.canvas.restore_region(self.background)
        #self.ax.draw_artist(self.lines)
        self.ax.draw_artist(self.lines)
        self.fig.canvas.blit(self.ax.bbox)

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

        '''
    def init_plot(self):
        plt.ion()
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, self.xlim)
        self.ax.set_ylim(0, self.bankroll * 2)
        plt.xlabel('Transactions')
        plt.ylabel('Funds')
        self.ax.hold(True)
        plt.show(False)
        plt.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        #self.points = self.ax.plot(self.transactions, self.bankroll, 'o')[0]
        self.lines, = self.ax.plot(self.transactions, self.get_bankroll(), 'o')

    def update_plot(self):
        """
        Work in progress
        Updates plot on each transaction.
        #TODO: solid line graph
        #TODO: scroll once transaction > self.xlim if not already by default
        """
        self.xlim += 1
        #self.ax.set_xlim(0, self.xlim)
        self.lines.set_data(self.transactions, self.get_bankroll())
        #self.points.set_data(self.transactions, self.bankroll)
        self.fig.canvas.restore_region(self.background)
        self.ax.draw_artist(self.lines)
        self.fig.canvas.blit(self.ax.bbox)
'''