"""
utilities.gauss_frac - root -2 rational numbers module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module provides the following classes:

        RootM2Frac - a quadratic rational number class (with discriminant
            D=-2) derived from class _QFrac.

    The root -2 rational numbers are complex numbers of the form

             a + b√-2
            ---------
               c

    where a, b and c are integers (with c ≠ 0).  The set of root -2
    rationals is denoted ℚ(√-2).

    An important subset is the set of root -2 integers, where c = 1.
    These form a Euclidean domain as they share a number of important
    number-theoretic properties with the ordinary integers ℤ, for example:

        1.  division algorithm;
        2.  unique factorization (up to units);
        3.  every ideal is a principal ideal;
        4.  the norm is multiplicative.

    The set of root -2 integers is denoted ℤ[√-2]

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
from math import trunc, floor, ceil
from fractions import Fraction
from utilities._quadratic import _QFrac, _tsqrt

class RootM2Frac(_QFrac):
    """the root -2 rational numbers ℚ(√-2)"""

    def __init__(self, a:int, b:int, c:int, d:int=-2):
        """constructor

        If the value of d is anything except -2, then a ValueError
        exception is raised.  This parameter is retained for
        compatibility with the base class.
        """
        super().__init__(a, b, c, d)
        if d != -2:
            raise ValueError("The value of the base must be d=-2.")

            # ROUNDING ROUTINES

    def __round__(self, ndigits=0):
        """round to the nearest modulo -2 integer (minimize the norm)"""
        if ndigits != 0:
            raise NotImplementedError("nearest only, ndigits must be 0")
        a = floor(self.real)
        b = floor(self.imag)
            # first possibility
        z = self._qfrac(a, b, 1)
        n = (self-z).sqnorm
            # second possibility
        y = self._qfrac(a+1, b, 1)
        m = (self-y).sqnorm
        if m < n:
            z, n = y, m
            # third possibility
        y = self._qfrac(a, b+1, 1)
        m = (self-y).sqnorm
        if m < n:
            z, n = y, m
            # last possibility
        y = self._qfrac(a+1, b+1, 1)
        m = (self-y).sqnorm
        if m < n:
            z, n = y, m
        return z

    def __trunc__(self):
        """round toward zero"""
        a = trunc(self.real)
        b = trunc(self.imag)
        return self._qfrac(a, b, 1)

    def __floor__(self):
        """greatest integer rounding

        Truncates in the southwest direction:

                 +-----+
                 |     |   Points in the interior round to corner X
                 |     |
                 +-----+
                X
                            i is north of zero
                            1 is east of zero
        """
        a = floor(self.real)
        b = floor(self.imag)
        return self._qfrac(a, b, 1)

    def __ceil__(self):
        """least integer rounding

        Truncates in the northeast direction:

                         X
                 +-----+
                 |     |   Points in the interior round to corner X
                 |     |
                 +-----+
                            i is north of zero
                            1 is east of zero
        """
        a = ceil(self.real)
        b = ceil(self.imag)
        return self._qfrac(a, b, 1)

    @property
    def southwest(self):
        """rounds to the southwest (lower left, same as floor)"""
        return floor(self)

    @property
    def southeast(self):
        """rounds to the southeast (lower right)"""
        a = ceil(self.real)
        b = floor(self.imag)
        return self._qfrac(a, b, 1)

    @property
    def northeast(self):
        """rounds to the northeast (upper right, same as ceil)"""
        return ceil(self)

    @property
    def northwest(self):
        """rounds to the northwest (upper left)"""
        a = floor(self.real)
        b = ceil(self.imag)
        return self._qfrac(a, b, 1)

    @classmethod
    def RootM2Frac(cls, z:(int, Fraction, "Root2Frac", _QFrac)):
        """converts the argument to a root -2 rational"""
        if isinstance(z, cls):
            return z
        if type(z) == int:
            return cls(z, 0, 1)
        if type(z) == Fraction:
            return cls(z.numerator, 0, z.denominator)
        if isinstance(z, _QFrac):
            a, b, c, d = z._value
            if b !=0 and d != -2:
                raise TypeError(f"{d=} incompatible with root -2 rational")
            return cls(a, b, c)
        raise TypeError("incompatible type for root D=-2 conversion")

    def __floordiv__(self, other):
        """rounding division"""
        if not isinstance(other, RootM2Frac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        return round(self / other)

    def __rfloordiv__(self, other):
        """reversed rounding division"""
        if not isinstance(other, RootM2Frac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        return round(self.reciprocal * other)

    def __mod__(self, other):
        """modulus (rounding division)"""
        if not isinstance(other, RootM2Frac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self / other)
        return self - q * other

    def __rmod__(self, other):
        """reversed modulus (rounding division)"""
        if not isinstance(other, RootM2Frac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self.reciprocal * other)
        return - self * q + other

    def __divmod__(self, other):
        """rounding division with remainder (division algorithm)"""
        if not isinstance(other, RootM2Frac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self / other)
        m = self - q * other
        return q, m

    def __rdivmod__(self, other):
        """reversed rounding division with remainder (division algorithm)"""
        if not isinstance(other, RootM2Frac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self.reciprocal * other)
        m = - self * q + other
        return (q, m)

# END utilities.rootm2_frac
