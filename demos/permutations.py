"""
demos.permutation - permutation groups
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module uses the ten symmetries of a regular pentagon to
    demonstrate programming with the SymmetricGroup class.

    Use it in conjunction with the documentation in file
    doc/permutations.md

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
from utilities.permutation import SymmetricGroup

ALPHABET = "ABCDE"
D5 = SymmetricGroup(alphabet=ALPHABET, name="D₅")

    # Define the identity
I = D5.identity
D5.store('ι', I)
print(f"ι('{ALPHABET}') = '{I.apply(ALPHABET)}'")

    # Define the basic rotation
R = D5.shift(1)
D5.store('ρ', R)
print(f"ρ('{ALPHABET}') = '{R.apply(ALPHABET)}'")

    # Define the remaining rotations
elems = ['ι', 'ρ']
superscripts = "⁰¹²³⁴"
for n in range(2, 5):
    name = f"ρ{superscripts[n]}"
    elems.append(name)
    D5.store(name, D5.shift(n))
    print(f"{name}('{ALPHABET}') = '{D5.fetch(name).apply(ALPHABET)}'")

    # checks
assert R ** 0 == I
assert R ** 1 == R
assert R ** 2 == D5.fetch('ρ²')
assert R ** 3 == D5.fetch('ρ³')
assert R ** 4 == D5.fetch('ρ⁴')
assert R ** 5 == I
assert R ** -1 == R ** 4
assert R * (R ** -1) == I == (R ** -1) * R

    # Define the basic reflection...
T = D5.swap('B', 'E') * D5.swap('C', 'D')
D5.store('τ₀', T)
elems.append('τ₀')
print(f"τ₀('{ALPHABET}') = '{T.apply(ALPHABET)}'")

    # Compose τ₀ with the nontrivial rotations
nu = elems[-1]
g = D5.fetch(nu)
assert g == T
for n in range(1,5):
    mu = elems[n]
    f = D5.fetch(mu)
    print(f"({mu}*{nu})('{ALPHABET}') = '{(f*g).apply(ALPHABET)}'")
    print(f"({nu}*{mu})('{ALPHABET}') = '{(g*f).apply(ALPHABET)}'")

# At this point we discover that we need to rotate two places ccw if we
# reflect first then rotate (i.e. rotate*reflect) inorder to move the
# axis of rotation to the next vertex ccw.

# We have also verified that the dihedral group of the pentagon is not
# commutative.
print("\t*** Note that the group is not commutative ***")

    # fill in the remaining four reflections
subscripts = "₀₁₂₃₄"
f = D5.fetch("ρ²")
for n in range(1, 5):
    g = (f**n)*T
    name = f"τ{subscripts[n]}"
    permuted = g.apply(ALPHABET)
    print(f"{name}('{ALPHABET}') = '{permuted}'")
    assert permuted[n] == ALPHABET[n]
    D5.store(name, g)
    elems.append(name)
print(elems)
print(f"order of {D5.name}: {len(elems)}")

    # observe that the reflections are their own inverses!
for n in range(5, 10):
    name = elems[n]
    f = D5.fetch(name)
    print(f"{name}⁻¹ = {name};     {name}² = ι")
    g = f.inverse
    h = f ** 2
    assert f == g
    assert h == I

    # prepare tables for the dihedral group D₅
print(f"Tables for {D5.name}")
print()
print("Inverses:")
print(" μ   ║", end="")
for n in range(10):
    print(f" {elems[n]:2}", end="")
print()
print("═════╬" + "═"*31)
print(" μ⁻¹ ║", end="")
for n in range(10):
    f = D5.fetch(elems[n])
    g = f.inverse
    if f == g:              # identity or reflection
        print(f" {elems[n]:2}", end="")
    else:                   # non-trivial rotation
        inverse = "ERROR"
        for m in range(1, 5):
            name = elems[m]
            if D5.fetch(name) == g:
                inverse = name
                break
        print(f" {inverse:2}", end="")
print()
print()
print("Compositions:")
print("   μ*ν ║", end="")
for nu in elems:
    print(f" {nu:2}", end="")
print(" = ν")
print("═══════╬" + "═"*31)
first, other = "μ = ", "    "
for mu in elems:
    print(first, end="")
    first = other
    print(f"{mu:2} ║", end="")
    f = D5.fetch(mu)
    for nu in elems:
        g = D5.fetch(nu)
        h = f*g
        prod = "ERROR"
        for name in elems:
            if D5.fetch(name) == h:
                prod = name
                break
        print(f" {prod:2}", end="")
    print()

        # Associativity
for mu in elems:
    f = D5.fetch(mu)
    for nu in elems:
        g = D5.fetch(nu)
        for sigma in elems:
            h = D5.fetch(sigma)
            if f*(g*h) != (f*g)*h:
                print(f"{mu=} {nu=} {sigma=}  not associative")
