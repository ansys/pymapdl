.. _stochastic_fem_example:

Stochastic finite element method with PyMAPDL
=============================================

This example leverages PyMAPDL for stochastic finite element analysis via the Monte Carlo simulation.
Numerous advantages / workflow possibilities that PyMAPDL affords users is demonstrated through this
extended example. Important theoretical concepts are first explained before the example is presented.

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
A distinction between random variables and stochastic processes is attempted in this section. Explaining these
concepts is important since they are used for modelling the system randomness. Random variables are easier to
understand from elementary probability theory, the same cannot be said for stochastic processes. Readers are
advised to consult books on SFEM if the explanation here seems too brief.

Random variables
~~~~~~~~~~~~~~~~
**Definition:** A random variable is a rule for assigning to every possible outcome :math:`\theta` of an experiment a
number :math:`X(\theta)`. For notational convenience, the dependence on :math:`\theta` is usually dropped and the
random variable is written as :math:`X`.

Practical example
+++++++++++++++++
Imagine a beam with a concentrated load :math:`P` applied at a specific point. The value of :math:`P`
is uncertain—it could vary due to manufacturing tolerances, loading conditions, or measurement errors. Mathematically,
:math:`P` is a random variable:

.. math:: P : \Theta \longrightarrow \mathbb{R}

where :math:`\Theta` is the sample space of all possible loading scenarios, and :math:`\mathbb{R}` represents the set of
possible load magnitudes. For example, :math:`P` could be modeled as a random variable with a probability density
function (PDF) such as:

.. math:: f_P(p) = \frac{1}{\sqrt{2\pi\sigma^2}}e^{-\frac{(p-\mu)^2}{2\sigma^2}},

where :math:`\mu` is the mean load, and :math:`\sigma^2` is its variance.

Stochastic processes
~~~~~~~~~~~~~~~~~~~~
**Definition:**
recall that a random variable is defined as a rule that assigns a number :math:`X` to every outcome :math:`\theta`
of an experiment. However, in some applications, the experiment evolves with respect to a deterministic parameter :math:`t`,
which belongs to an interval :math:`I`. For example, this occurs in an engineering system subjected to random dynamic loads
over a time interval :math:`I \subseteq \mathbb{R}^+`. In such cases, the system's response at a specific material point is
described not by a single random variable but by a collection of random variables :math:`\{X(t)\}` indexed by :math:`t \in I`. 
This 'infinite' collection of random variables over the interval :math:`I` is called a stochastic process and is denoted as
:math:`\{X(t), t \in I\}` or simply :math:`X`. In this way, a stochastic process generalizes the concept of a random variable,
as it assigns to each outcome :math:`\theta` of the experiment a function :math:`X(t, \theta)`, known as a realization or sample
function. Lastly, if :math:`X` is indexed by some spatial coordinate :math:`s \in D \subseteq \mathbb{R}^n` rather than time :math:`t`,
then :math:`\{X(s), s \in D\}` is called a random field.

Practical example
+++++++++++++++++
Now, consider the material property of the beam, such as Young's modulus :math:`E(x)`, which may vary randomly along
the length of the beam :math:`x`.  Instead of being a single random value, :math:`E(x)` is a random field—its value
is uncertain at each point along the domain, and it changes continuously across the beam. Mathematically, :math:`E(x)`
is a random field:

.. math:: E(x) : x \in [0,L] \longrightarrow \mathbb{R}

Here:

* :math:`x` is the spatial coordinate along the length of the beam (:math:`x \in [0,L]`).
* :math:`E(x)` is a random variable at each point :math:`x`, and its randomness is described
  by a covariance function or an autocorrelation function.

For example, :math:`E(x)` could be a Gaussian random field, in which case it has the stationarity
property, making its statistics completely defined by its mean (:math:`\mu_E`), standard deviation
(:math:`\sigma_E`) and covariance function :math:`C_E(x_i,x_j)`. This 'stationarity' simply means
that the mean and standard deviation of every random variable :math:`E(x)` is constant and equal to
:math:`\mu_E` and :math:`\sigma_E` respectively. :math:`C_E(x_i,x_j)` describes how random variables
:math:`E(x_i)` and :math:`E(x_j)` are related. For a zero-mean Gaussian random field, the covariance function is given by:

