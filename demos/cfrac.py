"""
demos.cfrac - Continued fraction table
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This demo produces tables of continued fractions and convergents
    for nonsquare discriminants from 2 through 99. 

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
        ##### IMPORTS
from fractions import Fraction

from utilities._quadratic import _QFrac
from utilities.inequalities import ContinuedFraction

print("Initializing... ", end="")

        ##### GLOBAL DATA

indices = list()
surds = dict()
targets = dict()
cfracs = dict()

        ##### SUPPORT FUNCTIONS

def factor(n:int):
    """factor an integer which is between 1 and 121

    All composite numbers in this range have either 2 or 3 or 5 or 7
    as a factor.
    """
    assert type(n) == int and 1 < n < 121
    factors = dict()
    for p in [2, 3, 5, 7]:      # small primes for n in [2, 120]
        if n % p != 0:
            continue
        factors[p] = 0
        while n % p == 0:
            factors[p] += 1
            n //= p
    if n != 1:
        factors[n] = 1
    return factors

assert factor(40) == {2:3, 5:1}

print("ok!")

        ##### PHASE 1. GATHER THE SURDS

print("Phase 1. Collect the surds... ", end="")
for n in range(2, 100):
    factors = factor(n)
    m, d = 1, 1             # multiplier and discriminant
    for p in factors:        # prime factors
        e = factors[p]          # exponent
        if e % 2 == 1:
            d *= p
        m *= p ** (e // 2)
    if d == 1:
        continue            # perfect square (reject)
    indices.append(n)
    surds[n] = _QFrac(0, m, 1, d)

print("ok!")
#print(indices)
#print(surds)
assert len(indices) == len(surds)

        ##### PHASE 2. GATHER THE TARGETS

print("Phase 2. Gather the targets... ", end="")
for n in indices:
    surd = surds[n]
    targets[n] = [surd, (1+surd)/2, (1+surd)/3, (2+surd)/3]
    
print("ok!")
#print(targets)
assert len(targets) == len(indices)

        ##### PHASE 3. CALCULATE THE CONTINUED FRACTIONS

print("Phase 3. Calculations... ", end="")
for target_list in targets.values():
    for target in target_list:
        # print(target)
        cfracs[target] = ContinuedFraction(target)        
print("ok!")
#print(surds[2], cfracs[surds[2]])

        ##### TABLE 1

print()
print("Table 1.  Table of continued fractions of surds")
print()
print(" n\t√n\tregular continued fraction")
print(f"--\t-----\t{'-'*40}")
for n in indices:
    surd = surds[n]
    print(f"{n:2}\t{surd}\t{cfracs[surd]}")

        ##### TABLE 2

print()
print("Table 2.  Table of continued fractions of (1+√n)/2")
print()
print(" n\t(1+√n)/2\tregular continued fraction")
print(f"--\t--------\t{'-'*40}")
for n in indices:
    target = targets[n][1]
    print(f"{n:2}\t{target}\t{cfracs[target]}")

        ##### TABLE 3

print()
print("Table 3.  Table of continued fractions of (1+√n)/3")
print()
print(" n\t(1+√n)/3\tregular continued fraction")
print(f"--\t--------\t{'-'*40}")
for n in indices:
    target = targets[n][2]
    print(f"{n:2}\t{target}\t{cfracs[target]}")

        ##### TABLE 4

print()
print("Table 4.  Table of continued fractions of (2+√n)/3")
print()
print(" n\t(2+√n)/3\tregular continued fraction")
print(f"--\t--------\t{'-'*40}")
for n in indices:
    target = targets[n][3]
    print(f"{n:2}\t{target}\t{cfracs[target]}")

        ##### TABLE 5 (CONVERGENTS)

print()
print("Table 5.  Table of some convergents of √n")
print()
for n in indices:
    surd = surds[n]
    cfrac = cfracs[surd]
    convergents = list()
    length = 0
    for m in range(2,14):
        z = cfrac.convergent(m)
        length += len(str(z)) + 1
        if length > 74:
            break
        convergents.append(z)
    print(f"{n=}, surd={surd}")
    print("   ", end="")
    for convergent in convergents:
        print(f" {convergent}", end="")
    print()

        ##### TABLE 6 (CONVERGENTS)

print()
print("Table 6.  Table of some convergents of (1+√n)/2")
print()
for n in indices:
    target = targets[n][1]
    cfrac = cfracs[target]
    convergents = list()
    length = 0
    for m in range(2,14):
        z = cfrac.convergent(m)
        length += len(str(z)) + 1
        if length > 74:
            break
        convergents.append(z)
    print(f"{n=}, surd={target}")
    print("   ", end="")
    for convergent in convergents:
        print(f" {convergent}", end="")
    print()

        ##### TABLE 7 (CONVERGENTS)

print()
print("Table 7.  Table of some convergents of (1+√n)/3")
print()
for n in indices:
    target = targets[n][2]
    cfrac = cfracs[target]
    convergents = list()
    length = 0
    for m in range(2,14):
        z = cfrac.convergent(m)
        length += len(str(z)) + 1
        if length > 74:
            break
        convergents.append(z)
    print(f"{n=}, surd={target}")
    print("   ", end="")
    for convergent in convergents:
        print(f" {convergent}", end="")
    print()

        ##### TABLE 8 (CONVERGENTS)

print()
print("Table 8.  Table of some convergents of (2+√n)/3")
print()
for n in indices:
    target = targets[n][3]
    cfrac = cfracs[target]
    convergents = list()
    length = 0
    for m in range(2,14):
        z = cfrac.convergent(m)
        length += len(str(z)) + 1
        if length > 74:
            break
        convergents.append(z)
    print(f"{n=}, surd={target}")
    print("   ", end="")
    for convergent in convergents:
        print(f" {convergent}", end="")
    print()

        ##### TABLE (CONVERGENTS WITH ERROR BOUND)

maxerr = Fraction(1, 100000)
print()
print(f"Table 9.  Table of convergents with error < {maxerr}")
print()
for n in indices:
    target_list = targets[n]
    surd = target_list[0]
    m = 4
    cfrac = cfracs[surd]
    while True:
        c1 = cfrac.convergent(m)
        c2 = cfrac.convergent(m+1)
        if abs(c1-c2) < maxerr:
            break
        m += 1
    print(f"{n=}\t{surd}\t{c1}\t{c2}")
    for k in range(1, 4):
        surd = target_list[k]
        m = 4
        cfrac = cfracs[surd]
        while True:
            c1 = cfrac.convergent(m)
            c2 = cfrac.convergent(m+1)
            if abs(c1-c2) < maxerr:
                break
            m += 1
        print(f"\t{surd}\t{c1}\t{c2}")
print()

# END demos.cfrac
