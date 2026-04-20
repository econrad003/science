"""
polynomials.polymod - univariate polynomials modulo n
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
from polynomials.superscript import to_superscript

def _make_poly(R:"Ring", indeterminate:str="x") -> "Class:R[x]":
    """create a class of polynomials with coefficients in a given ring"""

    class Polynomial(object):
        """polynomials over a ring"""

        __R = R
        __var = str(indeterminate)

        def __init__(self, *coeffs):
            """constructor"""
            if len(coeffs) == 1:
                if isinstance(coeffs[0], Polynomial):
                    self.__coeffs = tuple(coeffs[0].__coeffs)
                    return
                if isinstance(coeffs[0], (list, tuple)):
                    coeffs = coeffs[0]
            coeffs = list(self.__R(coeff) for coeff in coeffs)
            while coeffs and coeffs[-1] == 0:
                coeffs.pop()
            self.__coeffs = tuple(coeffs)

        @classmethod
        def coefficient_ring(cls):
            """the class of coefficients"""
            return cls.__R

        def __hash__(self):
            """the hash value"""
            if len(self.__coeffs) == 0:
                return hash(0)                  # zero polynomial
            if len(self.__coeffs) == 1:
                return hash(self.coeffs[0])     # constant polynomial
            token = (_make_poly, self.__R, self.__coeffs)
            return hash(token)

        def __eq__(self, other):
            """equality"""
            if isinstance(other, Polynomial):
                return self.__coeffs == other.__coeffs
            if len(self.__coeffs) == 0:
                return other == 0
            if len(self.__coeffs) == 1:
                return self.__coeffs[0] == other
            return False

        def __len__(self):
            """return the number of terms, including terms with coefficient zero"""
            return len(self.__coeffs)

        @property
        def deg(self):
            """return the degree

            deg(0) is defined here as -1.
            """
            return len(self.__coeffs) - 1

        def __abs__(self):
            """for a polynomial, we use the degree"""
            return self.deg

                # accessing the coefficients

        @property
        def coeffs(self) -> list:
            """all the coefficients as a list"""
            return list(self.__coeffs)

        def __iter__(self):
            """the coeffecients from low order to high order, as an iterable"""
            for a in self.__coeffs:
                yield a

        def __getitem__(self, index:int):
            """access the coefficients from low to high

            If the index is for a coefficient of too high degree, the
            return value is 0.

            If the index is negative:
                Returns a[n-index] where n is the number of terms;
                IndexError is raised when n-index is less than zero.

            Usage Examples (assuming coefficient ring modulus > 5):
                f = Polynomial(1, 2, 3, 4, 5)   <- constructor
                f(x)=5x⁴+4x³+3x²+2x+1           <- string
                f.coeffs = [1, 2, 3, 4, 5]      <- coefficients

                    non-negative indexing
                f[0] = 1        constant term
                f[1] = 2        linear coefficient
                f[4] = 5        lead coefficient
                f[5] = 0        index > deg(f)

                    negative indexing
                f[-1] = 5       lead coefficient
                f[-4] = 2       linear coefficient
                f[-5] = 1       constant term
                f[-6]           raises IndexError
            """
            if not isinstance(index, int):
                raise TypeError("[]: index must be an integer")
            if index >= 0:
                if index >= len(self.__coeffs):
                    return self.__R(0)
                return self.__coeffs[index]
            index = len(self.__coeffs) + index
            if index < 0:
                raise IndexError("[]: negative index overflow")
            return self.__coeffs[index]

        @staticmethod
        def __power2str(x:str, n:int):
            """convert a power to a string"""
            if n == 0:
                return ""               # constant
            if n == 1:
                return str(x)           # linear term
            return str(x) + to_superscript(n)

        @classmethod
        def __term2str(cls, coeff:"R", n:int):
            """convert a term to a string"""
            if coeff == 0:
                return ""
            if n == 0:
                return f"{coeff:+}"
            power = cls.__power2str(cls.__var, n)
            if coeff == 1:
                return f"+{power}"
            if coeff == -1:
                return f"-{power}"
            return f"{coeff:+}{power}"

        def __str__(self):
            """string representation"""
            if len(self.__coeffs) == 0:
                return "0"
            if len(self.__coeffs) == 1:
                return str(self.__coeffs[0])
            s = ""
            stack = list(self.__coeffs)
            n = self.deg
            while stack:
                coeff = stack.pop()
                s += self.__term2str(coeff, n)
                n -= 1
            if s[0] == "+":
                return s[1:]
            return s

        def repr(self):
            """representation of the instance"""
            return str(self)            # same as str

        def __pos__(self):
            """returns the polynomial (no change)"""
            return self

        def __neg__(self):
            """returns the arithmetic negation"""
            coeffs = list(self.__coeffs)
            for i in range(len(coeffs)):
                coeffs[i] = - coeffs[i]
            return Polynomial(coeffs)

        def __add__(self, other):
            """returns the sum

            We use the fact that addition in R is commutative.
            """
            if other == 0:
                return self
            if isinstance(other, Polynomial):
                coeffs = list()
                a = self.__coeffs
                b = other.__coeffs
                if len(b) > len(a):
                    a, b = b, a                 # (R,+) is commutative
                for i in range(len(b)):
                    coeffs.append(a[i]+b[i])
                for i in range(len(b), len(a)):
                    coeffs.append(a[i])
                return Polynomial(coeffs)
            if type(other) == int:
                coeffs = list(self.__coeffs) + [0]      # need at least one
                coeffs[0] += self.__R(other)
                return Polynomial(coeffs)
            if isinstance(other, self.__R):     # Note: Zn ⊆ int (subclass)
                coeffs = list(self.__coeffs) + [0]      # need at least one
                coeffs[0] += other
                return Polynomial(coeffs)
            return NotImplemented

        def __radd__(self, other):
            """reversed addition"""
            return self + other                 # commutative addition

        def __sub__(self, other):
            """subtraction"""
            return self + (-other)

        def __rsub__(self, other):
            """reversed subtraction"""
            return (-self) + other

        def __mul__(self, other):
            """multiplication of polynomials"""
            if isinstance(other, (int, self.__R)):
                    ### scalar multiplication
                a = list(self.__coeffs)
                for i in range(len(self.__coeffs)):
                    a[i] *= other
                return Polynomial(a)
            if not isinstance(other, Polynomial):
                return NotImplemented
            a = self.__coeffs
            b = other.__coeffs
            n = self.deg + other.deg
            c = [0] * (n+1)
            for i in range(len(a)):
                for j in range(len(b)):
                    c[i+j] += a[i] * b[j]
            return Polynomial(c)

        def __rmul__(self, other):
            """reversed multiplication (using commutativity)"""
            return self * other

        @property
        def inverse(self):
            """multiplicative inverse

            Only when the polynomial has degree 0 and the constant is
            a unit.
            """
            if self.deg != 0:
                raise ValueError("inverse: degree is not 0")
            return self.__coeffs[0].inverse
            
        @property
        def reciprocal(self):
            """multiplicative inverse (same as self.inverse)"""
            return self.inverse

        @staticmethod
        def _nonnegative(n:int, method=""):
            """make sure other is a nonnegative integer"""
            if not isinstance(n, int):
                raise TypeError(method + "non-negative integer required")
            if n < 0:
                raise ValueError(method + "non-negative integer required")
            return n

        def __rshift__(self, n:int):
            """right shift (e.g. multiply by x^n)"""
            self._nonnegative(n, method=">>:")
            if n == 0:
                return self
            a = [0] * n + list(self.__coeffs)
            return Polynomial(a)

        def __lshift__(self, n:int):
            """left shift (e.g. divide by x^n and discard remainder)"""
            self._nonnegative(n, method="<<:")
            if n == 0:
                return self
            a = list(self.__coeffs[n:])
            return Polynomial(a)

        def __divmod__(self, other):
            """division with remainder (division algorithm)"""
            if type(other) == int:
                other = self.__R(other)
            if isinstance(other, self.__R):
                if other.is_zero_divisor:
                    raise ZeroDivisionError("divmod: divide by divisor of zero")
                return (self * other.inverse, 0)
            if not isinstance(other, Polynomial):
                return NotImplemented
            if len(other.__coeffs) == 0:
                raise ZeroDivisionError("divmod: divide by zero")
            bk = other.__coeffs[-1] # divisor lead coefficient (b[-1])
            if bk.is_zero_divisor:
                raise ZeroDivisionError("divmod: lead coefficient divides zero")
            m1 = bk.inverse         # multiplier
            b = other               # divisor (fixed)
            q = Polynomial(0)       # quotient
            r = self                # remainder
            while r.deg >= b.deg:
                    #  Precondition: self = bq + r
                m2 = r.__coeffs[-1] * m1        # divide r[-1] by b[-1]
                n = r.deg - b.deg
                delta = (b * m2) >> n
                q += Polynomial(m2) >> n
                r -= delta
#                print(f"b={b}, q={q}, r={r}")      # for debugging
            return q, r

        def __rdivmod__(self, other):
            """floor division"""
            if type(other) == int:
                other = self.__R(other)
            if isinstance(other, self.__R):
                other = Polynomial(other)
            if isinstance(other, Polynomial):
                return divmod(other, self)
            return NotImplemented

        def __floordiv__(self, other):
            """floor division"""
            q, r = divmod(self, other)
            return q

        def __rfloordiv__(self, other):
            """reversed floor division"""
            q, r = divmod(other, self)
            return q

        def __truediv__(self, other):
            """true division"""
            q, r = divmod(self, other)
            if r != 0:
                raise ValueError(f"{self} is not divisible by {other}")
            return q

        def __rtruediv__(self, other):
            """reversed true division"""
            q, r = divmod(other, self)
            if r != 0:
                raise ValueError(f"{other} is not divisible by {self}")
            return q

        def __mod__(self, other):
            """remainder after division"""
            q, r = divmod(self, other)
            return r

        def __rmod__(self, other):
            """remainder after reversed division"""
            q, r = divmod(other, self)
            return r

        def __pow__(self, other:int):
            """compute integer powers"""
            if not isinstance(other, int):
                return NotImplemented
            if other < 0:
                raise ValueError("pow: negative powers are not permitted")
            q = other
            product = Polynomial(1)
            power = self
            while q > 0:
                q, r = divmod(q, 2)
                if r:
                    product *= power
                power *= power
            return product

        def apply(self, x:"R"):
            """evaluate the polynomial at x"""
            power = self.__R(1)
            total = self.__R(0)
            for a in self.__coeffs:
                total += a * power
                power *= x
            return total

    Polynomial.__name__ = f"{R.__name__}[{indeterminate}]"
    Polynomial.__doc__ = f"polynomials over the ring {R.__name__}"
    return Polynomial

def make_poly(n:int, indeterminate:str="x") -> "Class:(ℤ/nℤ)[x]":
    """create a mod-n polynomial class

    Returns a class.

    In addition, this creates the base ring class.  The ring class may be
    found using the class method "coefficient_ring".

    If the ring class has already been created, you can use the entry
    point "_make_poly".  Duck-type compatibility is the only requirement.
    """
    from utilities.modn import make_Zn

    R = make_Zn(n)
    return _make_poly(R, indeterminate)

def polynomialGCD(f:"Polynomial", g:"Polynomial"):
    """Euclidean algorithm

    EXCEPTIONS

        ZeroDivisionError can be raised if the ring of coefficients has
        a nonzero divisor of zero.

    NOTES

        I don't know whether the algorithm works for coefficients in
        cyclic rings which are not fields, i.e. when the additive order
        is not prime.
    """
    def normalize(p:"Polynomial"):
        """want lead coefficient = 1"""
        if p == 0:
            return p        # don't normalize zero
        return p / p[-1]

            # handle trivial cases
    if g == 0:
        return normalize(f)
    if f == 0:
        return normalize(g)

            # start the algorithm
    _, r = divmod(f, g)
    while r != 0:
        f = g
        g = r
        _, r = divmod(f, g)
    return normalize(g)

def cfrac(f:"Polynomial", g:"Polynomial", maxterms=50):
    """express the ratio f/g as a continued fraction"""
            # handle trivial cases
    if g == 0:
        raise ZeroDivisionError("divisor in continued fraction can't be zero")

            # start the Euclidean algorithm
    q, r = divmod(f, g)
    assert g*q + r == f
    result = [q] 
    while r != 0 and len(result) < maxterms:
        f = g
        g = r
        q, r = divmod(f, g)
        assert g*q + r == f
        result.append(q)
    return result

# END polynomials.polymod
