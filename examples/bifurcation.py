# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Basic example of the use of the simcx framework to plot the bifurcation diagram
of the logistic equation.

"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

# Allow the import of the framework from one directory down the hierarchy
import sys
sys.path.insert(1,'..')

import simcx

if __name__ == '__main__':
    display = simcx.Display(simcx.BifurcationDiagram, 0.01)
    #display = simcx.Display(simcx.BifurcationDiagram, 0.01,
    #                        start_r=3.5, end_r=3.8, dr=0.001)
    simcx.run()
