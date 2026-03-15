"""
tests.brouncker - Brounckerian (D=2) rational numbers tests
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module tests rational and integer division in ℚ(√2).

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

from utilities.brouncker_frac import BrounckerFrac as BFrac

print("TESTING BROUNCKERIAN (D=2) RATIONALS MODULE")
print()
ONE = BFrac(1, 0, 1)
print(f"{ONE} = 1")
assert ONE == 1
assert ONE.sqnorm == 1, f"{ONE.sqnorm} == 1"
assert str(ONE) == "1"
assert abs(ONE) == 1

I = BFrac(1, 1, 1)
print(f"z={I}=1+i√2", f" (abs(z)={abs(I)}; N(z)={I.sqnorm})")
assert I.sqnorm == -1, f"N({I}) = {I.sqnorm}, expected -1"
assert abs(I) == 1, f"abs({I}) = {abs(I)}, expected 1"

print()
print("SECTION 1. ROUNDING")
print()
print("Verify rounding:")
max_delta = -float("inf")
min_delta = float("inf")
for i in range(-10, 11):
    for j in range(-10, 11):
        z = BFrac(i, j, 10)
        iz = round(z)
        n1 = z.sqnorm
        n2 = iz.sqnorm
        bottom = iz.denominator
        delta = (z-iz).sqnorm
        max_delta = max(max_delta, delta)
        min_delta = min(min_delta, delta)
        if delta > 0:
            print(f"{i:2} {j:2} z={z} N(z)={n1}",
                  f" ||z||={iz} N(||z||)={n2}",
                  f" Δ={delta}")
        assert delta < 1, f"{i=} {j=} {z} {iz} Δ={delta}"
        assert iz.is_int, f"{i=} {j=} {z} {iz} ENF={iz.enf}"
        if delta == 0:
            assert z.is_int
        else:
            assert not z.is_int

print(f"delta range: [{min_delta},{max_delta}]")
print(f"             [{float(min_delta)},{float(max_delta)}]")

print()
print("Here we see where rounding problems occur...")

errors = dict()

def rounded(which, z, nbr):
    """display the neighbor"""
    delta = (z-nbr).sqnorm
    if delta >= 1:
        print(f"\t{which}: z={z} nbr={nbr} Δ={delta}≥1")
        if not (which in errors):
            errors[which] = 0
        errors[which] += 1

for i in range(5):
    for j in range(5):
        z = BFrac(i, j, 4)
        rounded("   round", z, round(z))
        rounded("   trunc", z, trunc(z))
        rounded("   floor", z, floor(z))
        rounded("    ceil", z, ceil(z))
        rounded("southwest", z, z.southwest)
        rounded("southeast", z, z.southeast)
        rounded("northeast", z, z.northeast)
        rounded("northwest", z, z.northwest)

#print()
for which in errors:
    print(f"{which}: {errors[which]} warnings...")
if len(errors) > 0:
    print("\tDirected rounding should be used with caution.")
else:
    print("\tAll rounding attempts were within tolerance.")

print()
print("SECTION 2. RATIONAL DIVISION")
print()

def easyBkr(n:int, d:int=1, no_zeros:bool=False) -> BFrac:
    """generate a random Brouncker rational

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
    return BFrac(a, b, c)

n = 0
while n < 100:
    a = easyBkr(100, d=50)
    b = easyBkr(100, d=50, no_zeros=True)
    q = a / b
    assert a == q*b, f"{a}  {b}  {q}"
    n += 1
    if n <= 5:
        print(f"{n}: ({a}) / ({b}) = {q}")
print(f"{n} divisions verified ({min(5,n)} displayed)")

print()
print("SECTION 3. DIVISION ALGORITHM (INTEGRAL)")
print()

n = 0
while n < 500:
    a = easyBkr(100, d=50)
    b = easyBkr(100, d=50, no_zeros=True)
    q, r = divmod(a, b)
    assert a == q*b + r, f"{a}  {b}  {q}  {r}"
    assert abs(r.sqnorm) < abs(b.sqnorm), f"{a}  {b}  {q}  {r}  {b.sqnorm}  {r.sqnorm}"
    assert q == a // b, f"{a}  {b}  {q}  {r}  a//b={a//b}"
    assert r == a % b, f"{a}  {b}  {q}  {r}  a%b={a%b}"
    assert q.sqnorm == int(q.sqnorm), f"{a}  {b}  {q}  {r}  {b.sqnorm}  {r.sqnorm}"
    n += 1
print(f"{n} integer divisions verified")

print()
print("SECTION 4. EUCLIDEAN ALGORITHM")
print()

common = I*7 + 25
a = dividend = easyBkr(100000, d=1, no_zeros=True) * common
b = divisor = easyBkr(10000, d=1, no_zeros=True) * common
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
print("SECTION 3. CONTINUED FRACTION")
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

# END tests.brouncker
