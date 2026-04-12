"""
polynomials.factor - rational roots theorem polynomials factoring
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an inefficient implementation of the rational roots test
    for finding roots and linear factors of univariate rational
    polynomials.  It should be adequate for coefficients up to 10,000
    or perhaps more, but there are much better methods.

    For more information on alternatives, see the following article:

        [1] "Lenstra–Lenstra–Lovász lattice basis reduction algorithm"
            in Wikipedia. 5 January 2026. Web. Accessed 12 April 2026.

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
from fractions import Fraction

from polynomials.polynomial import deg, Polynomial

class NoLinearFactor(Exception):
    """exception raised by _factor"""
    pass

def _factor(f:Polynomial):
    """try to find a proper rational linear factor

    DESCRIPTION

        Returns a triple (d, g, h) where:
            d is a scalar
            g is a linear factor
            h is a polynomial of degree 1 or more
          and
            dg(x)h(x) = f(x).

        The factor is found using the rational roots test.

    EXCEPTIONS

        Raises RuntimeError if deg f < 2.

        Raises NoLinearFactor if no such factor g can be found.

    WARNING

        If either the leading coefficient or the constant term in the normal
        form is a large integer, this may take a lot of time.
    """
    if deg(f) < 2:
        raise RuntimeError("_factor: require degree 2 or greater")
    d, g = f.normal2            # dg(x) = f(x)
    coeffs = g.coeffs
    x = f.indeterminate

        # constant term
    c = coeffs[0]
    assert c.denominator == 1
    c = abs(c.numerator)

        # is x a linear factor?
    if c == 0:
        return (d, Polynomial(0, 1, indeterminate=x), g<<1)

        # leading coeff
    a = coeffs[-1]
    assert a.denominator == 1
    a = abs(a.numerator)

        # search for factors
        #   This can be time-consuming!
        #   The search favors linear factors with small coefficients...
        #   One question:
        #       Would there be a time savings if we checked whether
        #           g(-dc/da) = 0 before dividing to obtain quotient q(x)?

    for dc in range(1, c+1):
        if c % dc != 0:
            continue                    # not a divisor
        for da in range(1, c+1):
            if a % da != 0:
                continue                    # not a divisor
#            print("trying:", da, dc)
            h = Polynomial(dc, da, indeterminate=x)
            q, r = divmod(g, h)
            if r == 0:
                return (d, h, q)            # FOUND!
            h = Polynomial(-dc, da, indeterminate=x)
            q, r = divmod(g, h)
            if r == 0:
                return (d, h, q)            # FOUND!
    raise NoLinearFactor("_factor: no linear factor found")

def _ckfactor(f:Polynomial):
    """try to find a proper rational linear factor

    DESCRIPTION

        Returns a triple (d, g, h) where:
            d is a scalar
            g is a linear factor
            h is a polynomial of degree 1 or more
          and
            dg(x)h(x) = f(x).

        The factor is found using the rational roots test.

        This version checks whether f(-c/a) = 0 before dividing by ax+c...

    EXCEPTIONS

        Raises RuntimeError if deg f < 2.

        Raises NoLinearFactor if no such factor g can be found.

    WARNING

        If either the leading coefficient or the constant term in the normal
        form is a large integer, this may take a lot of time.
    """
    if deg(f) < 2:
        raise RuntimeError("_factor: require degree 2 or greater")
    d, g = f.normal2            # dg(x) = f(x)
    coeffs = g.coeffs
    x = f.indeterminate

        # constant term
    c = coeffs[0]
    assert c.denominator == 1
    c = abs(c.numerator)

        # is x a linear factor?
    if c == 0:
        return (d, Polynomial(0, 1, indeterminate=x), g<<1)

        # leading coeff
    a = coeffs[-1]
    assert a.denominator == 1
    a = abs(a.numerator)

        # search for factors
        #   This can be time-consuming!
        #   The search favors linear factors with small coefficients...
        #   One question:
        #       Would there be a time savings if we checked whether
        #           g(-dc/da) = 0 before dividing to obtain quotient q(x)?

    for dc in range(1, c+1):
        if c % dc != 0:
            continue                    # not a divisor
        for da in range(1, c+1):
            if a % da != 0:
                continue                    # not a divisor
#            print("trying:", da, dc)
            if g.apply(Fraction(-dc,da)) == 0:
                h = Polynomial(dc, da, indeterminate=x)
                q = g // h
                return (d, h, q)            # FOUND!
            if g.apply(Fraction(dc,da)) == 0:
                h = Polynomial(-dc, da, indeterminate=x)
                q = g // h
                return (d, h, q)            # FOUND!
    raise NoLinearFactor("_factor: no linear factor found")

def factor(f:Polynomial):
    """find linear factors

            *** CAUTION ***

    This is a rudimentary factoring algorithm which will find all proper
    rational linear factors of a given polynomial.  The last returned factor might
    have quadratic or higher degree proper rational factors.
    """
    d, f = f.normal2
    factors = list()
    while deg(f) >= 2:
#        print("f(x)=", f)
        try:
            c, g, h = _ckfactor(f)      # _ckfactor or _factor
        except NoLinearFactor:
            return tuple([d] + factors + [f])
        d *= c
        factors.append(g)
        f = h
    return tuple([d] + factors + [f])

# END polynomials.factor
