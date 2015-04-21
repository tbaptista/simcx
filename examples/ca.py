# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
One-dimensional cellular automaton using the simcx framework.

"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

# Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1,'..')

import simcx
import numpy as np
import pyglet


class CA(simcx.Simulator):
    """Wolfram's elementary cellular automaton."""

    QUAD_WHITE = (255, 255, 255) * 4

    def __init__(self, width=50, cell_size=20, rule=30):
        super(CA, self).__init__(width * cell_size, width//2 * cell_size,
                                 use_mpl=False)

        self.size = width
        self.rule = 30
        self.values = np.zeros(width)
        self._next_values = np.zeros(width, dtype='uint8')
        self._cur_step = 0
        self._nhood = (-1, 0, 1)
        self._neighbours = np.zeros(8, dtype='uint8')
        self._rule_template = np.unpackbits(np.array([rule], dtype='uint8'))[::-1]
        self._cell = cell_size

        # create graphics batch
        self.batch = pyglet.graphics.Batch()

    def init_random(self, prob):
        self.values = np.random.choice((0, 1), self.size, p=(1-prob, prob))
        self._update_graphics()
        self._cur_step += 1

    def init_fixed(self):
        self.values = np.zeros(self.size, dtype='uint8')
        self.values[self.size // 2] = 1

        self._update_graphics()
        self._cur_step += 1

    def step(self):
        for x in range(self.size):
            for i, dx in enumerate(self._nhood):
                self._neighbours[-(i+1)] = self.values[(x + dx) % self.size]
            self._next_values[x] = self._apply_rule(self._neighbours)

        temp = self.values
        self.values = self._next_values
        self._next_values = temp
        self._update_graphics()
        self._cur_step += 1

    def draw(self):
        self.batch.draw()

    def _apply_rule(self, neighbours):
        a = np.packbits(neighbours)
        i = a[0]
        return self._rule_template[i]

    def _update_graphics(self):
        y = self._cur_step
        for x in range(self.size):
            if self.values[x] == 1:
                self.batch.add(4, pyglet.gl.GL_QUADS, None,
                ('v2i', (x * self._cell, y * self._cell,
                         x * self._cell + self._cell, y * self._cell,
                         x * self._cell + self._cell, y * self._cell + self._cell,
                         x * self._cell, y * self._cell + self._cell)),
                ('c3B', CA.QUAD_WHITE))


if __name__ == '__main__':
    ca30 = CA(100, 10, 30)
    ca30.init_fixed()

    display = simcx.Display(interval=0.2)
    display.add_simulator(ca30)
    simcx.run()
