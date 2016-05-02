# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2016 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
One-dimensional cellular automaton using the simcx framework.

"""

from __future__ import division
import simcx
import numpy as np
import pyglet


__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


class CA(simcx.Simulator):
    """Wolfram's elementary cellular automaton."""

    def __init__(self, rule=30, width=50):
        super(CA, self).__init__()

        self.size = width
        self.rule = rule
        self.values = np.zeros(width)
        self._next_values = np.zeros(width, dtype=np.uint8)
        self.cur_step = 0
        self._neighbourhood = (-1, 0, 1)
        self._neighbours = np.zeros(8, dtype=np.uint8)
        self._rule_template = np.unpackbits(np.array([rule],
                                                     dtype=np.uint8))[::-1]

    def init_random(self, prob):
        self.values = np.random.choice((0, 1), self.size, p=(1-prob, prob))
        self.cur_step += 1

    def init_fixed(self):
        self.values = np.zeros(self.size, dtype=np.uint8)
        self.values[self.size // 2] = 1

        self.cur_step += 1

    def step(self, delta=0):
        for x in range(self.size):
            for i, dx in enumerate(self._neighbourhood):
                self._neighbours[-(i+1)] = self.values[(x - dx) % self.size]
            self._next_values[x] = self._apply_rule(self._neighbours)

        temp = self.values
        self.values = self._next_values
        self._next_values = temp
        self.cur_step += 1

    def _apply_rule(self, neighbours):
        a = np.packbits(neighbours)
        i = a[0]
        return self._rule_template[i]


class CAVisual(simcx.Visual):
    QUAD_WHITE = (255, 255, 255) * 4
    QUAD_BLACK = (0, 0, 0) * 4

    def __init__(self, sim: CA, cell_size=20):
        self.size = sim.size
        self._cell = cell_size
        self._last_step = 0

        super(CAVisual, self).__init__(sim, width=self.size * cell_size,
                                       height=(self.size//2 + 1) * cell_size)

        # create graphics batch
        pyglet.gl.glClearColor(1, 1, 1, 1)  # Set background color to white
        self._batch = pyglet.graphics.Batch()

    def draw(self):
        if self.sim.cur_step > self._last_step:
            self.update_graphics()
            self._last_step = self.sim.cur_step

        self._batch.draw()

    def update_graphics(self):
        y = self.size // 2 - self.sim.cur_step + 1
        for x in range(self.size):
            if self.sim.values[x] == 1:
                self._batch.add(4, pyglet.gl.GL_QUADS, None,
                ('v2i', (x * self._cell, y * self._cell,
                         x * self._cell + self._cell, y * self._cell,
                         x * self._cell + self._cell, y * self._cell + self._cell,
                         x * self._cell, y * self._cell + self._cell)),
                ('c3B', self.QUAD_BLACK))


if __name__ == '__main__':
    display = simcx.Display(interval=0.2, visible=False)

    ca126 = CA(126, 101)
    ca126.init_fixed()
    display.add_simulator(ca126)

    vis = CAVisual(ca126, 10)
    display.add_visual(vis)

    display.set_visible(True)

    simcx.run()
