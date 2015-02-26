#coding: utf-8
#-----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
#-----------------------------------------------------------------------------

"""
A simulation framework for complex systems modeling and analysis
"""

from __future__ import division
from .__version__ import __version__

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io


#Try to import the pyglet package
try:
    import pyglet
    from pyglet.window import key
except ImportError:
    print("Please install the pyglet package!")
    exit(1)

class Simulator(object):

    def __init__(self, width = 800, height = 600):
        self.width = width
        self.height = height
        self.dpi = 80
        self.step_size = 1.0
        self.figure = plt.figure(figsize=(width/self.dpi, height/self.dpi), dpi=self.dpi)

    def step(self):
        pass

    def draw(self):
        pass


class Display(pyglet.window.Window):
    def __init__(self, sim_type, *args):
        self.sim_type = sim_type
        self.args = args
        self.sim = sim_type(*args)
        super().__init__(self.sim.width, self.sim.height,
                         caption = 'Complex Systems')
        self._create_canvas()

    def _create_canvas(self):
        self._canvas = FigureCanvas(self.sim.figure)
        data = io.BytesIO()
        self._canvas.print_raw(data, dpi=self.sim.dpi)
        self.image = pyglet.image.ImageData(self.sim.width, self.sim.height,
                                            'RGBA', data.getvalue(),
                                            -4 * self.sim.width)

    def on_draw(self):
        #clear window
        self.clear()

        #draw simulator
        self._draw_plot()

        #draw gui
        self._draw_gui()

    def _draw_gui(self):
        pass

    def _draw_plot(self):
        self.image.blit(0,0)

    def _update_image(self):
        self.sim.draw()
        data = io.BytesIO()
        self._canvas.print_raw(data, dpi=self.sim.dpi)
        self.image.set_data('RGBA', -4 * self.sim.width, data.getvalue())

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)

        if symbol == key.S:
            self.sim.step()
            self._update_image()

        elif symbol == key.R:
            self.sim = self.sim_type(*self.args)
            self._create_canvas()

def run():
    pyglet.app.run()


