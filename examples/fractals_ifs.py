# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Basic example of the use of the simcx framework to plot cobweb diagrams

"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

# Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1,'..')

import simcx
from matplotlib.transforms import Affine2D


def sierpinski_triangle():
    t1 = Affine2D().scale(1/2, 1/2)
    t2 = Affine2D().scale(1/2, 1/2).translate(1/2, 0)
    t3 = Affine2D().scale(1/2, 1/2).translate(1/4, 1/2)

    s1 = s2 = s3 = 1/3

    return [t1, t2, t3], [s1, s2, s3]


def koch_curve():
    t1 = Affine2D().scale(1/3, 1/3)
    t2 = Affine2D().scale(1/3, 1/3).rotate_deg(60).translate(1/3, 0)
    t3 = Affine2D().scale(1/3, 1/3).rotate_deg(-60).translate(1/2, 3**0.5/6)
    t4 = Affine2D().scale(1/3, 1/3).translate(2/3, 0)

    s1 = s2 = s3 = s4 = 1/4

    return [t1, t2, t3, t4], [s1, s2, s3, s4]

if __name__ == '__main__':
    transform, probs = sierpinski_triangle()
    #transform, probs = koch_curve()

    sim = simcx.IFS(transform, probs)

    display = simcx.Display()
    display.add_simulator(sim)
    simcx.run()
