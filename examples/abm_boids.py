# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Implementation of boids using pyafai and simcx.

"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

# Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1,'..')


import pyafai
import numpy as np
from scipy.spatial import cKDTree
import math
import random
import simcx


RAD2DEG = 180.0 / math.pi

class BoidBody(pyafai.Object):
    def __init__(self, x, y, angle):
        self.pos = np.zeros(2)
        super(BoidBody, self).__init__(x, y, angle)

        self._vel = np.zeros(2)
        self._max_vel = 200.0

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos[0] = value

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos[1] = value

    @property
    def velocity(self):
        return self._vel

    @velocity.setter
    def velocity(self, v: np.ndarray):
        norm = np.linalg.norm(v)
        if norm > self._max_vel:
            self._vel[:] = v / norm * self._max_vel
        else:
            self._vel[:] = v

        self.angle = math.atan2(self._vel[1], self._vel[0]) * RAD2DEG

    def update(self, delta):
        self.pos += self._vel * delta


class Boid(pyafai.Agent):
    def __init__(self, x, y, angle, size=8, radius=50, color=('c3B', (200, 0, 0))):
        super(Boid, self).__init__()

        # Create body
        triangle = pyafai.shapes.Triangle(-size/2, -size/2, -size/2, size/2, size, 0, color=color)
        self.body = BoidBody(x, y, angle)
        self.body.add_shape(triangle)

        self.radius = radius
        self.size = size

    def _think(self, delta):
        neighbours = self.world.get_neighbours(self, self.radius)

        # Separation
        s = np.zeros(2)
        for ag in neighbours:
            v = self.body.pos - ag.body.pos
            d = np.linalg.norm(v)
            if 0 < d < self.size*3:
                v /= d**2
                s += v * self.size**2

        # Alignment
        a = np.zeros(2)
        if neighbours:
            for ag in neighbours:
                a += ag.body.velocity

            a /= len(neighbours)
            a -= self.body.velocity

        # Cohesion
        c = np.zeros(2)
        if neighbours:
            for ag in neighbours:
                if ag is not self:
                    c += ag.body.pos

            c /= len(neighbours)
            c -= self.body.pos

        # Target
        t = self.world.target - self.body.pos

        self.body.velocity += c * 0.005 + a * 0.01 + s * 1 + t * 0.005


class BoidsWorld(pyafai.World):
    def __init__(self):
        super(BoidsWorld, self).__init__()

        self.kdt = None
        self._target = np.array([250.0, 250.0])

        self._target_shape = pyafai.shapes.Rect(10, 10, self.target[0], self.target[1])
        self._target_shape.add_to_batch(self._batch)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, v):
        move = v - self._target
        self._target[:] = v
        self._target_shape.vertexlist.vertices[:] = self._target_shape.translate(move[0], move[1])

    def update(self, delta):
        pos = np.array([[a.body.x, a.body.y] for a in self._agents])
        self.kdt = cKDTree(pos)

        super(BoidsWorld, self).update(delta)

    def get_neighbours(self, agent, size):
        indices = self.kdt.query_ball_point((agent.body.x, agent.body.y), size)
        return [self._agents[i] for i in indices if agent is not self._agents[i]]

    def get_agents(self):
        return self._agents



def setup(n):
    world = BoidsWorld()
    world.target = [400.0, 300.0]

    for i in range(n//2):
        agent = Boid(random.randint(-100, 0), random.randint(-100, 0), 0, radius=100)
        agent.body.velocity = np.random.uniform(10, 20, 2)
        world.add_agent(agent)

    for i in range(n//2):
        agent = Boid(random.randint(900, 1000), random.randint(-100, 0), 0, color=('c3B', (0, 0, 200)), radius=50)
        agent.body.velocity = np.random.uniform(-10, -20, 2)
        world.add_agent(agent)

    sim = simcx.PyafaiSimulator(world, width=800, height=600)

    display = simcx.Display(800, 600, interval=0.016)
    display.add_simulator(sim)

if __name__ == '__main__':
    setup(50)
    simcx.run()