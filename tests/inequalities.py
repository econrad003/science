"""
tests.inequalities - inequalities involving quadratic rationals
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Test the inequalities module

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
from math import floor, ceil, sqrt, pi, e
from fractions import Fraction
from decimal import Decimal
from random import randrange

from utilities.inequalities import *
from utilities._quadratic import _QFrac
from utilities.brouncker_frac import BrounckerFrac
from utilities.golden_frac import GoldenFrac

print(dir())

print()
print("Task 1. Check the functions...")
print("integer input...")
z = randrange(1000, 10000)
assert is_real(0)
assert is_real(z)
assert is_real(-z)
assert not is_positive(0)
assert is_positive(z)
assert not is_positive(-z)
assert not is_negative(0)
assert not is_negative(z)
assert is_negative(-z)
assert is_zero(0)
assert not is_zero(z)
assert not is_zero(-z)
assert bounds(z) == (z, z)
assert ifloor(z) == z
assert iceil(z) == z
print("ok!")

print("fraction input...")
z1 = randrange(1000, 5000)
z2 = randrange(5001, 10000)
z = Fraction(z1, z2)
zero = Fraction(0,1)
assert is_real(zero)
assert is_real(z)
assert is_real(-z)
assert not is_positive(zero)
assert is_positive(z)
assert not is_positive(-z)
assert not is_negative(zero)
assert not is_negative(z)
assert is_negative(-z)
assert is_zero(zero)
assert not is_zero(z)
assert not is_zero(-z)
assert bounds(z) == (floor(z), ceil(z))
assert bounds(-z) == (floor(-z), ceil(-z))
assert bounds(zero) == (0, 0)
assert ifloor(z) == floor(z)
assert iceil(z) == ceil(z)


print()
print("Task 2. Find the continued fraction for an integer (trivial)...")
print("as an int:")
z = randrange(1000, 10000)
frac = ContinuedFraction(z, debug=True)
print(str(frac))
assert str(frac) == f"[{z};]"
assert len(frac) == 1
assert frac[0] == z
assert frac.is_terminating == True
assert frac.convergent(-1) == 0, f"{frac.convergent(-1)}"
assert frac.convergent(0) == float('inf'), f"{frac.convergent(0)}"
assert frac.convergent(1) == z, f"{frac.convergent(1)}"

print("as a fraction with denominator 1:")
zf = Fraction(z, 1)
frac = ContinuedFraction(zf, debug=True)
print(str(frac))
assert str(frac) == f"[{z};]"
assert len(frac) == 1
assert frac[0] == z
assert frac.is_terminating == True
assert frac.convergent(-1) == 0, f"{frac.convergent(-1)}"
assert frac.convergent(0) == float('inf'), f"{frac.convergent(0)}"
assert frac.convergent(1) == z, f"{frac.convergent(1)}"
print("ok!")

print()
print("Task 3. Find the continued fraction for a fraction...")
z1 = randrange(1000, 5000)
z2 = randrange(5001, 10000)
z = Fraction(z2, z1)
frac = ContinuedFraction(z, debug=True)
print(str(frac), "<-- CFRAC")
a = [0, 1]
b = [1, 0]
for n in range(len(frac)):
    q = frac[n]
    a0 = q*a[-1] + a[-2]
    a.append(a0)
    b0 = q*b[-1] + b[-2]
    b.append(b0)
    print(f"{n+1} q={q} a={a0} b={b0}")
assert z == Fraction(a0, b0)
assert frac.is_terminating == True
assert frac.convergent(-1) == 0, f"{frac.convergent(-1)}"
assert frac.convergent(0) == float('inf'), f"{frac.convergent(0)}"
assert frac.convergent(1) == floor(z), f"{frac.convergent(1)}"
for n in range(0, len(frac)):
    conv = frac.convergent(n+1)
    exp = Fraction(a[n+2],b[n+2])
    assert conv == exp, f"{n+1} {conv} {exp}"
print("ok!")

print()
print("Task 4. Find the continued fraction for the square root of two...")
z = BrounckerFrac(0, 1, 1)
print(f"z={z}  bounds={bounds(z)}  positive? {is_positive(z)}")
assert bounds(z) == (1, 2), f"{bounds(z)}"
assert is_real(z)
assert is_positive(z)
assert not is_negative(z)
assert quadrant_I(z), f"real?={is_real(z)}, Re(z)={z.real}, Im(z)={z.imag}"
frac = ContinuedFraction(z, debug=True)
assert str(frac) == "[1; | 2]"
assert len(frac) == 2
assert frac.is_terminating == False
assert frac.convergent(-1) == 0, f"{frac.convergent(-1)}"
assert frac.convergent(0) == float('inf'), f"{frac.convergent(0)}"
assert frac.convergent(1) == ifloor(z), f"{frac.convergent(1)}"
a = [0, 1]
b = [1, 0]
for n in range(15):
    q = frac[n]
    assert q == 2 if n>0 else 1
    a0 = q*a[-1] + a[-2]
    a.append(a0)
    b0 = q*b[-1] + b[-2]
    b.append(b0)
    print(f"{n+1} q={q} a={a0} b={b0}  est={float(a0/b0)}")
print(f"\t{z}: {sqrt(2)}")
err = sqrt(2) - a0/b0
print(f"\tError: {err}")
assert abs(err) < 0.0001
for n in range(1, 15):
    conv = frac.convergent(n)
    exp = Fraction(a[n+1],b[n+1])
    # print(f"NEXT {n} {conv} {exp}")
    assert conv == exp, f"{n} {conv} {exp}"
print("ok!")

print()
print("Task 5. Find the continued fraction for the square root of three...")
z = _QFrac(0, 1, 1, 3)
print(f"z={z}  bounds={bounds(z)}  positive? {is_positive(z)}")
assert bounds(z) == (1, 2), f"{bounds(z)}"
assert is_real(z)
assert is_positive(z)
assert not is_negative(z)
assert quadrant_I(z), f"real?={is_real(z)}, Re(z)={z.real}, Im(z)={z.imag}"
frac = ContinuedFraction(z, debug=True)
assert str(frac) == "[1; | 1,2]"
assert len(frac) == 3
assert frac.is_terminating == False
a = [0, 1]
b = [1, 0]
for n in range(15):
    q = frac[n]
    assert q == 2 if n>0 and n%2==0 else 1
    a0 = q*a[-1] + a[-2]
    a.append(a0)
    b0 = q*b[-1] + b[-2]
    b.append(b0)
    print(f"{n+1} q={q} a={a0} b={b0}  est={float(a0/b0)}")
print(f"\t{z}: {sqrt(3)}")
err = sqrt(3) - a0/b0
print(f"\tError: {err}")
assert abs(err) < 0.0001
print("ok!")

print()
print("Task 6. Find the continued fraction for the golden ratio...")
print("\tNOTE: Convergence is as slow it gets!  (All those ones!)")
z = GoldenFrac(1, 1, 2)
print(f"z={z}  bounds={bounds(z)}  positive? {is_positive(z)}")
assert bounds(z) == (1, 2), f"{bounds(z)}"
assert is_real(z)
assert is_positive(z)
assert not is_negative(z)
assert quadrant_I(z), f"real?={is_real(z)}, Re(z)={z.real}, Im(z)={z.imag}"
frac = ContinuedFraction(z, debug=True)
assert str(frac) == "[1; | 1]"
assert len(frac) == 2
assert frac.is_terminating == False
a = [0, 1]
b = [1, 0]
for n in range(15):
    q = frac[n]
    assert q == 1
    a0 = q*a[-1] + a[-2]
    a.append(a0)
    b0 = q*b[-1] + b[-2]
    b.append(b0)
    print(f"{n+1} q={q} a={a0} b={b0}  est={float(a0/b0)}")
print(f"\t{z}: {(1+sqrt(5))/2}")
err = (1+sqrt(5))/2 - a0/b0
print(f"\tError: {err}")
assert abs(err) < 0.0001
errphi = err
print("ok!")

print()
print("Task 7. Improve the estimate for the golden ratio...")
print("7a) find a continued fraction for √5")
z = GoldenFrac(0, 1, 1)
print(f"z={z}  bounds={bounds(z)}  positive? {is_positive(z)}")
assert bounds(z) == (2, 3), f"{bounds(z)}"
assert is_real(z)
assert is_positive(z)
assert not is_negative(z)
assert quadrant_I(z), f"real?={is_real(z)}, Re(z)={z.real}, Im(z)={z.imag}"
frac = ContinuedFraction(z, debug=True)
assert str(frac) == "[2; | 4]"
assert len(frac) == 2
assert frac.is_terminating == False
a = [0, 1]
b = [1, 0]
for n in range(10):
    q = frac[n]
    assert q == 4 if n > 0 else 2
    a0 = q*a[-1] + a[-2]
    a.append(a0)
    b0 = q*b[-1] + b[-2]
    b.append(b0)
    print(f"{n+1} q={q} a={a0} b={b0}  est={float(a0/b0)}")
print(f"\t{z}: {sqrt(5)}")
err = sqrt(5) - a0/b0
print(f"\tError: {err}")
assert abs(err) < 0.0001
print("7b) Here is our new estimate of the golden ratio:")
print(f"\t{(z+1)/2}: {(1+sqrt(5))/2}")
err = (sqrt(5) - a0/b0)/2
print(f"\tError: {err}")
assert abs(err) < 0.0001
print(f"NOTE: 2/3 effort, improvement factor {round(abs(errphi/err),-5)}")
print("ok!")

print()
print("Task 8. Bombelli's continued fraction for √13...")
print("\tNOTE 1: Convergence is slow!  (All those ones!)")
print("\tNOTE 2: Bombelli (1572) used a different representation.")
z = _QFrac(0, 1, 1, 13)
print(f"z={z}  bounds={bounds(z)}  positive? {is_positive(z)}")
assert bounds(z) == (3, 4), f"{bounds(z)}"
assert is_real(z)
assert is_positive(z)
assert not is_negative(z)
assert quadrant_I(z), f"real?={is_real(z)}, Re(z)={z.real}, Im(z)={z.imag}"
frac = ContinuedFraction(z, debug=True)
assert str(frac) == "[3; | 1,1,1,1,6]"
assert len(frac) == 6
assert frac.is_terminating == False
a = [0, 1]
b = [1, 0]
for n in range(15):
    q = frac[n]
    if n == 0:
        assert q==3 # n=0
    else:
        assert q == 6 if n%5==0 else 1 # n>0
    a0 = q*a[-1] + a[-2]
    a.append(a0)
    b0 = q*b[-1] + b[-2]
    b.append(b0)
    print(f"{n+1} q={q} a={a0} b={b0}  est={float(a0/b0)}")
print(f"\t{z}: {sqrt(13)}")
err = sqrt(13) - a0/b0
print(f"\tError: {err}")
assert abs(err) < 0.0001
err13 = err
print("ok!")

print()
print("Task 9. Improve the rational estimate of sqrt(13)...")
print("\tNOTE: Convergence is slow!  (All those ones!)")
z = _QFrac(1, 1, 2, 13)
print(f"z={z}  bounds={bounds(z)}  positive? {is_positive(z)}")
assert bounds(z) == (2, 3), f"{bounds(z)}"
assert is_real(z)
assert is_positive(z)
assert not is_negative(z)
assert quadrant_I(z), f"real?={is_real(z)}, Re(z)={z.real}, Im(z)={z.imag}"
frac = ContinuedFraction(z, debug=True)
assert str(frac) == "[2; | 3]"
assert len(frac) == 2
assert frac.is_terminating == False
a = [0, 1]
b = [1, 0]
for n in range(15):
    q = frac[n]
    assert q == 3 if n>0 else 2
    a0 = q*a[-1] + a[-2]
    a.append(a0)
    b0 = q*b[-1] + b[-2]
    b.append(b0)
    print(f"{n+1} q={q} a={a0} b={b0}  est={float(a0/b0)}")
print(f"\t{z}: {(1+sqrt(13))/2}")
err = (1+sqrt(13))/2 - a0/b0
print(f"\tError: {err}")
assert abs(err) < 0.0001
print("NOTE: Here is our new estimate of Bombelli's number:")
print(f"\t{z*2-1}: {sqrt(13)}")
err = sqrt(13) - 2*a0/b0 + 1
print(f"\tError: {err}")
assert abs(err) < 0.0001
print(f"NOTE: same effort, improvement factor {round(abs(err13/err),-4)}")
print("ok!")

print()
print("Task 10. A messy continued fraction...")
z = _QFrac(103, 1, 97, 1297)
print(f"z={z}  bounds={bounds(z)}  positive? {is_positive(z)}")
assert bounds(z) == (1, 2), f"{bounds(z)}"
assert is_real(z)
assert is_positive(z)
assert not is_negative(z)
assert quadrant_I(z), f"real?={is_real(z)}, Re(z)={z.real}, Im(z)={z.imag}"
frac = ContinuedFraction(z, debug=True)
assert str(frac) == "[1; 2 | 3,4,5]"
assert len(frac) == 5
assert frac.is_terminating == False
a = [0, 1]
b = [1, 0]
qs = [1, 2, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5]
for n in range(12):
    q = frac[n]
    assert q == qs[n], f"{q} {qs[n]}"
    a0 = q*a[-1] + a[-2]
    a.append(a0)
    b0 = q*b[-1] + b[-2]
    b.append(b0)
    print(f"{n+1} q={q} a={a0} b={b0}  est={float(a0/b0)}")
print(f"\t{z}: {(103+sqrt(1297))/97}")
err = (103+sqrt(1297))/97 - a0/b0
print(f"\tError: {err}")
assert abs(err) < 0.0001
for n in range(10):
    print(n, frac.convergent(n))
c12 = frac.convergent(12)
assert frac.convergent(12) == Fraction(3723550, 2598189), f"{c11}"
print("ok!")

print()
print("Task 11. Messing around with π...")
print("11a) Some standard estimates of π:")

print("="*20, "3.14", "="*20)
z = Decimal("3.14")
z1 = z.as_integer_ratio()
z2 = Fraction(*z1)
frac = ContinuedFraction(z2, debug=True)
print(f"\t{z} = {frac}  err={pi-z2:.5}")

print("="*20, "22/7", "="*20)
z = Fraction(22, 7)
frac = ContinuedFraction(z, debug=True)
print(f"\t{z} = {frac}  err={pi-z:.5}")

print("="*19, "355/113", "="*18)
z = Fraction(355, 113)
frac = ContinuedFraction(z, debug=True)
print(f"\t{z} = {frac}  err={pi-z:.8f}")

print("11b) Pythonic estimate of π:")
z = Fraction(pi)
frac = ContinuedFraction(z, debug=True)
print(f"\t{pi} = {z} = {frac}  err={pi-z}")
print("convergents:")
for n in range(1, 10):
    zn = frac.convergent(n)
    err = pi-zn
    print(f"{n:2} {zn} {err=}")

print()
print("Task 12. Messing around with e...")
print("11a) Some standard estimates of e:")
z = Decimal("2.7")
z1 = z.as_integer_ratio()
z2 = Fraction(*z1)
frac = ContinuedFraction(z2, debug=True)
print(f"\t{z} = {frac}  err={e-z2:.5}")

z = Decimal("2.718281828")
z1 = z.as_integer_ratio()
z2 = Fraction(*z1)
frac = ContinuedFraction(z2, debug=True)
print(f"\t{z} = {frac}  err={e-z2:.15}  2.7 Andrew Jackson Andrew Jackson")

z = e
z2=Fraction(z)
frac = ContinuedFraction(z2, debug=True)
print(f"\t{z} = {frac}  err={z-z2:.15}")

print()
print("sqrt(e):")
z = sqrt(e)
z2=Fraction(z)
frac = ContinuedFraction(z2, debug=True)
print(f"\t{z} = {frac}  err={z-z2:.15}")

print("SUCCESS!")
