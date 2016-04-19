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
This module provides several ready-made simulator classes. Used mainly for the
examples given in the Complex Systems course. In this current version, these
should *not* be considered stable in terms of API.

"""

from __future__ import division
from simcx import Simulator
import numpy as np

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


class FunctionIterator(Simulator):
    def __init__(self, func, initial_states):
        super(FunctionIterator, self).__init__()
        self._state = [state for state in initial_states]
        self._n_states = len(self._state)
        self.func = func
        self.time = 0
        self.x = [0]
        self.y = [[state] for state in initial_states]

    def step(self, delta=0):
        self.time += 1
        for i in range(self._n_states):
            self._state[i] = self.func(self._state[i])
            self.y[i].append(self._state[i])
        self.x.append(self.time)


class FunctionIterator2D(Simulator):
    def __init__(self, func, initial_state):
        super(FunctionIterator2D, self).__init__()

        self._func = func
        self._state = initial_state
        self.time = 0
        self.x = [0]
        self.y = [[initial_state[0]], [initial_state[1]]]

    def step(self, delta=0):
        self.time += 1
        self._state = self._func(*self._state)
        self.x.append(self.time)
        self.y[0].append(self._state[0])
        self.y[1].append(self._state[1])


class FinalStateIterator(Simulator):
    def __init__(self, func, seed, start, end, discard=1000, samples=250,
                 delta=0.01):
        super(FinalStateIterator, self).__init__()

        self._func = func
        self._seed = seed
        self._a = start
        self.start = start
        self.end = end
        self._discard = discard
        self._samples = samples
        self._delta = delta

        self.x = self.y = np.zeros(self._samples)
        self.y = self.y = np.zeros(self._samples)

    def step(self, delta=0):
        if self._a <= self.end:
            x = self._seed
            for i in range(self._discard):
                x = self._func(self._a, x)
            for i in range(self._samples):
                x = self._func(self._a, x)
                self.y[i] = x

            self.x = np.zeros(self._samples)
            self.x += self._a
            self._a += self._delta


class IFS(Simulator):
    """An Iterated Function Systems simulator using the Chaos Game."""

    def __init__(self, transforms, probs, step_size=100):
        super(IFS, self).__init__()

        self._discard = 10
        self._step_size = step_size
        self._transforms = transforms[:]
        self._n = len(transforms)
        self._probs = probs[:]

        self._point = np.array([0.0, 0.0], dtype=np.float64)
        self.draw_points = []

        for i in range(self._discard):
            self.step(0, discard=True)

    def _get_random_transform(self):
        i = np.random.choice(self._n, p=self._probs)
        return self._transforms[i]

    def step(self, delta=0, discard=False):
        for _ in range(self._step_size):
            transform = self._get_random_transform()
            self._point = transform.transform_point(self._point)
            if not discard:
                self.draw_points.append(self._point)