# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015-2016 Tiago Baptista
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

"""
A simulation framework for complex systems modeling and analysis.
"""

from __future__ import division
from .__version__ import __version__

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import animation
from matplotlib import verbose
import pyglet

try:
    from io import BytesIO as StringIO
except ImportError:
    from cStringIO import StringIO

__docformat__ = 'restructuredtext'
__author__ = 'Tiago Baptista'


class Simulator(object):
    def __init__(self):
        self.dirty = True

    def step(self, delta=0):
        assert False, "Not implemented!"

    def reset(self):
        assert False, "Not implemented!"


class PyafaiSimulator(Simulator):
    def __init__(self, world):
        super(PyafaiSimulator, self).__init__()

        self.world = world
        self.world.paused = False
        pyglet.clock.unschedule(self.world._start_schedule)

    def step(self, delta=0):
        self.world.update(delta)


class Visual(object):
    def __init__(self, sim: Simulator, **kwargs):
        self.width = kwargs.get('width', 500)
        self.height = kwargs.get('height', 500)
        self.sim = sim

    def draw(self):
        assert False, "Not implemented!"


class MplVisual(Visual):
    def __init__(self, sim: Simulator, **kwargs):
        super(MplVisual, self).__init__(sim, width=kwargs.get('width', 500),
                                        height=kwargs.get('height', 500))

        self.dpi = 80
        self.figure = plt.figure(figsize=(self.width/self.dpi,
                                          self.height/self.dpi),
                                 dpi=self.dpi)
        self._create_canvas()

    def _create_canvas(self):
        self.canvas = FigureCanvas(self.figure)
        data = StringIO()
        self.canvas.print_raw(data, dpi=self.dpi)
        self.image = pyglet.image.ImageData(self.width, self.height,
                                            'RGBA', data.getvalue(),
                                            -4 * self.width)

    def update_image(self):
        data = StringIO()
        self.canvas.print_raw(data, dpi=self.dpi)
        self.image.set_data('RGBA', -4 * self.width, data.getvalue())


class PyafaiVisual(Visual):
    def __init__(self, sim: PyafaiSimulator, width=500, height=500):
        self.world = sim.world

        if hasattr(self.world, 'width'):
            width = self.world.width

        if hasattr(self.world, 'height'):
            height = self.world.height

        super(PyafaiVisual, self).__init__(sim, width, height)

    def draw(self):
        self.world.draw()
        self.world.draw_objects()


