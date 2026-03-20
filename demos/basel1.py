"""
demos.basel1 - The Basel problem, a series approximation of pi
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module looks at using the reciprocal squares series to
    approximate pi.

BACKGROUND

    Leonhard Euler (1707-1783) solved the Basel Problem in 1734 by
    equating an infinite product series expansion of the sine function
    with the Maclaurin series. The problem was first proposed by Pietro
    Mengoli in 1650.  (The association with Basel is due to an assessment
    of the problem's importance by Jacob Bernoulli.)  Euler's proof did
    have a gap.  The gap was closed by Weierstrass who proved that Euler's
    product expansion of sine was correct.

    Euler's result:

             1     1      1      1           π²
        1 + --- + --- + ---- + ---- + ... = ----
             4     9     16     25           6

    The denominators are perfect squares.

OUR GOAL HERE

    Our goal here is to use the series here to approximate π.  But we
    want to do this as inexpensively as possible.  The idea here is
    to get a good estimate with as little arithmetic as we can.

    A bad estimate would be to simply add up a million terms.  Why?
    Well the series is monotone increasing.  The million term adds
    one trillionth to the sum: the error at that point is over one
    trillionth, and it is not immediately obvious how much over.

A FIRST STEP

    Call the sum S.

    Now throw away the odd terms -- those with odd denominators and
    call the sum T:

              1      1      1      1
        T =  --- + ---- + ---- + ---- + ...
              4     16     36     64

              1     1    1     1       1             π²     S
          =  --- ( ---+ --- + ---- + ---- + ... ) = ---- = ---
              4     1    4     9      16             24     4

    Now subtract 2T from S

                      1     1      1      1           π²
        S - 2T = 1 - --- + --- - ---- + ---- - ... = ----
                      4     9     16     25           12

    This series is alternating and the terms are (as before) decreasing in
    absolute value.  If we add up one million terms, we know the error
    must be strictly less that one over one trillion one.  We have made
    an improvement -- we have a quantifiable bound on the error.  We also
    know whether the error is an overshoot or an undershoot -- with each
    term we know whether our approximation is too low or too high.

SECOND STEP

    We can reduce the time complexity (but only linearly) by taking the
    terms in pairs.  Here we use the relation:

         1     1     A + B
        --- + --- = -------
         A     B      AB

    Here we replace three floating point operations ("fops" - two
    multiplications -- namely the reciprocals -- and one addition
    by two integer operations and one fop.

THIRD STEP

    We can take several terms at a time, for example:

         1     1     1     1     A + B     C + D
        --- + --- + --- + --- = ------- + -------
         A     B     C     D      AB        CD

                                  (A+B)CD + (C+D)AB
                              = --------------------
                                        ABCD

A CHANGE OF DIRECTION

    One possibiliy is to compare the series (known as ζ(2)) to a known
    telescoping series.  For example:
              2          1       1          1      1
        Σ -------- = ( ----- - ----- ) + ( --- - ----- )
           k² - 1       a-1     a+1         a     a+2

                         1       1           1       1
                   + ( ----- - ----- ) + ( ----- - ----- ) + O(1/k)
                        a+1     a+3         a+2     a+4

                       1       1
                   = ----- + -----
                      a-1      a

    If we take the above series starting at k=2, note that
              1          1           1
        Σ -------- - Σ ---- = Σ ------------
           k² - 1       k²       k²(k² - 1)

    Terms now decrease with the fourth power.  (We lose the alternating
    series with this particular comparison, but this is fixable.)

    We note that the telescoping happens in conjunction with parity:
    even terms cancel with even, and odd with odd.  So the fix is to
    throw in a Pₖ = (-1)^(k-1), then we have:

             Pₖ         Pₖ          Pₖ
        Σ -------- - Σ ---- = Σ ------------
           k² - 1       k²       k²(k² - 1)

    If the first term is indexed by k=a, then the telescoping sum on
    the left reduces to:
              Pₖ               1      1
        Σ -------- =  P(a) ( ----- - --- ) / 2
           k² - 1             a-1     a

CAVEAT EMPTOR

    We have been assuming that we are using exact rational estimates.
    But we will actually use floating point arithmetic, so there are some
    roundoff error issues.  This is why we want to use as little arithmetic
    as possible. With one million terms, we might have a sizable roundoff
    error...

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
import math
from fractions import Fraction
import textwrap

def pi():
    """string pi"""
    return "π"

def pi_sqr_over(over:int):
    """string pi sqr over"""
    return f"{pi()}²/{over}"

def series(args:tuple, next_sign:int=1):
    """string a series"""
    s = ""
    for term in args:
        if term > 0:
            if type(term) == float:
                s += f" + {term:0.5f}"
            else:
                s += f" + {term}"
        elif term < 0:
            if type(term) == float:
                s += f" - {-term:0.5f}"
            else:
                s += f" - {-term}"
    s += " + ..." if next_sign == 1 else " - ..."
    if s[1] == "+":
        s = s[3:]
    return s

print("Python's math.pi =", math.pi)
print()
print("Classical estimates")
print("22/7 =", 22/7, "\terror", math.pi - 22/7)
print("355/113 =", 355/113, "\terror", math.pi - 355/113)
print()

print("Euler's Basel series")
s = tuple(Fraction(1,(x*x)) for x in range(1,6))
print(series(s), "=", pi_sqr_over(6), "=", math.pi**2/6)
print("    after 1000 terms")
s = 0
for n in range(1, 1001):
    s += 1/(n*n)
print(f"\tS(1000) = {s}", "\terror", math.pi**2/6 - s)
est = math.sqrt(6*s)
print(f"\tpi(1000) = {est}", "\terror", math.pi - float(est))
print("    after 1000 terms using Fraction")
s = 0
for n in range(1, 10001):
    s += Fraction(1, n*n)
print(f"\tS(1000) = {float(s)}", "\terror", math.pi**2/6 - float(s))
est = math.sqrt(6*s)
print(f"\tpi(1000) = {est}", "\terror", math.pi - est)
print("    after 10,000 terms")
s = 0
for n in range(1, 10001):
    s += 1/(n*n)
print(f"\tS(10,000) = {s}", "\terror", math.pi**2/6 - s)
est = math.sqrt(6*s)
print(f"\tpi(10,000) = {est}", "\terror", math.pi - float(est))
print("    after 10,000 terms using Fraction")
s = 0
for n in range(1, 1001):
    s += Fraction(1, n*n)
print(f"\tS(10,000) = {float(s)}", "\terror", math.pi**2/6 - float(s))
est = math.sqrt(6*s)
print(f"\tpi(10,000) = {est}", "\terror", math.pi - est)
print("NOTE: 10,000 terms does not compete with 355/113")
print()

print("First cut - alternating series")
def altsign(x):
    """returns 1 if odd and -1 if even"""
    return 1 if x%2 else -1

s = tuple(altsign(x) * Fraction(1,(x*x)) for x in range(1,6))
print(series(s, -1), "=", pi_sqr_over(12), "=", math.pi**2/12)
print("    after 1000 terms")
s = 0
for n in range(1, 1001):
    s += altsign(n) * 1/(n*n)
print(f"\tS(1000) = {s}", "\terror", math.pi**2/12 - s)
est = math.sqrt(12*s)
print(f"\tpi(1000) = {est}", "\terror", math.pi - float(est))
print("    after 1000 terms using Fraction")
s = 0
for n in range(1, 10001):
    s += altsign(n) * Fraction(1, n*n)
print(f"\tS(1000) = {float(s)}", "\terror", math.pi**2/12 - float(s))
est = math.sqrt(12*s)
print(f"\tpi(1000) = {est}", "\terror", math.pi - est)
print("NOTE 1: Our estimate is now better than 355/113...")
print("NOTE 2: Proof that it's better is Leibniz AST...")
print("        AST = alternating series test")
print("NOTE 3: Sadly, still too much arithmetic")

print()
print("second cut - pairing terms using alternating series above")
print("We can cut complexity in half by pairing terms")
    #
    # 1/j**2 +- 1/k**2 = (k**2 +- j**2) / (j*k)**2
    #
def pairsum(j, k):
    """sum of two reciprocal squares"""
    return Fraction(j*j + k*k, j*j*k*k)
    
def pairdiff(j, k):
    """difference of two reciprocal squares"""
    return Fraction(k*k - j*j, j*j*k*k)

print("NOTE: accuracy is essentially unchanged...")
print("NOTE: still too much arithmetic...")

    # terms in consective pairs
print("    (a) consecutive pairs - 500 pairs, 1000 terms")
s = tuple(pairdiff(2*n-1, 2*n) for n in range(1,6))
print("    ", series(s), "=", pi_sqr_over(12))
s = 0
for n in range(1,501):
    s += float(pairdiff(2*n-1, 2*n))
print(f"\tS(1000) = {s}", "\terror", math.pi**2/12 - s)
est = math.sqrt(12*s)
print(f"\tpi(1000) = {est}", "\terror", math.pi - float(est))

    # pairing from opposite ends
print("    (b) pairs from opposite ends - 500 pairs, 1000 terms")
s = tuple(pairdiff(2*n-1, 1002-2*n) for n in range(1,4))
print("     ", series(s), "=", pi_sqr_over(12))
s = tuple(float(pairdiff(2*n-1, 1002-2*n)) for n in range(1,6))
print("     ", series(s), "=", pi_sqr_over(12))
s = 0
for n in range(1,501):
    s += float(pairdiff(2*n-1, 1002-2*n))
print(f"\tS(1000) = {s}", "\terror", math.pi**2/12 - s)
est = math.sqrt(12*s)
print(f"\tpi(1000) = {est}", "\terror", math.pi - float(est))

print()
print("third step - 250 quadruplets, 1000 terms")

four_as_one = """
         1     1     1     1     A + B     C + D
        --- + --- + --- + --- = ------- + -------
         A     B     C     D      AB        CD

                                  (A+B)CD + (C+D)AB
                              = --------------------
                                        ABCD