.. math:: C_E(x_i,x_j) = \sigma_E^2e^{-\frac{\lvert x_i-x_j \rvert}{\ell}}

where :math:`\sigma_E^2` is the variance, and :math:`\ell` is the correlation length parameter.

To aid understanding, the figure below is a diagram depicting two equivalent ways of visualizing a
stochastic process / random field, that is, as an infinite collection of random variables or as a
realization/sample function assigned to each outcome of an experiment.

.. figure:: realizations.png

   A random field as a collection of random variables or realizations

.. note::
  The concepts above generalize to more dimensions, for example, a random vector instead of a random
  variable, or an :math:`\mathbb{R}^d`-valued stochastic process. The presentation above is however
  sufficient for this example.

Series expansion of stochastic processes
----------------------------------------
Since a stochastic process involves an infinite number of random variables, most engineering applications
involving stochastic processes will be mathematically and computationally intractable if there isn't a way of
approximating them with a series of a finite number of random variables. A series expansion method which will
be used in this example is explained next.

The Karhunen-Loève (K-L) series expansion for a Gaussian process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
More generally, the K-L expansion of any process is based on a spectral decomposition of its covariance function. Analytical
solutions are possible in a few cases, and such is the case of a Gaussian process.


For a zero-mean stationary Gaussian process, :math:`X(t)`, with covariance function
:math:`C_X(t_i,t_j)=\sigma_X^2e^{-\frac{\lvert t_i-t_j \rvert}{b}}` defined on a symmetric domain :math:`\mathbb{D}=[-a,a]`,
the K-L series expansion is given by:

.. math:: X(t) = \sum_{n=1}^\infty \sqrt{\lambda_{c,n}}\cdot\varphi_{c,n}(t)\cdot\xi_{c,n} + \sum_{n=1}^\infty \sqrt{\lambda_{s,n}}\cdot\varphi_{s,n}(t)\cdot\xi_{s,n},\quad t\in\mathbb{D}

where,

.. math:: \lambda_{c,n} = \frac{2b}{1+\omega_{c,n}^2\cdot b^2},\quad \varphi_{c,n}(t) = k_{c,n}\cos(\omega_{c,n}\cdot t)
.. math:: k_{c,n} = \frac{1}{\sqrt{a+\frac{\sin(2\omega_{c,n}\cdot a)}{2\omega_{c,n}}}}

where :math:`\omega_{c,n}` is obtained as the solution of

.. math:: \frac{1}{b} - \omega_{c,n}\cdot\tan(\omega_{c,n}\cdot a) = 0 \quad \text{in the range} \quad \biggl[(n-1)\frac{\pi}{a}, (n-\frac{1}{2})\frac{\pi}{a}\biggr]

and,

.. math:: \lambda_{s,n} = \frac{2b}{1+\omega_{s,n}^2\cdot b^2},\quad \varphi_{s,n}(t) = k_{s,n}\sin(\omega_{s,n}\cdot t)
.. math:: k_{s,n} = \frac{1}{\sqrt{a-\frac{\sin(2\omega_{s,n}\cdot a)}{2\omega_{s,n}}}}

where :math:`\omega_{s,n}` is obtained as the solution of

.. math:: \frac{1}{b}\cdot\tan(\omega_{s,n}\cdot a) + \omega_{s,n} = 0 \quad \text{in the range} \quad \biggl[(n-\frac{1}{2})\frac{\pi}{a}, n\frac{\pi}{a}\biggr]

.. note::
  In the case of an asymmetric domain e.g. :math:`\mathbb{D}=[-t_{min},t_{max}]`, a shift parameter :math:`T = (t_{min}+t_{max})/2` is required and the corresponding
  symmetric domain becomes

  .. math:: D' = D - T = \biggl[\frac{t_{min}-t_{max}}{2}, \frac{t_{max}-t_{min}}{2} \biggr]

  And the series expansion becomes

  .. math:: X(t) = \sum_{n=1}^\infty \sqrt{\lambda_{c,n}}\cdot\varphi_{c,n}(t-T)\cdot\xi_{c,n} + \sum_{n=1}^\infty \sqrt{\lambda_{s,n}}\cdot\varphi_{s,n}(t-T)\cdot\xi_{s,n},\quad t\in\mathbb{D}

