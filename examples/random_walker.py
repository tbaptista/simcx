# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2016 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Tutorial of the usage of pyafai with simcx. Implementation of random walkers.

"""

from __future__ import division
import simcx
import pyafai
import numpy as np
import random

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


class RandomWalker(pyafai.Agent):
    def __init__(self, x=0, y=0, vel=50, angle=0, color=('c3B', (200, 0, 0)),
                 size=10):
        super(RandomWalker, self).__init__()

        obj = pyafai.objects.SimplePhysicsObject(x, y, angle)
        shape = pyafai.shapes.Triangle(0, -size, size*2, 0, 0, size,
                                       color=color)
        obj.add_shape(shape)
        obj.velocity = vel
        self.body = obj
        self._last_think = 0.0

    def _think(self, delta):
        self._last_think += delta
        if self._last_think >= 0.2:
            self._last_think = 0
            rotate = np.random.choice((-180, 0, 180))
            self.body.ang_velocity = rotate

        return []


def setup(n, width=800, height=600):

    world = pyafai.World2D(width, height)
    sim = simcx.PyafaiSimulator(world)
    vis = simcx.PyafaiVisual(sim)
    display = simcx.Display(width, height)

    display.add_simulator(sim)
    display.add_visual(vis)

    # Create agents.
    x = np.random.randint(10, width-10, n)
    y = np.random.randint(10, height-10, n)
    speed = np.random.randint(50, 100, n)
    angle = np.random.randint(0, 359, n)
    for i in range(n):
        ag = RandomWalker(x[i], y[i],
                          speed[i],
                          angle[i],
                          ('c3B', (random.randint(0,255),
                                    random.randint(0,255),
                                    random.randint(0,255))),
                          5)
        world.add_agent(ag)


if __name__ == '__main__':
    setup(50)
    simcx.run()