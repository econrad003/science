"""
Genes.amino_acid - amino acids table
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

REFERENCES

    Information was obtained from Wikipedia:

        [1] "Genetic code" in Wikipedia. 5 Jan 2026. Web.
             Accessed 27 Jan 2026.
             URL: https://en.wikipedia.org/wiki/Genetic_code

        [2] "DNA and RNA codon tables", in Wikipedia. 16 Nov 2025.
            Web. Accessed 18 Jan 2026.
            URL: https://en.wikipedia.org/wiki/DNA_and_RNA_codon_tables

        [3] "Amino acid" in *Wikipedia**. 18 Jan. 2026. Web.
            Accessed 27 Jan. 2026.
            URL: https://en.wikipedia.org/wiki/Amino_acid

        [4] "N-Formylmethionine", in Wikipedia. 18 July 2025. Web.
            Accessed 25 Jan. 2026.
            URL: https://en.wikipedia.org/wiki/N-Formylmethionine

NOTES

    The amino acids table (name: amino_acids) currently lists 21 amino
    acids, 20 of which are used in the standard genetic code.

    The remaining amino acid in the table is formylethionine (aka:
    N-formylmethionine).  Data for formylmethionine (symbol fM and
    type polar) are uncertain and should be taken with a grain of
    salt. The abbreviation fMet was found in the accessed references.
    Formylmethionine is used in certain bacteria.  In humans, its
    presence generates a response from the immune system.

    There are apparently 22 amino acids in total in the genetic code.
    So I am apparently missing one (two if formylmethionine is
    treated as a variant form of methionine).

DISCLAIMER

    None of the claims made here have been certified by an organic
    chemist.  I am not an organic chemist and I've never even had
    a course in organic chemistry, so treat all claims made here
    with reasonable suspicion.

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

amino_acids = dict()

class AminoAcid(object):
    """amino acids"""

    __slots__ = ("__name", "__symbol", "__abbrev", "__settings")

    VERBOSE = True

    def __init__(self, name:str, symbol:str, abbrev:str, atype:str=None):
        """define an amino acid"""
        amino_acids[abbrev] = self
        self.__name = name
        self.__symbol = symbol
        self.__abbrev = abbrev
        self.__settings = dict()
        self["verbose"] = False
        self["type"] = atype        # np, p, b, a

    def __getitem__(self, setting:str):
        """return the value of a setting"""
        return self.__settings.get(setting)

    def __setitem__(self, setting:str, value:any):
        """create a setting"""
        self.__settings[setting] = value

    def __delitem__(self, setting:str):
        """remove a setting"""
        del self.__settings[setting]

    @property
    def name(self) -> str:
        """returns the name for the amino acid"""
        return self.__name

    @property
    def abbrev(self) -> str:
        """returns the three-character abbreviation for the amino acid"""
        return self.__abbrev

    @property
    def symbol(self) -> str:
        """returns the one-character symbol for the acid"""
        return self.__symbol

    @property
    def atype(self) -> str:
        """returns the type of amino acid:
            p - polar
            np - non-polar
            a - acid
            b - base
        """
        return self["type"]

    @property
    def verbose(self) -> bool:
        """returns the verbose class setting

        This is a global setting for the class!
        """
        return self.__class__.VERBOSE

    @verbose.setter
    def verbose(self, value:bool):
        """modify the verbose class setting

        This is a global setting for the class!
        """
        if type(value) != bool:
            raise TypeError
        self.__class__.VERBOSE = value

    def __str__(self) -> str:
        """returns the symbol or the abbreviation

        The return value is controlled by the verbose setting.  The
        default (verbose=True) is the abbreviation for the amino acid.
        """
        if bool(self["verbose"]):
            return self.name
        return self.base

AminoAcid("phenylalanine", "F", "Phe", atype="np")  # 1
AminoAcid("leucine", "L", "Leu", atype="np")        # 2
AminoAcid("isoleucine", "I", "Ile", atype="np")     # 3
AminoAcid("methionine", "M", "Met", atype="np")     # 4
AminoAcid("valine", "V", "Val", atype="np")         # 5

AminoAcid("serine", "S", "Ser", atype="p")          # 6
AminoAcid("proline", "P", "Pro", atype="np")        # 7
AminoAcid("threonine", "T", "Thr", atype="p")       # 8
AminoAcid("alanine", "A", "Ala", atype="np")        # 9

AminoAcid("tyrosine", "Y", "Tyr", atype="p")        # 10
AminoAcid("histidine", "H", "His", atype="b")       # 11
AminoAcid("glutamine", "Q", "Gln", atype="p")       # 12
AminoAcid("asparagine", "N", "Asn", atype="p")      # 13
AminoAcid("lysine", "K", "Lys", atype="b")          # 14

AminoAcid("cysteine", "C", "Cys", atype="p")        # 15
AminoAcid("tryptophan", "W", "Trp", atype="np")     # 16
AminoAcid("arginine", "R", "Arg", atype="b")        # 17
AminoAcid("aspartic acid", "D", "Asp", atype="a")   # 18
AminoAcid("glutamic acid", "E", "Glu", atype="a")   # 19

AminoAcid("glycine", "G", "Gly", atype="np")        # 20

    # The 20 amino acids above are used in the "standard" genetic code.
    # The references indicate that there are at least two more that are
    # used.

assert len(amino_acids) == 20       # standard genetic code amino acids

    # N-formylmethionine is a derivative of methionine with an attached
    # formyl group.  It plays an important role in the synthesis of
    # proteins in bacteria, mitochondria and chloroplasts.  In humans,
    # it is recognized by the immune system as foreign material or as
    # material released by damaged cells.  For more information, see [3]

    # I believe it is classed as polar, but I am not certain.

AminoAcid("formylmethionine", "fM", "fMet",
          atype="p")                                # 21

    # There is apparently one more that should be included for
    # completeness.

assert len(amino_acids) == 21       # currently tabulated

# END module Genes.amino_acid
