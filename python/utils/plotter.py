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
        self.plt = plt
        self.resolution = resolution
        self.resize_factor = 2
        self.init_plot(x, y)

    def init_plot(self, x, y):
        self.plt.ion()
        self.fig = self.plt.figure()
        self.plt.xlabel('Transactions')
        self.plt.ylabel('Funds')
        self.plt.ylim(0, 2000)
        self.plt.xlim(0, self.resolution)
        self.plt.hold(True)
        self.plt.show(False)
        self.plt.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        self.lines = self.plt.plot(x, y, 'o')[0]

    def update_plot(self, x, y):
        """
        Updates plot. Blitting=True ensures only changed pixels are updated.
        """
        print self.resolution
        if x[-1] % self.resolution == 0:
            # Increase x-lim as line is reaching the edge.
            self.plt.xlim(0, self.resolution * self.resize_factor)
            self.plt.draw()
            self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)
            self.resize_factor += 1
        self.lines.set_data(x, y)
        self.fig.canvas.restore_region(self.background)
        self.fig.draw_artist(self.lines)
        self.fig.canvas.blit(self.fig.bbox)
        #self.fig.canvas.draw()