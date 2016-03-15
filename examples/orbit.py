# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2016 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Basic example of the use of the simcx framework to plot the orbit of 1D
dynamical systems.

"""

from __future__ import division
import simcx

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


def sqrt(x):
    return x**0.5

if __name__ == '__main__':

    sim_sqrt = simcx.simulators.FunctionIterator(sqrt, [0.2, 0.8, 1.0, 1.2, 1.8, 2, 3, 4])
    vis = simcx.visuals.LinesVisual(sim_sqrt)

    display = simcx.Display()
    display.add_simulator(sim_sqrt)
    display.add_visual(vis)

    simcx.run()
