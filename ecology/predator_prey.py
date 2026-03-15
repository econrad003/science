"""
ecology.predator_prey - the Lotka-Volterra predator prey model
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The Lotka-Volterra predator-prey model is a system of two ordinary
    differential equations which describes the basic dynamics of
    a biological system with just two populations, namely a predator
    population (L) and a prey population (H).  (The labels are
    derived from the Canada lynx and the snowshoe hare.  Data from
    nimbers of pelts of each sold to the Hudson Bay Company from
    about 1845 to 1935 is often used to illustrate the model.)

    The differential equations are:

        H' = H'(t) =   aH - bHL
        L' = L'(t) = - cL + dHL

    where:

        * H and L denote the respective densities of the prey and the predator
          populations, the dependent variables;
        * t denotes time, the independent variable;
        * the parameter a denotes the per capita birth rate of prey;
        * the product bL denotes the per capita death rate of prey --
          the parameter b thus describes the effect of the presence of
          predators on the prey population;
        * the parameter c denotes the per capita death rate of prey; and
        * the product dH denotes the per capita birth rate of predators --
          the parameter d thus describes the effect of the presence of
          prey on the predator population.

    The parameters a, b, c, and are all positive.  The system makes a number
    of simplifying assumptions, some which might be unrealistic:

        * prey have an unlimited food supply, predators have unlimited
          appetite, and predator food supply depends only on prey supply;
        * environmental factors other that densities of the two species
          don't matter;
        * variation within the populations, such as age or sex distribution,
          doesn't matter; and
        * migration is not a factor.

    Note that if the predator density is zero, the prey equation reduces
    to an exponential growth equation:

        H' = aH

    Similarly if the prey density is zero, the predator equation reduces
    to an exponential decay equation:

        L' = - cL

DYNAMICS

    The system can be rewritten as follows:

        H' = (  a - bL)H
        L' = (- c + dH)L

    Setting the expressions in parentheses equal to zero leads to an
    equilibrium point:

        (H, L) = (c/d, a/b)

    In addition, there is equilinrium point at (H,L) = (0,0), representing
    the extinction of both species.

    The prey (hare) population is decreasing whenever a-bL<0, i.e. whenever
    L>a/b, Conversely, it is increasing whenever L<a/b. 

    The predator (lynx) population is decreasing whenever c-dH>0, i.e. whenever
    H<c/d, Conversely, it is increasing whenever H>a/b.

    We can summarize these statements in the following table (assuming that
    H and L are both positive):

                                    Prey Density
                            H < c/d                 H > c/d
        Predator Density    ----------------------------------------
            L < a/b         H increasing            H increasing
                            L decreasing            L increasing
                            ----------------------------------------
            L > a/b         H decreasing            H decreasing
                            L decreasing            L increasing

    This analysis fits with an informal view of the situation:

        * if the prey supply is plentiful, the predator population will grow;
        * if the predator population is large, the prey supply will shrink.

    If we view these equations purely as mathematical objects, we might
    be interested in both positive and negative values of the densities.
    We can extend the table to these non-physical situations:

                                        Prey
                        H < 0       0 < H < c/d     H > c/d
         Predator       ----------------------------------------
            L < 0       H↓ L↑       H↑ L↑           H↑ L↓
        0 < L < a/b     H↓ L↓       H↑ L↓           H↑ L↑
            L > a/b     H↑ L↓       H↓ L↓           H↓ L↑

    Along the line H=0, the prey density remains constant (H=0 for all time).
    Similarly along the line L=0, the predator density is constant.

    We can plot this in a phase plane for another view:


                    L (predator)
                    ^
                    |
             H↑ L↓  |  H↓ L↓    H↑ L↓
                    |
                    |
                a/b +        P
                    |
             H↓ L↓  |  H↑ L↓    H↑ L↑
                    |
            --------O--------+-------> H (prey)
                    |        c/d
             H↓ L↑  |  H↑ L↑    H↑ L↓
                    |
                    |

    The equilibrium point at the origin is unstable unless exactly one
    of the densities is negative.

    A detailed analysis of the equilibrium at P(c/d, a/b) shows that
    if the model has a point in the first quadrant, then all its points
    are in the first quadrant.  Physical solutions are periodic simple
    closed loops about P.

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

class PredatorPreyModel(object):
    """the Lotka-Volterra predator-prey model

    DESCRIPTION

        This is an attempt to approximate a Lotka-Volterra predator-prey
        model in Python.

        The ordinary differential equations are:
                H' = H'(t) =   aH - bHL
                L' = L'(t) = - cL + dHL
        where H and L are predator and prey densities, t is time and
        a, b, c, and d are positive parameters.
    """

    __slots__ = ("a", "b", "c", "d")

    def __init__(self, a:float, b:float, c:float, d:float):
        """constructor

        REQUIRED ARGUMENTS

            a, b, c, d - the parameters for the model
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def model(self, h0:float, l0:float, dt:float,
              n:int, crash=True):
        """simulate the equation with the given parameters

        DESCRIPTION

            This model approximates the differential system using
            Euler's tangent method.

        REQUIRED ARGUMENTS

            h0 - the initial prey density
            l0 - the initial predator density
            dt - the time differential for the approximations
            n - number of iterations for the simulation

        OPTIONAL ARGUMENTS

            crash (default=True) - if True, the simulation stops if either
                density becomes negative.

        NOTES

            The value of dt needs to be "small" to produce results which
            mimic the the infinitesimals.  But small is a relative term.
            Near the equilibrium point, the value of dt might need to be
            extremely small to produce a simple circuit which orbits the
            equilibrium.

            Away from the equilibrium, values of dt which are too large
            may cause one of the populations to crash.  (If the predator
            population becomes extinct, the prey density grows exponentially
            wihout bound.  Conversely, if the prey population becomes
            extinct, the predator density will decay exponentially.  If
            either density becomes negative, the simulation is no longer
            a physical model of the predator/prey relationship.)

        RETURN VALUE

            a list of (t, H, L) ordered triples.  Unless the simulation
            crashes, the list contains n+1 entries.
        """
        t, h, l = 0, h0, l0
        a, b, c, d = self.a, self.b, self.c, self.d

        result = list()
        result.append((t,h,l))
        for _ in range(n):
            if crash and (h <= 0 or l <= 0):
                print(f"Population crash: H={h}, L={l}")
                return result
            t += dt
            h += (a*h - b*h*l) * dt
            l += (d*h*l - c*l) * dt
            result.append((t,h,l))
        return result

# end module ecology.predator_prey
