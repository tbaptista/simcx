# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Basic example of the use of the simcx framework to plot trajectories of 1D
dynamic systems.

"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

# Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1,'..')

import simcx


def sqrt(x):
    return x**0.5

if __name__ == '__main__':
    sim = simcx.Trajectory(sqrt, [0.2, 0.8, 1, 1.2, 1.8, 2, 3, 4], '$\sqrt{x}$',
                           grid=True)
    sim2 = simcx.TrajectoryDiff(sqrt, 0.2, 4, '$\sqrt{x}$', grid=True)
    display = simcx.Display()
    display.add_simulator(sim, 0, 500)
    display.add_simulator(sim2)
    simcx.run()
