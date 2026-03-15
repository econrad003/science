"""
Genes.mitochondial - create codon tables for vertibrate mitochondrial DNA/RNA
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module defines functions which prepare a decoding tables for vertibrate
    mitochondrial DNA and RNA.

    This module can be used as a template for defining other variations of
    the standard RNA and DNA decoding tables.

REFERENCES

        [1] "Genetic code" in Wikipedia. 5 Jan 2026. Web.
             Accessed 27 Jan 2026.
             URL: https://en.wikipedia.org/wiki/Genetic_code

        [2] "DNA and RNA codon tables", in Wikipedia. 16 Nov 2025.
            Web. Accessed 18 Jan 2026.
            URL: https://en.wikipedia.org/wiki/DNA_and_RNA_codon_tables

USAGE

    make_table(source)

    REQUIRED ARGUMENTS

        source must be either "DNA" or "RNA"

    RETURNS

        A table of codons.  Note that the additional stop codons are not normally
        associated with colors.  Here, for no particular reason, we distinguish
        them as "red" and "green".

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
import Genes.RNA_codons as _RNA
import Genes.DNA_codons as _DNA

def make_table(source:str) -> dict:
    """create a vertibrate mitochondrial encoding table

    REQUIRED ARGUMENTS

        source - either "DNA" or "RNA".
    """
    codons = dict()
    if source not in {"DNA", "RNA"}:
        raise ValueError("source must be DNA or RNA")
    std_codons = _DNA.codons if source == "DNA" else _RNA.codons
    for key, value in std_codons.items():
        if key == "AGA":
            codons[key] = "red"                     # stop codon (std: Arg)
        elif key == "AGG":
            codons[key] = "green"                   # stop codon (std: Arg)
        elif key in {"ATA", "AUA"}:
            codons[key] = amino_acids["Met"]        # methionine (std: Ile)
        elif key in {"TGA", "UGA"}:
            codons[key] = amino_acids["Trp"]        # tryptophan (std: opal stop)
        else:
            codons[key] = value                     # same as standard value
    return codons

# END Genes.mitochondrial
