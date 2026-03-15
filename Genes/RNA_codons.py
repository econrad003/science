"""
Genes.RNA_codons - standard RNA protein decoding table
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module prepares a standard RNA decoding table.

REFERENCES

    Information was obtained from Wikipedia:

        [1] "Genetic code" in Wikipedia. 5 Jan 2026. Web.
             Accessed 27 Jan 2026.
             URL: https://en.wikipedia.org/wiki/Genetic_code

        [2] "DNA and RNA codon tables", in Wikipedia. 16 Nov 2025.
            Web. Accessed 18 Jan 2026.
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

codons = dict()
start_codons = {"AUG"}

# First base - Uracil - RNA table
    # UU
codons["UUU"] = codons["UUC"] = amino_acids["Phe"]          # phenylalanine
codons["UUA"] = codons["UUG"] = amino_acids["Leu"]          # leucine
    # UC
codons["UCU"] = codons["UCC"] \
    = codons["UCA"] = codons["UCG"] = amino_acids["Ser"]    # serine
    # UA
codons["UAU"] = codons["UAC"] = amino_acids["Tyr"]          # tyrosine
codons["UAA"] = "ochre"
codons["UAG"] = "amber"
    # UG
codons["UGU"] = codons["UGC"] = amino_acids["Cys"]          # cysteine
codons["UGA"] = "opal"
codons["UGG"] = amino_acids["Trp"]                          # tryptophan

# First base - Cytosine - RNA table
    # CU
codons["CUU"] = codons["CUC"] \
    = codons["CUA"] = codons["CUG"] = amino_acids["Leu"]    # leucine
    # CC
codons["CCU"] = codons["CCC"] \
    = codons["CCA"] = codons["CCG"] = amino_acids["Pro"]    # proline
    # CA
codons["CAU"] = codons["CAC"] = amino_acids["His"]          # histidine
codons["CAA"] = codons["CAG"] = amino_acids["Gln"]          # glutamine
    # CG
codons["CGU"] = codons["CGC"] \
    = codons["CGA"] = codons["CGG"] = amino_acids["Arg"]    # arginine

# First base - Adenine - RNA table
    # AU
codons["AUU"] = codons["AUC"] \
    = codons["AUA"] = amino_acids["Ile"]                    # isoleucine
codons["AUG"] = amino_acids["Met"]                          # methionine
    # AC
codons["ACU"] = codons["ACC"] \
    = codons["ACA"] = codons["ACG"] = amino_acids["Thr"]    # threonine
    # AA
codons["AAU"] = codons["AAC"] = amino_acids["Asn"]          # asparagine
codons["AAA"] = codons["AAG"] = amino_acids["Lys"]          # lysine
    # AG
codons["AGU"] = codons["AGC"] = amino_acids["Ser"]          # serine
codons["AGA"] = codons["AGG"] = amino_acids["Arg"]          # arginine

# First base - Guanine - RNA table
    # GU
codons["GUU"] = codons["GUC"] \
    = codons["GUA"] = codons["GUG"] = amino_acids["Val"]    # valine
    # GC
codons["GCU"] = codons["GCC"] \
    = codons["GCA"] = codons["GCG"] = amino_acids["Thr"]    # threonine
    # GA
codons["GAU"] = codons["GAC"] = amino_acids["Asp"]          # aspartic_acid
codons["GAA"] = codons["GAG"] = amino_acids["Glu"]          # glutamic_acid
    # GG
codons["GGU"] = codons["GGC"] \
    = codons["GGA"] = codons["GGG"] = amino_acids["Gly"]    # glycine

class UnknownCodonError(Exception):
    """exception raised when a codon is not recognized"""
    pass

class Decoder(object):
    """an RNA/DNA protein decoding engine"""

    __slots__ = ("__settings")


    def __init__(self):
        """constructor"""
        self.__settings = dict()

    def __getitem__(self, key):
        """returns a setting"""
        return self.__settings.get(key)

    def __setitem__(self, key, value):
        self.__settings[key] = value

    def decode(self, strand:str, *, codons:dict=codons,
               start_codons:set=start_codons,
               leader:int=0) -> list:
        """RNA/DNA decoder

        POSITIONAL ARGUMENTS

            strand - the RNA or DNA strand to be decoded

        OPTIONAL NAMED ARGUMENTS

            codons - the decoding table to be used.  The default is the
                standard RNA decoding table.

            start_codons - a set of start codons.  If this is empty or None,
                decoding starts with the first three bases in the strand.
                The default is {"AUG"}. Note that "AUG" encodes methionine
                from RNA.

            leader - the number of bases to ignore before starting the decoding.
                The default is 0.  As an example "AUGAUG" returns ["Met", "Met"]
                by default, but just ["Met"] if leader is 3 and [] if leader is
                6.

        DESCRIPTION

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
        self["start"] = None
        self["stop"] = None
        self["color"] = None
        self["result"] = list()
        index = leader if leader > 0 else 0
        frame = strand[index:index+3]
        if start_codons:
                # look for the starting frame
            while len(frame) == 3 and frame not in start_codons:
                index += 1
                frame = strand[index:index+3]
            if len(frame) == 3:
                self["start"] = frame
        self["leader"] = index
                # decoding starts in earnest
        while len(frame) == 3:
            if frame not in codons:
                raise UnknownCodonError(f"Undefined codon '{frame}'")
            amino_acid = codons[frame]
            index += 3
            if type(amino_acid) == str:             # stop codon
                self["stop"] = frame
                self["color"] = amino_acid
                self["trailer"] = len(strand) - index
                return self["result"]
            abbrev = amino_acid.abbrev
            self["result"].append(abbrev)    # save the amino acid key
            frame = strand[index:index+3]
        self["trailer"] = len(frame)
        return self["result"]

# END Genes.RNA_codons
