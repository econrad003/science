"""
demos.basel3 - The Basel problem, continued fraction approximations
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module adds organizes the tests in module demos.basel2 and
    adds some additional tests. More of the same, but with more
    detail.

RETAINED DESCRIPTION

    This uses the results found in module demos.basel1 to obtain some
    continued fraction estimates of the limit π²/6, obtained by Leonhard
    Euler in 1734, of the Basel series:

             1     1      1      1           π²
        1 + --- + --- + ---- + ---- + ... = ----
             4     9     16     25           6

    and also the limit π²/12 of the alternating Basel series:

             1     1      1      1           π²
        1 - --- + --- - ---- + ---- - ... = ----.
             4     9     16     25           12

    As noted in module demos.basel1, these series converge slowly. We can
    speed up convergence, that is, we can dramatically reduce the number
    of terms need to get a sharp estimate by comparing the series to a
    telescoping series, with denominators equal to k²-1 instead of k².
    Both the absolute form (numerator = 1) and the alternating form
    (numerators alternate between 1 and -1) are telescoping.  The
    resulting series converges with O(1/k⁴) instead of O(1/k²).  This
    is still not very fast, but it is adequate for estimates that are
    better than can be obtained using a double precision floating point
    estimate.

REFERENCES

    [1] "Basel problem", in Wikipedia. 5 March 2026. Web.
        Accessed 11 March 2026.
        URL: https://en.wikipedia.org/wiki/Basel_problem 

    [2] "Riemann Zeta Function zeta(2)", in Wolfram MathWorld. Web.
        Accessed 11 March 2026.
        URL: https://mathworld.wolfram.com/RiemannZetaFunctionZeta2.html

    [3] Sourangshu Ghosh. The Basel Problem. 7 October 2020.
        Revised 24 February 2021. Web. Accessed 11 March 2026.
        URL: https://arxiv.org/pdf/2010.03953 (expository article)
        URL: https://arxiv.org/abs/2010.03953 (abstract)

        This article covers several proofs of Euler's result.

    [4] "Speeding up the convergence of ζ(2)", in StackExchange. Web.
        Accessed 11 March 2026.
        URL: https://math.stackexchange.com/questions/ -
                2332172/speeding-up-the-convergence-of-zeta2

        The trick described in this reference is not new.  I came up with
        the same idea when I was faced with this exact problem in a question
        on a general exam in graduate school circa 2000.   (The choice
        of series here is the same as the one I used then.)  I am quite
        sure that many others have arrived at essentially the same approach
        long before I did.

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
from fractions import Fraction
from math import pi, sqrt, log
import textwrap

def alternate(a, k):
    """alternate the sign"""
    return a(k) if k%2==1 else -a(k)

class Series(object):
    """series manipulation"""

    def __init__(self, a:"function"):
        """constructor

        ARGUMENTS

            a - the general term, a function that maps an integer to the
                range set.
        """
        self.term = a
        self.name1 = "A series"
        self.name2 = "An alternating series"

    def a(self, k, alternating=False):
        """return the kth term"""
        return alternate(self.term, k) if alternating else self.term(k)

    def partial_sum(self, N:int, alternating=False):
        """return the requested partial sum"""
        return sum(self.a(k, alternating) for k in range(1, N+1))

    def __add__(self, other:"SumSeries"):
        """add the two series"""
        a = lambda k: self.a(k) + other.a(k)
        return Series(a)

    def __sub__(self, other:"SumSeries"):
        """subtract the two series"""
        a = lambda k: self.a(k) - other.a(k)
        return Series(a)

    def rename(self, name1:str, name2:str):
        """give the series a name"""
        self.name1 = name1
        self.name2 = name2

print("Self-test... ", end="")

a = lambda k: k
triangle = Series(a)
assert triangle.term(1) == 1
assert triangle.partial_sum(10) == 55, f"{triangle.partial_sum(10)=}"
assert triangle.partial_sum(10, True) == -5, f"{triangle.partial_sum(10,True)=}"
dup = triangle + triangle
assert dup.term(1) == 2
assert dup.partial_sum(10) == 110, f"{dup.partial_sum(10)=}"
nil = triangle - triangle
assert nil.term(1) == 0
assert nil.partial_sum(10) == 0, f"{nil.partial_sum(10)=}"
print("ok!")

def paragraph(msg):
    """write a paragraph"""
    print()
    msg = textwrap.wrap(msg, width=77, initial_indent='   ',
                       fix_sentence_endings=True)
    for line in msg:
        print(line)

def intro(phase, msg:str):
    """introduce a phase"""
    print("-"*72)
    print("SECTION", phase)
    paragraph(msg)

def test(s:Series, N:int, Z:float, err:float,
         show:bool=False, alternating=False):
    """run a test"""
    print()
    name = s.name2 if alternating else s.name1
    print(f"{name}: {N} terms")
    if show:
        print("terms: ", end="")
        for k in range(1, N+1):
            print(f"{s.a(k, alternating)}, ", end="")
        print("...")
    z = s.partial_sum(N, alternating)
    perr = err if type(err) == Fraction else f"{err:.10f}"
    print(f"            sum = {z}, estimated error: {perr}")
    print(f"reference value = {Z},    actual error: {float(Z-z):.10f}")
    print(f"     error ratio: actual/guess = {float((Z-z)/err):.5f}")
    return z

msg = """
    Here we briefly introduce each of the series and show partial
