"""
tests.amino_acid - test the amino acids module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

REFERENCES

    Information was obtained from Wikipedia:

        [1] "DNA and RNA codon tables", in Wikipedia. 16 Nov. 2025. Web.
            Accessed 18 Jan. 2026.

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
    # import the amino acids table
from Genes.amino_acid import amino_acids

def display_table(amino_acids, sanity_check=True):
    """display a table of amino acids"""
        # prepare a table of amino acids
    print("\tAmino Acids")
    print("  n key  L      amino acid       type")
    print("--- ---- -- -------------------- ----------")
    keys = list(amino_acids.keys())
    keys.sort()
    types = {"np":"non-polar", "p":"polar", "a":"acid", "b":"base"}
    n = 0
    for key in keys:
        acid = amino_acids[key]
        n += 1
        classification = types[acid["type"]]
        name = acid.name
        symbol = acid.symbol
        abbrev = acid.abbrev
        print("%3d %-4s %-2s %-20s %s" % (n, abbrev, symbol, name, classification))
        if sanity_check:
            assert abbrev == key
    print("Notes:")
    print("  [fM] N-formylmethionine is used in bacteria.")

if __name__ == "__main__":
    import sys, argparse
    parser = argparse.ArgumentParser(description="test amino acids module")
    parser.add_argument("-v", "--verbose", action="store_true", \
        help="display testing comments.  The default is to simply display" \
        + " the table of amino acids in alphabetical order.")
    args = parser.parse_args(sys.argv[1:])
    if args.verbose:
        print(" --- Testing amino acids module---")
    display_table(amino_acids)
        # check the entry for alanine
    if args.verbose:
        print(" --- [1] checking the entry for alanine (Ala)...")
    alanine = amino_acids["Ala"]
    assert alanine.name == "alanine"
    assert alanine.abbrev == "Ala"
    assert alanine.symbol == "A"
    assert alanine.atype == "np"
    if args.verbose:
        print(" --- [1] ok!")
    if args.verbose:
        print(" --- Testing results:")
        print("SUCCESS!")

# END tests.amino_acid
