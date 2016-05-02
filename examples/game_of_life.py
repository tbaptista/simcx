# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2016 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Game of Life example using the simcx framework.

"""

from __future__ import division
import simcx
from scipy import signal
import numpy as np
import pyglet

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


class GameOfLife(simcx.Simulator):
    """A Game of Life simulator."""

    def __init__(self, width=50, height=50):
        super(GameOfLife, self).__init__()

        self.width = width
        self.height = height
        self.values = np.zeros((self.height, self.width))
        self.neighbourhood = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        self.dirty = False

    def random(self, prob):
        self.values = np.random.choice((0, 1), (self.height, self.width),
                                       p=(1-prob, prob))
        self.dirty = True

    def add_block(self, block, pos_x, pos_y):
        height, width = block.shape

        for y in range(height):
            for x in range(width):
                self.values[pos_y + y, pos_x + x] = block[y, x]

        self.dirty = True

    def step(self, delta=0):
        neighbours = signal.convolve2d(self.values, self.neighbourhood,
                                       mode='same', boundary='wrap')
        for y in range(self.height):
            for x in range(self.width):
                n = neighbours[y, x]
                if (n == 3) or (self.values[y, x] == 1 and n == 2):
                    self.values[y, x] = 1
                else:
                    self.values[y, x] = 0

        self.dirty = True


class Grid2D(simcx.Visual):
    QUAD_BLACK = (0, 0, 0) * 4
    QUAD_WHITE = (255, 255, 255) * 4

    def __init__(self, sim: simcx.Simulator, cell_size=20):
        super(Grid2D, self).__init__(sim, sim.width * cell_size,
                                     sim.height * cell_size)

        self._grid_width = sim.width
        self._grid_height = sim.height

        # create graphics objects
        self._batch = pyglet.graphics.Batch()
        self._grid = []
        for y in range(self._grid_height):
            self._grid.append([])
            for x in range(self._grid_width):
                vertex_list = self._batch.add(4, pyglet.gl.GL_QUADS, None,
                                             ('v2i',
                                              (x * cell_size, y * cell_size,
                                               x * cell_size + cell_size,
                                               y * cell_size,
                                               x * cell_size + cell_size,
                                               y * cell_size + cell_size,
                                               x * cell_size,
                                               y * cell_size + cell_size)),
                                             ('c3B', self.QUAD_BLACK))
                self._grid[y].append(vertex_list)

    def draw(self):
        if self.sim.dirty:
            self._update_graphics()
        self._batch.draw()

    def _update_graphics(self):
        for y in range(self._grid_height):
            for x in range(self._grid_width):
                if self.sim.values[y, x] == 1:
                    self._grid[y][x].colors[:] = self.QUAD_WHITE
                else:
                    self._grid[y][x].colors[:] = self.QUAD_BLACK


if __name__ == '__main__':
    # Example patterns
    glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])

    gol = GameOfLife(50, 50)
    #gol.random(0.2)
    gol.add_block(glider, 10, 10)
    vis = Grid2D(gol, 10)

    display = simcx.Display(interval=0.1)
    display.add_simulator(gol)
    display.add_visual(vis)
    simcx.run()
