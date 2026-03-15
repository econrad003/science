# a Kolmogorov-type two-species competition model

Class *CompetitionModel* in module *ecology.competition* models two species competition using a system of two ordinary differential equations that generalize the logistic equation.  The system is:
```
    x'(t) = ρx(1 - αx - βy)
    y'(t) = σy(1 - γx - δy)
```
The Latin letters x and y represent population densities as functions of time.

The Greek letters α, β, γ and δ represent extinction rates due to competition while ρ and σ represent logistic growth rates.  These quantities are assumed here to be positive.

The determinant *D* of the 2x2 matrix (α, β | γ, δ) is given by *D*=αδ-βγ.  The value of *D* will tell a lot about the asymptotic behavior (as time approaches infinity or as it runs backward to negative infinity).

In addition, if the determinant is not zero, there is an equilibrium at (x,y)=((δ-β)/*D*,(α-γ)/*D*).  Note that it might not be in the first quadrant.

There are three more equilibrium points obtained by setting x or y to 0:
```
    x = 0:
        1 - δy = 0
        y = 1/δ
    y = 0:
        1 - αx = 0
        x = 1/α
    x = y = 0
```

## β = γ = 0 (logistic model)

If the interspecies extinction rates β and γ are 0, the system reduces to two logistic equations:
```
    x'(t) = ρx(1 - αx)
    y'(t) = σy(1 - δy)
```
In this trivialization, there are essentially two types of solutions to the two equations.  The two equations are isomorphic, so we consider just the first:

* When 0 < x(0) < 1, the solution to the first equation is a sigmoid curve which increases asymptotically to 1.  If we let time run backwards, then the solution would decay asymptotically to zero.
* When x(0) > 1, the solution decays asymptotically to 1.

## References

The system is discussed in the following preprint on ArXiv.org.  (A search in a research library by someone with easy access will probably locate many other references.)

* [1] Sudeepto Bhattacharya and L M  Saha. "A model of discrete Kolmogorov-type competitive interaction in a two-species ecosystem" in ArXiv. 28 Jul 2015. Web. Accessed 27 Jan 2026.  Abstract: [https://arxiv.org/abs/1507.07645](https://arxiv.org/abs/1507.07645). PDF: [https://arxiv.org/pdf/1507.07645](https://arxiv.org/pdf/1507.07645)

## Examples

The gallery contains the results of some tests.  These are discussed in the examples below.

Here is the help information for the test module:
```
$ python -m tests.competition -h
usage: competition.py [-h] [-r RHO] [-s SIGMA] [--dt DT] [-n ITERATIONS] [-d]
                      a b c d

a Kolmogorov-type two-species competition model

positional arguments:
  a                     α, the intraspecies extinction rate for species 1.
  b                     β, the interspecies extinction rate for species 1.
  c                     γ, the interspecies extinction rate for species 2.
  d                     δ, the intraspecies extinction rate for species 2.

options:
  -h, --help            show this help message and exit
  -r RHO, --rho RHO     ρ, the logistic growth rate for species 1.
                        (Default=1.)
  -s SIGMA, --sigma SIGMA
                        σ, the logistic growth rate for species 2.
                        (Default=1.)
  --dt DT               the time differential for the simulation.
                        (default=0.01)
  -n ITERATIONS, --iterations ITERATIONS
                        the number of iterations. (default=100)
  -d, --debug

DESCRIPTION

    The model is a system of two ordinary differential equations that
    generalize the logistic equation:

        x'(t) = ρx(1 - αx - βy)
        y'(t) = σy(1 - γx - δy)

    The population densities at time t are speciied by x(t) and y(t).
    The simulation starts at time t=0 with species densities set to 1.
    Euler's tangent method is used to approximate the solutions.
```

### Example 1 (α=1, β=0.5, γ=0.6, δ=0.7)

Here is the transcript:
```
$ python -m tests.competition 1 0.5 0.6 0.7 -n 3000
determiminant αδ - βy = 0.39999999999999997, positive
equilibrium ((0.49999999999999994, 1.0000000000000002))
    first quadrant equilibrium
Additional equilibria:
	(0, 1.4285714285714286)
	(1.0, 0)
	(0, 0)
```

The rates ρ and σ are 1 in this example.

The determinant:
```
    D = αδ-βy = 0.7 - 0.3 = 0.4 > 0.
```
The equilibrium point is in the first quadrant:
```
    (x, y) = (δ-β, α-γ)/D = (0.2, 0.4)/0.4 = (0.5, 1)
```
These are the values that were displayed on the console, but with some rounding error due to the use of floating point.

The saved file is *gallery/competition_1.png*.

If we look at the top graph. we note that both populations started at densities of 1 (the default starting densities).  Over time, the density of species 1 (variable x) decayed to 0.5, while the density of species 2 (y) initially fell (due to competition with species 1) to a value of about y=0.85 at roughly t=2.

The graph at the bottom is the phase plane, Comparing this graph with the top graph of density over time, we see that at time t=0, the phase curve starts in the upper right at (x,y)=(1,1), and proceeds leftward to approach the equiibrium point (0.5,1).  3000 iterations (t=30) yielded a value very close to equilibrium.

#### Additional notes

Note that interchanging x and y in the the two equations changes the sign of the determinant.  But the equilibrium is still an attractor in the first quadrant.

The values of rates ρ and σ affect how fast the solutions approach the attracting equilibrium.

If the parameter *dt* (default=0.01) is set too large, chaos may ensue.  (When is *dt* too large?  It depends on the other parameters.)  Note that chaotic behavior is interesting in its own right.  Here, chaotic behavior implies that our finite difference model using Euler's tangent method is qualitatively behaving very differently from the underlying differential equations.  But this isn't the only implication.  In addition, we would expect small changes in the initial values (x=y=1 at t=0) to produce substantially different values as the number of iterations increase.  (This is referred to as "sensitive dependence on initial conditions" or, more informally, as the Brazilian butterfly effect.)

### Example 2 (α=1, β=0.7, γ=0.7, δ=1)

Transcript:
```
$ python -m tests.competition 1 0.7 0.7 1 -n 1000
determiminant αδ - βy = 0.51, positive
equilibrium ((0.5882352941176472, 0.5882352941176472))
    first quadrant equilibrium
Additional equilibria:
	(0, 1.0)
	(1.0, 0)
	(0, 0)
```

Again we have a positive determinant and a first quadrant equilibrium.  The determinant is exactly 0.51, and equilibrium is at:
```
    x = y = 0.3 / 0.51= 30/51.
```

The saved file is *gallery/competition_2.png*.

The two curves in the top graph are identical and both simply decay asymptotically to the equilibrium value of exactly 30/51 (or about 0.59).

The phase plane is a straight line segment starting at x=y=1, proceeding downward and leftward, approaching x=y=30/51 as t gets large.

### Example 3 (α=1, β=0.7, γ=0.7, δ=0.1)

Transcript:
```
$ python -m tests.competition 1 0.7 0.7 0.1 -n 1000
determiminant αδ - βy = -0.3899999999999999, negative
equilibrium ((1.5384615384615388, -0.7692307692307695))
    equilibrium is not in the first quadrant
Additional equilibria:
	(0, 10.0)
	(1.0, 0)
	(0, 0)
```
The determinant is negative.  But just interchanging x and y would change the sign, so this isn't signfificant.  (But chaos is apt to result if the determinant is sufficiently close to zero.)

Note that the calculated equilibrium is in the fourth quadrant, so this equilibrium doesn't factor into physical interpretations of the results.  There are three physical equilibria.  We can fill these in as follows:
```
    x = 0: y = 1/δ = 10
        (0, 10)
    y = 0: x = 1/α = 1
        (1, 0)
    x = y = 0
        (0, 0)
```

The saved file is *gallery/competition_3.png*.

In the graph of density over time, we see a population crash (density x approaching zero) in species 1, and species 2 approaches equilibrium at y=10.

In the phase plane, the phase curve starts at (1,1) in the lower right and moves left and up, approaching the equilibrium at (0, 10).
