"""
utilities.eisenstein_frac - Eisensteinian rational numbers module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module provides the following classes:

        EisensteinFrac - a quadratic rational number class (with
    discriminant D=-3) derived from class _QFrac.

    The Eisensteinian rational numbers are complex numbers of the form

             a + b√-3
            ---------
               c

    where a, b and c are integers (with c ≠ 0).  The set of Eisensteinian
    rationals is denoted ℚ(√-3).

    Since the discriminant D=-3 is square-free and congruent to 1 modulo 4,
    we need to generate the imaginary part of the integer number field using

                1 + √-3
            ω = -------
                  2

    To decide whether a field element is a quadratic integer, we essentially
    need to rewrite:

             a + b√-3   (a-b) + b(1+√-3)
            --------- = ----------------
               c
                         a-b     2bω
                      = ----- + -----
                          c       c

    If (a-b)/c and 2b/c are integers, then (a + b√-3)/c is an Eisensteinian
    integer.

CAUTION

    The directed rounding routines do not always return an Eisenstein integer
    which differs less than 1 in norm.  Specifically, integer division should
    not be configured using the floor, ceil, or trunc methods, or the
    southwest, southeast, northeast, or northwest property attributes.

    The integer division here is configured using the round method, which in
    turn evaluates all four properties and chooses the property which minimizes
    the square-norm of the error.  This is slow, but it does find the nearest
    Eisentein integer to the quotient.

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

class EisensteinFrac(_QFrac):
    """the Eisensteinian rational numbers ℚ(√-3)"""

            # coefficients of the Eisenstein normal form
    __slots__ = ("__A", "__B")

    def __init__(self, a:int, b:int, c:int, d:int=-3):
        """constructor

        If the value of d is anything except -3, then a ValueError
        exception is raised.  This parameter is retained for
        compatibility with the base class.
        """
        super().__init__(a, b, c, d)
        if d != -3:
            raise ValueError("The value of the base must be d=-3.")

                # coefficient A + Bω
        self.__A = Fraction(a-b, c)
        self.__B = Fraction(b+b, c)

    @property
    def omega(self):
        """returns ω"""
        return self._qfrac(1, 1, 2)

    @property
    def omegabar(self):
        """returns the conjugate of ω"""
        return self._qfrac(1, -1, 2)

    @property
    def ENF(self) -> tuple:
        """returns the coefficients (A,B) of A+Bω in the Eisenstein expansion"""
        return self.__A, self.__B

    @property
    def ENFstr(self) -> str:
        """returns the ENF expansion as a string"""
        if self.imag == 0:
            return str(self.real)

        a, b = self.ENF
        if a == 0:
            if b.numerator == 1:
                top = "ω"
            elif b.numerator == -1:
                top = "-ω"
            else:
                top = f"{b.numerator}ω"
            return top if b.denominator == 1 else f"{top}/{b.denominator}"

        if b.numerator == 1:
            imag = "+ω"
        elif b.numerator == -1:
            imag = "-ω"
        else:
            imag = f"{b.numerator:+}"
        if b.denominator != 1:
            imag = f"{imag}/{b.denominator}"
        return str(a) + imag

    @property
    def is_int(self) -> bool:
        """returns True if the number is an Eisensteinian integer"""
        a, b = self.ENF
        return a.denominator == 1 == b.denominator

            # ROUNDING ROUTINES

    def __trunc__(self):
        """round toward zero"""
        a, b = trunc(self.real), trunc(self.imag)
        return self._qfrac(a, b, 1)

    def __floor__(self):
        """greatest integer rounding

        Truncates in the southwest direction:

                 +-----+
                 |     |   Lower triangle rounds to corner X
                 |     |   Upper triangle rounds to midpoint
                 +-----+
                X
                            i is north of zero
                            1 is east of zero
        """
        a0, b0 = self.real, self.imag
        a1, b1 = floor(a0), floor(b0)       # the point X
        a2, b2 = a0-a1, b0-b1               # the fractional parts

        if a2 + b2 < 1:
            return self._qfrac(a1, b1, 1)   # the point X
        a3, b3 = a1 + a1 + 1, b1 + b1 + 1
        return self._qfrac(a3, b3, 2)       # the midpoint

    def __ceil__(self):
        """least integer rounding

        Truncates in the northeast direction:

                         X
                 +-----+
                 |     |   Upper triangle rounds to corner X
                 |     |   Lower triangle rounds to midpoint
                 +-----+
                            i is north of zero
                            1 is east of zero
        """
        a0, b0 = self.real, self.imag
        a1, b1 = ceil(a0), ceil(b0)         # the point X
        a2, b2 = a1-a0, b1-b0               # the fractional parts

        if a2 + b2 < 1:
            return self._qfrac(a1, b1, 1)   # the point X
        a3, b3 = a1 + a1 - 1, b1 + b1 - 1
        return self._qfrac(a3, b3, 2)       # the midpoint

    @property
    def southwest(self):
        """rounds to the southwest (lower left, same as floor)"""
        return floor(self)

    @property
    def southeast(self):
        """rounds to the southeast (lower right)

        Truncates in the southeast direction:

                 +-----+
                 | U   |   Lower triangle rounds to corner X
                 |   L |   Upper triangle rounds to midpoint
                 +-----+
                        X   i is north of zero
                            1 is east of zero
        """
        a0, b0 = self.real, self.imag
        a1, b1 = ceil(a0), floor(b0)        # the point X
        a2, b2 = a1-a0, b0-b1               # the fractional parts

        if a2 + b2 < 1:
            return self._qfrac(a1, b1, 1)   # the point X
        a3, b3 = a1 + a1 - 1, b1 + b1 + 1
        return self._qfrac(a3, b3, 2)       # the midpoint

    @property
    def northeast(self):
        """rounds to the northeast (upper right, same as ceil)"""
        return ceil(self)

    @property
    def northwest(self):
        """rounds to the northwest (upper left)

        Truncates in the northwest direction:

                X
                 +-----+
                 | U   |   Upper triangle rounds to corner X
                 |   L |   Lower triangle rounds to midpoint
                 +-----+
                            i is north of zero
                            1 is east of zero
        """
        a0, b0 = self.real, self.imag
        a1, b1 = floor(a0), ceil(b0)        # the point X
        a2, b2 = a0-a1, b1-b0               # the fractional parts

        if a2 + b2 < 1:
            return self._qfrac(a1, b1, 1)   # the point X
        a3, b3 = a1 + a1 + 1, b1 + b1 - 1
        return self._qfrac(a3, b3, 2)       # the midpoint

    def __round__(self, ndigits=0):
        """round to the nearest Eisensteinian integer (minimize the norm)"""
        if ndigits != 0:
            raise NotImplementedError("nearest only, ndigits must be 0")
        if self.is_int:
            return self

        z = self.southwest
        n = (self-z).sqnorm
        alternates = [self.southeast, self.northeast, self.northwest]
        for w in alternates:
            m = (self-w).sqnorm
            if m < n:
                z = w
                n = m
        return z

    @classmethod
    def EisensteinFrac(cls, z:(int, Fraction, "Root2Frac", _QFrac)):
        """converts the argument to an Eisensteinian rational"""
        if isinstance(z, cls):
            return z
        if type(z) == int:
            return cls(z, 0, 1)
        if type(z) == Fraction:
            return cls(z.numerator, 0, z.denominator)
        if isinstance(z, _QFrac):
            a, b, c, d = z._value
            if b !=0 and d != -3:
                raise TypeError(f"{d=}!=-3 for Eisensteinian rational")
            return cls(a, b, c)
        raise TypeError("incompatible type for Eisenstenian (D=-3) conversion")

    def __floordiv__(self, other):
        """rounding division"""
        if not isinstance(other, EisensteinFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        return round(self / other)

    def __rfloordiv__(self, other):
        """reversed rounding division"""
        if not isinstance(other, EisensteinFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        return round(self.reciprocal * other)

    def __mod__(self, other):
        """modulus (rounding division)"""
        if not isinstance(other, EisensteinFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self / other)
        return self - q * other

    def __rmod__(self, other):
        """reversed modulus (rounding division)"""
        if not isinstance(other, EisensteinFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self.reciprocal * other)
        return - self * q + other

    def __divmod__(self, other):
        """rounding division with remainder (division algorithm)"""
        if not isinstance(other, EisensteinFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self / other)
        m = self - q * other
        return q, m

    def __rdivmod__(self, other):
        """reversed rounding division with remainder (division algorithm)"""
        if not isinstance(other, EisensteinFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self.reciprocal * other)
        m = - self * q + other
        return (q, m)

# END utilities.eisenstein_frac
