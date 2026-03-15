"""
tests.predator_prey - test the Lotka-Volterra predator/prey module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

REFERENCES

    [1] "Lotka–Volterra equations" in Wikipedia. 9 Nov. 2025. Web.
        Accessed 25 Jan. 2026. 
        URL: https://en.wikipedia.org/wiki/Lotka-Volterra_equations

LICENSE
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import matplotlib.pyplot as plt
from ecology.predator_prey import PredatorPreyModel

DESCR = "Lotka-Volterra predator/prey equations"
HELP_A = """the birth rate for prey.  The increase in prey density is
the product of the prey density and this rate."""
HELP_B = """the death rate for prey.  The decreate in prey density is
the product of the predator and prey densities and this rate."""
HELP_C = """the death rate for predators.  The decrease in predator density is
the product of the predator density and this rate."""
HELP_D = """the birth rate for predators.  The increase in predator density is
the product of the predator and prey densities and this rate."""
DT = 0.01
HELP_DT = f"the time differential for the simulation. (default={DT})"
N = 100
HELP_N = f"the number of iterations. (default={N})"
HELP_DBG = "when set, displays the arguments and the calculated values."
EPILOG = """The simulation starts at time t=0 with predator and prey
densities set to 1."""

def calculate(a, b, c, d, dt, n, H0=1, L0=1) -> tuple:
    """run a simulation"""
    assert a >= 0
    assert b >= 0
    assert c >= 0
    assert d >= 0
    assert dt > 0
    assert H0 >= 0
    assert L0 >= 0
    sim = PredatorPreyModel(a, b, c, d)
    return tuple(sim.model(H0, L0, dt, n))

def main(args:"Namespace"):
    """runs the simulation and outputs the result"""
    a, b, c, d = args.a, args.b, args.c, args.d
    result = calculate(a, b, c, d, args.dt, args.iterations)
    time = list()
    prey = list()
    predator = list()
    debug = getattr(args, "debug", False)
    for triple in result:
        if debug:
            print(f"(t, H, L) = {triple}")
        t, h, l = triple
        time.append(t)
        prey.append(h)
        predator.append(l)
        # plot the results
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('Lotka-Volterra Predator/Prey Model')
    ax1.plot(time, prey, label=f"prey α={a}, β={b}")
    ax1.plot(time, predator, label=f"predator γ={c}, δ={d}")
    ax1.set_xlabel("time t")
    ax1.set_ylabel("population density")
    ax1.legend()
    ax2.plot(prey, predator)
    ax2.plot(c/d, a/b, 'o', label=f"equilibrium")
    ax2.set_xlabel("prey density H(t)")
    ax2.set_ylabel("predator density L(t)")
    ax2.legend()
    plt.show()

def parse_args(argv, descr=DESCR):
    """argument parser"""
    import argparse

    parser = argparse.ArgumentParser(description=descr, epilog=EPILOG)
    parser.add_argument("a", type=float, help=HELP_A)
    parser.add_argument("b", type=float, help=HELP_B)
    parser.add_argument("c", type=float, help=HELP_C)
    parser.add_argument("d", type=float, help=HELP_D)
    parser.add_argument("--dt", type=float, help=HELP_DT, default=DT)
    parser.add_argument("-n", "--iterations", type=int, help=HELP_N, default=N)
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args(argv)
    if args.debug:
        print(args)
    main(args)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])