sums for five, ten and twenty terms.  Since we represent the
terms as rational fractions, the sums are exact.
"""
intro("1. Introducing the series", msg)

msg = """
    The ratio of the actual error to the error guesstimate
should normally be positive and less than or equal to one.
A positive ratio indicates that the error estimate actually
points in the direction of the limiting value.  A ratio larger
than one in absolute value indicates that the we have
underestimated the error.  Ideally we would like the ratio
to be equal or close to 1, but that usually isn't practical.
"""
paragraph(msg)

print()
print("5 terms...")

msg = """
    The limit of Basel series and its alternating counterpart are the
series we want to estimate using partial sums.  The six remaining
series (in three pairs: a bounded monotone increasing series and its
alternating counterpart) are the series we will use for comparison.
"""
paragraph(msg)

f = lambda k: Fraction(1, k*k)
basel = Series(f)
basel.rename("The Basel series", "The alternating Basel series")
z = test(basel, 5, pi**2/6, Fraction(1, 5), show=True)
print(f"\t({z} = {float(z)}, 1/5=0.2)")
print("\tLimit: π² / 6")
print("\tThis is the Basel series whose limit was first found by Euler")
z = test(basel, 5, pi**2/12, Fraction(-1, 36), show=True, alternating=True)
print(f"\t({z} = {float(z)}, -1/36={-1/36:.10f})")
print("\tLimit: π² / 12")
print("\tThis alternating series is closely related to the Basel series")

def f1(k):
    """reciprocal quadratic 1"""
    if k == 1:
        return 0
    return Fraction(1, k*k - 1)
leibniz1 = Series(f1)
leibniz1.rename("1/(k²-1) series", "Alternating 1/(k²-1) series")
z = test(leibniz1, 5, 3/4, Fraction(1, 5), show=True)
print(f"\t({z} = {float(z)}, 1/5=0.2)")
print("\tLimit: 3/4")
z = test(leibniz1, 5, -1/4, Fraction(-1, 35), show=True, alternating=True)
print(f"\t({z} = {float(z)}, -1/35={-1/35:.10f})")
print("\tLimit: -1/4")

def f2(k):
    """reciprocal quadratic 2"""
    if k == 1:
        return 0
    return Fraction(1, k*k - k)
leibniz2 = Series(f2)
leibniz2.rename("1/(k²-k) series", "Alternating 1/(k²-k) series")
z = test(leibniz2, 5, 1, Fraction(1, 5), show=True)
print(f"\t({z} = {float(z)}, 1/5=0.2)")
print("\tLimit: 1")
z = test(leibniz2, 5, 1-2*log(2), Fraction(-1, 30), show=True, alternating=True)
print(f"\t({z} = {float(z)}, -1/30={-1/30:.10f})")
print("\tLimit: 1-2 log 2")
print("\tThis series is closely related to the alternating harmonic series")

f3 = lambda k: 1 / (k**2 - Fraction(1, 4))
leibniz3 = Series(f3)
leibniz3.rename("1/(k²-1/4) series", "Alternating 1/(k²-1/4) series")
z = test(leibniz3, 5, 2, Fraction(1, 5), show=True)
print(f"\t({z} = {float(z)}, 1/5=0.2)")
print("\tLimit: 2")
z = test(leibniz3, 5, pi-2, -f3(6), show=True, alternating=True)
print(f"\t({z} = {float(z)}, {-f3(6)}={float(-f3(6)):.10f})")
print("\tLimit: π - 2")
print("\tThis series is closely related to the inverse tangent (arctan) series")

print()
print("10 terms...")
z = test(basel, 10, pi**2/6, 1/10)
z = test(basel, 10, pi**2/12, 1/121, alternating=True)
z = test(leibniz1, 10, 3/4, 1/10)
z = test(leibniz1, 10, -1/4, 1/120, alternating=True)
z = test(leibniz2, 10, 1, 1/10)
z = test(leibniz2, 10, 1-2*log(2), 1/110, alternating=True)
z = test(leibniz3, 10, 2, 1/10)
z = test(leibniz3, 10, pi-2, f3(11), alternating=True)

print()
print("20 terms...")
z = test(basel, 20, pi**2/6, 1/20)
z = test(basel, 20, pi**2/12, 1/441, alternating=True)
z = test(leibniz1, 20, 3/4, 1/20)
z = test(leibniz1, 20, -1/4, 1/440, alternating=True)
z = test(leibniz2, 20, 1, 1/20)
z = test(leibniz2, 20, 1-2*log(2), 1/420, alternating=True)
z = test(leibniz3, 20, 2, 1/20)
z = test(leibniz3, 20, pi-2, f3(21), alternating=True)

print()
print("Setting up the series in float mode... ", end="")
f = lambda k: 1 / (k*k)
basel = Series(f)
basel.rename("The Basel series", "The alternating Basel series")

def f1(k):
    """reciprocal quadratic 1"""
    if k == 1:
        return 0
    return 1 / (k*k - 1)
leibniz1 = Series(f1)
leibniz1.rename("1/(k²-1) series", "Alternating 1/(k²-1) series")

def f2(k):
    """reciprocal quadratic 2"""
    if k == 1:
        return 0
    return 1 / (k*k - k)
leibniz2 = Series(f2)
leibniz2.rename("1/(k²-k) series", "Alternating 1/(k²-k) series")

f3 = lambda k: 1 / (k**2 - 1/4)
leibniz3 = Series(f3)
leibniz3.rename("1/(k²-1/4) series", "Alternating 1/(k²-1/4) series")

print("complete!")

msg = """
The first set of comparisons involves the following setup:
"""
intro("2. First Leibniz series comparisons)", msg)

print()
print("   1         1             1")
print("  ---- - -------- = - -------------   whenever k > 1")
print("   k²     k² - 1       k² (k² - 1)")

msg = """
We first run several comparisons of the Basel series with the first
of the six series.  We just subtract corresponding terms. We will
tests.
"""
intro("2.1. Basel series (first comparison)", msg)

msg = """
    The terms are increasing montonically to zero.  The First term
