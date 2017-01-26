# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2017 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Basic example of the use of the SimCX framework to plot the bifurcation diagram
of the logistic equation.

"""

from __future__ import division
import simcx
from math import sin,pi

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


def logistic(r, x):
    return r*x*(1-x)


if __name__ == '__main__':
    sim = simcx.simulators.FinalStateIterator(logistic, 0.1, 0.0, 4.0, delta=0.01)
    vis = simcx.visuals.BifurcationDiagram(sim, ymin=0, ymax=1)

    display = simcx.Display()
    display.add_simulator(sim)
    display.add_visual(vis)

    simcx.run()
