"""
utilities._quadratic - quadratic rationals base module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module provides the following classes:

        _QFrac - a quadratic rational number class.

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
from math import sqrt, isqrt, gcd
from numbers import Complex
from fractions import Fraction

from utilities.primality import is_square_free

def _tsqrt(d:int) -> (int, float):
    """modified square root function (typed square root)

    The input d must be a non-negative integer.

    If d is a perfect square, then the return value is an int and
    is the exact value of the square root.

    Otherwise, the return value is a float.
    """
    if type(d) != int or d < 0:
        raise RuntimeError("'d' must be a non-negative integer")
    root = isqrt(d)
    if root * root == d:
        return root
    return sqrt(d)

class _QFrac(Complex):
    """a quadratic rational class"""

    __slots__ = ("__value", )

    DISPLAY_WARNING = True
    ZERO_RAISE_ZERO = False     # if true: 0**0 == 1 (for power series)
    IMATH = "i"                 # change to "j" for engineering

    @classmethod
    def engineering(cls):
        """changes IMATH to j"""
        cls.IMATH = "j"

    @classmethod
    def mathematics(cls):
        """changes IMATH to back to i"""
        cls.IMATH = "i"

    def __init__(self, a:int, b:int, c:int, d:int):
        """construct a quadratic rational number

        POSITIONAL ARGUMENTS

            a, b, c, d
                integers.  Represent the number (a + b sqrt(d)) / c.  The
                integer d is called the base.

        EXCEPTIONS

            ZeroDivisionError is raised if c is zero.

            ValueError is raised if d is a perfect square.

        EXAMPLES
            5 + 2i:             _QFrac(5, 2, 1, -1)
            0                   _QFrac(0, 0, 1, -1)
                The value of 'd' can be any non-square integer
            6 + sqrt(2)         _QFrac(6, 1, 1, 2)
            6 + sqrt(2)i        _QFrac(6, 1, 1, -2)
            (1 + sqrt(5))/2     _QFrac(1, 1, 2, 5)
                This is known as the golden ratio.
            sqrt(2)             _Qfrac(0, 1, 1, 2)
                The Babylonians had a very nice estimate of this number
                in the second millenium BCE.  For this reason, the square
                root of two is occasionally referred to as the
                Babylonian constant.
        """
        if not is_square_free(d):
            raise ValueError(f"'d' must be a square-free integer ({d=})")
        if d == 1:
            raise ValueError("'d' must not be equal to 1")
        if type(a) != int:
            raise TypeError("'a' must be an int")
        if type(b) != int:
            raise TypeError("'b' must be an int")
        if type(c) != int:
            raise TypeError("'c' must be an int")
#        if type(d) != int:
#            raise TypeError("'d' must be an int")
        if c == 0:
            raise ZeroDivisionError("'c' may not be zero")
#        if d in {0, 1}:
#            raise ValueError("'d' must not be 0 or 1")
        self.__value = (a, b, c, d)
        self._normalize()

    def _qfrac(self, a, b, c, d=None):
        """make a new value in the current class"""
        if d == None:               # use same base
            d = self.__value[3]
        return self.__class__(a, b, c, d)

    def _normalize(self):
        """rudimentary normalization

        All we do here is make sure the denominator c is positive and
        the gcd of the values of a, b, and c is 1
        """
        a, b, c, d = self.__value
        factor = gcd(a, b, c)
        if factor > 1:
            a //= factor
            b //= factor
            c //= factor
        if c < 0:
            a *= -1
            b *= -1
            c *= -1
        self.__value = (a, b, c, d)

    def __repr__(self):
        """representation"""
        clsname = self.__class__.__name__
        a, b, c, d = self.__value
        return f"{clsname}(({a}{b:+}√{d})/{c})"

    def __str__(self):
        """string form"""
        a, b, c, d = self.__value
        if b == 0:
            return str(Fraction(a, c))

        LB, RB = "(", ")"
        IMATH = self.__class__.IMATH
        if d == -1:
            ROOT = IMATH
        else:
            ROOT = "√" + str(d) if d>0 else IMATH + "√" + str(-d)
        DIV = "/"

        if a == 0:
            if abs(b) == 1:
                TOP = ROOT if b == 1 else "-" + ROOT
            else:
                TOP = str(b) + ROOT
            if c == 1:
                return TOP
            return TOP + DIV + str(c)

        B = "+" if b>0 else "-"
        B += ROOT if abs(b)==1 else str(abs(b)) + ROOT
        TOP = str(a) + B
        if c == 1:
            return TOP
        return f"{LB}{TOP}{RB}/{c}"

    @property
    def TeXform(self):
        """LaTeX string form"""
        a, b, c, d = self.__value
        if a == 0 == b:
            return "0"
        LB, RB = "{", "}"
        ROOT = "\\sqrt"
        FRAC = "\\frac"
        I = "\\imath"
        if b == 0:
            B = ""
        else:
            B = "+" if b > 0 else "-"
            if abs(b) == 1:
                B += "" if d > 0 else I
            else:           # abs(b) > 1
                B += str(abs(b)) if d > 0 else str(abs(b)) + I
            if abs(d) != 1:
                B += f"{ROOT}{LB}{abs(d)}{RB}"
        TOP = B if a == 0 else f"{a}{B}"
        if TOP[0] == "+":
            TOP = TOP[1:]
        if c == 1:
            return TOP 
        return f"{FRAC}{LB}{TOP}{RB}{LB}{c}{RB}"

    @property
    def _value(self) -> list:
        """returns the value list"""
        return list(self.__value)

    def conjugate(self):
        """returns the d-conjugate of the number"""
        a, b, c, d = self.__value
        return self._qfrac(a, -b, c)

    @property
    def real(self):
        """returns the rational part of the number"""
        a, b, c, d = self.__value
        re = Fraction(a, c)
        if re.denominator == 1:
            return re.numerator
        return re

    @property
    def imag(self):
        """returns the rational part of the number"""
        a, b, c, d = self.__value
        im = Fraction(b, c)
        if im.denominator == 1:
            return im.numerator
        return im

    @property
    def discriminant(self):
        """returns the discriminant"""
        a, b, c, d = self.__value
        return d

    @property
    def numerator(self):
        """returns the numerator"""
        a, b, c, d = self.__value
        if b == 0:
            return a
        return self._qfrac(a, -b, 1)

    @property
    def denominator(self):
        """returns the numerator"""
        a, b, c, d = self.__value
        return c

    @property
    def sqnorm(self):
        """returns the square-norm

        Use this to determine whether the number is a rational integer.
        """
        a, b, c, d = self.__value
        norm = self * self.conjugate()
        if norm.imag == 0:
            return norm.real    # this is what should return!
        if self.__class__.DISPLAY_WARNING:
            print(" *** Multiplication error ***")
            self.__class__.DISPLAY_WARNING = False
        raise Warning("norm's imaginary/irrational part is not zero")

    def __abs__(self):
        """returns the d-relative absolute value"""
        norm = abs(self.sqnorm)
        if type(norm) == int:
            return _tsqrt(norm)
        top = _tsqrt(norm.numerator)
        bottom = _tsqrt(norm.denominator)
        if type(top) == int and type(bottom) == int:
            return Fraction(top, bottom)
        return top / bottom

    def __neg__(self):
        """returns the additive inverse"""
        a, b, c, d = self.__value
        return self._qfrac(-a, -b, c)

    def __pos__(self):
        """returns a copy"""
        a, b, c, d = self.__value
        return self._qfrac(a, b, c)

    def __complex__(self):
        """converts to type complex"""
        a, b, c, d = self.__value
        if d < 0:
            return complex(a / c, b * sqrt(-d) / c)
        return complex((a + b * sqrt(d))/ c)

    def __float__(self):
        """converts to type float"""
        a, b, c, d = self.__value
        if d < 0:
            raise ValueError("'d' must be positive for a float conversion")
        return float((a + b * sqrt(d))/ c)

    def __int__(self):
        """converts to integer type"""
        a, b, c, d = self.__value
        if b == 0 and c == 1:
            return a
        raise NotImplementedError("not a rational integer")

    def __eq__(self, other):
        """checks for equality"""
        a1, b1, c1, d1 = self.__value
        if isinstance(other, _QFrac):
            a2, b2, c2, d2 = other._value
            if b2 == 0:
                d2 = d1
        elif type(other) == int:
            a2, b2, c2, d2 = other, 0, 1, d1
        elif type(other) == Fraction:
            a2, b2, c2, d2 = other.numerator, 0, other.denominator, d1
        else:
            return NotImplemented
        return a1==a2 and b1==b2 and c1==c2 and d1==d2

    def __hash__(self):
        """create a hash"""
        a, b, c, d = self.__value
        if b == 0:
            if c == 1:
                return hash(a)
            else:
                return hash(Fraction(a, c))
        return hash(("_QFrac", self.__value))

    def __add__(self, other):
        """add two quadratic rationals"""
        a1, b1, c1, d1 = self.__value
        if type(other) == int:
            a3 = a1 + c1 * other
            return self._qfrac(a3, b1, c1)
        if type(other) == Fraction:
            a2, c2 = other.numerator, other.denominator
            a3 = a1*c2 + a2*c1
            b3 = b1*c2
            c3 = c1*c2
            return self._qfrac(a3, b3, c3)
        if isinstance(other, _QFrac):
            a2, b2, c2, d2 = other._value
            if d1 != d2:
                raise ValueError("self.d != other.d")
            a3 = a1*c2 + a2*c1
            b3 = b1*c2 + b2*c1
            c3 = c1*c2
            return self._qfrac(a3, b3, c3)
        return NotImplemented

    def __radd__(self, other):
        """add two quadratic rationals"""
        return self + other         # addition is commutative

    def __mul__(self, other):
        """multiply two quadratic rationals"""
        a1, b1, c1, d1 = self.__value
        if type(other) == int:      # scalar multiplication
            a3 = a1 * other
            b3 = b1 * other
            return self._qfrac(a3, b3, c1)
        if type(other) == Fraction: # scalar multiplication
            a2, c2 = other.numerator, other.denominator
            a3 = a1 * a2
            b3 = b1 * a2
            c3 = c1*c2
            return self._qfrac(a3, b3, c3)
        if isinstance(other, _QFrac):
            a2, b2, c2, d2 = other._value
            if d1 != d2:
                raise ValueError("self.d != other.d")
            a3 = a1*a2 + b1*b2*d1
            b3 = a1*b2 + a2*b1
            c3 = c1*c2
            return self._qfrac(a3, b3, c3)
        return NotImplemented

    def __rmul__(self, other):
        """multiply two quadratic rationals"""
        return self * other         # multiplication is commutative

    @property
    def reciprocal(self):
        """compute 1/z

               c              c (a - b√d)        a*c - bc√d
            --------- = --------------------- = ------------
             a + b√d     (a + b√d) (a - b√d)      aa - bbd
        """
        a1, b1, c1, d = self.__value
        if a1 == 0 == b1:
            raise ZeroDivisionError("Reciprocal of zero is undefined")
        a2 = a1 * c1
        b2 = - b1 * c1
        c2 = a1*a1 - b1*b1*d
        return self._qfrac(a2, b2, c2)

    def __pow__(self, other:int):
        """integer powers only"""
        if type(other) != int:
            return NotImplemented
        a1, b1, c1, d = self.__value

            # SPECIAL CASES

        if a1 == 0 == b1:                   # 0^n
            if other > 0:
                return 0
            if other == 0 and self.__class__.ZERO_RAISE_ZERO:
                return 1
            return ZeroDivisionError("non-positive power of zero")

        if other == 0:                      # z^0
            return self._qfrac(1, 0, 1, d)

        if a1 == 1 == c1 and b1 == 0:       # 1^n
            return 1

            # If n is negative, we take (1/z)^(-n)

        if other < 0:
            return self.reciprocal ** (- other)

            # GENERAL CASE
            #   1) write other as a binary numeral
        queue = list()
        while other > 0:
            queue.append(other % 2)         # remainder (0 or 1)
            other //= 2                     # quotient
        # print(queue)

            #   2) initialize
        result = self._qfrac(1, 0, 1, d)
        multiplier = self

            #   3) loop over the digits (low to high):
            #           multiply if the digit is 1
            #           square the multiplier
        for i in queue:
            if i == 1:
                result *= multiplier
            multiplier *= multiplier
        return result

    def __rpow__(self, other):
        """not allowed"""
        return NotImplemented

    def __truediv__(self, other):
        """multiply by the reciprocal"""
        if type(other) == int:
            return self * Fraction(1, other)
        if type(other) == Fraction:
            return self * (1 / other)
        if isinstance(other, _QFrac):
            return self * other.reciprocal
        return NotImplemented

    def __rtruediv__(self, other):
        """multiply by the reciprocal"""
        if type(other) in {int, Fraction}:
            return self.reciprocal * other
        return NotImplemented

# end module utilities.quadratic