of the combined series is 1 since the Leibniz series starts with k=2.
So the partial sums decrease monotonically from 1 to the limit
of the combined series.
"""
paragraph(msg)

print()
print("\tLimit of series = π²/6 - 3/4")

msg = """
    For the error estimate, we ignore low order terms in the denominator
of the general term and estimate the error using the integral test.
"""
paragraph(msg)

print()
print("\tEstimated error: E(N) = - 1 / (3N³)")

E = lambda N: -1 / (3*N*N*N)
compare = basel - leibniz1
compare.rename("1 / (k² (k² - 1))", "Alternating 1 / (k² (k² - 1))")

print()
print("3, 5, 10, 20, 50, 100 and 200 terms...")

def test2(s:Series, N:int, Z:float, err:float, show:bool=False):
    target = pi*pi/6
    z = test(s, N, target - Z, err, show)
    zstar = z + Z
    pi1 = sqrt(6*zstar)
    print(f"\tπ²/6: {zstar:.10f}, actual {target:.10f},",
          f"diff={target-zstar:.10f}")
    print(f"\t   π: {pi1:.10f}, actual {pi:.10f},",
          f"diff={pi-pi1:.10f}")

z = test2(compare, 3, 3/4, E(3), show=True)
z = test2(compare, 5, 3/4, E(5))
z = test2(compare, 10, 3/4, E(10))
z = test2(compare, 20, 3/4, E(20))
z = test2(compare, 50, 3/4, E(50))
z = test2(compare, 100, 3/4, E(100))
z = test2(compare, 200, 3/4, E(200))

msg = """
Now we run several comparisons of the alternating Basel series with the
alternating form of the first pair.
Again we just subtract corresponding terms. We will
tests.
"""
intro("2.2. Alternating Basel series (first comparison)", msg)

print()
print("3, 5, 10, 20, 50, 100 and 200 terms...")

def test3(s:Series, N:int, Z:float, err:float, show:bool=False,):
    target = pi*pi/12
    z = test(s, N, target - Z, err, show, alternating=True)
    zstar = z + Z
    pi1 = sqrt(12*zstar)
    print(f"\tπ²/12: {zstar:.10f}, actual {target:.10f},",
          f"diff={target-zstar:.10f}")
    print(f"\t   π: {pi1:.10f}, actual {pi:.10f},",
          f"diff={pi-pi1:.10f}")

F = lambda k: - compare.a(k, alternating=True)
z = test3(compare, 3, -1/4, F(3), show=True)
z = test3(compare, 5, -1/4, F(5))
z = test3(compare, 10, -1/4, F(10))
z = test3(compare, 20, -1/4, F(20))
z = test3(compare, 50, -1/4, F(50))
z = test3(compare, 100, -1/4, F(100))
z = test3(compare, 200, -1/4, F(200))

msg = """
The second set of comparisons involves the following setup:
"""
intro("3. Second Leibniz series comparisons)", msg)

print()
print("   1         1              1")
print("  ---- - -------- = - -------------   whenever k > 1")
print("   k²     k² - k       k (k² - k)")


msg = """
    We again take the difference term by term.
