"""
tests.golden - Golden (D=5) rational numbers tests
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module tests rational and integer division in ℚ(√5).

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
from random import randrange
from math import trunc, floor, ceil, sqrt
from fractions import Fraction

from utilities.golden_frac import GoldenFrac as GFrac

print("TESTING GOLDEN (D=5) RATIONALS MODULE")
print()
ONE = GFrac(1, 0, 1)
print(f"{ONE} = 1, GNF={ONE.GNFstr}")
assert ONE == 1
assert ONE.sqnorm == 1, f"{ONE.sqnorm} == 1"
assert str(ONE) == "1"
assert abs(ONE) == 1
assert ONE.GNFstr == "1"
assert ONE.GNF == (1, 0)

I = GFrac(1, 1, 2)
print(f"z={I}=1+i√2", f" (abs(z)={abs(I)}; N(z)={I.sqnorm}); GNF={I.GNFstr}")
assert I.sqnorm == -1, f"N({I}) = {I.sqnorm}, expected -1; GNF = {I.GNFstr}"
assert abs(I) == 1, f"abs({I}) = {abs(I)}, expected 1"
assert I.GNF == (0, 1), f"N({I}) = {I.sqnorm}, expected -1; GNF = {I.GNFstr}"
assert I.GNFstr == "φ", f"N({I}) = {I.sqnorm}, expected -1; GNF = {I.GNFstr}"

print()
print("SECTION 1. UNITS")
print()

PHI = I
PHIBAR = PHI.conjugate()
print(f"1/φ = {-PHIBAR};  conj(φ) = {PHIBAR}")

print("Powers of φ and conj(φ):")
H2 = "--"
H15 = "-" * 15
print(" n  φ^n              N  conj(φ)^n        N")
print(f"{H2}  {H15} {H2}  {H15} {H2}")
assert PHIBAR == -1 / PHI
for i in range(11):
    unit1 = PHI ** i
    norm1 = unit1.sqnorm
    unit2 = PHIBAR ** i
    norm2 = unit2.sqnorm
    print(f"{i:2}  {str(unit1):15} {norm1:2}  {str(unit2):15} {norm2:2}")
    a, b = unit1.GNF
    assert unit1 == a + b * PHI, f"{a} {b} {unit1} {unit1.GNF}  {a+b*PHI}"
    a, b = unit2.GNF
    assert unit2 == a + b * PHI, f"{a} {b} {unit2} {unit2.GNF}  {a+b*PHI}"

print()
print("Powers of φ in golden normal form (GNF):")
print(f"{H2}  {H15}  {H15} {H2}")
for i in range(20):
    unit1 = PHI ** i
    print(f"{i:2}  {str(unit1):15}  {unit1.GNFstr:15}")

print()
print("If we write the units in golden normal form, then the components")
print("of the units are consecutive Fibonacci numbers.")

print()
print("SECTION 2. ROUNDING")
print()
print("Verify rounding:")
max_delta = -float("inf")
min_delta = float("inf")
for i in range(-10, 11):
    for j in range(-10, 11):
        z = GFrac(i, j, 10)
        iz = round(z)
        n1 = z.sqnorm
        n2 = iz.sqnorm
        bottom = iz.denominator
        delta = (z-iz).sqnorm
        max_delta = max(max_delta, delta)
        min_delta = min(min_delta, delta)
        if delta != 0:
            print(f"{i:2} {j:2} z={z} N(z)={n1}",
                  f" [z]={iz} N([z])={n2}",
                  f" Δ={delta}")
        assert abs(delta) < 1, f"{i=} {j=} {z} {iz} Δ={delta}, {z.GNFstr} {iz.GNFstr}"
        assert iz.is_int, f"{i=} {j=} {z} {iz} {iz._value}"
        if delta == 0:
            assert z.is_int
        else:
            assert not z.is_int
        assert iz.sqnorm.denominator == 1, f"{i=} {j=} {z} {iz} {iz.sqnorm} {iz._value}"

print(f"delta range: [{min_delta},{max_delta}]")
print(f"             [{float(min_delta)},{float(max_delta)}]")

print()
print("Here we see where rounding problems occur...")

errors = dict()
maxerr = dict()
minerr = dict()

def rounded(which, z, nbr):
    """display the neighbor"""
    delta = (z-nbr).sqnorm
    if not which in maxerr:
        maxerr[which] = - float('inf')
        minerr[which] = float('inf')
    if delta < minerr[which]:
        minerr[which] = delta
    if delta > maxerr[which]:
        maxerr[which] = delta
    if abs(delta) >= 1:
        if not (which in errors):
            print(f"\t{which}: z={z} nbr={nbr} Δ={delta}≥1")
            errors[which] = 0
        errors[which] += 1

n = 0
print("    This may take some time...")
for i in range(-23, 24):
    for j in range(-23, 24):
        z = GFrac(i, j, 23)
        n += 1
        rounded("   round", z, round(z))
        rounded("   trunc", z, trunc(z))
        rounded("   floor", z, floor(z))
        rounded("    ceil", z, ceil(z))
        rounded("southwest", z, z.southwest)
        rounded("southeast", z, z.southeast)
        rounded("northeast", z, z.northeast)
        rounded("northwest", z, z.northwest)
print(f"    {n} values tested")

print("Square-norm error ranges:")
for which in maxerr:
    low = minerr[which]
    high = maxerr[which]
    print(f"\t{which}: [{low}, {high}]\t[{float(low):.4f},{float(high):.4f}]")

print()
for which in errors:
    print(f"{which}: {errors[which]} warnings...")
if len(errors) > 0:
    print("\tDirected rounding should be used with caution.")
else:
    print("\tAll rounding attempts were within tolerance.")

print()
print("SECTION 3. RATIONAL DIVISION")
print()

def easyGold(n:int, d:int=1, no_zeros:bool=False) -> GFrac:
    """generate a random Golden rational

    The distribution is not uniform.

    ARGUMENTS

        n - the numerator coefficients a drawn from range(-n, n+1)
        d (default 1) - the largest possible denominator
        no_zeros (default False) - if True, zero is not in the domain
    """
    while True:
        a = randrange(-n, n+1)
        b = randrange(-n, n+1)
        if no_zeros and (a == 0 == b):
            continue        # reject
        break
    c = 1 + randrange(d)
    return GFrac(a, b, c)

n = 0
while n < 100:
    a = easyGold(100, d=50)
    b = easyGold(100, d=50, no_zeros=True)
    q = a / b
    assert a == q*b, f"{a}  {b}  {q}"
    n += 1
    if n <= 5:
        print(f"{n}: ({a}) / ({b}) = {q}")
print(f"{n} divisions verified ({min(5,n)} displayed)")

print()
print("SECTION 4. DIVISION ALGORITHM (INTEGRAL)")
print()

n = 0
while n < 500:
    a = easyGold(100, d=50)
    b = easyGold(100, d=50, no_zeros=True)
    q, r = divmod(a, b)
    assert a == q*b + r, f"{a}  {b}  {q}  {r}"
    assert abs(r.sqnorm) < abs(b.sqnorm), f"{a}  {b}  {q}  {r}  {b.sqnorm}  {r.sqnorm}"
    assert q == a // b, f"{a}  {b}  {q}  {r}  a//b={a//b}"
    assert r == a % b, f"{a}  {b}  {q}  {r}  a%b={a%b}"
    assert q.sqnorm == int(q.sqnorm), f"{a}  {b}  {q}  {r}  {b.sqnorm}  {r.sqnorm}"
    n += 1
print(f"{n} integer divisions verified")

print()
print("SECTION 5. EUCLIDEAN ALGORITHM")
print()

common = I*7 + 25
a = dividend = easyGold(100000, d=1, no_zeros=True) * common
b = divisor = easyGold(10000, d=1, no_zeros=True) * common
print(f"dividend={a}, divisor={b}")
qs = list()
r = 1
n = 0
while r != 0:
    n += 1
    q, r = divmod(a, b)
    print(f"{n:2}: a={a}  b={b}  q={q}  r={r}")
    assert a == q*b + r          # definition of division
    print(f"\tN(r)={r.sqnorm}  N(b)={b.sqnorm}")
    assert abs(b.sqnorm) > abs(r.sqnorm)   # remainder constraint (for convergence)
    qs.append(q)
    a = b
    b = r
print(f"\t\t{n} passes...")
assert len(qs) == n
print(f"--- GCD({dividend},{divisor}) = {a}")
assert dividend % a == 0
assert divisor % a == 0
print("......... common divisor? yes!")
assert a % common == 0
p1 = dividend / a
p2 = divisor / a
assert dividend / divisor == p1 / p2
assert p1 == dividend // a
assert p2 == divisor // a
g = a           # the gcd

print()
print("SECTION 6. CONTINUED FRACTION")
print()

print("We will recover the dividend and the divisor using the sequence")
print("of quotients.")

A = [0, 1]
B = [1, 0]
expected = dividend / divisor
fmt = "%15s %20s %20s"
print(fmt % ("q", "a", "b"), "   error")
print("-" * 75)
print(fmt % ("", A[0], B[0]))
print(fmt % ("", A[1], B[1]))
fmt1 = fmt + "  %.9f"
fmt2 = fmt + "  %d"
for i in range(len(qs)):
    q = qs[i]
    A.append(a := q*A[i+1] + A[i])
    B.append(b := q*B[i+1] + B[i])
    diff = expected - a / b
    if diff.sqnorm == 0:
        err = 0
        print(fmt2 % (q, a, b, 0))
    else:
        err = abs(diff)
        print(fmt1 % (q, a, b, err))
assert err == 0
assert dividend == a * g, f"{dividend}  {a*g}  GCD={g}"
assert divisor == b * g, f"{divisor}  {b*g}  GCD={g}"
print()
print("......... recovered? yes!")
print(f"dividend: ({a}) * ({g}) = {dividend}")
print(f" divisor: ({b}) * ({g}) = {divisor}")

print()
print("SUCCESS!")

# END tests.golden
