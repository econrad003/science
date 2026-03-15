"""
tests.mitochondial - test tables for vertibrate mitochondrial DNA/RNA
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module verifies the mitochondrial module by displaying the associated
    decoding tables for vertibrate mitochondrial DNA and RNA.

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
from Genes.amino_acid import amino_acids 
from Genes.mitochondrial import make_table

from tests.RNA_codons import display_table

RNA_title = "vertibrate mitochondrial RNA"
RNA_bases = ["U", "C", "A", "G"]

DNA_title = "vertibrate mitochondrial RNA"
DNA_bases = ["T", "C", "A", "G"]

titles = {"RNA":RNA_title, "DNA":DNA_title}
the_bases = {"RNA":RNA_bases, "DNA":DNA_bases}

if __name__ == "__main__":
    import sys, argparse

    parser = argparse.ArgumentParser(description="DNA codon tester")
    parser.add_argument("-s", "--source", type=str, default="RNA", \
        help="Either RNA (default) or DNA.")
    args = parser.parse_args(sys.argv[1:])
    assert args.source in {"RNA", "DNA"}
    codons = make_table(args.source)
    title = titles[args.source]
    bases = the_bases[args.source]
    display_table(codons, title, bases)
        # two simple tests
    assert codons["AGA"] == "red"
    assert codons["AGG"] == "green"

# END tests.mitochondrial

