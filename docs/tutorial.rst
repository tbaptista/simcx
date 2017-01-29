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

In this tutorial we will use SimCX to model population growth using difference
equations. We will use an example taken from Hiroki Sayama's book Introduction
to the Modeling and Analysis of Complex Systems [1]. To start we will model a
population with exponential growth, using the following equation:

.. math::
    x_t = a x_{t-1}

Here, :math:`x_t` is the population size at time step :math:`t`, :math:`x_{t-1}`
is the population size at time step :math:`t-1`, and :math:`a` is the growth
ratio of the population per time step. This simple model will give us an
unbounded exponential growth of the population, which is not very life like. We
can thus consider adding a bound to the size of the population, using the
following equation:

.. math::
    x_t = x_{t-1} + r x_{t-1} \left(1 - \frac{x_{t-1}}{K} \right)

We have introduced a new parameter :math:`K` that represents the carrying
capacity of the environment. Also, we have made the following substitution
:math:`r=a-1`. To get more details on the mathematical modelling and derivation
of these equations, refer to [1].



Implementing the Model
______________________




Running
_______

TBD.
