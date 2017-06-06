# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2016-2017 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Compute and display the Julia Set of the function f(z) = z^2 + c.

"""

from __future__ import division
import simcx


__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


if __name__ == '__main__':
    c = -1

    sim = simcx.simulators.JuliaSet(c, samples=500, iterations=80)
    vis = simcx.visuals.FractalVisual(sim, gamma=1.0, cmap='hot',
                                      width=500, height=500)

    display = simcx.Display()
    display.add_simulator(sim)
    display.add_visual(vis)

    simcx.run()
