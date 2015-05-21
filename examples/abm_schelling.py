# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Implementation of Thomas Schelling's segregation model using pyafai and simcx.

"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

# Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1,'..')


import pyafai
import random
import numpy as np
import simcx


class Agent(pyafai.Agent):
    def __init__(self, x, y, equal_threshold=0.33):
        super(Agent, self).__init__()

        self.equal_threshold = equal_threshold

        self.body = pyafai.Object(x, y)

        self.add_perception(EqualNeighbours())
        self._equal = self._perceptions['equal_neighbours']

    def _think(self, delta):
        # Only relocate if no other agent relocated in this time step
        if not self.world.agent_moved:
            if self._equal.value < self.equal_threshold:
                self.relocate()

    def relocate(self):
        new_cell = self.world.get_empty_cell()
        self.world.exit_cell(self.body.x, self.body.y)
        self.body.x = new_cell[0]
        self.body.y = new_cell[1]

    def get_equal_neighbours(self):
        return self._equal.value


class Square(Agent):
    def __init__(self, x, y, equal_threshold=0.33, size=20):
        super(Square, self).__init__(x, y, equal_threshold)

        shape = pyafai.shapes.Rect(size, size, color=('c3B', (200, 50, 50)))
        self.body.add_shape(shape)


class Triangle(Agent):
    def __init__(self, x, y, equal_threshold=0.33, size=20):
        super(Triangle, self).__init__(x, y, equal_threshold)

        shape = pyafai.shapes.Triangle(-size/2, -size/2, size/2, -size/2, 0, size/2, color=('c3B', (50, 200, 50)))
        self.body.add_shape(shape)


class EqualNeighbours(pyafai.Perception):
    def __init__(self):
        super(EqualNeighbours, self).__init__(float, 'equal_neighbours')

    def update(self, agent):
        neighbours = agent.world.get_neighbours(agent.body.x, agent.body.y)
        count = 0
        for obj in neighbours:
            if type(obj.agent) == type(agent):
                count += 1

        if len(neighbours) > 0:
            self.value = count / len(neighbours)
        else:
            return 1.0


class PolygonWorld(pyafai.World2DGrid):
    def __init__(self, width, height, cell, equal_threshold=0.33, init_dist=(0.50, 0.50), init_empty=0.2):
        assert sum(init_dist) == 1.0, "The initial distribution has to sum up to 1.0!"

        super(PolygonWorld, self).__init__(width, height, cell)

        self.equal_threshold = equal_threshold
        self.empty_cells = set([(x, y) for y in range(height) for x in range(width)])
        self.agent_moved = False

        types = (Square, Triangle)
        n = len(types)

        for y in range(height):
            for x in range(width):
                if random.random() > init_empty:
                    i = np.random.choice(n, p=init_dist)
                    agent = types[i](x, y, size=cell * 0.6, equal_threshold=equal_threshold)
                    self.add_agent(agent)
                    agent._update_perceptions()

    def add_agent(self, agent):
        super(PolygonWorld, self).add_agent(agent)

        self.empty_cells.remove((agent.body.x, agent.body.y))

    def update(self, delta):
        self.agent_moved = False
        random.shuffle(self._agents)
        super(PolygonWorld, self).update(delta)

    def exit_cell(self, x, y):
        self.empty_cells.add((x, y))
        self.agent_moved = True

    def get_empty_cell(self):
        return self.empty_cells.pop()

    def get_segregation(self):
        total = 0
        for agent in self._agents:
            total += agent.get_equal_neighbours()

        avg = total / len(self._agents)
        seg = (avg - 0.5) * 2
        if seg < 0:
            seg = 0

        return seg


class SegregationPlot(simcx.Simulator):
    def __init__(self, world: PolygonWorld, **kwargs):
        super(SegregationPlot, self).__init__(**kwargs)

        self.world = world
        self.x = [0]
        self.y = [world.get_segregation() * 100]

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Segregation (%)')
        self.ax.set_xlim(0,100)
        self.ax.set_ylim(0,100)
        self._max_time = 100
        self.l, = self.ax.plot(self.x, self.y)
        self.update_image()

    def step(self, dt=None):
        self.x.append(self.x[-1] + 1)
        self.y.append(self.world.get_segregation() * 100)

    def draw(self):
        if self.x[-1] > self._max_time:
            self._max_time += 50
            self.ax.set_xlim(0, self._max_time)

        self.l.set_data(self.x, self.y)


def setup(equal_threshold):
    world = PolygonWorld(20, 20, 20, equal_threshold=equal_threshold)
    sim = simcx.PyafaiSimulator(world)
    display = simcx.Display()

    display.add_simulator(sim, 0, 200)
    display.add_simulator(SegregationPlot(world, width=400, height=300))

if __name__ == '__main__':
    setup(0.5)
    simcx.run()