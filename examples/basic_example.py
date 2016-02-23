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
        self.f = lambda x: x
        self.x = []
        self.y = []

    def step(self, dt):
        if self.next_x <= self.end_x:
            x = self.next_x
            self.next_x += self.step_size
            self.x.append(x)
            self.y.append(self.f(x))

    def reset(self):
        self.x = []
        self.y = []


class PlotVisual(simcx.MplVisual):
    def __init__(self, sim: SimpleFunction):
        super(PlotVisual, self).__init__(sim)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(-10,10)
        self.ax.set_ylim(-10,10)
        self.l, = self.ax.plot(self.sim.x, self.sim.y)

    def draw(self):
        self.l.set_data(self.sim.x, self.sim.y)


if __name__ == '__main__':
    sim = SimpleFunction()
    vis = PlotVisual(sim)
    display = simcx.Display()
    display.add_simulator(sim)
    display.add_visual(vis)
    simcx.run()