"""
intro("3.1. Basel series (second comparison)", msg)

print()
print("\tLimit of series = π²/6 - 1")

msg = """
    As before, we ignore low order terms in the denominator
of the general term and estimate the error using the integral test.
"""
paragraph(msg)

print()
print("\tEstimated error: E(N) = - 1 / (2N²)")
G = lambda N: - 1 / (2*N+N)

compare = basel - leibniz2
compare.rename("1 / (k (k² - k))", "Alternating 1 / (k (k² - k))")

print()
print("3, 5, 10, 20, 50, 100 and 200 terms...")

z = test2(compare, 3, 1, G(3), show=True)
z = test2(compare, 5, 1, G(5))
z = test2(compare, 10, 1, G(10))
z = test2(compare, 20, 1, G(20))
z = test2(compare, 50, 1, G(50))
z = test2(compare, 100, 1, G(100))
z = test2(compare, 200, 1, G(200))

msg = """
    And now the alternating comparison.
"""
intro("3.1. Basel series (second comparison)", msg)

delta = 1 - 2*log(2)
F = lambda k: - compare.a(k, alternating=True)
z = test3(compare, 3, delta, F(3), show=True)
z = test3(compare, 5, delta, F(5))
z = test3(compare, 10, delta, F(10))
z = test3(compare, 20, delta, F(20))
z = test3(compare, 50, delta, F(50))
z = test3(compare, 100, delta, F(100))
z = test3(compare, 200, delta, F(200))

msg = """
The final set of comparisons involves the following setup:
"""
intro("4. Second Leibniz series comparisons)", msg)

print()
print("   1         1               1/4")
print("  ---- - ---------- = - -------------   for all k")
print("   k²     k² - 1/4       k (k² - k)")


msg = """
    We again take the difference.
"""
intro("4.1. Basel series (third comparison)", msg)

print()
print("\tLimit of series = π²/6 - 2   (This value is negative!)")

msg = """
    As before, we ignore low order terms in the denominator
of the general term and estimate the error using the integral test.
"""
paragraph(msg)

print()
print("\tEstimated error: E(N) = - 1 / (3N³)")

compare = basel - leibniz3
compare.rename("1 / (k (k² - 1/4))", "Alternating 1 / (k (k² - 1/4))")

print()
print("3, 5, 10, 20, 50, 100 and 200 terms...")

z = test2(compare, 3, 2, E(3), show=True)
z = test2(compare, 5, 2, E(5))
z = test2(compare, 10, 2, E(10))
z = test2(compare, 20, 2, E(20))
z = test2(compare, 50, 2, E(50))
z = test2(compare, 100, 2, E(100))
z = test2(compare, 200, 2, E(200))

msg = """
    And now the alternating comparison.
"""
intro("4.1. Basel series (third comparison)", msg)

delta = pi - 2
F = lambda k: - compare.a(k, alternating=True)
z = test3(compare, 3, delta, F(3), show=True)
z = test3(compare, 5, delta, F(5))
z = test3(compare, 10, delta, F(10))
z = test3(compare, 20, delta, F(20))
z = test3(compare, 50, delta, F(50))
z = test3(compare, 100, delta, F(100))
z = test3(compare, 200, delta, F(200))


print("-" * 72)
print("SUCCESS!")

