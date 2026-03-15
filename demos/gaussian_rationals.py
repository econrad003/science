"""
demos.gaussian_rationals - Gaussian rational numbers demonstration
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module uses the utilities to display some facts about the
    Gaussian rational numbers.  It also checks to make sure that the
    module does what it is supposed to do.

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
    # imports from standard packages
from math import sqrt, gcd, trunc, floor, ceil
from random import randrange as p
from fractions import Fraction

    # imports from the science utilities module
from utilities._quadratic import _QFrac
from utilities.gauss_frac import GaussianFrac

print("Performing sanity checks...")
    # verify the square-free check
for d in {300, 2*3*89*89}:
    try:
        _QFrac(1,1,1,d)
        assert False, f"{d} is not square-free"
    except ValueError as msg:
        print(f"{msg} (OK: {d} is not square-free)")

    # define some constants
ONE = GaussianFrac(1, 0, 1)                     # 1
MINUS_ONE = - ONE                               # -1
I = GaussianFrac(0, 1, 1)                       # i
MINUS_I = - I                                   # -i

D2a = ONE + I                                   # 1+i  (prime divisors of two)
D2b = D2a.conjugate()                           # 1-i           "
D2c = - ONE - I                                 # -1-i          "
D2d = D2c.conjugate()                           # -1+i          "
s2 = {D2a, D2b, D2c, D2d}
TWO = D2a * D2b                                 # 2

THREE = GaussianFrac(3, 0, 1)                   # 3
FOUR = GaussianFrac(4, 0, 1)                    # 4

D5a = GaussianFrac(1, 2, 1)                     # 1+2i (prime divisors of 5)
D5b = ONE - TWO * I                             # 1-2i          "
D5c = - D5a                                     # -1-2i         "
D5d = - D5b                                     # -1+2i         "
D5e = GaussianFrac(2, 1, 1)                     # 2+i           "
D5f = TWO - I                                   # 2-i           "
D5g = - D5e                                     # -2-i          "
D5h = - D5f                                     # -2+i          "
s5 = {D5a, D5b, D5c, D2d, D5e, D5f, D5g, D5h}
FIVE = GaussianFrac(5, 0, 1)                    # 5

    # lots of assertions
assert ONE == 1, f"{ONE} = 1"
assert MINUS_ONE == -1, f"{MINUS_ONE} = -1"
assert MINUS_I._value == [0, -1, 1, -1], f"{MINUS_I}: {MINUS_I._value}  [0,-1,1,-1]"
assert MINUS_I == GaussianFrac(0, 2, -2), f"{MINUS_I},{GaussianFrac(0, 2, -2)}  -i"
assert I.reciprocal == MINUS_I, f"{I.reciprocal} = {MINUS_I}  -i"
assert MINUS_I == 1 / I, f"{MINUS_I} = {1/I}  -i"

assert D2a == GaussianFrac(2, 2, 2), f"{D2a} = {GaussianFrac(2,2,2)}  1+i"
assert D2b == ONE - I, f"{D2b} = {ONE} - {I} = {ONE-I}  1-i"
assert D2c == MINUS_ONE * D2a, f"{D2c} = {MINUS_ONE}*{D2A} = {MINUS_ONE*D2a}  -1-i"
assert D2d == I * D2a, f"{D2d} = {I}*{D2a} == {I*D2a}  -1+i"

assert D5a * D5b == FIVE == D5c * D5d, f"{D5a*D5b} == {FIVE} == {D5c*D5d}  5"
assert D5e * D5f == FIVE == D5g * D5h, f"{D5e*D5f} == {FIVE} == {D5g*D5h}  5"

assert D5a * D5d == - FIVE == D5b * D5c, f"{D5a*D5d} == {FIVE} == {D5b*D5c}  -5"
assert D5e * D5h == - FIVE == D5b * D5c, f"{D5e*D5h} == {FIVE} == {D5f*D5g}  -5"

assert D5a * D5e == FIVE * I == D5c * D5g, f"{D5a*D5e} == {FIVE*I} == {D5c*D5g}  5i"

        #      4    +-------------+
        #           |             |
        #   11/3    |             |
        #           |             |
        #   10/3    |             |
        #           |             |
        #      3    +-------------+
        #           2   7    8    3
        #              ---  ---
        #               3    3
print("rounding checks")
z = GaussianFrac(7, 11, 3)
assert round(z) == GaussianFrac(2, 4, 1)
assert trunc(z) == GaussianFrac(2, 3, 1)
assert floor(z) == z.southwest == GaussianFrac(2, 3, 1)
assert ceil(z) == z.northeast == GaussianFrac(3, 4, 1)
assert z.southeast == GaussianFrac(3, 3, 1)
assert z.northwest == GaussianFrac(2, 4, 1)
q, r = divmod(z, ONE)
assert z == q + r
assert r.sqnorm < 1
assert z // ONE == q
assert z % ONE == r

z = GaussianFrac(-7, -11, 3)
assert round(z) == GaussianFrac(-2, -4, 1)
assert trunc(z) == GaussianFrac(-2, -3, 1)
assert floor(z) == z.southwest == GaussianFrac(-3, -4, 1)
assert ceil(z) == z.northeast == GaussianFrac(-2, -3, 1)
assert z.southeast == GaussianFrac(-2, -4, 1)
assert z.northwest == GaussianFrac(-3, -3, 1)
q, r = divmod(z, ONE)
assert z == q + r
assert r.sqnorm < 1
assert z // ONE == q
assert z % ONE == r

# assert False, "OK TO HERE!"

a, b, c = p(50), p(50), 1+p(50)
z = GaussianFrac(a, b, -c)              # a random third quadrant fraction
assert z == - GaussianFrac(a, b, c)
assert z.conjugate() == GaussianFrac(-a, b, c)
assert z * I == GaussianFrac(b, -a, c)
assert z * z.reciprocal == ONE

print("Sanity checks passed!")

if __name__ == "__main__":
    def rounded(foo:complex) -> str:
        """round a complex number to four places to right"""
        x = "%0.4f" % foo.real
        y = "%+0.4f" % foo.imag
        return x + y + "i"

    print("-" * 72)
    print("Facts about ℚ(i) and ℤ[i]...")
    print("1. The Gaussian rational numbers ℚ(i) consist of complex numbers whose")
    print("   real and imaginary parts are both rational.  For example:")
    print(f"        z = {z}")
    print(f"   The real part is Re(z)={z.real} and its imaginary part Im(z)={z.imag}.")
    print("   We write these in a normal form (a+bi)/c where a, b and c are")
    print("   integers, c is positive, and the greatest common divisor of a, b,")
    print("   and c is 1:")
    print(f"       gcd({a},{b},{c}) = {gcd(a,b,c)}")
    print()
    print("2. The number i is one of two square roots of -1.  If we draw two")
    print("   perpendicular number lines, one horizontal with integers increasing")
    print("   from left to right and the other vertical with integers increasing")
    print("   from bottom to top, then 0 is (0,0), 1 is (1,0), and i is (0,1).")
    print("   The coordinate system is right-handed, so the first coordinate is")
    print("   horizontal, the second vertical.  The other square root of -1 is -i,")
    print("   located at (0,-1).")
    print()
    print("3. We consider only the rational points in our coordinate system. If")
    print("   the first coordinate is x and the second y, then the point (x,y)")
    print("   is the location of z=x+iy.  This respresentation of complex numbers")
    print("   as points in a Cartesian plane is known as the Argand plane.")
    print()
    print(f"   Our sample point z={z} is located in the third quadrant, {a}/{c}")
    print(f"   units to the left and {b}/{c} units down from the origin.")
    print()
    print("4. The complex norm or absolute value is somewhat inconvenient as square")
    print("   roots may be required, so we normally square the norm:")
    print(f"       N({z}) = (z.real)² + (z.imag)² = {z.sqnorm}")
    print(f"       |z| = √N(z) ≈ {abs(z)}")
    print("   The square norm N(z) (python z.sqnorm) is an exact value, but the")
    print("   calculated absolute value (or norm) given here is an approximation,")
    print("   unless N(z) is a perfect square.")
    print()
        # Pythagorean triples
    z1 = GaussianFrac(5, 12, 1)
    z2 = GaussianFrac(5, 12, 13)
    print("5. Rational Pythagorean triples occur when the square norm N(z) is")
    print("   a perfect square.  For example consider the following fact:")
    print(f"       5² + 12² = {z1.sqnorm}  and √169 = {abs(z1)}")
    print("   Let z=5+12i.  Then |z|=13 (exactly).  So (5,12,13) is an example")
    print("   of a Pythagorean triple.  We can obtain more triples from this one")
    print("   in a number of ways,  Three trivial ways are as follows:")
    print("       a) change the sign of some of the entries; or")
    print("       b) interchange some of the entries; or")
    print("       c) multiply the numbers by the same rational number.")
    print("   But (5,12,13) is special in ways that others obtained in either way")
    print("   are not:")
    print("       a) 5, 12, and 13 are all integers;")
    print("       b) 5 ≤ 12 ≤ 13;")
    print("       c) 5, 12, and 13 are all positive; and")
    print("       d) gcd(5, 12, 13) = 1.")
    print("   A Pythagorean triple which satisfies all four conditions is")
    print("   primitive.  If the one or all of the entries are zero, then the")
    print("   triple is trivial.  So:")
    print("       a) (3,4,5), (5,12,13) and (8,15,17) are primitive;")
    print("       b) (0, 0, 0), (1,0,1) and (0, -17, 0) are trivial;")
    print("       c) (15, 8, 17) is not primitive (interchange);")
    print("       d) (-5, 8, 13) is not primitive (sign);")
    print("       e) (6, 8, 10) is not primitive (gcd);")
    print("       f) (3, 4, 6) is not a Pythagorean triple (3²+4²=25≠6²)")
    print("   If we divide by the third number, something interesting happens:")
    print(f"       Let z = {z2}.  Then:")
    print(f"        N(z) = (5/13)² + (12/13)² = {z2.sqnorm}")
    print("   The square norm and the norm are both equal to 1.  Basically we")
    print("   have projected the Pythagorean triple onto the unit circle about")
    print("   the origin.")
    print()
    print("   Pythagorean triples have been known since ancient times.  Our")
    print("   first evidence for them comes from cuneiform tablets in")
    print("   Mesopotamia dating to about 1850 BCE, or about 1200 to 1300 years")
    print("   before Pythagoras.  We know that some Babylonian scribes knew some")
    print("   way of constructing them, but we don't know the actual procedure")
    print("   that they used, or how complete it was.  The first known complete")
    print("   algorithm for finding primitive Pythagorean triples is found in")
    print("   Euclid's Elements and is usually dated to about 300 BCE, or about")
    print("   1500 years after they were encountered in Babylonian records, and")
    print("   about 200 years after Pythagoras.")
    print()

        # Gaussian integers

    print()
    print("6. If we restrict ourselves to Gaussian fractions with denominator 1,")
    print("   our domain is the set ℤ[i] of Gaussian integers.  Although the")
    print("   Gaussian integers are not ordered, they do share many properties")
    print("   with the ordinary integers.  Among others are the facts that they")
    print("   contain a subset of prime numbers and that there is a unique")
    print("   factorization theorem.")
    print()
    print("       Brace yourself... this gets involved!")
    print()
    print("   In the \"natural numbers\", the positive integers and zero, there")
    print("   is a well-defined division operation (apart from dividing by")
    print("   zero) which satisfies the following theorem:")
    print()
    print("       Division Algorithm for ℕ:")
    print("          For every natural number a and every positive integer b,")
    print("       there are unique natural numbers q and r such that:")
    print("              i)  a = qb + r; and")
    print("              ii) 0 ≤ r < b.")
    print()
    print("   The numbers a and b are known as the dividend and the divisor.")
    print("   The numbers q and r are known as the quotient and the remainder.")
    print("   To generalize this to the integers, we need the notion of absolute")
    print("   value.  Once we have it, it is easy to generalize:")
    print()
    print("       Division Algorithm for ℤ:")
    print("          For every integer a and every nonzero integer b,")
    print("       there are unique integers q and r such that:")
    print("              i)  a = qb + r; and")
    print("              ii) 0 ≤ r < |b|.")
    print()
    print("   Note that very little wording has changed.  The big change was")
    print("   enclosing the divisor in absolute value bars in point (ii).  Other")
    print("   that, we just changed the domain.  This is called floor division:")
    print()
    print("          a   b                                      q   r")
    print("         24   5   24 =  4 ×  5 + 4; 0 ≤ 4 < |5|      4   4")
    print("        -24   5  -24 = -5 ×  5 + 1; 0 ≤ 1 < |5|     -5   1")
    print("         24  -5   24 = -4 × -5 + 4; 0 ≤ 4 < |-5|    -4   4")
    print("        -24  -5  -24 =  5 × -5 + 1; 0 ≤ 1 < |-5|     5   1")
    print()
    print("   Note that the quotient in this particular division is not")
    print("   symmetric with respect to arithmetic sign:")
    print()
    print("         24/5 = -24/-5 = 4.8")
    print("        -24/5 = 24/-5 = -4.8")
    print()
    print("   But we can make the quotient symmetric by changing the requirements")
    print("   for the remainder:")
                    # b=5  r=-2 -1 0 1 2
                    # b=6  r= -2 -1 0 1 2 3
    print()
    print("       Symmetric Division Algorithm for ℤ:")
    print("          For every integer a and every nonzero integer b,")
    print("       there are unique integers q and r such that:")
    print("              i)   a = qb + r;")
    print("              ii)  0 ≤ |r| < |b|; and")
    print("              iii) if r ≠ 0, then sgn(r) = sgn(a)")
    print()
    print("   Condition (iii) on the remainder makes sure that, if there is a ")
    print("   remainder, then its sign is the same as the sign of the dividend.")
    print()
    print("          a   b                                          q   r")
    print("         24   5   24 =  4 ×  5 + 4; 0 ≤  |4| < |5|       4   4")
    print("        -24   5  -24 = -4 ×  5 - 4; 0 ≤ |-4| < |5|      -4  -4")
    print("         24  -5   24 = -4 × -5 + 4; 0 ≤  |4| < |-5|     -4   4")
    print("        -24  -5  -24 =  4 × -5 - 4; 0 ≤ |-4| < |-5|      4  -4")
    print()
    print("7. Division algorithm.")
    print("   The Gaussian integers also have a division algorithm.  We can")
    print("   make it unique, but it is easier to state conditions if we don't")
    print("   worry about uniqueness.")
    print()
    print("       Division Algorithm for ℤ[i]:")
    print("          For every Gaussian integer a and every nonzero Gaussian")
    print("          integer b, there are Gaussian integers q and r such that:")
    print("              i)  a = qb + r; and")
    print("              ii) 0 ≤ |r| < |b|.")
    print()
    print("   To make it unique, we could add conditions on the quadrants for")
    print("   the quotient and remainder.  These conditions are implicit in the")
    print("   how we rounded quotient.  Now for a few examples.")
    print()
    z3 = z * z.denominator
    z3 *= z3 + 10
    u = I * 3 - 2
    q, r = divmod(z3, u)
    print(f"   Let a = {z3} and b = {u}.  One possibility:")
    print(f"         q = {q} and r = {r}.")
    print(f"   Does this meet the requirements?")
    print(f"         bq + r = {u*q+r}")
    print(f"         N(r) = {r.sqnorm};  N(b) = {u.sqnorm}")
    assert u*q+r == z3
    assert r.sqnorm < u.sqnorm
    print("   Since a=bq+r and N(r)<N(b), the requirements have been met.")
    print("   (The square norm is never negative, and it is the square of")
    print("   the absolute value.  So all we need to do for (ii) is to compare")
    print("   the square norms.)")
    print()
    print("8. Gaussian primes.")
    print("   Positive prime integers are Gaussian primes if and only if")
    print("   they are congruent to 3 modulo 4.  So 3, 7 and 11 are Gaussian")
    print("   but 2, 5 and 13 are not.  Let's try dividing each of those")
    print("   ordinary primes by Gaussian integers to get the divisors of")
    print("   each.  We can stay in the first quadrant...")

    divisors = dict()
    dividends = dict()
    for x in 2, 3, 5, 7, 11, 13:
        dividends[x] = GaussianFrac(x, 0, 1)
        divisors[x] = set()

    for i in range(1, 14):
        for j in range(0, 14):
            divisor = GaussianFrac(i, j, 1)
            for x in dividends:
                dividend = dividends[x]
                q, r = divmod(dividend, divisor)
                if r == 0:
                    divisors[x].add(divisor)

    for x in 2, 3, 5, 7, 11, 13:
        print()
        n = 0
        print(f"   Divisors of {x} in the first quadrant:")
        s = ""
        for y in divisors[x]:
            if n % 10 == 0 and n > 0:
                s += "\n"
            s += str(y) + ", "
            n += 1
        s = s[:-2]
        m = max(5, 50-len(s))
        print("       {" + s + "}", " " * m, f"\td({x})={4*n}")
        if n == 2:
            print(f"       {x} is a Gaussian prime.")

    print()
    print("   The value d(p) on the right is the actual number of divisors.")
    print("   The missing divisors are found by multiplying by i, -1 and -i.")
    print("   To see that 2+3i is a divisor of 13, multiply by the conjugate:")
    print()
    a, b = I*3+2, -I*3+2
    print(f"       ({a}) × ({b}) = {a*b}")
    assert a*b == 13

    print()
    print("9. The Euclidean algorithm.")
    print("   The Gaussian integers have a greatest common denominator algorithm.")
    print("   In honor of Euclid, the basic algorithm is known as the Euclidean")
    print("   algorithm.  It does not involve any actual factoring -- it is")
    print("   just a sequence of repeated divisions.")
    print()
    print("   Let's see how it works by finding the gcd of 4180 and 177905:")
    print()
    print("            a      b      q      r")
    print("       ------ ------ ------ ------")
    print("       177905   4180     42   2345    b |= a; r |= b")
    print("         4180   2345      1   1835")
    print("         2345   1835      1    510")
    print("         1835    510      3    305")
    print("          510    305      1    205")
    print("          305    205      1    100")
    print("          205    100      2      5")
    print("          100      5     20      0    if r = 0, then b |= gcd")
    print()
    print("   Then gcd(177905, 4180) = 5.")
    print()
    print("   The maximum number of steps is aproximately the logarithm to the")
    print("   base (1+√5)/2 of the larger number.  This particular logarithm")
    print("   of 177905 is about 25.122, so we expect no more than 25 or 26 steps.")
    print("   The actual number of steps was 8.")
    print()
    print("   Now, using the sequence of quotients:")
    print()
    print("            1")
    print("       42 + --------------------------")
    print("                1")
    print("            1 + ----------------------")
    print("                    1")
    print("                1 + ------------------")
    print("                        1")
    print("                    3 + --------------")
    print("                            1")
    print("                        1 + ----------")
    print("                                1")
    print("                            1 + ------")
    print("                                    1")
    print("                                2 + --")
    print("                                    20")
    print()
    print("   The numerators are all 1.  The term before each plus sign is a")
    print("   quotient.  As a shorthand, we write this as an augmented row")
    print("   vector:")
    print()
    print("       [42; 1 1 3 1 1 2 20]")
    print()
    print("                   0      1")
    print("                   1      0")
    print("       42         42      1      42")
    print("        1         43      1      43")
    print("        1         85      2      42.5")
    print("        3        298      7      42.57142857142857")
    print("        1        383      9      42.55555555555556")
    print("        1        681     16      42.5625")
    print("        2       1745     41      42.5609756097561")
    print("       20      35581    836      42.561004784689")
    print()
    print("   If we multiply 35581 and 836 by the 5, we get 177905 and 4180.")
    print("   Those were our starting numbers and 5 was their GCD.")
    print("   The last column is a series of successive decimal estimates of")
    print("   35581/836, or equivalently, 177905/4180.  We can read off the")
    print("   actual rational estimates from the middle two columns:")
    print()
    print("       42, 43, 85/2, 298/7, 383/9, 681/16, 174/41, 35581/836")
    print()
    print("   A modification of this algorithm allows up to estimate irrational")
    print("   numbers using a continued fraction, or equivalently, an infinite")
    print("   sequence of rational numbers.  (\"Allows\" is not literally true.")
    print("   There are a additional considerations.)")
    print()
    print("   Now let us try it with Gaussian integers.  We will start by")
    print("   building two Gaussian integers.  The units are 1, -1, i, and -i.")
    print("   The unit are 1, -1, i, and -i.  Multiplying by a unit does not")
    print("   change the GCD.")

    afactors = [I+1, I*3+2, I*5+7, I*11-13, I*19-23]
    a = 1
    s = ""
    for factor in afactors:
        a *= factor
        s += "(" + str(factor) + ")"
    print(f"       a = {s} = {a}")
    print(f"       N(a) = {a.sqnorm}")

    bfactors = [I, I+1, I*5-3, I*11+7, I*13-7]
    b = 1
    s = ""
    for factor in bfactors:
        b *= factor
        s += "(" + str(factor) + ")"
    print(f"       b = {s} = {b}")
    print(f"       N(b) = {b.sqnorm}")
    print(f"       gcd(N(a), N(b)) = {gcd(a.sqnorm,b.sqnorm)}")
    a0, b0 = a, b

    print()
    print("\t\t\ta = qb + r")
    print("\t" + "-" * 43)
    print("\t%12s %10s %8s %10s   %7s>%7s" % ("a", "b", "q", "r", "N(b) ", "N(r) "))
    print("\t%12s %10s %8s %10s   %7s %7s" % ("-"*12, "-"*10, "-"*8,
                                               "-"*10, "-"*7, "-"*7))

    qs = list()
    r = float("inf")
    while r != 0:
        q, r = divmod(a, b)
        qs.append(q)
        print("\t%12s %10s %8s %10s   %7d %7d" % (a, b, q, r, b.sqnorm, r.sqnorm))
        a = b
        b = r

    print()
    print(f"   From the last row of the table, the GCD of {a0}")
    print(f"   and {b0} is {a}.  Dividing by the GCD:")
    a1 = a0 / a
    b1 = b0 / a
    print(f"       ({a0}) / ({a}) = {a1}")
    print(f"       ({b0}) / ({a}) = {b1}")
    print("   Also note that:")
    result = a0 / b0

    print(f"       ({a0}) / ({b0})")
    print(f"                  = ({a1}) / ({b1})")
    print(f"                 = {result}")
    print(f"                 ≈ {rounded(complex(result))}")
    assert result == a1 / b1

    print("   Let's work out the continued fraction convergents from the")
    print("   quotient column.")

    print()
    print("\t%11s %11s %11s    error" % ("q", "A", "B"))
    print("                              0           1")
    print("                              1           0")
    A = [0, 1]
    B = [1, 0]
    for q in qs:
        a = A[-1]*q + A[-2]
        b = B[-1]*q + B[-2]
        A.append(a)
        B.append(b)
        delta = result - a / b
        diff = "0" if delta == 0 else "%f" % float(abs(delta))
        print("\t%11s %11s %11s   %s" % (q, a, b, diff))

    print()
    print("   The values in the columns A and B are obtained as follows:")
    print("        A[n] = q[n] A[n-1] + A[n-2]")
    print("        B[n] = q[n] B[n-1] + B[n-2]")
    print("   The bracketed number indicates the row.")
    print()
    print("   The values in the error columns are the complex absolute value")
    print("   of the difference between the result and the estimate A[n]/B[n].")
    print("   Note that these errors decrease to zero (exact).")

# Unicode Double-Struck letters ℕ ℤ ℚ ℝ ℂ
# END demos.gaussian_rationsls
