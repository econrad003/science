"""
tests.RNA_codons - test the standard RNA protein encoding table
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

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
from Genes.amino_acid import amino_acids
from Genes.RNA_codons import codons, start_codons, UnknownCodonError, Decoder

bases = ["U", "C", "A", "G"]

def display_table(codons=codons, header="Standard RNA decoding", bases=bases):
    """display the decoding table"""
    leader = " " * max(0, (75 - len(header)) // 2)
    print(f"{leader}{header}")
    print("-" * 75)
    for base1 in bases:
        for base3 in bases:
            row = ""
            for base2 in bases:
                codon = base1 + base2 + base3
                amino_acid = codons[codon]
                if type(amino_acid) == str:
                    name = f"STOP:{amino_acid}"
                else:
                    name = amino_acid.name
                if row:
                    row += "  "
                row += f"{codon} {name:13}"
            print(row)
        print("-" * 75)

if __name__ == "__main__":
    import sys, argparse

    parser = argparse.ArgumentParser(description="RNA codon tester")
    parser.add_argument("-v", "--verbose", action="store_true", \
        help="track testing operations.")
    args = parser.parse_args(sys.argv[1:])
    if args.verbose:
        print(" --- Testing Genes.RNA_codons module...")
    display_table()
    if args.verbose:
        print(" --- Testing Genes.RNA_codons.Decoder...")
        print("[1] decode '' (empty string)...", end="")
    decoder = Decoder()
    result = decoder.decode("")
    assert result == list()
    assert decoder["leader"] == 0
    assert decoder["trailer"] == 0
    assert decoder["start"] == None
    assert decoder["stop"] == None
    assert decoder["color"] == None
    if args.verbose:
        print(f" ok!")
        print("[2] decode 'AUGUAA' (Met/ochre)...", end="")
    result = decoder.decode("AUGUAA")
    assert result == ["Met"]
    assert decoder["leader"] == 0
    assert decoder["trailer"] == 0
    assert decoder["start"] == "AUG"
    assert decoder["stop"] == "UAA"
    assert decoder["color"] == "ochre"
    if args.verbose:
        print(f" ok!")
        print("[3] decode 'XXXXAUGUAA' (Met/ochre/leader=4)...", end="")
    result = decoder.decode("XXXXAUGUAA")
    assert result == ["Met"]
    assert decoder["leader"] == 4
    assert decoder["trailer"] == 0
    assert decoder["start"] == "AUG"
    assert decoder["stop"] == "UAA"
    assert decoder["color"] == "ochre"
    if args.verbose:
        print(f" ok!")
        print("[4] decode 'AUGGUUUGAXXXX' (Met/Val/opal)...", end="")
    result = decoder.decode("AUGGUUUGAXXXX")
    assert result == ["Met", "Val"]
    assert decoder["leader"] == 0
    assert decoder["trailer"] == 4
    assert decoder["start"] == "AUG"
    assert decoder["stop"] == "UGA"
    assert decoder["color"] == "opal"
    if args.verbose:
        print(f" ok!")
        print("SUCCESS!")

# END tests.RNA_codons