"""
print(four_as_one)

def iops(a, b, c, d):
    """returns a fraction"""
    cd = c*d
    ab = a*b
    top = (a+b)*cd + (c+d)*ab
    bottom = ab * cd
    return Fraction(top, bottom)

print("    four consecutively as a group")
s = 0
for n in range(1, 251):
    a = 4*n - 3
    b = 4*n - 2
    c = 4*n - 1
    d = 4*n
    term = float(iops(a*a, -b*b, c*c, -d*d))
    s += term
print(f"\tS(1000) = {s}", "\terror", math.pi**2/12 - s)
est = math.sqrt(12*s)
print(f"\tpi(1000) = {est}", "\terror", math.pi - float(est))

# if instead we take three consecutive terms at a time...

print()
print("terms in blocks of three")

three_as_one = """
         1     1     1     A - B     1
        --- - --- + --- = ------- + ---
         A     B     C      AB       C

                                 (B-A)C + AB
                              = --------------
                                     ABC

                                 BC - AC + AB
                              = -------------- > 0
                                     ABC

TERMS: The resulting series is alternating!
       (A, B, and C change sign in each consecutive group)
"""
print(three_as_one)

def iops3(a, b, c, sign):
    """three consecutive terms"""
    ab = a*b
    ac = a*c
    bc = b*c
    abc = a*bc
    top = (bc - ac + ab) * sign
    return top / abc

n = 0
sign = 1
s = 0
prev = float("inf")
goal = 2e-7
print("\tGOAL: known error less than {goal=}, to beat 355/113")
while True:
    a = 3*n + 1
    b = 3*n + 2
    c = 3*n + 3
    n += 1
    term = iops3(a*a, b*b, c*c, sign)
    s += term
    sign = - sign
    if n < 5:
        print(f"\t{n=} term={term:0.5f} partial sum={s:0.5f}")
    abserr = abs(term)
    if abserr < goal:
        break
    if abserr >= prev:
        print(f"WARNING: nondecreasing error at {n=}")
    prev = abserr
print(f"\thalt after {n=} terms:")
print(f"\t\tsum={s} error={term}")
print(f"\tS({n}) = {s}", "\terror", math.pi**2/12 - s)
est = math.sqrt(12*s)
print(f"\tpi({n}) = {est}", "\terror", math.pi - float(est))

print()
print("speeding up convergence by comparing to a telescoping series")
scope = (1 + 0.5)/2     # the telescoping partner (0.75)
s0 = 1                  # the leading terms
sk = lambda k: 1 / (k**2 * (k**2 - 1))
# tk = lambda k: 1 / (k**2 - 1)
s = 0
# t = 0
n = 100
for k in range(2, n+1):
    s += sk(k)
#    t += tk(k)
# print(s, t)   # t should be an estimate of 0.75
        # scope - (zeta(2)-s0) = s
        # scope - s = zeta(2) - s0
        # scope + s0 - s = zeta(2)
s = scope + s0 - s
print(f"\tS({n}) = {s}", "\terror", math.pi**2/6 - s)
est = math.sqrt(6*s)
print(f"\tpi({n}) = {est}", "\terror", math.pi - float(est))
print("NOTE: 100 terms gets us competitive with 355/113")

print()
print("comparing to a telescoping alternating series")
scope = -(1 - 0.5)/2    # the telescoping partner (-0.25)
s0 = 1                  # the leading terms
pk = lambda k: 1 if k % 2 == 1 else -1
sk = lambda k: pk(k) / (k**2 * (k**2 - 1))
# tk = lambda k: pk(k) / (k**2 - 1)
s = 0
# t = 0
k = 1
maxerr = 2e-7
while True:
    k += 1
    s += sk(k)
#     t += tk(k)
    error_term = sk(k+1)
    if abs(error_term) < maxerr:
        break

# print(s, t)   # t should be an estimate of -0.25
        # scope - (zed(2)-s0) = s
        # scope - s = zed(2) - s0
        # scope + s0 - s = zed(2)
s = scope + s0 - s
print(f"\tS({k}) = {s}", "\terror", math.pi**2/12 - s)
print(f"\t\tAST error term = {error_term}")
est = math.sqrt(12*s)
print(f"\tpi({k}) = {est}", "\terror", math.pi - float(est))
print(f"NOTE: {k} terms gets us competitive with 355/113")

print()
print("               APPROXIMANTS OF π")
print(" k       S(k)        e(k)       pi(k)         err           π")
print("-- ---------- -----------  ---------- -----------  ----------")
s = 0
for k in range(2, 51):
    s += sk(k)
    S = scope + s0 - s
    ek = sk(k+1)
    pik = math.sqrt(12*S)
    errk = math.pi - pik
    msg = f"{k:2} {S:9.8f} {ek:+9.8f}  {pik:9.8f} {errk:+9.8f}"
    msg += f"  {math.pi:9.8f}"
    if k == 2:
        msg += "  √10"
    if k == 7:
        msg += "  cf. 22/7"
    if k == 47:
        msg += "  cf. 355/113"
    print(msg)

print()
print("Legend")
print("k - the index of the approximant")
print("S(k) - partial sum estimate - the alternating sum of reciprocal")
print("   squares after subtracting the Leibniz partial sum and adding")
print("   the limit of the Leibniz sum")
print("e(k) - the alternating sum error estimate")
print("pi(k) - √(12 S(k)) - the corresponding estimate of π")
print("err - the difference between the reference value and the estimate")
print("π - the reference value (Python: math.pi)")
print()
print("Notes:")
print("   [1] Values in the table are rounded to nearest 1/100,000,000.")
print("   [2] Note how the rate of convergence slows down as k increases.")
print("   [3] First partial sum (1 at k=1) is omitted.")
print("   [4] The second partial sum (k=2) yields the estimate √10")
print()

epilog = """
With the second partial sum (k=2) we have roughly a typical ancient Egyptian
estimate (about 3.16) of π.  (This estimate is found in the Rhind papyrus
which is dated to about 1550 BCE.)  This Egyptian estimate is close to
the square root of 10, an approximation sometimes used in practical work
by mathematicians in India, for example Brahmagupta (598-668 CE).
(See note [4]: The k=2 estimate is exactly √10.)
After k=7, we have improved upon the
estimate of 22/7 by Archimdes (287-212 BCE)
based on approximating a circle with a 96-gon.
At about k=47, we have a partial sum which improves upon the estimate
of 355/113 known to Chinese mathematician Zu Chongzhi (429-500 CE).
"""
epilog = textwrap.wrap(epilog, width=77, initial_indent='   ',
                       fix_sentence_endings=True)
print("EPILOGUE:")
for line in epilog:
    print(line)
