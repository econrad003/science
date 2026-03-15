"""
utilities.golden_frac - root 5 rational numbers module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module provides the following classes:

        GoldenFrac - a quadratic rational number class (with discriminant
            D=5) derived from class _QFrac.

    The name comes from the golden ratio:

             1 + √5
        φ = --------
               2

    The golden rational numbers are complex numbers of the form

             a + bφ    a + b(1 + b√5)/2   (2a+b) + b√5
            -------- = ---------------- = ------------
               c             c                 2c

    where a, b and c are integers (with c ≠ 0).  The set of golden
    rationals is denoted ℚ(√5) or, equivalently ℚ(φ).

    We can write these as rational linear combinations of 1 and √5:

             a + b√5     a + b(-1 + (1+√5))     (a-b) + 2φ
            --------- = -------------------- = ------------
               c                c                    c

    An important subset is the set of Brounckerian integers, where c = 1.
    These form a Euclidean domain as they share a number of important
    number-theoretic properties with the ordinary integers ℤ, for example:

        1.  division algorithm;
        2.  unique factorization (up to units);
        3.  every ideal is a principal ideal;
        4.  the norm is multiplicative.

    The set of Brounckerian integers is denoted ℤ[φ].

    The golden integers have infinitely many units.  These may be
    found using solutions to the following Pell equations:
        a² - 5b² = 1,
        a² - 5b² = -1,
    where a and b are integers.  (The solutions are, in fact, consecutive
    Fibonacci numbers.)

    The units have square norm values of 1 and -1.  For example:

        577² - 2·408² = 332,929 - 332,928 = 1.

    Since N(a + b√2) = a² - 2b², it follows that 577+408√2 is a Brounkerian
    unit.

    Note that 577/408 ≈ 1.41421568627 ≈ √2.  (This is not an accident!)

FINDING INTEGER SOLUTIONS TO PELL'S EQUATION (D=2)

    We note first that (a,b)=(1,0) and (a,b)=(-1,0) are both solutions.
    These correspond to the units 1 and -1.

    We can get other solutions by looking for best rational approximations
    of φ.  We use a modification of the continued fraction algorithm
    where we "divide by 1" to break the estimate up into an integer part
    q and an irrational fractional part r:
        1 + √5       √5 - 1                                   √5 - 1
        ------ = 1 + ------                         q=1     r=------
          2             2                                        2

          2      2(√5 + 1)   1 + √5
        ------ = --------- = ------
        √5 - 1      5 - 1      2

    Since our remainder is an exact repeat (and this happen whenever and
    only when the number we are estimating is a solution to some quadratic
    equation), it follows that our continued fraction repeats:

                           1 + √5
        [1; 1,1,1,1,...] = ------ = φ
                             2


    (We have omitted a few details, but this can be made rigorous.)

    Now we "recover" φ from the sequence of quotients:

        row  q      A       B       estimate (A/B)      A² - 5B²
       --- --- -----   -----       --------------      --------
        -1          0       1                              -5        -1
         0          1       0                               1         5
         1   1      1       1       1                      -4         4
         2   1      2       1       2                      -1        19
         3   1      3       2       1.5                    -1
         4   1      5       3       1.66666666667           4
         5   2      8       5       1.6                    -1
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

class GoldenFrac(_QFrac):
    """the Golden rational numbers ℚ(√5)"""

            # coefficients of the Golden normal form

    __slots__ = ("__A", "__B")

    def __init__(self, a:int, b:int, c:int, d:int=5):
        """constructor

        If the value of d is anything except 5, then a ValueError
        exception is raised.  This parameter is retained for
        compatibility with the base class.
        """
        super().__init__(a, b, c, d)
        if d != 5:
            raise ValueError("The value of the base must be d=5.")

                # coefficient A + Bω
        self.__A = Fraction(a-b, c)
        self.__B = Fraction(b+b, c)

    @property
    def is_int(self) -> bool:
        """checks whether the given Golden rational is integral"""
        a, b, c, d = self._value
        if c == 1:
            return True
        if c == 2:
            return a % 2 == 1 == b % 2
        return False

    @property
    def is_unit(self) -> bool:
        """checks whether the given Brouncker rational is an integer unit

        There are two requirements:
            1) must be a Brouncker integer
            2) norm must be 1 or -1
        """
        return self.is_int and abs(self.sqnorm) == 1

    @property
    def phi(self):
        """returns φ"""
        return self._qfrac(1, 1, 2)

    @property
    def phibar(self):
        """returns the conjugate of φ"""
        return self._qfrac(1, -1, 2)

    @property
    def GNF(self) -> tuple:
        """returns the coefficients (A,B) of A+Bω in the Eisenstein expansion"""
        return self.__A, self.__B

    @property
    def GNFstr(self) -> str:
        """returns the ENF expansion as a string"""
        if self.imag == 0:
            return str(self.real)

        a, b = self.GNF
        if a == 0:
            if b.denominator == 1:
                if b.numerator == 1:
                    return "φ"
                return f"{b.numerator}φ"
            return f"{b.numerator}φ/{b.denominator}"

        if abs(b.numerator) == 1:
            if b.numerator == 1:
                imag = "+φ"
            else:
                imag = "-φ"
        else:
            imag = f"{b.numerator:+}φ"
        return str(a) + imag

            # ROUNDING ROUTINES

    def _Dnorm(self, other):
        """return the unsigned square norm of the difference"""
        return abs((self-other).sqnorm)

    def __round__(self, ndigits=0):
        """round to the nearest modulo 5 integer (minimize the norm)"""
        if ndigits != 0:
            raise NotImplementedError("nearest only, ndigits must be 0")
        if self.is_int:
            return self
            # first possibility
        z = self.southwest
        # print(f">>> {self}  z={z}  norm of diff={self._Dnorm(z)}")
        for w in (self.southeast, self.northeast, self.northwest):
            # print(f">>> {self}  z={w}  norm of diff={self._Dnorm(w)}")
            if self._Dnorm(z) > self._Dnorm(w):
                z = w
        return z

    def __trunc__(self):
        """round toward zero"""
        if not self.is_int:
            if self.imag >= 0:
                if self.real >= 0:                  # Quadrant I
                    return self.southwest
                else:                               # Quadrant II
                    return self.southeast
            else:                           # self.imag < 0
                if self.real < 0:                   # Quadrant III
                    return self.northeast
                else:                               # Quadrant IV
                    return self.northwest
        return self

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
        return self.southwest

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
        return self.northeast

    @property
    def southwest(self):
        """rounds to the southwest (lower left, same as floor)"""
        if self.is_int:
            return self
        a = floor(self.real)
        b = floor(self.imag)
        z = self._qfrac(a, b, 1)
        w = z + self.phi
        if self._Dnorm(z) > self._Dnorm(w):
            return w
        return z

    @property
    def southeast(self):
        """rounds to the southeast (lower right)"""
        if self.is_int:
            return self
        a = ceil(self.real)
        b = floor(self.imag)
        z = self._qfrac(a, b, 1)
        w = z - self.phibar
        if self._Dnorm(z) > self._Dnorm(w):
            return w
        return z

    @property
    def northeast(self):
        """rounds to the northeast (upper right, same as ceil)"""
        if self.is_int:
            return self
        a = ceil(self.real)
        b = ceil(self.imag)
        z = self._qfrac(a, b, 1)
        w = z - self.phi
        if self._Dnorm(z) > self._Dnorm(w):
            return w
        return z

    @property
    def northwest(self):
        """rounds to the northwest (upper left)"""
        if self.is_int:
            return self
        a = floor(self.real)
        b = ceil(self.imag)
        z = self._qfrac(a, b, 1)
        w = z + self.phibar
        if self._Dnorm(z) > self._Dnorm(w):
            return w
        return z

    @classmethod
    def GoldenFrac(cls, z:(int, Fraction, "GoldenFrac", _QFrac)):
        """converts the argument to a Gokdeb (discriminant 5) rational"""
        if isinstance(z, cls):
            return z
        if type(z) == int:
            return cls(z, 0, 1)
        if type(z) == Fraction:
            return cls(z.numerator, 0, z.denominator)
        if isinstance(z, _QFrac):
            a, b, c, d = z._value
            if b !=0 and d != 5:
                raise TypeError(f"{d=} incompatible with Golden rational")
            return cls(a, b, c)
        raise TypeError("incompatible type for Golden rational conversion")

    def __floordiv__(self, other):
        """rounding division"""
        if not isinstance(other, GoldenFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        return round(self / other)

    def __rfloordiv__(self, other):
        """reversed rounding division"""
        if not isinstance(other, GoldenFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        return round(self.reciprocal * other)

    def __mod__(self, other):
        """modulus (rounding division)"""
        if not isinstance(other, GoldenFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self / other)
        return self - q * other

    def __rmod__(self, other):
        """reversed modulus (rounding division)"""
        if not isinstance(other, GoldenFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self.reciprocal * other)
        return - self * q + other

    def __divmod__(self, other):
        """rounding division with remainder (division algorithm)"""
        if not isinstance(other, GoldenFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self / other)
        m = self - q * other
        return q, m

    def __rdivmod__(self, other):
        """reversed rounding division with remainder (division algorithm)"""
        if not isinstance(other, GoldenFrac):
            if type(other) not in (int, Fraction):
                return NotImplemented
        q = round(self.reciprocal * other)
        m = - self * q + other
        return (q, m)

# END utilities.rootm2_frac
