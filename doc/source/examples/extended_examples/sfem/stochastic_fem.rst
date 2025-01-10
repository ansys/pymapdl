.. _stochastic_fem_example:

Stochastic finite element method with PyMAPDL
=============================================

This example leverages PyMAPDL for stochastic finite element analysis via the Monte Carlo simulation.
Numerous advantages / workflow possibilities that PyMAPDL affords users is demonstrated through this
extended example. Important concepts are first explained before the example is presented.

Introduction
------------
Often in a mechanical system, system parameters (geometry, materials, loads, etc.) and response parameters
(displacement, strain, stress, etc) are taken to be deterministic. This simplification, while sufficient for a
wide range of engineering applications, results in a crude approximation of actual system behaviour.

To obtain a more accurate representation of a physical system, it is essential to consider the randomness
in system parameters and loading conditions, along with the uncertainty in their estimation and their
spatial variability. The finite element method is undoubtedly the most widely used tool for solving deterministic
physical problems today and to account for randomness and uncertainty in the modeling of engineering systems,
the stochastic finite element method (SFEM) was introduced.

The stochastic finite element method (SFEM) extends the classical deterministic finite element approach
to a stochastic framework, offering various techniques for calculating response variability. Among these,
the Monte Carlo simulation (MCS) stands out as the most prominent method. Renowned for its versatility and
ease of implementation, MCS can be applied to virtually any type of problem in stochastic analysis.

Random variables vs stochastic processes
----------------------------------------
A distinction between random variables and stochastic processes (also called random fields) is attempted in this
section. Explaining these concepts is important since they are used for modelling the system randomness.
Random variables are easier to understand from elementary probability theory, the same cannot be said for stochastic
processes. Readers are advised to consult books on SFEM if the explanation here seems to brief.

Random variables
~~~~~~~~~~~~~~~~
Imagine a beam with a concentrated load :math:`P` applied at a specific point on the beam. The value of :math:`P`
is uncertain — it could vary due to manufacturing tolerances, loading conditions, or measurement errors. Mathematically,
:math:`P` is a random variable:

.. math:: P : \Omega \longrightarrow \mathbb{R}