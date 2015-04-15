# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Basic example of the use of the simcx framework to plot cobweb diagrams. Also
shows how to add several Simulator instances to the same Display.
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
    sim = simcx.Cobweb(sqrt, [0.2, 2], 0, 2.5, '$\sqrt{x}$', width=800,
                       height=400)
    sim2 = simcx.Trajectory(sqrt, [0.2, 2], '$\sqrt{x}$', width=800,
                            height=400)
    display = simcx.Display()
    display.add_simulator(sim)
    display.add_simulator(sim2, 0, 400)
    simcx.run()
