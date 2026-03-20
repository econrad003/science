"""
demos.basel2 - The Basel problem, continued fraction approximations
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

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
from math import pi                 # reference estimate
from math import log, sqrt, ceil, floor
from fractions import Fraction
import textwrap

print("                   CONTENTS")
print()
print("1. The Basel and the alternating Basel series")
print("2. Reference values using Python math.pi")
print("3. Estimates by summing the series")
print("4. Estimates using the speedup")
print("5. Convergents of the reference values")
print()
print("Epilogue")

    # Let's get some idea of the size of the integers that we
    # might be dealing with...

print()
print("SECTION 1: The Basel and the alternating Basel series")
print()
series ="""
Basel series (B):
             1     1      1      1           π²
        1 + --- + --- + ---- + ---- + ... = ----
             4     9     16     25           6

alternating Basel series (A):
             1     1      1      1           π²
        1 - --- + --- - ---- + ---- - ... = ----.
             4     9     16     25           12
"""
print(series)

def cfrac(x:Fraction, err:float):
    """obtain a continued fraction"""
    err = abs(err)
    frac = list()
    q = floor(x)
    frac.append(q)
    y = x - q
    b = y.numerator
    a = y.denominator
    A2, B2 = 1, 0
    A1, B1 = q, 1
    A0, B0 = q, 1
    # print(q, A1, B1) 
    while abs(y) > err/2:
        q = floor(Fraction(a, b))
        r = a % b
        frac.append(q)
        A0, B0 = q*A1 + A2, q*B1 + B2
        # print(q, A0, B0)
        if r == 0:
            break
        y = x - Fraction(A0, B0)
        A2, B2 = A1, B1
        A1, B1 = A0, B0
        a = b
        b = r
    return frac, Fraction(A0, B0)

## TEST cfrac
# foo = cfrac(Fraction(sqrt(2)), 0.001)
# print(foo)

print()
print("SECTION 2: Reference values using Python math.pi")
print()

print("Reference values (Python):")
print("\tπ²/6 =", pi*pi/6)
frac, est = cfrac(Fraction(pi*pi/6), 1e-10)
print("\t\tcontinued fraction:")
print(f"\t\t  {frac}")
print("\t\testimate =", float(est), f"  err < 1e-10")
print("\tπ²/12 =", pi*pi/12)
frac, est = cfrac(Fraction(pi*pi/12), 1e-10)
print("\t\tcontinued fraction:")
print(f"\t\t  {frac}")
print("\t\testimate =", float(est), f"  err < 1e-10")

print()
print("SECTION 3: Estimates by summing the series")
print()

intro = """
    In this section, we simply sum the first 100 terms of
    each series.  The series converge slowly.  100 terms of
    the Basel series gives us only three significant digits
    of precision.  Note that the rate of convergence is
    actually decreasing (i.e. convergence decelerates).  As we
    attempt to get six, nine, twelve significant digits, we will
    need increasing numbers of additional terms.
"""
intro = textwrap.wrap(intro, width=77, initial_indent='   ',
                       fix_sentence_endings=True)
for line in intro:
    print(line)
print()

print("Estimate of π²/6 using 100 terms:")
s = sum(Fraction(1, k*k) for k in range(1, 101))
print(f"\tB(100) = {s}")
digits = len(str(s.numerator))
print(f"\t\tdigits in numerator: {digits}")
digits = len(str(s.denominator))
print(f"\t\tdigits in denominator: {digits}")
exp = pi*pi/6
got = float(s)
diff = exp-got
print(f"\t\treference value: {exp}, sum: {got}")
print(f"\t\terror: {diff:.5f}")
print("\tWith 100 terms, we get about 3 significant digits.")
frac, est = cfrac(s, diff)
print("\tContinued fraction:", frac)
print("\testimate =", est, f"({float(est)})")

def odd(k:int):
    """returns 1 if odd and -1 if even"""
    return 1 if k%2 else -1

print()
print("Estimate of π²/12 using 100 terms:")
s = sum(Fraction(odd(k), k*k) for k in range(1, 101))
print(f"\tA(100) = {s}")
digits = len(str(s.numerator))
print(f"\t\tdigits in numerator: {digits}")
digits = len(str(s.denominator))
print(f"\t\tdigits in denominator: {digits}")
exp = pi*pi/12
got = float(s)
diff = exp-got
print(f"\t\treference value: {exp}, sum: {got}")
print(f"\t\terror: {diff:.7f}")
print(f"\t\talternating series error:  {-1/(101*101):.7f}")
print("\tWith 100 terms, we get about 5 significant digits.")
frac, est = cfrac(s, diff)
print("\tContinued fraction:", frac)
print("\testimate =", est, f"({float(est)})")

print()
print("SECTION 4: Estimates using the speedup")
print()

intro = """
    In this section, we get a speedup of convergence by comparing
    the two series to two related telescoping series.  The benefit
    is that we get a substantial boost in the rate of convergence.
    But, as with the basic series, the rate of convergence
    is still decreasing, so we still need a lot of terms for marginal
    increases in the numbers of significant digits.
