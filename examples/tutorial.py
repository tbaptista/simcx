# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2017 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Example used on the introductory tutorial. Check the documentation at
http://simcx.readthedocs.io.

"""

import simcx
from simcx.simulators import FunctionIterator
from simcx.visuals import TimeSeries


def eq1(a):
    return lambda x: a*x


def eq2(r, K):
    return lambda x: x + r*x*(1 - (x / K))


if __name__ == '__main__':
    display = simcx.Display()

    a = 1.2
    x0 = [0, 10, 200, 1000]
    K = 1000
    sim = FunctionIterator(eq2(a - 1, K), x0)

    orbit = TimeSeries(sim)

    display.add_simulator(sim)
    display.add_visual(orbit)

    simcx.run()
