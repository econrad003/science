# The Lotka-Volterra predator/prey equations

## Description

The Lotka-Volterra predator/prey equations are a system of ordinary differential equations that models a two-species predator/prey system in time.  If *t* is time, *H=H(t)* the prey density as a function of time, and *L=L(t)* the predator density likewise as a function of time, then the system is given two ordinary differential equations:

* *H' = αH - βHL*
* *L' = -γL + δHL*

The coefficients are positive and represent birth rates (for terms that are added) and death rates (for terms that are subtracted).  For example, the first term *αL* says roughly that the *increase* in prey density due to births in one unit of time is the product of the birth rate *α* and the prey density *H*.  The second term says that the *decrease* in prey density due to deaths is the product of the death rate *β* and the product of both the prey and the predator densities.

Note that if *β=δ=0*, the quadratic terms vanish, the first equation reduces to exponential growth, and the second reduces to exponential decay.

If *H=0* or *L=α/β*, then *H'=0*.  Similarly, if *L=0* or *H=γ/δ*, then *L'=0*.  If either density happens to be zero at some point in time, it will be zero for all time (past and future).   But we are primarily interested in points where both populations are positive.  In this case, we have an equilibrium at *(H,L)=(γ/δ,α/β)*.  Solutions in the first quadrant are elliptic and orbit the equilibrium.  (They are simple closed circuits and not ellipses in the usual geometric sense.)

## Implementation

The module *ecology.predator_prey* implements the Lotka-Volterra model as a class (*PredatorPreyModel*) with four parameters *a*, *b*, *c* and *d* corresponding to the Greek letters *α*, *β*, *γ* and *δ* above.  After instantiating the class, one can run the *model* method, defined as follows:

```python
        def model(self, h0:float, l0:float, dt:float,
                  n:int, crash=True):
```
The values *h0* and *l0* represent *H(0)* and *L(0)*, respectively.  The *model* method uses Euler's tangent method to approximate a solution to the differential equation.  Thus *dt* is actually *Δt*, a fixed time increment, and *n* is the number of iterations.  The simulation then approximates values of *H(t)* and *L(t)* for values of *t* from 0 through *nΔt*, inclusive, in increments of *Δt*.  The *crash* option basic stops the simulation at any increment in which either density is no longer positive.  If this option is set to *False*, the simulation will continue with negative values.  Note that any floating point exceptions such as overflow checks and zero divide checks remain in full force.

Here is how one might create a list of *(t,H,L)* triples to feed into a plotting program:

```python
    from ecology.predator_prey import PredatorPreyModel

       # set the parameters
    alpha = 0.5     # prey birth rate
    beta = 0.1      # prey death rate
    gamma = 0.2     # predator death rate
    delta = 0.3     # predator birth rate

        # set up the simulator
    sim = PredatorPreyModel(alpha, beta, gamma, delta)

        # run the simulation [(t0,H0,L0), (t1,H1,L1), ...]
    h0, l0= 1, 1    # initial densities
    dt = 0.01       # a small positive increment
    n = 1000        # t=0 through t=10
    result = sim.model(h0, l0, dt, n)
```

Note that if dt is too large, the results of the run will be poor estimates of the actual values.  If dt is to small, many iterations will be required to produce a small portion of the close circuit.

## Test module

The test module *tests.predator_prey* provides a way of producing simple data plots.  The plots from three runs are saved in the gallery folder.  Each plot consists of a time plot of both *H(t)* and *L(t)* (over *t*) on the same axes, and a phase plot of *L(t)* over *H(t)* on a second pair of axes.  The equilibrium point is plotted as well on the phase plot.

Here are the commands used to create the three plots:
```
$ python -m tests.predator_prey 0.2 0.1 0.2 0.3 -n 5000
$ python -m tests.predator_prey 0.5 0.1 0.2 0.3 -n 5000
$ python -m tests.predator_prey 0.8 0.1 0.2 0.3 -n 5000
```

The only value that has been varied is *α* (0.2, 0.5, and 0.5).  The remaining parameters for all three runs were *β=0.1*, *γ=0.2*, and *δ=0.3*.  The default increment (*dt=Δt=0.1*) was used, and to get reasonable plots, 5000 iterations were plotted.  Note that the top graph in each plot runs from *t=0* through *t=50* inclusive.  The graphs show approximately two periods of the functions *H(t)* and *L(t)*.  The test program fixes the initial densities at exactly 1 each.  (I might add the ability to specify the initial densities in a future update.)

## Usage information

```
$ python -m tests.predator_prey -h
usage: predator_prey.py [-h] [--dt DT] [-n ITERATIONS] [-d] a b c d

Lotka-Volterra predator/prey equations

positional arguments:
  a                     the birth rate for prey. The increase in prey density
                        is the product of the prey density and this rate.
  b                     the death rate for prey. The decreate in prey density
                        is the product of the predator and prey densities and
                        this rate.
  c                     the death rate for predators. The decrease in predator
                        density is the product of the predator density and
                        this rate.
  d                     the birth rate for predators. The increase in predator
                        density is the product of the predator and prey
                        densities and this rate.

options:
  -h, --help            show this help message and exit
  --dt DT               the time differential for the simulation.
                        (default=0.01)
  -n ITERATIONS, --iterations ITERATIONS
                        the number of iterations. (default=100)
  -d, --debug

The simulation starts at time t=0 with predator and prey densities set to 1.
```

```
```

## References

[1] "Lotka–Volterra equations" in *Wikipedia*. 9 Nov. 2025. Web. Accessed 25 Jan. 2026. URL: [https://en.wikipedia.org/wiki/Lotka-Volterra_equations](https://en.wikipedia.org/wiki/Lotka-Volterra_equations)
