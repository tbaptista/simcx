Introductory Tutorial
=====================

In this first contact with the SimCX framework, we will walk you through its
basic components and create an example project in that process.

The framework has been mainly developed as a tool to teach complex systems. As
such, a lot of the design decisions are biased towards that purpose. Most of
the examples have also that bias.

In SimCX there are three base components (implemented as python classes): The
**Simulator** that implements the simulation core, the **Visual** that is used
to show the state of a simulator, and the **Display** that controls one
application window and can contain several visuals. We then provide, in two
submodules, several specific implementations of simulators and visuals. You can
use these, or create your own simulators and visuals, by deriving the base
classes.

The framework is generic in the sense that we can use several modelling and
simulation paradigms, like difference equations, diferential equations, or 
agent-based modelling. In this first tutorial we will focus on using difference
equations to simulate a dynamical system. 


Installation
____________

Before we start, we need to install SimCX and all its dependencies. Be aware
that the framework has been developed for Python 3, and mainly tested on that
version. Nevertheless, we make an effort to make it compatible with Python 2.

SimCX is available from the PyPI repository. To install, on a terminal (Command
Prompt on Windows), execute the following command:

.. code-block:: bash

    $ pip install simcx

That command will install SimCX and all its dependencies. Make sure that the pip
command you are running is from the Python version you wish to install the
framework on. On Windows, the pip command may not be on the system path. In that
case you will need to provide the full path to the pip executable, or navigate
to its directory before executing.


Model Description
_________________

TBD.


Implementing the Model
______________________

TBD.


Running
_______

TBD.