The K-L expansion of a gaussian process has the property that :math:`\xi_{c,n}` and :math:`\xi_{s,n}` are independent
standard normal variables, that is, they follow the :math:`\mathcal{N}(0,1)` distribution. The other great property is
that :math:`\lambda_{c,n}` and :math:`\lambda_{s,n}` converge to zero fast (in the mean square sense). For practical implementation,
this means that the infinite series of the K-L expansion above is truncated after a finite number of terms, giving the approximation:

.. math:: X(t) \approx \hat{X}(t) = \sum_{n=1}^P \sqrt{\lambda_{c,n}}\cdot\varphi_{c,n}(t)\cdot\xi_{c,n} + \sum_{n=1}^Q \sqrt{\lambda_{s,n}}\cdot\varphi_{s,n}(t)\cdot\xi_{s,n}

The equation above is computationally feasible to handle. Let's summarize how it can be used to generate realizations of :math:`X(t)`.

1. To generate the j-th realization, we draw a random value for each :math:`\xi_{c,n}, n=1,\dots ,P, \quad \xi_{s,n}, n=1,\dots ,Q` from the standard
   normal distribution :math:`\mathcal{N}(0,1)` and obtain :math:`\xi_{c,1}^j,\dots ,\xi_{c,P}^j, \quad \xi_{s,1}^j,\dots ,\xi_{s,P}^j`

2. We insert these values into the equation in other to obtain the j-th realization:

.. math:: \hat{X}^j(t) = \sum_{n=1}^P \sqrt{\lambda_{c,n}}\cdot\varphi_{c,n}(t)\cdot\xi_{c,n}^j + \sum_{n=1}^Q \sqrt{\lambda_{s,n}}\cdot\varphi_{s,n}(t)\cdot\xi_{s,n}^j

3. To generate additional realizations, we simply draw new random values for :math:`\xi_{c,n}, n=1,\dots ,P, \quad \xi_{s,n}, n=1,\dots ,Q` each from :math:`\mathcal{N}(0,1)`

The Monte Carlo simulation
--------------------------
For linear static problems in the context of FEM, the system equations which must be solved change from

.. math:: \pmb{K}\pmb{U} = \pmb{F}

to

.. math:: \pmb{K}(\pmb{\xi})\pmb{U}(\pmb{\xi}) = \pmb{F}(\pmb{\xi})

where :math:`\pmb{\xi}` collects a sources of system randomness. The Monte Carlo simulation for solving the equation above
consists of generating a large number of :math:`N_{sim}` of samples :math:`\pmb{\xi}, i=1,\dots ,N_{sim}` from their probability
distribution and for each of these samples, solve the deterministic problem

.. math:: \pmb{K}(\pmb{\xi}_{(i)})\pmb{U}(\pmb{\xi}_{(i)}) = \pmb{F}(\pmb{\xi}_{(i)})

The next step is to collect the :math:`N_{sim}` response vectors :math:`\pmb{U} := \pmb{U}(\pmb{\xi}_{(i)})` and perform a statistical
post-processing in order to extract useful information such as mean value, variance, histogram,
empirical pdf/cdf, etc.


Problem description
-------------------
In the following plane stress problem

.. figure:: problem.png

   A two-dimensional cantilver structure under a point load

:math:`P` is a random variable following the Gaussian distribution :math:`\mathcal{N}(0,1)` (kN) and the modulus of elasticity is a
random field given by the expression:

.. math:: E(x) = 10^5(1+0.10f(x)) (kN/m^2)

with :math:`f(x)` being a zero mean stationary Gaussian field with unit variance. The covariance function for :math:`f` is

.. math:: C_f(x_i,x_j)=e^{-\frac{\lvert x_i-x_j \rvert}{3}}

We are to do the following:

1. Using the K-L series expansion, generate 5000 realizations for :math:`E(x)` and perform Monte 
   Carlo simulation to the probability density function of the response :math:`u`, at the bottom right corner 
   of the cantilever. 

2. If :math:`u` must not exceed :math:`0.2 m`, how confident can we be of this requirement?