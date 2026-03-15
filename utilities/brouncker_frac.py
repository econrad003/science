"""
utilities.brouncker_frac - root 2 rational numbers module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module provides the following classes:

        BrounckerFrac - a quadratic rational number class (with discriminant
            D=2) derived from class _QFrac.

    I chose the name Brouncker because William Brouncker (1620-1684) studied
    the equation:
        a² - 2b² = 1,                                       (1)
    where a and b are integers. 

    This is a special case of Pell's equation:
        a² - Db² = 1,                                       (2)
    where a and b are integers, and D>1 and D is a square-free integer.

    Leonhard Euler (1707-1783) mistakenly attributed the equation to John
    Pell (1611-1685).  Indian mathematicians including Brahmagupta (c 598-668 CE)
    and Bhāskara II (c 1114-1185) also studied cases of the equation, and the
    D=2 case was studied by the Pythagoreans and early mathematicians in India.
    (Brouncker was by no means first.)

    For lack of a better name, I will refer to the quadratic rational numbers
    with discriminant 2 as the Brounckerian rationals and the integer subclass
    as the Brounckerian integers.  (This name is by no means standard and I
    am not making a formal proposal.)

    The Brouncker rational numbers are complex numbers of the form

             a + b√2
            ---------                                       (3)
               c

    where a, b and c are integers (with c ≠ 0).  The set of Brounckerian
    rationals is denoted ℚ(√2).

    An important subset is the set of Brounckerian integers, where c = 1.
    These form a Euclidean domain as they share a number of important
    number-theoretic properties with the ordinary integers ℤ, for example:

        1.  division algorithm;
        2.  unique factorization (up to units);
        3.  every ideal is a principal ideal;
        4.  the norm is multiplicative.

    The set of Brounckerian integers is denoted ℤ[√2].

    The Brounckerian integers have infinitely many units.  These may be
    found using solutions to Equation (1) and to the related equation:
        a² - 2b² = -1,                                       (4)
    where a and b are integers.

    The units have square norm values of 1 and -1.  For example:

        577² - 2·408² = 332,929 - 332,928 = 1.

    Since N(a + b√2) = a² - 2b², it follows that 577+408√2 is a Brounkerian
    unit.

    Note that 577/408 ≈ 1.41421568627 ≈ √2.  (This is not an accident!)

FINDING INTEGER SOLUTIONS TO PELL'S EQUATION (D=2)

    We note first that (a,b)=(1,0) and (a,b)=(-1,0) are both solutions.
    These correspond to the units 1 and -1.

    We can get other solutions by looking for best rational approximations
    of √2.  We use a modification of the continued fraction algorithm
    where we "divide by 1" to break the estimate up into an integer part
    q and an irrational fractional part r:

        √2 = 1 + (√2 - 1)                           q=1     r=√2 - 1

           1     √2 + 1
        ------ = ------ = √2 + 1 = 2 + (√2 - 1)     q=2     r=√2 - 1
        √2 - 1    2 - 1

    Since our remainder is an exact repeat (and this happen whenever and
    only when the number we are estimating is a solution to some quadratic
    equation), it follows that our continued fraction repeats:

        [1; 2,2,2,2,...] = √2

    (We have omitted a few details, but this can be made rigorous.)

    Now we "recover" √2 from the sequence of quotients:

        row  q      A       B       estimate (A/B)      A² - 2B²
        --- --- -----   -----       --------------      --------
        -1          0       1                              -2
         0          1       0                               1
         1   1      1       1       1                      -1
         2   2      3       2       1.5                     1
         3   2      7       5       1.4                    -1
         4   2     17      12       1.41666666667           1
         5   2     41      29       1.41379310345          -1
         6   2     99      70       1.41428571429           1
         7   2    239     169       1.41420118343          -1
         8   2    577     408       1.41421568627           1
         9   2   1393     985       1.41421319797          -1
        10   2   3363    2378       1.41421362489           1
                               √2 ≈ 1.41421356237

    First let q[n], A[n], and B[n], respectively, be the values of
    q, A, and B in row n.  Note that q is only in rows 1 through 10
    while there are values of A and B in rows -1 through 10.

    The first two rows are used to set up the recurrences:
        A[n] = q[n] A[n-1] + A[n-2]
        B[n] = q[n] B[n-1] + B[n-2]
    for n = 1, 2, 3, ...

    If we divide A[n] by B[n] we get an approximation of the square root
    of 2. With an increase of two rows, we get roughly one additional digit
    of precision in our estimate.

    For our purposes, it is the last column that is especially interesting.
    From row 0 on, A² - 2B² is either 1 or -1.  Row zero gives the
    multiplicative identity 1.  Rows 2, 3 and 4 give the units 1+√2,
    3+2√2, and 7+5√2 and so on.  These alternate in square norm, either 1
    in even rows or -1 in odd rows.  The even rows are solutions in
    non-negative integers to Pell's equation (1), while those in odd rows,
    except row -1, are solutions to the variant equation (4).

    To get units in other quadrants, change the sign of the components
    accordingly.  From 1+√2 we get √2-1, -1-√2, and 1-√2 in quadrants II,
    III and IV, respectively.

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

class BrounckerFrac(_QFrac):
    """the Brounckerian rational numbers ℚ(√2)"""

    def __init__(self, a:int, b:int, c:int, d:int=2):
        """constructor

        If the value of d is anything except 2, then a ValueError
        exception is raised.  This parameter is retained for
        compatibility with the base class.
        """
        super().__init__(a, b, c, d)
        if d != 2:
            raise ValueError("The value of the base must be d=2.")

    @property
    def is_int(self) -> bool:
        """checks whether the given Brouncker rational is integral

        There is one requirement: the denominator must be 1.
        """
        return self._value[2] == 1

    @property
    def is_unit(self) -> bool:
        """checks whether the given Brouncker rational is an integer unit

        There are two requirements:
            1) must be a Brouncker integer
            2) norm must be 1 or -1
        """
        return self.is_int and abs(self.sqnorm) == 1

            # ROUNDING ROUTINES

    def __round__(self, ndigits=0):
        """round to the nearest modulo -2 integer (minimize the norm)"""
        if ndigits != 0:
            raise NotImplementedError("nearest only, ndigits must be 0")
        a = round(self.real)
        b = round(self.imag)
            # first possibility
        z = self._qfrac(a, b, 1)
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
    def BrounckerFrac(cls, z:(int, Fraction, "BrounckerFrac", _QFrac)):
        """converts the argument to a Brouncker (discriminant 2) rational"""
        if isinstance(z, cls):
            return z
        if type(z) == int:
            return cls(z, 0, 1)
        if type(z) == Fraction:
            return cls(z.numerator, 0, z.denominator)
        if isinstance(z, _QFrac):
            a, b, c, d = z._value
            if b !=0 and d != 2:
                raise TypeError(f"{d=} incompatible with Brouncker rational")
            return cls(a, b, c)
        raise TypeError("incompatible type for Brouncker rational conversion")

    def __floordiv__(self, other):
        """rounding division"""
        if not isinstance(other, BrounckerFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        return round(self / other)

    def __rfloordiv__(self, other):
        """reversed rounding division"""
        if not isinstance(other, BrounckerFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        return round(self.reciprocal * other)

    def __mod__(self, other):
        """modulus (rounding division)"""
        if not isinstance(other, BrounckerFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self / other)
        return self - q * other

    def __rmod__(self, other):
        """reversed modulus (rounding division)"""
        if not isinstance(other, BounckerFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self.reciprocal * other)
        return - self * q + other

    def __divmod__(self, other):
        """rounding division with remainder (division algorithm)"""
        if not isinstance(other, BrounckerFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self / other)
        m = self - q * other
        return q, m

    def __rdivmod__(self, other):
        """reversed rounding division with remainder (division algorithm)"""
        if not isinstance(other, BrounckerFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self.reciprocal * other)
        m = - self * q + other
        return (q, m)

# END utilities.brouncker_frac
