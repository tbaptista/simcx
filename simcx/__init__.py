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
import numpy as np

try:
    from io import BytesIO as StringIO
except ImportError:
    from cStringIO import StringIO

# Try to import the pyglet package
try:
    import pyglet
    from pyglet.window import key
except ImportError:
    print("Please install the pyglet package!")
    exit(1)


class Simulator(object):
    def __init__(self, width=800, height=600):
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
    def __init__(self, sim_type, *args, **kwargs):
        self.sim_type = sim_type
        self.args = args
        self.sim = sim_type(*args, **kwargs)
        super().__init__(self.sim.width, self.sim.height,
                         caption = 'Complex Systems (paused)')

        self.paused = True
        self.update_delta = 1 / 10.0
        self.show_fps = False
        self.fps_display = pyglet.clock.ClockDisplay()

        self._create_canvas()

    def _create_canvas(self):
        self._canvas = FigureCanvas(self.sim.figure)
        data = StringIO()
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

        #show fps
        if self.show_fps:
            self.fps_display.draw()

    def _draw_gui(self):
        pass

    def _draw_plot(self):
        self.image.blit(0,0)

    def _update_image(self):
        self.sim.draw()
        data = StringIO()
        self._canvas.print_raw(data, dpi=self.sim.dpi)
        self.image.set_data('RGBA', -4 * self.sim.width, data.getvalue())

    def _step_simulation(self, delta = None):
        self.sim.step()
        self._update_image()

    def _reset_simulation(self):
        self.sim = self.sim_type(*self.args)
        self._create_canvas()

    def _start_simulation(self):
        pyglet.clock.schedule_interval(self._step_simulation, self.update_delta)

    def _pause_simulation(self):
        pyglet.clock.unschedule(self._step_simulation)

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)

        if symbol == key.S:
            if self.paused:
                self._step_simulation()

        elif symbol == key.R:
            if self.paused:
                self._reset_simulation()

        elif symbol == key.SPACE:
            if self.paused:
                self._start_simulation()
                self.paused = False
                self.set_caption(self.caption.replace(" (paused)", ""))
            else:
                self._pause_simulation()
                self.paused = True
                self.set_caption(self.caption + " (paused)")


def run():
    pyglet.app.run()


class Trajectory(Simulator):
    """ Class to build and display the trajectory of a 1D, linear, first-order.
    autonomous system."""

    def __init__(self, func, initial_states, func_string='', grid=False):
        super(Trajectory, self).__init__()

        self._state = [x for x in initial_states]
        self._func = func
        self._trajectories = [[x] for x in initial_states]
        self._time = [0]

        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Trajectory ' + func_string)
        self.ax.set_xlabel('Time $t$')
        self.ax.set_ylabel('$x_t$')
        self._lines = []
        for i in range(len(self._trajectories)):
            line, = self.ax.plot(self._time, self._trajectories[i],
                                 label=str(self._state[i]))
            self._lines.append(line)

        self.ax.legend()

        if grid:
            self.ax.grid()


    def step(self):
        for i in range(len(self._state)):
            self._state[i] = self._func(self._state[i])
            self._trajectories[i].append(self._state[i])

        self._time.append(self._time[-1] + 1)

    def draw(self):
        for i in range(len(self._lines)):
            self._lines[i].set_data(self._time, self._trajectories[i])
        self.ax.relim()
        self.ax.autoscale_view()


class Cobweb(Simulator):
    """ Class to build and display the cobwed diagram of a 1D system."""

    def __init__(self, func, initial_states, min, max, func_string='',
                 legend = True):
        super(Cobweb, self).__init__()

        self._func = func
        self._t = 0
        self._states = [x for x in initial_states]
        self._cobx = [[x, x] for x in initial_states]
        self._coby = [[0, self._func(x)] for x in initial_states]
        self._x = np.linspace(min, max, 1000)
        func_vec = np.vectorize(self._func)
        self._y = func_vec(self._x)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('t = 0')
        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$f(x)$')

        # PLot function
        self.ax.plot(self._x, self._y, label='$f(x)=$' + func_string)

        # Plot f(x) = x
        self.ax.plot(self._x, self._x, ':k', label='$f(x)=x$')

        # Create initial cobweb plots
        self._cobweb_lines = []
        for i in range(len(initial_states)):
            line, = self.ax.plot(self._cobx[i], self._coby[i], label='$x_0=' + str(self._states[i]) + '$')
            self._cobweb_lines.append(line)
            self._states[i] = self._func(self._states[i])

        if legend:
            self.ax.legend()

    def step(self):
        for i in range(len(self._states)):
            self._cobx[i].append(self._states[i])
            self._coby[i].append(self._states[i])
            self._cobx[i].append(self._states[i])
            self._states[i] = self._func(self._states[i])
            self._coby[i].append(self._states[i])

        self._t += 1

    def draw(self):
        for i in range(len(self._cobweb_lines)):
            self._cobweb_lines[i].set_data(self._cobx[i], self._coby[i])

        self.ax.set_title('t = ' + str(self._t))

