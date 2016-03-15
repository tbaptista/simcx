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
from simcx import Simulator

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


class FunctionIterator(Simulator):
    def __init__(self, func, initial_states: list):
        super(FunctionIterator, self).__init__()
        self._state = [state for state in initial_states]
        self.func = func
        self.x = [0]
        self.y = [[state] for state in initial_states]

    def step(self, delta=0):
        for i in range(len(self._state)):
            self._state[i] = self.func(self._state[i])
            self.y[i].append(self._state[i])
        self.x.append(self.x[-1] + 1)
