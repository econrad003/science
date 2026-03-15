"""
utilities.inequalities - inequalities involving quadratic rationals
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a collection of utilities for doing approximations with
    quadratic rationals.  See the individual methods for more information.

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
from math import floor, ceil, isqrt
from fractions import Fraction

from utilities._quadratic import _QFrac

_types = (int, Fraction, _QFrac)
_ordinary_types = (int, Fraction)

    # for real types, we want to know whether a quantity is positive,
    # negative, or zero.  The classes are mutually exclusive.

def is_real(z:_types) -> bool:
    """returns True if the quadratic rational is a real quantity"""
    if isinstance(z, _ordinary_types):
        return True             # special cases
    if not isinstance(z, _QFrac):
        raise TypeError("the argument must be a quadratic rational")
    if z.discriminant > 0:
        return True
    return z.imag == 0

def is_positive(z:_types) -> bool:
    """returns True if the quantity is positive

    A ValueError exception is raised if the value is complex imaginary.
    """
    if not is_real(z):
        raise ValueError("the argument must be real")
    if isinstance(z, _ordinary_types):
        return z > 0
    if z.discriminant < 0:
        return z.real > 0
    return z != 0 and ifloor(z) >= 0

def is_negative(z:_types) -> bool:
    """returns True if the quantity is negative

    A ValueError exception is raised if the value is complex imaginary.
    """
    if not is_real(z):
        raise ValueError("the argument must be real")
    if isinstance(z, _ordinary_types):
        return z < 0
    if z.discriminant < 0:
        return z.real < 0
    return z != 0 and iceil(z) <= 0

def is_zero(z:_types) -> bool:
    """returns True if the quantity is zero"""
    return z == 0

    # For complex types, we want to to identify which quadrant the number
    # is in.  Zero is not in any quadrant.  The quadrants are defined
    # relative to a semi-axis in the Argand plane.  For example points
    # in quadrant I include counterclockwise rotations of the x-axis
    # though angles of at least 0 degrees and strictly less than 90
    # degrees.  The Argand plane is partitioned into 0 and the four
    # quadrants.

def quadrant_I(z:_types) -> bool:
    """returns True if the quantity is in the first quadrant

    The first quadrant of the Argand plane includes the points where
    x is positive and y is non-negative.

    For a real quantity, the only requirement is that the quantity be
    positive.  This includes complex quantities whose imaginary part
    is zero.
    """
    if is_real(z):
        return is_positive(z)
    return z.real > 0 and z.imag >= 0

def quadrant_II(z:_types) -> bool:
    """returns True if the quantity is in the second quadrant

    The second quadrant of the Argand plane includes the points where
    y is positive and x is non-positive.

    There are no real quantities in this quadrant.
    """
    if is_real(z):
        return False
    return z.real <=0 and z.imag > 0

def quadrant_III(z:_types) -> bool:
    """returns True if the quantity is in the third quadrant

    The third quadrant of the Argand plane includes the points where
    x is negative and y is non-positive.

    For a real quantity, the only requirement is that the quantity be
    negative.  This includes complex quantities whose imaginary part
    is zero.
    """
    if is_real(z):
        return is_negative(z)
    return z.real < 0 and z.imag <= 0

def quadrant_IV(z:_types) -> bool:
    """returns True if the quantity is in the fourth quadrant

    The fourth quadrant of the Argand plane includes the points where
    y is negative and x is non-negative.

    There are no real quantities in this quadrant.
    """
    if is_real(z):
        return False
    return z.real >=0 and z.imag < 0

        # To get an estimate of a real quadratic integer, we first need to
        # estimate the irrational part.

def bounds(z:_types) -> tuple:
    """find a bounding interval for z

    The interval will be [floor(z), ceil(z)] expressed as an ordered pair.
    Note that if z is an ordinary integer, then this interval is [z,z].
    Otherwise the values will differ by 1.
    """
    if not is_real(z):
        raise ValueError("the argument must be real")
    if isinstance(z, _ordinary_types):
        return floor(z), ceil(z)
    if z.imag == 0:
        return floor(z.real), ceil(z.real)
            # we have a real quadratic rational which is not rational
    a, b, c, d = z._value
    assert d>0
    m = isqrt(b*b*d)
    if b < 0:
        m = - (m + 1)
    z0 = floor(Fraction(a+m, c))
    z1 = ceil(Fraction(a+m+1, c))
    assert z1 > z0
    while z1 > z0 + 1:              # binary search (inefficient)
        z2 = floor((z0 + z1) / 2)
        if is_positive(z-z2):
            z0 = z2
        else:
            z1 = z2
    return z0, z1

def ifloor(z:_types) -> int:
    """returns the integer floor"""
    a, b = bounds(z)
    return a

def iceil(z:_types) -> int:
    """returns the integer ceiling"""
    a, b = bounds(z)
    return b

class ContinuedFraction(object):
    """a continued fraction for a quadratic rational

    Note that if the number is rational, the continued fraction terminates.

    For quadratic rationals that are irrational, the continued fraction is
    repeating.
    """

    __slots__ = ("__z", "__head", "__tail", "__A", "__B")

    def __init__(self, z:_types, debug:bool=False):
        """constructor"""
        self.__A = list([0, 1])
        self.__B = list([1, 0])
        if not isinstance(z, _types):
            raise TypeError("the argument must be a quadratic rational")
        if not is_real(z):
            raise ValueError("the argument must be real")
        if isinstance(z, int):
            return self.__trivial(z, debug)
        if isinstance(z, Fraction):
            return self.__rational(z, debug)
                # quadratic rational
        if z.imag == 0:
            return self.__rational(z.real, debug)
        self.__irrational(z, debug)

    def __trivial(self, z:int, debug:bool):
        """integer -> [z]"""
        self.__z = z
        if debug:
            print(f"__trivial: z={z}")
        self.__head = (z, )
        self.__tail = tuple()           # empty list

    def __rational(self, z:Fraction, debug:bool):
        """fraction -> [a0; a1, a2, a3, ..., an]"""
        if z.denominator == 1:
            return self.__trivial(z.numerator, debug)
        self.__z = z
        if debug:
            print(f"__rational: z={z}")
        self.__tail = tuple()           # empty list since terminating
        head = list()
        while True:
            q = floor(z)                # integer part
            r = z - q                   # fractional part
            head.append(q)
            if debug:
                print(f"__rational: z={z}, q={q}, r={r}")
            if r == 0:
                break
            z = 1/r
        self.__head = tuple(head)

    def __irrational(self, z:_QFrac, debug:bool):
        """irrational quadratic rational -> [a0; a1, ..., ak, (b1, ..., bj)]"""
        self.__z = z
        if debug:
            print(f"__irrational: z={z}  {z}/{1}")
        head = list()
        qs = list()
        qrs = dict()                     # remainders map
        q = ifloor(z)                   # integer part
        r = z - q
        qs.append(q)
        if debug:
            print(f"__irrational: z={z}, q={q}, r={r}")
        z = r.reciprocal
        n = 1
        while True:
            q = ifloor(z)
            r = z - q
            if debug:
                print(f"__irrational: z={z}, q={q}, r={r}")
            if (q,r) in qrs:
                repeat_to = qrs[(q,r)]
                break
            qs.append(q)
            qrs[(q,r)] = n
            n += 1
            z = r.reciprocal
        # print("repeat_to:", repeat_to)
        # print("qs:", qs)
        self.__head = tuple(qs[:repeat_to])
        self.__tail = tuple(qs[repeat_to:])
        if debug:
            print(f"\t__irrational: result = {self}")

    @property
    def is_terminating(self) -> bool:
        """equivalently, z is rational"""
        return len(self.__tail) == 0

    def __getitem__(self, index:int):
        """return the indexed quotient"""
        if index < 0:
            raise IndexError("index must be non-negative")
        if index < len(self.__head):
            return self.__head[index]
        if len(self.__tail) == 0:
            return 0
        index = index - len(self.__head)
        index %= len(self.__tail)
        return self.__tail[index]

    def __len__(self):
        """returns the length if the continued fraction is terminating"""
        return len(self.__head) + len(self.__tail)

    def __str__(self):
        """returns the displayed form"""
        # print(self.__head, self.__tail)
        s = f"[{self[0]};"
        m = len(self.__head)
        n = len(self.__tail)
        if m > 1:
            s += f" {self[1]}"
            for i in range(2, m):
                s += f",{self[i]}"
        if n > 0:
            s += f" | {self[m]}"
            for i in range(1, n):
                s += f",{self[m+i]}"
        s += "]"
        return s

    def __a(self, m:int) -> int:
        """helper for a(n)"""
        k = len(self.__A)
        for j in range(k, m+1):
            q = self[j-2]
            a = q * self.__A[j-1] + self.__A[j-2]
            # print(f"{j:5} q={q:5} a={self.__A[j-1]:10} {self.__A[j-2]:10} -> {a:10}")
            self.__A.append(a)

    def __b(self, m:int) -> int:
        """helper for b(n)"""
        k = len(self.__B)
        for j in range(k, m+1):
            q = self[j-2]
            b = q * self.__B[j-1] + self.__B[j-2]
            # print(f"{j:5} q={q:5} b={self.__B[j-1]:10} {self.__B[j-2]:10} -> {b:10}")
            self.__B.append(b)

    def a(self, n:int) -> int:
        """determine the numerator of the nth convergent"""
        if type(n) != int:
            raise TypeError("n must be an integer")
        if n < -1:
            raise ValueError("n must be at least -1")
        # print(f"TRYING {n=}  A={self.__A}")
        try:
            return self.__A[n+1]
        except IndexError:
            self.__a(n+1)
        # print(f"FETCHING {n=}  A={self.__A}")
        return self.__A[n+1]

    def b(self, n:int) -> int:
        """determine the denominator of the nth convergent"""
        if type(n) != int:
            raise TypeError("n must be an integer")
        if n < -1:
            raise ValueError("n must be at least -1")
        # print(f"TRYING {n=}  B={self.__B}")
        try:
            return self.__B[n+1]
        except IndexError:
            self.__b(n+1)
        # print(f"FETCHING {n=}  B={self.__B}")
        return self.__B[n+1]

    def convergent(self, n:int) -> Fraction:
        """determine the nth convergent of a continued fraction"""
                # Do we already have the convergent?
        a = self.a(n)
        b = self.b(n)
        return float('inf') if b == 0 else Fraction(a, b)

__all__ = ('ContinuedFraction', 'bounds', 'iceil', 'ifloor',
           'is_negative', 'is_positive', 'is_real', 'is_zero',
           'quadrant_I', 'quadrant_II', 'quadrant_III', 'quadrant_IV')

# END utilities.inequalities
