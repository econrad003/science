"""
polynomials.polynomial - univariate rational polynomials module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

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
from numbers import Complex
from fractions import Fraction
from math import ceil, floor, gcd, lcm

from polynomials.superscript import to_superscript

SCALAR = (Fraction, int)
VECTOR = (list, tuple)

class Polynomial(Complex):
    """polynomials in a single variable with rational coefficients"""


    __slots__ = ("__coeffs", "__indeterminate")

    def __to_coeffs(self, a:VECTOR):
        """normalize the coefficients"""
        b = list()
        for item in a:
            if not isinstance(item, Fraction):
                item = Fraction(item)
            b.append(item)
        while len(b)>0 and b[-1]==0:
            b.pop()
        self.__coeffs = tuple(b)

    def __init__(self, *args, indeterminate:str=None):
        """constructor

        POSITIONAL ARGUMENTS

            a0, a1, a2, ... (*args) - coefficients
                a0 is the coefficient of the constant term; ak is the
                coefficient of x^k.  If no arguments are input, the
                polynomial is the zero polynomial.

                If one argument, a Polynomial is provided as a cast, then
                the polynomial is copied with an optional new indeterminate.  

        OPTIONAL ARGUMENTS

            inteterminate - the string to be used when displaying the
                polynomial (default None).  If an indeterminate is
                not given in the cast form, the indeterminate for the
                parent is copied; otherwise, 'x' is used.
        """
                # casts
        if len(args) == 1:
                        # from Polynomial
            if isinstance(args[0], Polynomial):
                self.__to_coeffs(args[0].coeffs)
                if not indeterminate:
                    indeterminate = args[0].indeterminate
                        # from list or tuple
            elif isinstance(args[0], VECTOR):
                self.__to_coeffs(args[0])
            elif isinstance(args[0], SCALAR):
                self.__to_coeffs(args)
            else:
                raise TypeError("Polynomial cast error")
        else:
            self.__to_coeffs(args)
        self.indeterminate = indeterminate if indeterminate else "x"

    @property
    def deg(self) -> int:
        """returns the degree of the polynomial

        The degree of the zero polynomial is defined here as -1.

        For other polynomials, the degree is the degree of the leading
        term, i.e. the term with the highest power of the indeterminate.
        """
        return len(self.__coeffs) - 1

    def __len__(self) -> int:
        """vector length"""
        return len(self.__coeffs)

    def __abs__(self) -> int:
        """returns the degree of the polynomial"""
        return self.deg

    @property
    def indeterminate(self) -> str:
        """indeterminate getter"""
        return self.__indeterminate

    @indeterminate.setter
    def indeterminate(self, other:str):
        """indeterminate setter"""
        self.__indeterminate = str(other) if other else "x"

    @property
    def coeffs(self) -> list:
        """return the coefficients"""
        return list(self.__coeffs)

    def __str__(self):
        """string representation"""
        if self.deg == -1:
            return "0"
        s = ""
        for i in range(len(self.__coeffs)-1, 0, -1):
            coeff = self.__coeffs[i]
            if coeff == 0:
                continue
            s += "+" if coeff > 0 else "-"
            coeff = abs(coeff)
            if coeff.numerator != 1:
                s += str(coeff.numerator)
            if i > 0:
                s += self.__indeterminate
                if i > 1:
                    s += to_superscript(i)
            if coeff.denominator != 1:
                s += f"/{coeff.denominator}"
        coeff = self.__coeffs[0]
        if coeff > 0:
            s += f"+" + str(coeff)
        elif coeff < 0:
            s += str(coeff)
        if s[0] == "+":
            return s[1:]
        return s

    def __repr__(self):
        """representation"""
        return str(self)

    def __hash__(self):
        """returns the hash"""
        if len(self.__coeffs) == 0:
            return hash(0)
        if len(self.__coeffs) == 1:
            return hash(self.__coeffs[0])
        return hash(("Polynomial", self.__coeffs))

    def __eq__(self, other):
        """returns True if the polynomials have the same coefficients

        The indeterminate is ignored.
        """
        if isinstance(other, Polynomial):
            return self.coeffs == other.coeffs
        if len(self.__coeffs) == 0 and other == 0:
            return True
        if len(self.__coeffs) == 1:
            return self.__coeffs[0] == other
        return NotImplemented

    def __pos__(self):
        """returns the polynomial"""
        return self

    def __neg__(self):
        """returns the additive inverse"""
        coeffs = self.coeffs
        for i in range(len(coeffs)):
            coeffs[i] = - coeffs[i]
        return Polynomial(*coeffs, indeterminate=self.indeterminate)

    def constant(self) -> Fraction:
        """returns the constant term"""
        return 0 if len(self.__coeffs) == 0 else self.__coeffs[0]

    def __complex__(self) -> complex:
        """returns the constant term as type complex"""
        return complex(self.constant)

    def imag(self) -> int:
        """returns zero"""
        return 0

    def real(self) -> SCALAR:
        """returns the constant term, converting to int if possible"""
        n = self.constant
        if n.denominator == 1:
            return n.numerator
        return n

    def conjugate(self):
        """returns the polynomial with coefficients reversed"""
        z = self.coeffs
        z.reverse()
        return Polynomial(z, indeterminate=self.indeterminate)

    def __float__(self) -> float:
        """returns the constant term as type float"""
        return float(self.constant)

    def __int__(self) -> int:
        """returns the greatest integer in the constant term"""
        return floor(self.constant)

    @staticmethod
    def vector_sum(x:VECTOR, y:VECTOR) -> VECTOR:
        """vector sum"""
        degx, degy = len(x), len(y)
        z = list()
        if degx > degy:
            degx, degy = degy, degx
            x, y = y, x
        for i in range(degx):
            z.append(x[i] + y[i])
        for i in range(degx, degy):
            z.append(y[i])
        while len(z) > 0 and z[-1] == 0:
            z.pop()
        return z

    @staticmethod
    def vector_diff(x:VECTOR, y:VECTOR) -> VECTOR:
        """vector sum"""
        degx, degy = len(x), len(y)
        z = list()
        if degx > degy:
            degx, degy = degy, degx
            x, y = y, x
        for i in range(degx):
            z.append(x[i] - y[i])
        for i in range(degx, degy):
            z.append(y[i])
        while len(z) > 0 and z[-1] == 0:
            z.pop()
        return z

    def __add__(self, other):
        """polynomial addition"""
        if other == 0:
            return self
        if isinstance(other, Polynomial):
            z = self.vector_sum(self.coeffs, other.coeffs)
            return Polynomial(z, indeterminate=self.indeterminate)
        if isinstance(other, VECTOR):
            z = self.vector_sum(self.coeffs, other)
            return Polynomial(z, indeterminate=self.indeterminate)
        if isinstance(other, SCALAR):
            z = self.vector_sum(self.coeffs, [other])
            return Polynomial(z, indeterminate=self.indeterminate)
        return NotImplemented

    def __sub__(self, other):
        """polynomial subtraction"""
        if other == 0:
            return self
        if isinstance(other, Polynomial):
            z = self.vector_diff(self.coeffs, other.coeffs)
            return Polynomial(z, indeterminate=self.indeterminate)
        if isinstance(other, VECTOR):
            z = self.vector_diff(self.coeffs, other)
            return Polynomial(z, indeterminate=self.indeterminate)
        if isinstance(other, SCALAR):
            z = self.vector_diff(self.coeffs, [other])
            return Polynomial(z, indeterminate=self.indeterminate)
        return NotImplemented

    def __radd__(self, other):
        """reversed addition

        Addition is commutative.
        """
        return self + other

    def __rsub__(self, other):
        """reversed subtraction

        Subtraction is not commutative.
        """
        return - self + other

    @staticmethod
    def scalar_mult(a:SCALAR, x:VECTOR) -> VECTOR:
        """scalar multiplication"""
        y = list()
        for xk in x:
            y.append(a * xk)
        return y

    @staticmethod
    def vector_mult(x:VECTOR, y:VECTOR) -> VECTOR:
        """Cayley multiplication"""
        degx, degy = len(x), len(y)
        z = [0] * (degx + degy)
        for i in range(degx):
            for j in range(degy):
                k = i + j
                z[k] += x[i] * y[j]
        return z

    def __mul__(self, other):
        """multiplication"""
        if other == 0:
            return Polynomial(indeterminate=self.indeterminate)
        if isinstance(other, Polynomial):
            z = self.vector_mult(self.coeffs, other.coeffs)
            return Polynomial(z, indeterminate=self.indeterminate)
        if isinstance(other, VECTOR):
            z = self.vector_mult(self.coeffs, other)
            return Polynomial(z, indeterminate=self.indeterminate)
        if isinstance(other, SCALAR):
            z = self.scalar_mult(other, self.coeffs)
            return Polynomial(z, indeterminate=self.indeterminate)
        return NotImplemented

    def __rmul__(self, other):
        """reverse multiplication"""
        return self * other         

    def __pow__(self, other:int):
        """powers"""
        if not isinstance(other, int):
            raise TypeError("the exponent must be an integer")
        if other < 0:
            raise ValueError("the exponent must be non-negative")
        if len(self) == 0 == other:
            raise ZeroDivisionError("0^0 is not defined")
        a = Polynomial(1, indeterminate=self.indeterminate)
        b = self
        while other:
            r = other % 2
            other = other // 2
            if r == 1:
                a *= b
            b *= b
        return a

    def __rpow__(self, other):
        """reversed powers"""
        raise NotImplemented

    def __truediv__(self, other:SCALAR):
        """true division"""
        if other == 0:
            raise ZeroDivisionError("division by 0 is not defined")
        if isinstance(other, int):
            other = Fraction(other)
        if isinstance(other, SCALAR):
            z = self.scalar_mult(1/other, self.coeffs)
            return Polynomial(z, indeterminate=self.indeterminate)
        return NotImplemented

    def __rtruediv__(self, other):
        """reversed true division"""
        return NotImplemented

    @staticmethod
    def shift_right(a:VECTOR, places:int=1):
        """multiply by x to a given power"""
        return [0] * places + list(a)

    @staticmethod
    def shift_left(a:VECTOR, places:int=1):
        """discard the constant and divide by x"""
        return list(a)[places:]

    def __rshift__(self, other:int):
        """right shift"""
        if not isinstance(other, int):
            raise TypeError("Undefined shift count")
        if other > 0:
            x = Polynomial.shift_right(self.coeffs, other)
            return Polynomial(x, indeterminate=self.indeterminate)
        if other < 0:
            x = Polynomial.shift_left(self.coeffs, -other)
            return Polynomial(x, indeterminate=self.indeterminate)
        return self

    def __lshift__(self, other:int):
        """left shift"""
        if not isinstance(other, int):
            raise TypeError("Undefined shift count")
        if other > 0:
            x = Polynomial.shift_left(self.coeffs, other)
            return Polynomial(x, indeterminate=self.indeterminate)
        if other < 0:
            x = Polynomial.shift_right(self.coeffs, -other)
            return Polynomial(x, indeterminate=self.indeterminate)
        return self

    @staticmethod
    def _deriv(a:VECTOR):
        """simulate the derivative map"""
        a = list(a)
        for i in range(len(a)):
            a[i] *= i
        return a[1:]

    @property
    def deriv(self):
        """polynomial derivative"""
        return Polynomial(self._deriv(self.coeffs), indeterminate=self.indeterminate)

    @staticmethod
    def _int(a:VECTOR, C:SCALAR=0):
        """simulate the integral map"""
        a = [Fraction(C)] + list(a)
        for i in range(1, len(a)):
#            print(i, a[i], Fraction(1, i), a[i]*Fraction(1,i))
            a[i] *= Fraction(1, i)
#        print(a)
        return a

    @property
    def int0(self):
        """polynomial integral with constant C=0"""
        return Polynomial(self._int(self.coeffs), indeterminate=self.indeterminate)

    def int(self, C:SCALAR):
        """polynomial integral with given value for constant C"""
        return Polynomial(self._int(self.coeffs, C=C), indeterminate=self.indeterminate)

    @staticmethod
    def division_algorithm(a:VECTOR, b:VECTOR) -> "q,r":
        """polynomial division"""
        b = list(b)
        while len(b)>0 and b[-1] == 0:
            b.pop()
        if len(b) == 0:
            raise ZeroDivisionError("Divide by Polynomial zero")

        a = list(a)
        while len(a)>0 and a[-1] == 0:
            a.pop()

        q = list()
        r = a

        while len(r) > len(b):
            places = len(r) - len(b)
            q0 = Fraction(r[-1]) / Fraction(b[-1])
            q1 = Polynomial.shift_right([q0], places)
            b0 = Polynomial.scalar_mult(q0, b)
            b0 = Polynomial.shift_right(b0, places)
            q = Polynomial.vector_sum(q, q1)
            r = Polynomial.vector_diff(r, b0)

        if len(r) == len(b):
            q0 = Fraction(r[-1]) / Fraction(b[-1])
            b0 = Polynomial.scalar_mult(q0, b)
            q = Polynomial.vector_sum(q, [q0])
            r = Polynomial.vector_diff(r, b0)

        return q, r

    def __divmod__(self, other):
        """division with remainder"""
        if other == 0:
            raise ZeroDivisionError("division by 0 is not defined")
        if isinstance(other, SCALAR):
            return self / other, 0
        if isinstance(other, Polynomial):
            other = other.coeffs
        if isinstance(other, VECTOR):
            q, r = Polynomial.division_algorithm(self.coeffs, other)
            q = Polynomial(q, indeterminate=self.indeterminate)
            r = Polynomial(r, indeterminate=self.indeterminate)
            return q, r
        return NotImplemented

    def __rdivmod__(self, other):
        """division with remainder"""
        return divmod(Polynomial(other), self)

    def __floordiv__(self, other):
        """floor division"""
        q, _ = divmod(self, other)
        return q

    def __rfloordiv__(self, other):
        """floor division"""
        q, _ = divmod(Polynomial(other), self)
        return q

    def __mod__(self, other):
        """floor division"""
        _, r = divmod(self, other)
        return r

    def __rmod__(self, other):
        """floor division"""
        _, r = divmod(Polynomial(other), self)
        return r

    def apply(self, x:"Location", modulus:int=None) -> "Value":
        """evaluate a polynomial at a given 'location'"""
        power = 1
        value = 0
        for a in self.coeffs:
            value += a * power
            power *= x
        if modulus:
            value %= modulus
        return value

    @property
    def normal(self):
        """normalization

        Our normal form is as follows:
            (1) the coefficients are integers
            (2) the coefficients have no nontrivial common factors
            (3) the coefficient of the leading term is positive

        For example:

            x/2 + 6: not normal (coefficient of x is not an integer)
                multiply by 2:
                    x + 12: normal
            2x + 6: not normal (both coefficients are divisible by 2)
                divide by 2:
                    x + 3: normal
            1 - x: not normal (negative leading coefficient)
                multiply by -1
                    x - 1: normal
        """
        coeffs = self.coeffs
#        print(coeffs)
        x = self.indeterminate
        if len(coeffs) == 0:
            return Polynomial(0, indeterminate=x)
        if len(coeffs) == 1:
            return Polynomial(1, indeterminate=x)
        args = list(a.denominator for a in coeffs)
#        print("args for lcm:", args)
        d = lcm(*args)
        coeffs = self.scalar_mult(d, coeffs)
#        print(f"LCD={d}", coeffs)
        args = list(a.numerator for a in coeffs if a!=0)
#        print("args for gcd:", args)
        d = Fraction(1, gcd(*args))
        if coeffs[-1] < 0:
            d = -d
        coeffs = self.scalar_mult(d, coeffs)
#        print(f"GCD={d}", coeffs)
        return Polynomial(coeffs, indeterminate=x)

    @property
    def normal2(self):
        """normalization with normalization factor

        Returns the both the normalization scalar and the normal form.
        The scalar product can be used to recover the input polynomial:
            d,g = f.normal2
            assert d*g == f

        Our normal form is as follows:
            (1) the coefficients are integers
            (2) the coefficients have no nontrivial common factors
            (3) the coefficient of the leading term is positive

        For example:

            x/2 + 6: not normal (coefficient of x is not an integer)
                multiply by 2:
                    x + 12: normal
            2x + 6: not normal (both coefficients are divisible by 2)
                divide by 2:
                    x + 3: normal
            1 - x: not normal (negative leading coefficient)
                multiply by -1
                    x - 1: normal
        """
        coeffs = self.coeffs
#        print(coeffs)
        x = self.indeterminate
        if len(coeffs) == 0:
            return Polynomial(0, indeterminate=x)
        if len(coeffs) == 1:
            return Polynomial(1, indeterminate=x)
        args = list(a.denominator for a in coeffs)
#        print("args for lcm:", args)
        d1 = lcm(*args)
        coeffs = self.scalar_mult(d1, coeffs)
#        print(f"LCD={d1}", coeffs)
        args = list(a.numerator for a in coeffs if a!=0)
#        print("args for gcd:", args)
        d2 = Fraction(1, gcd(*args))
        if coeffs[-1] < 0:
            d2 = -d2
        coeffs = self.scalar_mult(d2, coeffs)
#        print(f"GCD={d2}", coeffs)
        return 1/(d1*d2), Polynomial(coeffs, indeterminate=x)

def deg(f:Polynomial):
    """polynomial degree"""
    if not isinstance(f, Polynomial):
        f = Polynomial(f)
    return f.deg

def polynomialMod(f:Polynomial, modulus:int):
    """reduce the coefficients of a polynomial modulo the modulus"""
    x = f.coeffs
    for i in range(len(x)):
        item = x[i]
        if item.denominator != 1:
            raise ValueError("Unable to reduce a coefficient")
        x[i] = item.numerator % modulus
    return Polynomial(x, indeterminate=f.indeterminate)

def polynomialGCD2(f:Polynomial, g:Polynomial) -> Polynomial:
    """GCD of two rational polynomials"""
    a = Polynomial(f)
    b = Polynomial(g)
    if a == 0:
        return b
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
    return a.normal

def polynomialGCD(f:Polynomial, *args) -> Polynomial:
    """GCD of one or more rational polynomials"""
    for g in args:
        f = polynomialGCD2(f, g)
    return f

def polynomialCfrac(f:Polynomial, g:Polynomial) -> list:
    """express the ratio of two polynomials as a continued fraction"""
    a = Polynomial(f)
    b = Polynomial(g)
    if b == 0:
        raise ZeroDivisionError("Division by polynomial 0")
    if a == 0:
        return [a]
    cfrac = list()
    while b != 0:
        q, r = divmod(a, b)
        cfrac.append(q)
        a, b = b, r
    return cfrac

def cfrac2polynomials(cfrac:list, debug=False, normalize=True) -> list:
    """recover a polynomial ratio from a continued fraction"""
    x = cfrac[0].indeterminate
    zero = Polynomial(0, indeterminate=x)
    one = Polynomial(1, indeterminate=x)
    a0, b0 = zero, one
    a1, b1 = one, zero
    n = 1
    for q in cfrac:
        a2 = q * a1 + a0
        b2 = q * b1 + b0
        if debug:
            print(f"{n:2}: {str(a2):15} {str(b2):15}")
            n += 1
        a0, b0 = a1, b1
        a1, b1 = a2, b2
    if not normalize:
        return a1, b1
    if debug:
        print("     Normalization:")
    a, b = a1.coeffs, b1.coeffs
    args = list(c.denominator for c in a) + \
        list(c.denominator for c in b)
    d = lcm(*args)
    if debug:
        print(f"                 1 : LCM={d} {tuple(args)}")
    a = Polynomial.scalar_mult(d, a)
    b = Polynomial.scalar_mult(d, b)
    args = list(c.numerator for c in a if c!=0) + \
        list(c.numerator for c in b if c!=0)
    d = Fraction(1, gcd(*args))
    if a[-1] < 0:
        d = -d
    if debug:
        print(f"                 2 : 1/GCD={d} {tuple(args)}")
    a = Polynomial.scalar_mult(d, a)
    b = Polynomial.scalar_mult(d, b)
    return Polynomial(a, indeterminate=x), Polynomial(b, indeterminate=x)

# END polynomials.polynomial
