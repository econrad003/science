"""
Genes.DNA_codons - standard DNA protein decoding table
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module prepares a standard RNA decoding table.

REFERENCES

    Information was obtained from Wikipedia:

        [1] "DNA and RNA codon tables", in Wikipedia. 16 Nov 2025. Web.
            Accessed 18 Jan 2026.
            URL: https://en.wikipedia.org/wiki/DNA_and_RNA_codon_tables

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
from Genes.RNA_codons import UnknownCodonError

codons = dict()
start_codons = {"ATG"}

    # Use the RNA table to create the DNA table
for _key, _value  in _RNA.codons.items():
    _key2 = _key.replace('U', 'T')
    codons[_key2] = _value

class Decoder(_RNA.Decoder):
    """a DNA protein decoding engine"""

    def decode(self, strand:str, *, codons:dict=codons,
               start_codons:set=start_codons,
               leader:int=0) -> list:
        """DNA decoder

        POSITIONAL ARGUMENTS

            strand - the DNA strand to be decoded

        OPTIONAL NAMED ARGUMENTS

            codons - the decoding table to be used.  The default is the
                standard DNA decoding table.

            start_codons - a set of start codons.  If this is empty or None,
                decoding starts with the first three bases in the strand.
                The default is {"ATG"}. Note that "ATG" encodes methionine
                from RNA.

            leader - the number of bases to ignore before starting the decoding.
                The default is 0.  As an example "ATGATG" returns ["Met", "Met"]
                by default, but just ["Met"] if leader is 3 and [] if leader is
                6.

        DESCRIPTION

            The arguments (or defaults) are simply passed on to the parent
            class instance.

            Decoding is left to right after ignoring any leader bases.  The
            return value is the resulting protein strand expressed as a list of
            three character amino acid abbreviations.  The following
            additional information is saved as a setting in the decoder:

                start - the start codon, if any

                leader - the number of bases in the leftmost region of the
                    strand that were skipped before decoding started

                trailer - the number of bases in the rightmost region of
                    the strand that were skipped when decoding stopped

                result - the resulting protien strand (same as the return
                    value)

                stop - the stop codon, if any

                color - the stop color, if any
        """
        return super().decode(strand, codons=codons,
                              start_codons=start_codons,
                              leader=leader)

# END Genes.DNA_codons
