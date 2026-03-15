"""
utilities.quadratic_equation - quadratic equation analysis module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module provides the following classes:

        QuadraticEquation - an alalyzer of quadratic equations with integer
            coefficients.

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
from math import gcd, sqrt, isqrt
from fractions import Fraction

from utilities.moremath import Primes
from utilities._quadratic import _QFrac

class QuadraticEquation(object):
    """analysis of quadratic equations with integer coefficients"""

    __slots__ = ("__a", "__b", "__c", "__disc", "__sfdisc", "__sfroot")

    def __init__(self, a:int, b:int, c:int):
        """constructor

        Input the coefficients of a quadratic equation with integer
        coefficients.
        """
                # Validation
        if type(a) != int:
            raise TypeError("The lead coefficient 'a' must be an integer.")
        if a == 0:
            raise ZeroDivisionError("The lead coefficient 'a' must not be zero.")
        if type(b) != int:
            raise TypeError("The linear term 'b' must be an integer.")
        if type(c) != int:
            raise TypeError("The constant term 'c' must be an integer.")
        if a < 0:
            a = -a
            b = -b
            c = -c
        d = gcd(a, b, c)
        self.__a = a // d
        self.__b = b // d
        self.__c = c // d
            # discriminant
        self.__disc = b*b - 4 * a * c
        k = 1
        r, s = 1, self.__disc           # loop invariant:   disc = r √s
        while True:
            p = Primes.pi(k)            # return the kth prime
            k += 1
            q = p * p
            if q > abs(s):
                break                   # done!
            while s % q == 0:
                s //= q                     # √s := p √(s/q)
                r *= p                      # (invariant restored)
        self.__sfroot, self.__sfdisc = r, s

    def __str__(self):
        """string representation"""
        if self.__a == 1:
            a = "x²"
        elif self.__a == -1:
            a = "-x²"
        else:
            a = f"{self.__a}x²"

        if self.__b == 0:
            b = ""
        elif self.__b == 1:
            b = " + x"
        elif self.__b == -1:
            b = " - x"
        elif self.__b > 0:
            b = f" + {self.__b}x"
        else:
            b = f" - {-self.__b}x"

        if self.__c == 0:
            c = ""
        elif self.__c > 0:
            c = f" + {self.__c}"
        else:
            c = f" - {-self.__c}"
        
        return f"{a}{b}{c}"

    def __repr__(self):
        """representation"""
        return f"EQN({str(self)} = 0)"

    @property
    def coeffs(self) -> tuple:
        """returns the coefficients"""
        return (self.__a, self.__b, self.__c)

    def __getitem__(self, index:int) -> int:
        """returns a coefficient

        p[0] = p[-3] = a        leading (quadratic) coefficient
        p[1] = p[-2] = b        linear coefficient
        p[2] = p[-1] = c        constant term
        """
        return self.coeffs[index]

    @property
    def discriminant(self) -> int:
        """returns the discriminant"""
        return self.__disc

    @property
    def delta(self) -> int:
        """returns the square-free part of the discriminant"""
        return self.__sfdisc

    @property
    def multiplier(self) -> int:
        """returns the coefficient of the discriminant"""
        return self.__sfroot

    @property
    def roots(self) -> tuple:
        """return the roots of the equation"""
        d = self.delta
        if d == 0:                  # rational double root
            u = Fraction(- self.__b, 2*self.__a)
            return (u, u)
        
        if d == 1:                  # distinct rational roots
            u = Fraction(- self.__b, 2*self.__a)
            v = Fraction(self.__sfroot, 2*self.__a)
            return (u+v, u-v)

                # roots are distinct and not rational
        u = _QFrac(- self.__b, self.__sfroot, 2*self.__a, self.__sfdisc)
        return (u, u.conjugate())

    def eval(self, x:"Number", modulus=0) -> "Number":
        """evaluate at x

        If the modulus is not zero, the result is reduced modulo the modulus.
        """
        y = (self.__a * x + self.__b) * x + self.__c
        if y == 0:
            return 0                # since _QFrac doesn't support mod operator
        return y if modulus == 0 else y % modulus

    def check(self):
        """make sure the roots have been correctly evaluated"""
        r1, r2 = self.roots
        assert self.eval(r1) == 0, f"{self.eval(r1)}"
        assert self.eval(r2) == 0, f"{self.eval(r2)}"

    def __hash__(self):
        """returns the hash"""
        triple = (self.__a, self.__b, self.__c)
        return hash(triple)

    def __eq__(self, other):
        """returns True if the polynomials are equal"""
        if isinstance(other, QuadraticEquation):
            return self.coeffs == other.coeffs
        return NotImplemented

if __name__ == "__main__":
        # module tests
    from random import randrange
    from utilities.golden_frac import GoldenFrac
    from utilities.gauss_frac import GaussianFrac

    a, b, c = 1, 0, 0               # y = x²
    p = QuadraticEquation(a, b, c)
    print(f"{repr(p)}:")
    assert str(p) == "x²", f"{p} == x²"
    for x in range(-10, 11):
        assert p.eval(x) == x*x, f"{x}: {p.eval(x)} == {x*x}"
    assert p.discriminant == 0, f"{self.discriminant} == 0"
    assert p.roots == (0,0), f"{self.roots} == (0, 0)"
    assert p[0] == p[-3] == a
    assert p[1] == p[-2] == b
    assert p[2] == p[-1] == c
    assert p.delta == 0
    assert p.multiplier == 1
    p.check()
    q = QuadraticEquation(2, 0, 0)
    assert p == q, f"{repr(q)}"
    q = QuadraticEquation(-5, 0, 0)
    assert p == q, f"{repr(q)}"

    a, b, c = 1, 0, -4              # y = x² - 4
    p = QuadraticEquation(a, b, c)
    print(f"{repr(p)}:")
    assert str(p) == "x² - 4", f"{p} == x² - 4"
    for x in range(-10, 11):
        assert p.eval(x) == x*x-4, f"{x}: {p.eval(x)} == {x*x-4}"
    assert p[0] == p[-3] == a
    assert p[1] == p[-2] == b
    assert p[2] == p[-1] == c
    assert p.discriminant == 16, f"{p.discriminant} == 16"
    assert p.delta == 1, f"{p.delta}"
    assert p.multiplier == 4, f"{p.multiplier}"
    p.check()
    assert p.roots == (2, -2)

    a, b, c = 1, -5, 4              # y = x² - 5x + 4
    p = QuadraticEquation(a, b, c)
    print(f"{repr(p)}:")
    assert str(p) == "x² - 5x + 4", f"{p} == x² - 5x + 4"
    for x in range(-10, 11):
        assert p.eval(x) == x*x-5*x+4, f"{x}: {p.eval(x)} == {x*x-5*x+4}"
    assert p[0] == p[-3] == a
    assert p[1] == p[-2] == b
    assert p[2] == p[-1] == c
    assert p.discriminant == 9, f"{p.discriminant} == 9"
    assert p.delta == 1, f"{p.delta}"
    assert p.multiplier == 3, f"{p.multiplier}"
    p.check()
    assert p.roots == (4, 1)

    a, b, c = 1, -1, -1             # y = x² - x - 1 (Fibonacci)
    p = QuadraticEquation(a, b, c)
    print(f"{repr(p)}:")
    assert str(p) == "x² - x - 1", f"{p} == x² - x - 1"
    for x in range(-10, 11):
        assert p.eval(x) == x*x-x-1, f"{x}: {p.eval(x)} == {x*x-x-1}"
    assert p[0] == p[-3] == a
    assert p[1] == p[-2] == b
    assert p[2] == p[-1] == c
    assert p.discriminant == 5, f"{p.discriminant} == 5"
    assert p.delta == 5, f"{p.delta}"
    assert p.multiplier == 1, f"{p.multiplier}"
    p.check()
    PHI = GoldenFrac(1, 1, 2)
    PHIBAR = GoldenFrac(1, -1, 2)
    assert p.roots == (PHI, PHIBAR)

    root1 = GaussianFrac(3, 4, 1)
    root2 = GaussianFrac(3, -4, 1)
        # sum = 6, product = (3+4i)(3-4i) = 9+16 = 25
    # a, b, c = 1, -6, 25             # y = x² - 6x + 25
    a, b, c = 1, int(- root1 - root2), int(root1 * root2)
    p = QuadraticEquation(a, b, c)
    print(f"{repr(p)}:")
    assert str(p) == "x² - 6x + 25", f"{p} == x² - 6x + 25"
    for x in range(-10, 11):
        assert p.eval(x) == x*x-6*x+25, f"{x}: {p.eval(x)} == {x*x-6*x+25}"
    assert p[0] == p[-3] == a
    assert p[1] == p[-2] == b
    assert p[2] == p[-1] == c
    assert p.discriminant == -64, f"{p.discriminant} == -64"
    assert p.delta == -1, f"{p.delta}"
    assert p.multiplier == 8, f"{p.multiplier}"
    p.check()
    assert p.roots == (root1, root2)

        # small integer roots
    print("Integer roots...")
    for r1 in range(-5, 6):
        for r2 in range(r1, 6):
            a, b, c = 1, -(r1+r2), r1*r2
            p = QuadraticEquation(a, b, c)
            print(f"{repr(p)}: {r1}, {r2}")
            p.check()
            assert set(p.roots) == {r1, r2}

    print("SUCCESS!")

# END utilities.quadratic_equation
