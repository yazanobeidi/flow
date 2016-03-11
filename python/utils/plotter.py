import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

__author__ = 'yazan'

class Plotter(object):
    """
    Plotting base class. Used to create lightweight real-time updating plots.
    :param: x: List of x values
    :param: y: List of y values
        Note: If you pass single x, y List Ints that single point gets plotted.
    :param: resolution: desired initial upper x limit of plotter
    """
    def __init__(self, x, y, resolution=1000):
        self.resolution = resolution
        self.resize_factor = 2
        self.init_plot(x, y)

    def init_plot(self, x, y):
        plt.ion()
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
        Updates plot. Blitting=True ensures only changed pixels are updated.
        """
        print self.resolution
        if x[-1] % self.resolution == 0:
            # Increase x-lim as line is reaching the edge.
            plt.xlim(0, self.resolution * self.resize_factor)
            plt.draw()
            self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
            self.resize_factor += 1
        self.lines.set_data(x, y)
        self.fig.canvas.restore_region(self.background)
        self.fig.draw_artist(self.lines)
        self.fig.canvas.blit(self.fig.bbox)
        #self.fig.canvas.draw()