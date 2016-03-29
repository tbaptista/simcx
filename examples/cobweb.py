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
import simcx

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


def sqrt(x):
    return x**0.5

if __name__ == '__main__':
    sim_sqrt = simcx.simulators.FunctionIterator(sqrt, [0.2, 2])
    cobweb = simcx.visuals.CobWebVisual(sim_sqrt, 0, 2.5, '$\sqrt{x}$',
                                        width=800, height=400)

    display = simcx.Display()
    display.add_simulator(sim_sqrt)
    display.add_visual(cobweb)
    simcx.run()
