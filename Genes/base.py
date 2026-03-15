"""
Genes.base - nucleotide base module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module defines a class Base which includes the five usual
    DNA and RNA nucleotides, but could be used abstractly to identify
    nucleotides in non-standard and in fictional settings.

    The five nucleotides are defined here under the following names:

        adenine
        cytosine
        guanine
        thymine (DNA only)
        uracil (RNA only)
        

REFERENCES

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

class Base(object):
    """base class for a nucleotide"""

    __slots__ = ("__base", "__name", "__settings")

    VERBOSE = False

    def __init__(self, base:str, name:str, DNA:bool=False, RNA:bool=False):
        """define a nucleotide base

        ARGUMENTS

            base - the abbreviation for the base.  For DNA, the bases are
                A, C, G and T for adenine, cytosine, guanine and thymine,
                respectively.  For RNA, U (uracil) replaces thymine.

            name - the spelled-out name, i.e. "adenine", "cytosine",
                "guanine", "thymine" or "uracil".

        OPTIONAL ARGUMENTS

            DNA - default: False - set this to true for a DNA base

            RNA - default: False - set this to true for an RNA base
        """
        self.__abbrev = base
        self.__name = name
        self.__settings = dict()
        self["DNA"] = bool(DNA)
        self["RNA"] = bool(DNA)
            # These should be set separately
        self["class"] = None
        self["pairing"] = dict()

    @property
    def base(self) -> str:
        """returns the abbreviation for the base"""
        return self.__base

    @property
    def name(self) -> str:
        """returns the name for the base"""
        return self.__name

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

    @classmethod
    def verbosity(cls, value:bool=None) -> bool:
        """return, after optionally changing, the verbose class setting"""
        if value != None:
            if type(value) != bool:
                raise TypeError
            cls.VERBOSE = value
        return cls.VERBOSE

    def __getitem__(self, setting:str):
        """return the value of a setting

        For the DNA and RNA bases, the following settings are defined
        by the base module:
            class - str - either purine or pyramidine
            pairing - dict - a dictionary of pairings.  The dictionary contains
                one or two entries with indices "DNA" for DNA bases and "RNA"
                for RNA bases
            DNA - if True, this is a DNA nucleotide base
            RNA - if True, this is an RNA nucleotide base
        """
        return self.__settings.get(setting)

    def __setitem__(self, setting:str, value:any):
        """create a setting"""
        self.__settings[setting] = value

    def __delitem__(self, setting:str):
        """remove a setting"""
        del self.__settings[setting]

    def __str__(self) -> str:
        """returns the abbreviation or the name

        The return value is controlled by the verbose setting.  The
        default (verbose=False) is the abbreviation for the base.
        """
        if bool(self["verbose"]):
            return self.name
        return self.base

adenine = Base("A", "adenine", DNA=True, RNA=True)
cytosine = Base("C", "cytosine", DNA=True, RNA=True)
guanine = Base("G", "guanine", DNA=True, RNA=True)
thymine = Base("T", "thymine", DNA=True)
uracil = Base("U", "uracil", RNA=True)

adenine["class"] = "purine"
cytosine["class"] = "pyrimidine"
guanine["class"] = "purine"
thymine["class"] = "pyrimidine"
uracil["class"] = "pyrimidine"

adenine["pairing"] = {"DNA":thymine, "RNA":uracil}
cytosine["pairing"] = {"DNA":guanine, "RNA":guanine}
guanine["pairing"] = {"DNA":cytosine, "RNA":cytosine}
cytosine["pairing"] = {"DNA":guanine, "RNA":guanine}
thymine["pairing"] = {"DNA":adenine}
uracil["pairing"] = {"RNA":adenine}

DNA_BASES = {"A":adenine, "C":cytosine, "G":guanine, "T":thymine}
RNA_BASES = {"A":adenine, "C":cytosine, "G":guanine, "U":uracil}

# END module Genes.base
