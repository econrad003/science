"""
sequences.linear2o - second order linear module
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
from utilities.quadratic_equation import QuadraticEquation

def delta(n, k):
    """Kronecker delta"""
    return 1 if n == k else 0

def powerf(a):
    """returns the appropriate power function"""
    if a == 0:
        f = lambda n: delta(n, 0)
    elif a == 1:
        f = lambda n: 1
    else:
        f = lambda n: a ** n
    return f

class Sequences(object):
    """quadratic sequences based on second order linear difference equations

    DESCRIPTION

        These sequences are defined by recurrence relations having the following
        form:

            f[n+2] = af[n+1] + bf[n]

    CASE STUDY: FIBONACCI SEQUENCES

        For example, the Fibonacci sequence and the Lucas sequence are both
        examples of sequences satisfying a recurrence of this form with a=b=1.
        For the Fibonacci sequence, we add the following initial conditions:

            F[0] = 0
            F[1] = 1

        For the Lucas sequence, we instead start with:

            L[0] = 2
            L[1] = 1

        The sequences form a vector space of dimension 2.  We can write all
        such sequences as linear combinations of the Fibonacci sequence F (above)
        and the sequence G having initial conditions:

            G[0] = 1
            G[1] = 0

        The Lucas sequence L can then be defined by L = 2G + F.

        We can also take F and L as bases, and define the sequence G by
        G = (L - F) / 2.

    TERMS OF THE SEQUENCES

        We can always use the initial values and the difference equation to
        extend the sequence to the natural numbers.

        The first few terms of the three sequences above are:

            n   0   1   2   3   4   5   6   7   8   9  10  11  12
           -------------------------------------------------------
            F   0   1   1   2   3   5   8  13  21  34  55  89 144
            L   2   1   3   4   7  11  18  29  47  76 123 199 322
            G   1   0   1   1   2   3   5   8  13  21  34  55  89

        If b is not 0, we can expand the sequence to include all the integers.
        For sequences based on the Fibonacci recurrence, we see that:

            f(n) = f(n+2) - f(n+1)

        So for the first few negative values of n we have:

            n  -1  -2  -3  -4  -5  -6  -7  -8  -9  -10  -11  -12
           ------------------------------------------------------
            F   1  -1   2  -3   5  -8  13 -21  34  -55   89 -144
            L  -1   3  -4   7 -11  18 -29  47 -76  123 -199  322
            G  -1   2  -3   5  -8  13 -21  34 -55   89 -144  233

    RELATIONS BETWEEN THE SEQUENCES

        A number of relationships are provable using mathematical
        induction or by other means.  For example, from the tables
        we might suspect that:

            G(n) = F(n-1) for all integers n.

        This is, in fact provable by mathematical induction.

    CLOSED FORM SOLUTIONS

        We can obtain closed form solutions using the method of
        undetermined coefficients.  We start by assuming that f(n)
        has a nontrivial solution of the form f[n] = λⁿ.

        Then:
            λⁿ⁺² = λⁿ⁺¹ + λⁿ

        Equivalently:
            λⁿ⁺² - λⁿ⁺¹ - λⁿ = 0

        Factor:
            λⁿ (λ² - λ - 1) = 0

        The solution λⁿ = 0 reduces to λ = 0, which is trivial (i.e.
        it's the zero vector).

        Then:
            λ² - λ - 1 = 0

        This quadratic equation is the characteristic equation.  It
        has two distinct solutions, namely:

            φ = (1 + √5)/2  and  ψ = (1 - √5)/2

        These solutions (characteristic values, or eigenvalues) are real
        and distinct.  Since they are distinct, the characteristic
        functions φⁿ and ψⁿ are linearly independent. It follows that
        f(n) is a linear combination of the two eigenfunctions.

            f(n) = Aφⁿ + Bψⁿ

        To evaluate A and B, we consider the initial conditions:

            A  + B  = F(0) = 0
            Aφ + Bψ = F(1) = 1

        If we multiply the first by φ we have:
            Aφ + Bφ = 0
        Subtract this from the second:
            -B√5 = B(ψ - φ) = 1
            B = -1/√5
        From the first equation:
            A = -B = 1/√5

        Hence:

            F(n) = (φⁿ - ψⁿ) / √5

        (Note: the number φ was traditionally known as the mean-extreme
        ratio.  It is now known as the golden ratio.  The number ψ is
        known as the complementary golden ratio, usually written as phi-bar.)

        We could go through a similar process for G and L, but that isn't
        really necessary.  For G, we use the relation we found earlier:

            G(n) = F(n-1) = (φⁿ⁻¹ - ψⁿ⁻¹) / √5

        For L, we use L = 2G + F.  First note that:
            φ⁻¹ = 2 / (1 + √5) = 2(1 - √5) / (1 - 5) = -ψ
            2φ⁻¹ + 1 = √5
            ψ⁻¹ = 2 / (1 - √5) = 2(1 + √5) / (1 - 5) = -φ
            -2ψ⁻¹ + 1 = √5

        Then:
            L(n) = φⁿ + ψⁿ

    MURPHY'S LAW

        So what can go wrong?

        (1) A zero eigenvalue

            This can happen in one of two ways.  The first (and worst) is when
            a = b = 0.  For example:

                s[n+2] = 0

            In this case, the sequence simply vanishes for n > 1 and is undefined
            for the negative integers.  Our eigenfunctions are the Kronecker
            delta functions δ(n,0) and δ(n,1).

            The second possibility is when b=0.  In this case, the eigenvalues
            are a and 0.  Assuming here that a is not zero, our eigenfunctions
            are aⁿ and δ(n,0).

        (2) Duplicate eigenvalues

            This happens when the characteristic polynomial is a perfect square.
            Assuming the duplicated eigenvalue λ is not zero, our eigenfunctions
            are λⁿ and nλⁿ.

        (3) Imaginary eienvalues

            If the roots of the characteristic equation are imaginary complex
            conjugate values, then we can rewrite the eigenfunctions as a real
            exponential times linear combinations of a sine and a cosine
            function with the same real argument.

            We can do something similar with distinct real eigenvalues, but
            we replace the trigonometric sine and cosine by hyberbolic sine
            and cosine.
    """

    __slots__ = ("__eqn", "__a", "__b")

    def __init__(self, a:int, b:int):
        """constructor"""
        self.__eqn = QuadraticEquation(1, -a, -b)
        self.__a, self.__b = a, b

    @property
    def charpoly(self) -> QuadraticEquation:
        """return the characteristic equation"""
        return self.__eqn

    @property
    def eigenvalues(self) -> tuple:
        """return the eigen values"""
        return self.__eqn.roots

    def iterates(self, y0, y1, stop) -> list:
        """return a list of values for n=0, n=1, up to but not including n=stop

        ARGUMENTS

            y0, y1 - the initial values at n=0 and n=1, respectively

            stop - the end value for the range (noninclusive).

        The list will start with both initial values.
        """
        result = [y0, y1]
        for n in range(2, stop):
            y2 = self.__a * y1 + self.__b * y0
            result.append(y2)
            y0, y1 = y1, y2
        return result

    @property
    def eigenfunctions(self):
        """returns the eigenfunctions"""
        lambda1, lambda2 = self.eigenvalues
        if lambda1 == 0 == lambda2:
            f = lambda n: delta(n, 0)
            g = lambda n: delta(n, 1)
            return f, g
        if lambda1 == lambda2:      # duplicate eigenvalues
            g = powerf(lambda1)
            f = lambda n: n*g(n)
        else:                       # distinct eigenvalues
            f = powerf(lambda1)
            g = powerf(lambda2)
        return f, g

    def coeffs(self, y0, y1):
        """coefficients of the eigenfunctions"""
        u, v = self.eigenfunctions
                # Au(0) + Bv(0) = y0
                # Au(1) + Bv(1) = y1
                # Au(0)u(1) + Bu(1)v(0) = y0 u(1)
                # Au(0)u(1) + Bu(0)v(1) = y1 u(0)
                # B (u(1)v(0) - u(0)v(1)) = y(0) u(1) - y1 u(0)
        B = (u(1)*y0 - u(0)*y1) / (u(1)*v(0) - u(0)*v(1))
                # A = (y0 - Bv(0)) / u(0)
        A = (y0 - B*v(0)) / u(0)
        return A, B

# END sequences.linear2o
