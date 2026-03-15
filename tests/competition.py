"""
tests.competition - test the competitition module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

REFERENCES

        [1] Sudeepto Bhattacharya and L M  Saha. "A model of discrete
            Kolmogorov-type competitive interaction in a two-species
            ecosystem" in ArXiv. 28 Jul 2015.  Web.  Accessed 27 Jan 2026.
                Abstract: https://arxiv.org/abs/1507.07645
                PDF: https://arxiv.org/pdf/1507.07645

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
from ecology.competition import CompetitionModel

DESCR = "a Kolmogorov-type two-species competition model"
HELP_A = """α, the intraspecies extinction rate for species 1."""
HELP_B = """β, the interspecies extinction rate for species 1."""
HELP_C = """γ, the interspecies extinction rate for species 2."""
HELP_D = """δ, the intraspecies extinction rate for species 2."""
HELP_R = """ρ, the logistic growth rate for species 1. (Default=1.)"""
HELP_S = """σ, the logistic growth rate for species 2. (Default=1.)"""
DT = 0.01
HELP_DT = f"the time differential for the simulation. (default={DT})"
N = 100
HELP_N = f"the number of iterations. (default={N})"
HELP_DBG = "when set, displays the arguments and the calculated values."
EPILOG = """\
DESCRIPTION

    The model is a system of two ordinary differential equations that
    generalize the logistic equation:

        x'(t) = ρx(1 - αx - βy)
        y'(t) = σx(1 - γx - δy)

    The population densities at time t are speciied by x(t) and y(t).
    The simulation starts at time t=0 with species densities set to 1.
    Euler's tangent method is used to approximate the solutions.
"""

def calculate(a, b, c, d, r, s, dt, n, x0=1, y0=1) -> tuple:
    """run a simulation"""
    assert a >= 0
    assert b >= 0
    assert c >= 0
    assert d >= 0
    assert r >= 0
    assert s >= 0
    assert dt > 0
    assert x0 >= 0
    assert y0 >= 0
    sim = CompetitionModel(a, b, c, d, r, s)
    return tuple(sim.model(x0, y0, dt, n))

def main(args:"Namespace"):
    """runs the simulation and outputs the result"""
    a, b, c, d = args.a, args.b, args.c, args.d     # extinction rates
    r, s = args.rho, args.sigma                     # growth rates
    result = calculate(a, b, c, d, r, s, args.dt, args.iterations)
    time = list()
    species1 = list()
    species2 = list()
    debug = getattr(args, "debug", False)
    for triple in result:
        if debug:
            print(f"(t, x, y) = {triple}")
        t, x, y = triple
        time.append(t)
        species1.append(x)
        species2.append(y)
        # plot the results
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('a Kolmogorov-type two-species competition model')
    ax1.plot(time, species1, label=f"x (species 1): α={a}, β={b}, ρ={r}")
    ax1.plot(time, species2, label=f"y (species 2): γ={c}, δ={d}, σ={s}")
    ax1.set_xlabel("time t")
    ax1.set_ylabel("population density")
    ax1.legend()
    ax2.plot(species1, species2)
    det = a*d - b*c
    if det > 0:
        sign = "positive"
    elif det < 0:
        sign = "negative"
    else:
        sign = "singular"
    print(f"determiminant αδ - βy = {det}, {sign}")
    if abs(det) > 0.01:
        xstar = (d-b)/det
        ystar = (a-c)/det
        print(f"equilibrium ({xstar, ystar})")
        if xstar > 0 and ystar > 0:
            print("    first quadrant equilibrium")
            ax2.plot(xstar, ystar, 'o', label=f"equilibrium")
            ax2.legend()
        else:
            print("    equilibrium is not in the first quadrant")
    else:
        print("    determinant is less than 1/100 in absolute value...")
        print("    will assuming system is roughly singular...")
    print("Additional equilibria:")
    if d != 0:
        print(f"\t(0, {1/d})")
    if a != 0:
        print(f"\t({1/a}, 0)")
    print("\t(0, 0)")
    ax2.set_xlabel("species 1 density x(t)")
    ax2.set_ylabel("species 2 density y(t)")
    plt.show()

def parse_args(argv, descr=DESCR):
    """argument parser"""
    import argparse

    parser = argparse.ArgumentParser(description=descr,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG)
    parser.add_argument("a", type=float, help=HELP_A)
    parser.add_argument("b", type=float, help=HELP_B)
    parser.add_argument("c", type=float, help=HELP_C)
    parser.add_argument("d", type=float, help=HELP_D)
    parser.add_argument("-r", "--rho", type=float, help=HELP_R, default=1)
    parser.add_argument("-s", "--sigma", type=float, help=HELP_S, default=1)
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

