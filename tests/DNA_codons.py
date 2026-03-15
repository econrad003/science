"""
tests.DNA_codons - test the standard RNA protein encoding table
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
from Genes.DNA_codons import codons, start_codons, UnknownCodonError, Decoder
import tests.RNA_codons as _parent

bases = ["T", "C", "A", "G"]

def display_table(codons=codons, header="Standard DNA decoding", bases=bases):
    """display the decoding table"""
    _parent.display_table(codons, header, bases)

if __name__ == "__main__":
    import sys, argparse

    parser = argparse.ArgumentParser(description="DNA codon tester")
    parser.add_argument("-v", "--verbose", action="store_true", \
        help="track testing operations.")
    args = parser.parse_args(sys.argv[1:])
    if args.verbose:
        print(" --- Testing Genes.DNA_codons module...")
    display_table()
    if args.verbose:
        print(" --- Testing Genes.DNA_codons.Decoder...")
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
        print("[2] decode 'ATGTAA' (Met/ochre)...", end="")
    result = decoder.decode("ATGTAA")
    assert result == ["Met"]
    assert decoder["leader"] == 0
    assert decoder["trailer"] == 0
    assert decoder["start"] == "ATG"
    assert decoder["stop"] == "TAA"
    assert decoder["color"] == "ochre"
    if args.verbose:
        print(f" ok!")
        print("[3] decode 'XXXXATGTAA' (Met/ochre/leader=4)...", end="")
    result = decoder.decode("XXXXATGTAA")
    assert result == ["Met"]
    assert decoder["leader"] == 4
    assert decoder["trailer"] == 0
    assert decoder["start"] == "ATG"
    assert decoder["stop"] == "TAA"
    assert decoder["color"] == "ochre"
    if args.verbose:
        print(f" ok!")
        print("[4] decode 'ATGGTTTGAXXXX' (Met/Val/opal)...", end="")
    result = decoder.decode("ATGGTTTGAXXXX")
    assert result == ["Met", "Val"]
    assert decoder["leader"] == 0
    assert decoder["trailer"] == 4
    assert decoder["start"] == "ATG"
    assert decoder["stop"] == "TGA"
    assert decoder["color"] == "opal"
    if args.verbose:
        print(f" ok!")
        print("SUCCESS!")

# END tests.DNA_codons