class Display(pyglet.window.Window):
    def __init__(self, width=500, height=500, interval=0.05, multi_sampling=True, **kwargs):
        if multi_sampling:
            # Enable multi sampling if available on the hardware
            platform = pyglet.window.get_platform()
            display = platform.get_default_display()
            screen = display.get_default_screen()
            template = pyglet.gl.Config(sample_buffers=1, samples=4,
                                        double_buffer=True)
            try:
                config = screen.get_best_config(template)
            except pyglet.window.NoSuchConfigException:
                template = pyglet.gl.Config()
                config = screen.get_best_config(template)

            super(Display, self).__init__(width, height, 'Complex Systems (paused)', config=config, **kwargs)
        else:
            super(Display, self).__init__(width, height, caption='Complex Systems (paused)', **kwargs)

        self.paused = True
        self.show_fps = False
        self.real_time = True
        self._recording = False
        self._movie_writer = None
        self._interval = interval
        self._sims = []
        self._visuals = []
        self._pos = []

        self._fps_display = pyglet.clock.ClockDisplay()

        pyglet.clock.schedule_interval(self._update, self._interval)

    def add_simulator(self, sim: Simulator):
        if sim not in self._sims:
            self._sims.append(sim)

    def add_visual(self, visual: Visual, x=0, y=0):
        if visual not in self._visuals:
            self._visuals.append(visual)
            self._pos.append((x, y))
            self._resize_window()

            if isinstance(visual, MplVisual):
                visual.update_image()

    def start_recording(self, filename, fps=None, bitrate=1800):
        if self._movie_writer is None:
            if fps is None:
                fps = 1 // self._interval

            self._movie_writer = FFMpegWriter(fps=fps, bitrate=bitrate)
            self._movie_writer.setup(self, filename)
            self._recording = True
            print("Recording started...")
        else:
            print("A movie is already being recorded for this Display.")

    def on_draw(self):
        # clear window
        self.clear()

        # draw visuals
        for i in range(len(self._visuals)):
            vis = self._visuals[i]
            if isinstance(vis, MplVisual):
                vis.image.blit(*self._pos[i])
            else:
                pyglet.gl.glPushMatrix()
                pyglet.gl.glTranslatef(self._pos[i][0], self._pos[i][1], 0)
                vis.draw()
                pyglet.gl.glPopMatrix()

        # show fps
        if self.show_fps:
            self._fps_display.draw()

    def on_close(self):
        if self._movie_writer is not None:
            self._movie_writer.finish()

        super(Display, self).on_close()

    def on_key_press(self, symbol, modifiers):
        super(Display, self).on_key_press(symbol, modifiers)

        if symbol == pyglet.window.key.S:
            if self.paused:
                self._step_simulation(self._interval)

        elif symbol == pyglet.window.key.R:
            if pyglet.window.key.MOD_ALT & modifiers:
                self.start_recording(self._movie_filename)
            else:
                if self.paused:
                    self._reset_simulation()

        elif symbol == pyglet.window.key.SPACE:
            if self.paused:
                self.paused = False
                self.set_caption(self.caption.replace(" (paused)", ""))
            else:
                self.paused = True
                self.set_caption(self.caption + " (paused)")
        elif symbol == pyglet.window.key.F:
            self.show_fps = not self.show_fps

    def _draw_gui(self):
        pass

    def _update(self, dt):
        if not self.paused:
            self._step_simulation(dt)

    def _step_simulation(self, dt=None):
        if self._recording:
            self._movie_writer.grab_frame()

        if not self.real_time:
            dt = self._interval

        for sim in self._sims:
            sim.step(dt)

        for vis in self._visuals:
            if isinstance(vis, MplVisual):
                vis.draw()
                vis.update_image()

    def _reset_simulation(self):
        for sim in self._sims:
            sim.reset()

        for vis in self._visuals:
            if isinstance(vis, MplVisual):
                vis.draw()
                vis.update_image()

    def _resize_window(self):
        max_x = 0
        max_y = 0
        for i in range(len(self._visuals)):
            if self._pos[i][0] + self._visuals[i].width > max_x:
                max_x = self._pos[i][0] + self._visuals[i].width
            if self._pos[i][1] + self._visuals[i].height > max_y:
                max_y = self._pos[i][1] + self._visuals[i].height

        if max_x != self.width or max_y != self.height:
            self.set_size(max_x, max_y)
            self.clear()


class FFMpegWriter(animation.FFMpegWriter):
    @property
    def frame_size(self):
        """A tuple (width,height) in pixels of a movie frame."""
        return self.display.width, self.display.height

    def setup(self, display, outfile):
        """
        Perform setup for writing the movie file.
        display: `simcx.Display` instance
            The Display instance whose framebuffer we want to use.
        outfile: string
            The filename of the resulting movie file
        """
        self.outfile = outfile
        self.display = display

        # Run here so that grab_frame() can write the data to a pipe. This
        # eliminates the need for temp files.
        self._run()

    def grab_frame(self, **savefig_kwargs):
        """
        Grab the image information from the display and save as a movie frame.
        The keyword arguments are not being used in the subclass.
        """
        verbose.report('MovieWriter.grab_frame: Grabbing frame.',
                       level='debug')
        try:
            image = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
            self._frame_sink().write(image.get_data('RGBA', -4 * self.display.width))

        except RuntimeError:
            out, err = self._proc.communicate()
            verbose.report('MovieWriter -- Error '
                           'running proc:\n%s\n%s' % (out,
                                                      err), level='helpful')
            raise


def run():
    pyglet.app.run()

# import sub-modules
from . import simulators
from . import visuals


