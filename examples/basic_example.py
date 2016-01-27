#coding: utf-8
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
        self.x = []
        self.f = lambda x: x
        self.y = []
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(-10,10)
        self.ax.set_ylim(-10,10)
        self.l, = self.ax.plot(self.x, self.y)

        self.update_image()

    def step(self, dt):
        if self.next_x <= self.end_x:
            x = self.next_x
            self.next_x += self.step_size
            self.x.append(x)
            self.y.append(self.f(x))

    def draw(self):
        self.l.set_data(self.x, self.y)


if __name__ == '__main__':
    sim = SimpleFunction()
    display = simcx.Display()
    display.add_simulator(sim)
    simcx.run()