"""
intro = textwrap.wrap(intro, width=77, initial_indent='   ',
                       fix_sentence_endings=True)
for line in intro:
    print(line)
print()

print("Estimate of π²/6 using 20 terms of speedup:")
s1 = sum(Fraction(1, k*k) for k in range(1, 21))
s2 = sum(Fraction(1, k*k-1) for k in range(2, 21))
s = s1 - s2 + Fraction(3, 4)
print(f"\tB'(20) = {s}")
digits = len(str(s.numerator))
print(f"\t\tdigits in numerator: {digits}")
digits = len(str(s.denominator))
print(f"\t\tdigits in denominator: {digits}")
exp = pi*pi/6
got = float(s)
diff = exp-got
print(f"\t\treference value: {exp}, sum: {got}")
print(f"\t\terror: {diff:.8f}")
print("\tWith 20 terms, we get about 5 significant digits.")
frac, est = cfrac(s, diff)
print("\tContinued fraction:", frac)
print("\testimate =", est, f"({float(est)})")

print()
print("Estimate of π²/12 using 20 terms of speedup:")
s1 = sum(Fraction(odd(k), k*k) for k in range(1, 21))
s2 = sum(Fraction(odd(k), k*k-1) for k in range(2, 21))
s = s1 - s2 - Fraction(1, 4)
print(f"\tA'(20) = {s}")
digits = len(str(s.numerator))
print(f"\t\tdigits in numerator: {digits}")
digits = len(str(s.denominator))
print(f"\t\tdigits in denominator: {digits}")
exp = pi*pi/12
got = float(s)
diff = exp-got
print(f"\t\treference value: {exp}, sum: {got}")
print(f"\t\terror: {diff:.9f}")
print("\tWith 20 terms, we get about 6 significant digits.")
frac, est = cfrac(s, diff)
print("\tContinued fraction:", frac)
print("\testimate =", est, f"({float(est)})")

print()
print("Estimate of π²/6 using 40 terms of speedup:")
s1 = sum(Fraction(1, k*k) for k in range(1, 41))
s2 = sum(Fraction(1, k*k-1) for k in range(2, 41))
s = s1 - s2 + Fraction(3, 4)
print(f"\tB'(40) = {s}")
digits = len(str(s.numerator))
print(f"\t\tdigits in numerator: {digits}")
digits = len(str(s.denominator))
print(f"\t\tdigits in denominator: {digits}")
exp = pi*pi/6
got = float(s)
diff = exp-got
print(f"\t\treference value: {exp}, sum: {got}")
print(f"\t\terror: {diff:.9f}")
print("\tWith 40 terms, we get about 6 significant digits.")
frac, est = cfrac(s, diff)
print("\tContinued fraction:", frac)
print("\testimate =", est, f"({float(est)})")

print()
print("Estimate of π²/12 using 40 terms of speedup:")
s1 = sum(Fraction(odd(k), k*k) for k in range(1, 41))
s2 = sum(Fraction(odd(k), k*k-1) for k in range(2, 41))
s = s1 - s2 - Fraction(1, 4)
print(f"\tA'(40) = {s}")
digits = len(str(s.numerator))
print(f"\t\tdigits in numerator: {digits}")
digits = len(str(s.denominator))
print(f"\t\tdigits in denominator: {digits}")
exp = pi*pi/12
got = float(s)
diff = exp-got
print(f"\t\treference value: {exp}, sum: {got}")
print(f"\t\terror: {diff:.9f}")
print("\tWith 40 terms, we get about 7 significant digits.")
frac, est = cfrac(s, diff)
print("\tContinued fraction:", frac)
print("\testimate =", est, f"({float(est)})")

print()
print("SECTION 5: Convergents of the reference values")
print()

intro = """
    Python floating point can only represent rational numbers --
    irrational algebraic and transcendental numbers can only be
    estimated with about fifteen to sixteen decimal digits of
    precision.  (The actual representation is binary.)  Python
    does provide us with a way to get the actual rational number
    represented by a float as a ratio of two integers.  And rational
    numbers have terminating continued fractions...
"""
intro = textwrap.wrap(intro, width=77, initial_indent='   ',
                       fix_sentence_endings=True)
for line in intro:
    print(line)
print()

intro = """
    In this section, we expand Python's rational estimates into
    continued factions and display the quotients and convergents.
    The continued fractions for the underlying transcendental numbers
    that will probably differ in the last few quotients. 
"""
intro = textwrap.wrap(intro, width=77, initial_indent='   ',
                       fix_sentence_endings=True)
for line in intro:
    print(line)
print()

def cfrac2(x:float):
    """exact convergents of a floating point number"""
    x = Fraction(x)
    a = x.numerator
    b = x.denominator
    A2, B2 = 0, 1
    A1, B1 = 1, 0
    r = b
    n = 0
    while r != 0:
        n += 1
        q = a // b
        r = a % b
        A0 = q*A1 + A2
        B0 = q*B1 + B2
        print(f"\t{n:3} {q}", Fraction(A0, B0))
        A2, B2 = A1, B1
        A1, B1 = A0, B0
        a = b
        b = r

print("    π²/6:", pi*pi/6)
cfrac2(pi*pi/6)
print("    π²/12:", pi*pi/12)
cfrac2(pi*pi/12)
print("    π²:", pi)
cfrac2(pi)

print()
print("EPILOGUE:")
print()

epilog = """
    Euler's solution of the Basel problem in 1734, though incomplete,
was a major advance that cemented his reputation.  The problem, first
posed by Pietro Mengoli, was to find a closed form expression for the
sum of the reciprocal square series.  Euler's predecessors, including
Leibniz and the Bernoulli brothers had been stumped.  But Euler's
result, a derivation, was actually more general in that he showed
how the solution led to a closed form expression for the sum of each
series of any given reciprocal even power.  The gap in his derivation
was that it was based an an unproven product expansion of the sine
function.
"""
epilog = textwrap.wrap(epilog, width=77, initial_indent='   ',
                       fix_sentence_endings=True)
for line in epilog:
    print(line)
print()
