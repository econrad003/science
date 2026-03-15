"""
ecology.competition - a two-species competition model
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Implemented here is a simulation based on a simple two species
    competition model expressed in the following ordinary differential
    equations:

        A'(t) = r A(t) (1 - a A(t) - b B(t))
        B'(t) = s B(t) (1 - c A(t) - d B(t))

    The dependent variables A and B represent population densities of
    two competing species. The constants r and s represent logistic
    growth rates for the two populations, while the constants a, b, c,
    and d represent death rates.

    If we set the death rates to zero, the equations reduce to

        A' = rA and B' = sB

    which represent exponential growth.

    If we set the mixed term death coefficients (b and c) to 0, the
    equations reduce to:

        A' = rA(1-aA) and B'=sB(1-dB)

    which represent logistic growth, a type of sigmoid curve.

    Solving the equation A'=0, yields A=0 (extinction) or:

        aA + bB = 1

    If b is not 0, we can solve for B and rewrite this as:

        B = 1/b - aA/b

    In the phase plane, this is a decreasing line (slope -a/b) which
    passes through the origin at 1/b.  If aA + bB > 1 (i.e. above the
    line in the phase plane), then 1-aA-Bb is negative and A'<0, and
    the density A is decreasing (in time). On the other hand, if
    aA + bB < 1 (below, in the phase plane), then A'>0 and A is
    increasing (in time).

    The analysis for the second equation (B') is similar.  We can
    tabulate the results as follows:

                            density B
                    -------------------------------------------
        density A   B' < 0          B' = 0          B'>0
        ----------  -------------------------------------------
        A' < 0      aA + bB > 1     aA + bB > 1     aA + nB > 1
                    cA + dB > 1     cA + cB = 1     cA + dB < 1

        A' = 0      aA + bB = 1     aA + bB = 1     aA + bB = 1
                    cA + dB > 1     cA + cB = 1     cA + dB < 1

        A' < 0      aA + nB < 1     aA + nB < 1     aA + nB < 1
                    cA + dB > 1     cA + cB = 1     cA + dB < 1

            Assuming: a>0, b>0, c>0, and d>0

    The entry in the middle yields the equilibrium population levels:

        [ a  b ] [ A ]   [ 1 ]
        [      ] [   ] = [   ]
        [ c  d ] [ B ]   [ 1 ]

    The determinant of the 2x2 matrix is D=ad-bc.  So its inverse is:

         1  [  d -b ]
        --- [       ]
         D  [ -c  a ]

    Left-multiplying the vector on the right side by the inverse yields
    the vector:

         1  [ d-b ]
        --- [     ]
         D  [ a-c ]

    These matrix manipulations are equivalent to simultaneously solving
    the two equilibrium equations.  (This matrix method for 2x2 equations
    is sometimes called Cramer's rule.)  The physical equilibrium is:

             d - b          a - c
        A = -------    B = -------
            ad - bc        ad - bc

COEFFICIENT NOTES

    The coefficients a and d are rates or extinction due to interspecies
    competition.  The coefficients b and c are rates of extinction due
    to intraspecies competition.

RECOMMENDED EXERCISE

    Compare this model with the predator-prey model used in the
    Lotka-Volterra predator-prey equations. 

REFERENCES

        [1] Sudeepto Bhattacharya and L M  Saha. "A model of
            discrete Kolmogorov-type competitive interaction
            in a two-species ecosystem" in ArXiv. 28 Jul 2015.
            Web. Accessed 27 Jan 2026.
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

class CompetitionModel(object):
    """a Kolomogorov model of two species competition

    DESCRIPTION

        This is an attempt to approximate a simple competition
        model in Python.

        The ordinary differential equations are:
                A' = rA (1 - aA - bB)
                B' = sB (1 - cA - dB)
        where A and B are population densities, t is time and
        r, s, a, b, c, and d are positive parameters.
    """

    __slots__ = ("a", "b", "c", "d", "r", "s")

    def __init__(self, a:float, b:float, c:float, d:float, r:float, s:float):
        """constructor

        REQUIRED ARGUMENTS

            a, b, c, d, r, s - the parameters for the model
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.r = r
        self.s = s

    def model(self, a0:float, b0:float, dt:float,
              n:int, crash=True):
        """simulate the equation with the given parameters

        DESCRIPTION

            This model approximates the differential system using
            Euler's tangent method.

        REQUIRED ARGUMENTS

            a0, b0 - the initial densities A(0) and B(0)
            dt - the time differential for the approximations
            n - number of iterations for the simulation

        OPTIONAL ARGUMENTS

            crash (default=True) - if True, the simulation stops if either
                density becomes negative.

        RETURN VALUE

            a list of (t, A, B) ordered triples.  Unless the simulation
            crashes, the list contains n+1 entries.
        """
        t, rhoA, rhoB = 0, a0, b0
        a, b, c, d = self.a, self.b, self.c, self.d
        r, s = self.r, self.s

        result = list()
        result.append((t, rhoA, rhoB))
        for _ in range(n):
            if crash and (rhoA <= 0 or rhoB <= 0):
                print(f"Population crash: A={rhoA}, B={rhoB}")
                return result
            t += dt
            rhoA += r*rhoA * (1 - a*rhoA - b*rhoB) * dt
            rhoB += s*rhoB * (1 - c*rhoA - d*rhoB) * dt
            result.append((t, rhoA, rhoB))
        return result

# end module ecology.competition
