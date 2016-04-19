# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2016 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Basic example of the use of the simcx framework to draw fractals using Random
Iterated Function Systems.

"""

from __future__ import division
import simcx
from matplotlib.transforms import Affine2D


__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


def sierpinski_triangle():
    t1 = Affine2D().scale(1/2, 1/2)
    t2 = Affine2D().scale(1/2, 1/2).translate(1/2, 0)
    t3 = Affine2D().scale(1/2, 1/2).translate(1/4, 3**0.5/4)

    s1 = s2 = s3 = 1/3

    return [t1, t2, t3], [s1, s2, s3]


if __name__ == '__main__':
    transform, probs = sierpinski_triangle()

    sim = simcx.simulators.IFS(transform, probs, step_size=100)
    vis = simcx.visuals.Points2D(sim)

    display = simcx.Display()
    display.add_simulator(sim)
    display.add_visual(vis)
    simcx.run()
