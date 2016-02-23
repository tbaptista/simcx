# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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

    def step(self, dt):
        for i in range(self.n):
            self.x[i] += np.random.normal(0, self.sd)
            self.y[i] += np.random.normal(0, self.sd)

    def reset(self):
        # generate initial positions
        self.x = np.random.normal(0, 1, self.n)
        self.y = np.random.normal(0, 1, self.n)


class PointsVisual(simcx.MplVisual):
    def __init__(self, sim: RandomParticles):
        super(PointsVisual, self).__init__(sim)

        # create initial plot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(-4, 4)
        self.l, = self.ax.plot(self.sim.x, self.sim.y, '.')

    def draw(self):
        self.l.set_data(self.sim.x, self.sim.y)


if __name__ == '__main__':
    sim = RandomParticles()
    vis = PointsVisual(sim)
    display = simcx.Display()
    display.add_simulator(sim)
    display.add_visual(vis)

    # record the simulation on video
    display.start_recording('random.mp4')

    simcx.run()
