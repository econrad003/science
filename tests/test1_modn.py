"""
tests.test1_modn - basic tests for integers modulo n (ℤₙ)
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Module utilities.modn defines commutative ring classes ℤₙ
    for given integers n > 1.

USAGE
    test1_modn.py [-h] [-v] [-n] n
        Display basic data for ℤₙ.

    positional arguments:
          n              the order of the ring

    options:
          -h, --help     show this help message and exit
          -v, --verbose  show the docstring for the ring
          -n, --notes    show the notes

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
from math import gcd
import textwrap

from utilities.modn import make_Zn

def notes(indent=4):
    """prepare notes for the tests"""
    indent = " " * indent
    print("NOTES")
    print()
    text = "If n is (respectively) 1, prime, or composite,"
    text += " then ℤₙ would be (respectively)"
    text += " a trivial ring, or"
    text += " a field with a cyclic multiplicative group of units, or"
    text += " the ring would contain contain nonzero divisors of zero."
    text += " (The function \"make_Zn\" requires that n be an integer"
    text += " larger than 1.)"
    for line in textwrap.wrap(text, initial_indent=indent,
                              subsequent_indent=indent,
                              fix_sentence_endings=True):
        print(line)
    print()
    text = "When n is composite, the group of units is sometimes,"
    text += " but not always, cyclic."
    text += " Carl Friedrich Gauss (1777-1855) proved that the"
    text += " group of units is cyclic if and only if n is 1, 2, 4,"
    text += " a power of an odd prime, or twice the power of an odd prime."
    text += " For all other n, the group of units is a cross product"
    text += " of two or more cyclic groups."
    for line in textwrap.wrap(text, initial_indent=indent,
                              subsequent_indent=indent,
                              fix_sentence_endings=True):
        print(line)
    print()
    text = "For example, the group of units for the ring ℤ₈ is"
    text += " isomorphic to the group ℤ₂×ℤ₂.  The order 2 elements"
    text += " of the group of units of the integers between 1 and 8"
    text += " which are relatively prime to 8, i.e. 3, 5 and 7."
    text += " (For example 5 times 5 is 25, which is congruent to 1"
    text += " modulo 8, so 5 has order 2.)  The product of any two"
    text += " of these values gives the third, for example 3 time 5"
    text += " 15 congruent to 7 modulo 8, so the group is generated"
    text += " by any two of these numbers."
    for line in textwrap.wrap(text, initial_indent=indent,
                              subsequent_indent=indent,
                              fix_sentence_endings=True):
        print(line)
    print()
    print(indent * 2 + "Group of units for ℤ₈: (3)×(5) = {1,3,5,7}")
    print()
    print("        Table 1. Group of units for 2 ≤ n ≤ 20")
    print("        ======================================")
    print("     n   prime?  zero divisors      group of units")
    print("     2    Yes    0                  (1) ≅ ℤ₁")
    print("     3    Yes    0                  (2) ≅ ℤ₂")
    print("     4    No     0,2                (3) ≅ ℤ₂")
    print("     5    Yes    0                  (2) ≅ ℤ₄")
    print("     6    No     0,2,3,4            (5) ≅ ℤ₂")
    print("     7    Yes    0                  (3) ≅ ℤ₆")
    print("     8    No     0,2,4,8            (3)×(5) ≅ ℤ₂×ℤ₂")
    print("     9    No     0,3,6              (2) ≅ ℤ₆")
    print("    10    No     0,2,4,5,6,8        (3) ≅ ℤ₄")
    print("    11    Yes    0                  (2) ≅ ℤ₁₀")
    print("    12    No     0,2,3,4,6,8,9,10   (5)×(7) ≅ ℤ₂×ℤ₂")
    print("    13    Yes    0                  (2) ≅ ℤ₁₂")
    print("    14    No     0,2,4,6,7,8,10,12  (3) ≅ ℤ₆")
    print("    15    No     0,3,5,6,9,10,12    (2)×(11) ≅ ℤ₄×ℤ₂")
    print("    16    No     0,2,4,6,8,10,12,14 (3)×(7) ≅ ℤ₄×ℤ₂")
    print("    17    Yes    0                  (3) ≅ ℤ₁₆")
    print("    18    No     0,2,3,4,6,8,9,10,  (11) ≅ ℤ₆")
    print("                   12,14,15,16")
    print("    19    Yes    0                  (2) ≅ ℤ₁₈")
    print("    20    No     0,2,4,5,6,8,10,12, (3)×(11) ≅ ℤ₄×ℤ₂")
    print("                   14,15,16,18")
    print()
    print("       Notes for Table 1:")
    print("         (1) The unit group generators are the smallest choices.")

def test(n, verbose=False):
    """test ℤₙ for a specific value of n"""
    Ring = make_Zn(n)
    print("TESTING:", Ring.__name__)
    if verbose:
        print("help for", Ring.__name__, "=" * 50)
        print(Ring.__doc__)
        print("=" * 70)
    print(f"  {Ring.__name__}:",
          f"field? {'Yes' if Ring.is_field() else 'No'}! ",
          f"number of units={Ring.multiplicative_order()}")
    return Ring

def test_addition(Ring):
    """test the additive group"""
    print("Checking the additive group in", f"{Ring.__name__}...")
    if Ring.additive_order() > 200:
        print("        (This may take a little time...)")
    elements = Ring.elements()
    n = Ring.additive_order()
    print("    addition... ", end="")
    for x in elements:
        u = int(x)
        for y in elements:
            v = int(y)
            assert x + y == (u + v) % n, f"{x}+{y}={x+y} EXPECT {(u+v)%n}"
    print("ok!")
    print("    subtraction... ", end="")
    for x in elements:
        u = int(x)
        for y in elements:
            v = int(y)
            z = x - y
            assert y + z == x, f"{x}-{y}={z} EXPECT {(u-v)%n}"
    print("ok!")
    print("    additive inverses... ", end="")
    for x in elements:
        u = int(x)
        y = - x
        v = int(y)
        assert x + y == 0, f"{x}+{y}={x+y} EXPECT 0  RIGHT"
        assert y + x == 0, f"{y}+{x}={x+y} EXPECT 0  LEFT"
    print("ok!")

def test_multiplication(Ring):
    """test the multiplicative semigroup"""
    print("Checking the multiplicative semigroup in", f"{Ring.__name__}...")
    if Ring.additive_order() > 200:
        print("        (This may take a little time...)")
    elements = Ring.elements()
    n = Ring.additive_order()
    g = Ring.multiplicative_order()
    print("    multiplication... ", end="")
    for x in elements:
        u = int(x)
        for y in elements:
            v = int(y)
            assert x * y == (u * v) % n, f"{x}·{y}={x*y} EXPECT {(u*v)%n}"
    print("ok!")
    print("    division... ", end="")
    for x in elements:
        u = int(x)
        for y in elements:
            v = int(y)
            try:
                z = x / y
                assert y * z == x, f"{x}/{y}={z} by {y}*{z}≠{x}"
                assert not y.is_zero_divisor, f"Divide by {y} in ZD"
                assert gcd(v, n) == 1, f"({y},{n})={gcd(v,n)} EXPECT 1"
            except ZeroDivisionError:
                assert gcd(v, n) != 1, f"({y},{n})=1 EXPECT ≠1"
                assert y.is_zero_divisor, f"Should {y} be in ZD?"
    print("ok!")
    print("    multiplicative inverses... ", end="")
    for x in elements:
        u = int(x)
        try:
            y = x.inverse
            assert x * y == 1, f"{x}*{y}={x*y} EXPECT 1  RIGHT"
            assert y * x == 1, f"{y}+{x}={x+y} EXPECT 1  LEFT"
            assert not x.is_zero_divisor, f"Found {y} in ZD with inverse"
            assert gcd(u, n) == 1, f"({x},{n})={gcd(u,n)} EXPECT 1"
        except ZeroDivisionError:
            assert gcd(u, n) != 1, f"({x},{n})=1 EXPECT ≠1"
            assert x.is_zero_divisor, f"Should {x} be in ZD?"
    print("ok!")

def show_table(Ring, zero_divisors=False):
    """display additive inverse, multiplicative inverse and order"""
    print("         x         -x        1/x      order")
    print("========== ========== ========== ==========")
    elements = Ring.elements()
    for x in elements:
        if x.is_zero_divisor:
            if zero_divisors:
                print("%10d %10d" % (x, -x))
        else:
            print("%10d %10d %10d %10d" % (x, -x, x.inverse, x.ord))

def main(argv):
    """parse command line arguments"""
    import argparse

    DESCR = "Display basic data for ℤₙ."
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument("n", type=int, help="the order of the ring")
    parser.add_argument("-v", "--verbose", action="store_true", \
        help="show the docstring for the ring")
    parser.add_argument("-n", "--notes", action="store_true", \
        help="show the notes")
    parser.add_argument("-a", "--addition", action="store_true", \
        help="test addition and subtraction")
    parser.add_argument("-m", "--multiplication", action="store_true", \
        help="test multiplication and division")
    parser.add_argument("-t", "--table", action="store_true", \
        help="for each unit, show its inverses and orders")
    parser.add_argument("-i", "--include", action="store_true", \
        help="include zero divisor additive inverses in the table of inverses")
    args = parser.parse_args(argv)
#    print(args)
    Ring = test(args.n, verbose=args.verbose)
    if args.addition:
        test_addition(Ring)
    if args.multiplication:
        test_multiplication(Ring)
    if args.include:
        args.table=True
    if args.table:
        show_table(Ring, args.include)
    if args.notes:
        print()
        notes()
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

# END tests.test1_modn
