# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2016 Tiago Baptista
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
This module provides several ready-made visual classes. Used mainly for the
examples given in the Complex Systems course. In this current version, these
should not be considered stable in terms of API.

"""

from __future__ import division
from . import MplVisual, Simulator
from .simulators import FunctionIterator
import numpy as np

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


class LineVisual(MplVisual):
    def __init__(self, sim: Simulator, **kwargs):
        super(LineVisual, self).__init__(sim, **kwargs)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(-10,10)
        self.ax.set_ylim(-10,10)
        self.l, = self.ax.plot(self.sim.x, self.sim.y)

    def draw(self):
        self.l.set_data(self.sim.x, self.sim.y)


class LinesVisual(MplVisual):
    def __init__(self, sim: Simulator, **kwargs):
        super(LinesVisual, self).__init__(sim, **kwargs)

        self.ax = self.figure.add_subplot(111)
        self._lines = []
        for i in range(len(self.sim.y)):
            line, = self.ax.plot(self.sim.x, self.sim.y[i])
            self._lines.append(line)

    def draw(self):
        for i in range(len(self._lines)):
            self._lines[i].set_data(self.sim.x, self.sim.y[i])
        self.ax.relim()
        self.ax.autoscale_view()


class CobWebVisual(MplVisual):
    def __init__(self, sim: FunctionIterator, minx, maxx, func_string='',
                 **kwargs):
        super(CobWebVisual, self).__init__(sim, **kwargs)

        self.ax = self.figure.add_subplot(111)

        # PLot function
        x = np.linspace(minx, maxx, 1000)
        func_vec = np.vectorize(self.sim.func)
        y = func_vec(x)
        self.ax.plot(x, y, label='$f(x)=$' + func_string)

        # Plot f(x) = x
        self.ax.plot(x, x, ':k', label='$f(x)=x$')

        # Create initial cobweb plots
        self._cobx = [[x[0]] for x in self.sim.y]
        self._coby = [[0] for x in self.sim.y]
        self._cobweb_lines = []
        for i in range(len(self.sim.y)):
            line, = self.ax.plot(self._cobx[i], self._coby[i],
                                 label='$x_0=' + str(self.sim.y[i][0]) + '$')
            self._cobweb_lines.append(line)

    def draw(self):
        for i in range(len(self._cobweb_lines)):
            self._cobx[i].append(self.sim.y[i][-2])
            self._coby[i].append(self.sim.y[i][-2])
            self._cobx[i].append(self.sim.y[i][-2])
            self._coby[i].append(self.sim.y[i][-1])

            self._cobweb_lines[i].set_data(self._cobx[i], self._coby[i])


class FinalStateDiagram(MplVisual):
    def __init__(self, sim: FunctionIterator, discard_initial=1000, **kwargs):
        super(FinalStateDiagram, self).__init__(sim, **kwargs)

        self._discard_initial = discard_initial
        self._seeds = [y[0] for y in self.sim.y]

        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Final State Diagram')
        xmin = min([y[0] for y in self.sim.y])
        xmax = max([y[0] for y in self.sim.y])
        self.ax.set_xlim(xmin - 0.5, xmax + 0.5)
        self.ax.set_xlabel('$t={}$'.format(self.sim.time))
        self.ax.set_ylabel('Final Value(s)')

    def draw(self):
        self.ax.set_xlabel('$t={}$'.format(self.sim.time))
        if self.sim.time >= self._discard_initial:
            for i in range(len(self.sim.y)):
                self.ax.scatter([self._seeds[i]], self.sim.y[i][-1:], c='black')
