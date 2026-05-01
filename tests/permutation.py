"""
tests.permutation - a representation of a permutation 
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Test module utilities.permutation.

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
from utilities.permutation import ALPHABET, SymmetricGroup

DIGITS = "0123456789"

        # 1. duplicates are not allowed in the alphabet
print("1. Duplicates...")
try:
    alphabet = DIGITS + "0"
    SymmetricGroup(alphabet)
    assert False, f"1. Duplicates not permitted. {alphabet=}"
except ValueError as msg:
    print(f"   {msg=}")
    print(f"   ok!")

        # 2. create groups
print("2. Create groups...")
S = dict()
for i in range(1, 11):
    S[i] = SymmetricGroup(DIGITS[:i])
    print(f"   Created {S[i].name}...")
    assert S[i].n==i, "2. Mismatched index {i=}: {S[i].n=} != {i}"
    assert S[i].name == f"S({i})", f"{S[i].name=} != 'S({i})'"
S[26] = SymmetricGroup(name="S(English)")
assert S[26].n==26, "2. Mismatched index: {S[26].n=} != 26"
print(f"   Created {S[26].name}...")
assert S[26].name == "S(English)", f"{S[26].name=}"
print("   ok!")

        # 3. check the group indices
print("3. Check indices")
for i in range(1,11):
    G = S[i]
    for j in range(i):
        assert G[j]==str(j), f"G={G.name}, {j=}: {G[j]=} (expected {j})"
        assert G.to_index(str(j)) == j, f"G={G.name}, {G.to_index(str(j))}, {j=}"
G = S[26]
for j in range(26):
    assert G[j]==ALPHABET[j], f"G={G.name}, {j=}: {G[j]} != {ALPHABET[j]}"
    assert G.to_index(ALPHABET[j]) == j, f"G={G.name}, {ALPHABET[j]=}, {j=}"
print("   ok!")

        # 4. working in S(3)
G = S[3]
print(f"4. Working in group {G.name}")
print("   Adding the identity permutation...")
test_pattern = "01230123"
I = G.identity
G.store("I", I)
assert G.fetch("I") is I
assert I == I
assert I == 1
assert I*1 == I
assert 1*I == I
assert I*I == I
assert G.apply(I, test_pattern)==test_pattern
assert I.apply(test_pattern)==test_pattern

print("   Adding the three swaps...")
T12 = G.swap("1", "2")
G.store("T₀", T12)      # "0" is fixed
assert T12*T12 == I
assert T12.apply(test_pattern) == "02130213"
T02 = G.swap("0", "2")
G.store("T₁", T02)      # "1" is fixed
assert T02*T02 == I
assert T02.apply(test_pattern) == "21032103"
T01 = G.swap("0", "1")
G.store("T₂", T01)      # "2" is fixed
assert T01*T01 == I
assert T01.apply(test_pattern) == "10231023"
assert T01 != I
assert T01 != T02
assert T01 != T12

print("   Adding two non-trivial rotations...")
R = G.shift()
G.store("R₁", R)
assert R*R*R == I
assert R != I
assert R != T01
assert R != T02
assert R != T12
assert R.apply(test_pattern) == "12031203", R.apply(test_pattern)
R2 = R*R
G.store("R₂", R2)
assert R2 == G.shift(-1)
assert I == G.shift(3)
assert I == G.shift(0)
assert R == G.shift(-2)
assert R2.apply(test_pattern) == "20132013", R.apply(test_pattern)
assert R != R2
assert R2 != I

print("   Verifying inverses...")
assert I.inverse == I
assert R.inverse == R2
assert R2.inverse == R
assert T12.inverse == T12
assert T02.inverse == T02
assert T01.inverse == T01

elems = ("I", "R₁", "R₂", "T₀", "T₁", "T₂")
print("   ok!")

        # 5. tables for S(3)
print(f"5. Building tables for {G.name}...")
print("   Inverses:")
print("\t", end="")
for i in elems:
    print(f" {i:2}", end="")
print()
print("\t" + "═"*19)
print("\t", end="")
for i in elems:
    f = G.fetch(i)
    g = f.inverse
    for j in elems:
        if g == G.fetch(j):
            print(f" {j:2}", end="")
print()
print()
print("   Composition:")
print("\t *  ║", end="")
for i in elems:
    print(f" {i:2}", end="")
print()
print("\t════╬" + "═" * 19)
for i in elems:
    print(f"\t {i:2} ║", end="")
    image = set()
    f = G.fetch(i)
    for j in elems:
        g = f * G.fetch(j)
        for k in elems:
            if g == G.fetch(k):
                print(f" {k:2}", end="")
                image.add(k)
    print()
    assert len(image) == 6
print()
print("   ok!")

        # 6. tables for S(4)
G = S[4]
print(f"6. Building tables for {G.name}...")
test_pattern = "0123"
elems = list()
patterns = dict()

def mkp(label, value, match):
    """create an element"""
    result = value.apply(test_pattern)
    print(f"   {G.name} {label:2} [{test_pattern}]->[{result}]")
    assert result==match, f"mismatch {label} {result} != {match}"
    G.store(label, value)
    elems.append(label)
    patterns[result] = label
    return value

I = mkp("I", G.identity, "0123")                        # [0123] = ()
P0132 = mkp("H₃", G.swap("2", "3"), "0132")             # [0132] = (2 3)
P0213 = mkp("G₂", G.swap("1", "2"), "0213")             # [0213] = (1 2)
P0231 = mkp("C₁", G.cycle("1", "2", "3"), "0231")       # [0231] = (1 2 3)
P0312 = mkp("C₂", G.cycle("1", "3", "2"), "0312")       # [0312] = (1 3 2)
P0321 = mkp("G₃", G.swap("1", "3"), "0321")             # [0321] = (1 3)

P1023 = mkp("F₁", G.swap("0", "1"), "1023")             # [1023] = (0 1)
P1032 = mkp("P₁", P0132*P1023, "1032")                  # [0132] = (0 1)(2 3)
P1203 = mkp("C₃", G.cycle("0", "1", "2"), "1203")       # [1203] = (0 1 2)
P1230 = mkp("R₁", G.shift(1), "1230")                   # [1230] = (0 1 2 3)
P1302 = mkp("D₁", G.cycle("0", "1", "3", "2"), "1302")  # [1302] = (0 1 3 2)
P1320 = mkp("C₄", G.cycle("0", "1", "3"), "1320")       # [1320] = (0 1 3)

P2013 = mkp("C₅", G.cycle("0", "2", "1"), "2013")       # [2013] = (0 2 1)
P2031 = mkp("D₂", G.cycle("0", "2", "3", "1"), "2031")  # [2031] = (0 2 3 1)
P2103 = mkp("F₂", G.swap("0", "2"), "2103")             # [2103] = (0 2)
P2130 = mkp("C₆", G.cycle("0", "2", "3"), "2130")       # [2130] = (0 2 3)
P2301 = mkp("R₂", G.shift(2), "2301")                   # [2301] = (0 2)(1 3)
P2310 = mkp("D₃", G.cycle("0", "2", "1", "3"), "2310")  # [2310] = (0 2 1 3)

P3012 = mkp("R₃", G.shift(3), "3012")                   # [3012] = (0 3 2 1)
P3021 = mkp("C₇", G.cycle("0", "3", "1"), "3021")       # [3021] = (0 3 1)
P3102 = mkp("C₈", G.cycle("0", "3", "2"), "3102")       # [3102] = (0 3 2)
P3120 = mkp("F₃", G.swap("0", "3"), "3120")             # [3120] = (0 3)
P3201 = mkp("D₄", G.cycle("0", "3", "1", "2"), "3201")  # [3201] = (0 3 1 2)
P3210 = mkp("P₃", P3120*P0213, "3210")                  # [3210] = (0 3)(1 2)

print()
print("   Legend:")
print("       1 identity element (I)")
print("       6 2-cycles (F, G, H)")
print("       3 products of disjoint 2-cycles (P and R₂)")
print("       8 3-cycles (C)")
print("       6 4-cycles (D and R₁, R₃)")
print("     ━━━━")
print("      24 permutations  (4 of these (I, R₁, R₂, R₃) are rotations")
print()
assert len(elems) == 24, len(elems)
assert len(patterns) == 24, len(patterns)

print("   Inverses:")
print("    ", end="")
for i in elems:
    print(f" {i:2}", end="")
print()
print("    " + "═"*73)
print("    ", end="")
for i in elems:
    f = G.fetch(i)
    g = f.inverse
#    for j in elems:
#        if g == G.fetch(j):
#            print(f" {j:2}", end="")
    match = g.apply(test_pattern)
    print(f" {patterns[match]:2}", end="")
print()
print()
print("   Composition:")
print("    * ║", end="")
for i in elems:
    print(f" {i:2}", end="")
print()
print("   ═══╬" + "═" * 73)
for i in elems:
    print(f"    {i:2}║", end="")
    image = set()
    f = G.fetch(i)
    for j in elems:
        g = f * G.fetch(j)
#        for k in elems:
#            if g == G.fetch(k):
#                print(f" {k:2}", end="")
#                image.add(k)
        match = g.apply(test_pattern)
        print(f" {patterns[match]:2}", end="")
        image.add(patterns[match])
    print()
    assert len(image) == 24
print()
print("   ok!")


        # confirmation
print("All tests passed.")
print("SUCCESS!")

# end tests.permutation
