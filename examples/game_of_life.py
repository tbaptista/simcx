# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Game of Life example using the simcx framework.

"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

# Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1,'..')

import simcx
from scipy import signal
import numpy as np
import pyglet

class GameOfLife(simcx.Simulator):
    """A Game of Life simulator."""

    def __init__(self, width=50, height=50, cell_size=20):
        super(GameOfLife, self).__init__(width * cell_size, height * cell_size,
                                         use_mpl=False)

        self.grid_width = width
        self.grid_height = height
        self.values = np.zeros((self.grid_height, self.grid_width))
        self.nhood = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

        # create graphics objects
        self.batch = pyglet.graphics.Batch()
        self.grid = []
        for y in range(height):
            self.grid.append([])
            for x in range(width):
                vertex_list = self.batch.add(4, pyglet.gl.GL_QUADS, None,
                ('v2i', (x * cell_size, y* cell_size,
                         x * cell_size + cell_size, y * cell_size,
                         x * cell_size + cell_size, y * cell_size + cell_size,
                         x * cell_size, y * cell_size + cell_size)),
                ('c3B', (0, 0, 0) * 4))
                self.grid[y].append(vertex_list)

    def add_block(self, block, pos_x, pos_y):
        height, width = block.shape

        for y in range(height):
            for x in range(width):
                self.values[pos_y + y, pos_x + x] = block[y, x]

        self._update_graphics()

    def step(self):
        neighbours = signal.convolve2d(self.values, self.nhood, mode='same',
                                       boundary='wrap')
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                n = neighbours[y, x]
                if (n == 3) or (self.values[y, x] == 1 and n == 2):
                    self.values[y, x] = 1
                else:
                    self.values[y, x] = 0

        self._update_graphics()

    def draw(self):
        self.batch.draw()

    def _update_graphics(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.values[y, x] == 1:
                    self.grid[y][x].colors[:] = (255, 255, 255) * 4
                else:
                    self.grid[y][x].colors[:] = (0, 0, 0) * 4


if __name__ == '__main__':
    # Example patterns
    glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])

    gol = GameOfLife(30, 30, 20)
    gol.add_block(glider, 10, 10)

    display = simcx.Display()
    display.add_simulator(gol)
    simcx.run()
