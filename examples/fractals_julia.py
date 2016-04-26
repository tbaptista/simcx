# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2016 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Compute and display the Julia Set of the function f(z) = z^2 + c.

"""

from __future__ import division
import simcx
from matplotlib.transforms import Affine2D


__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


if __name__ == '__main__':
    sim = simcx.simulators.JuliaSet(-1, samples=1000, iterations=100)
    vis = simcx.visuals.Points2D(sim, -2., 2., -2., 2., width=1000, height=1000)

    display = simcx.Display()
    display.add_simulator(sim)
    display.add_visual(vis)

    simcx.run()
