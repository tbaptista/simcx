# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Simulate the random motion of particles using the simcx framework. Based on an
example in Hiroki Sayama's Introduction to the Modeling and Analysis of Complex
Systems book.
"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

# Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1, '..')

import simcx
import numpy as np


class RandomParticles(simcx.Simulator):
    def __init__(self):
        super().__init__()
        self.n = 1000       # Number of particles
        self.sd = 0.1       # Standard deviation

        # generate initial positions
        self.x = np.random.normal(0, 1, self.n)
        self.y = np.random.normal(0, 1, self.n)

        # create initial plot
        self.ax = self.figure.add_subplot(111)
        self.p, = self.ax.plot(self.x, self.y, '.')
        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(-4, 4)

        self.update_image()

    def step(self, dt):
        for i in range(self.n):
            self.x[i] += np.random.normal(0, self.sd)
            self.y[i] += np.random.normal(0, self.sd)

    def draw(self):
        self.p.set_data(self.x, self.y)


if __name__ == '__main__':
    sim = RandomParticles()
    display = simcx.Display()
    display.add_simulator(sim)
    simcx.run()
