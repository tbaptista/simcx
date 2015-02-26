#coding: utf-8
#-----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
#-----------------------------------------------------------------------------

"""
Basic example of the use of the simcx framework
"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

#Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1,'..')

import simcx

class SimpleFunction(simcx.Simulator):
    def __init__(self):
        super().__init__()
        self.next_x = -10.0
        self.end_x = 10.0
        self.step_size = 1
        self.x = []
        self.f = lambda x: x
        self.y = []
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(-10,10)
        self.ax.set_ylim(-10,10)
        self.l, = self.ax.plot(self.x, self.y)

    def step(self):
        if (self.next_x < self.end_x):
            x = self.next_x
            self.next_x += self.step_size
            self.x.append(x)
            self.y.append(self.f(x))

    def draw(self):
        self.l.set_data(self.x, self.y)


if __name__ == '__main__':
    display = simcx.Display(SimpleFunction)
    display.show_fps = True
    simcx.run()