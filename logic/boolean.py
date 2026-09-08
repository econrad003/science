"""
logic.boolean - two-valued vector logic
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    In a basic Boolean algebra, we have two values, namely 0 and 1.
    We have three basic operations on those values:

        a) logical negation (~p)
            ~p := 1-p
        b) logical addition or disjunction (p∨q)
            p∨q := max(p,q)
        c) logical multiplication or conjunction (p∧q)
            p∧q := min(p,q)

    In a multiple worlds scenario, we have 2ⁿ values arranged in an
    n-dimensional vector -- each component (called a bit) is one of the
    of the two values 0 and 1 and the three basic operations are
    performed component-wise.

    In a two worlds scenario, we have two bits per vector.  One of the
    two bits (for example, the last bit) represents the real world,
    while the other bit represents the alternate world.  The three basic
    operations in the two-world scenario are then:

                    p∨q |      p        p∧q |      p
         p | ~p       q | 00 01 10 11     q | 00 01 10 11
        ---+---     ----+------------   ----+------------
        00 | 11      00 | 00 01 10 11    00 | 00 00 00 00
        01 | 10      01 | 01 01 11 11    01 | 00 01 00 01
        10 | 01      10 | 10 11 10 11    10 | 00 00 10 10
        11 | 00      11 | 11 11 11 11    11 | 00 01 10 11

    We can treat these as little-endian binary integers in the decimal
    range [0,3]:
        binary      00 01 10 11
        decimal      0  1  2  3

    Note that logical negation inverts the interval, but the disjunction
    and conjunction operators are not integer maxima or minima:

                    p∨q |      p        p∧q |      p
         p | ~p       q |  0  1  2  3     q |  0  1  2  3
        ---+---     ----+------------   ----+------------
         0 |  3       0 |  0  1  2  3     0 |  0  0  0  0
         1 |  2       1 |  1  1  3  3     1 |  0  1  0  1
         2 |  1       2 |  2  3  2  3     2 |  0  0  2  2
         3 |  0       3 |  3  3  3  3     3 |  0  1  2  3

    With two or more worlds, we have modalities.  A statement can
    have one of four states:

        binary  decimal       state
        ------  -------  ------------------
          00       0     impossible           (false in both worlds)
          01       1     contingently true    (true only in the real world)
          10       2     contingently false   (false only in the real world)
          11       3     necessary            (true in both worlds)

    A statement is contingent (or possible) if it is true in at least
    one of the two worlds, i.e. if its truth value is 1, 2, or 3.

    For a two-world scenario, we have two practical ways of defining a
    necessary operator:

        a) ▫p := 1 if p=3 and 0 otherwise
                if p is necessary, then ▫p is contingently true
        b) ▫p := 3 if p=3 and 0 otherwise
                if p is necessary, then ▫p is necessary

    We typically define the possibility operator as:

        ◇p :- ~▫~p

    For the case (a), our modal operators are as follows:

        p   ▫p  ▫~p  ~▫p   ◇p
        ---------------------
        0    0    1    3    2
        1    0    0    3    3
        2    0    0    3    3
        3    1    0    2    3

    Note that in case (a), ▫▫p is always an impossible statement and
    ◇◇p is always a necessary statement.

    For the case (b), our modal operators are as follows:

        p   ▫p  ▫~p  ~▫p   ◇p
        ---------------------
        0    0    3    3    0
        1    0    0    3    3
        2    0    0    3    3
        3    3    0    0    3

    Note that in case (b), ▫▫p and ◇◇p are the same as ▫p and ◇p,
    respectively.

    With a three-world scenario, we have one real world and two alternate
    worlds.  A statement is impossible when false in all three worlds,
    true when true in the real world, possible when true in at least
    one world, contingently true when true only in the real world, and
    necessary when true in all three worlds.  We have more possible
    ways of defining a necessary operator:

         p       ▫ₒp   ▫₁p   ▫₂p   ▫₃p
        000-110  000   000   000   000
        111      111   001   011   101

    Note that ▫₂p and ▫₃p are isomorphic -- the values when p is
    necessary both represent true in both the real world and exactly one
    alternate world.

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

class BooleanLogic(object):
    """two-valued multiple worlds logic"""

    _NECESSITIES = {0, 1}

    __slots__ = ("__n", "__maxp", "__necessity")

    def __init__(self, n:int=1, necessity=1):
        """constructor

        ARGUMENTS
            n - number of worlds (default:1)
        """
        if type(n) != int:
            raise TypeError("number of worlds (n) must be an integer")
        if n < 1:
            raise ValueError("number of worlds (n) must be a positive integer")
        self.__n = n
        self.__maxp = 2**n - 1
        self._necessity = necessity

    def defined(self, p:int, var:str='p'):
        """check whether a truth value is defined"""
        if type(p) != int:
            raise TypeError(f"truth value ({var}) must be an integer")
        if 0 <= p <= self.__maxp:
            pass
        else:
            raise ValueError("truth value ({var}) must be in [0, {self.__maxp}]")

    def AND(self, p:int, q:int) -> int:
        """conjunction"""
        return p & q

    def OR(self, p:int, q:int) -> int:
        """inclusive disjunction"""
        return p | q

    def XOR(self, p:int, q:int) -> int:
        """exclusive disjunction"""
        return p ^ q

    def NOT(self, p:int) -> int:
        """logical negation"""
        return self.__maxp - p

    def IMP(self, p:int, q:int) -> int:
        """material implication"""
        return (self.__maxp - p)|q

    def EQU(self, p:int, q:int) -> int:
        """material equivalence"""
        return ((self.__maxp - p)|q) & ((self.__maxp - q)|p)

    def NECESSARILY1(self, p:int) -> int:
        """necessity

        Returns true in this world if the value is true in all worlds.
        Returns false otherwise.
        """
        return 1 if p==self.__maxp else 0

    def NECESSARILY2(self, p:int) -> int:
        """necessity

        Returns true in all worlds if the value is true in all worlds.
        Returns false otherwise.
        """
        return p if p==self.__maxp else 0

    def NECESSARILY(self, p:int) -> int:
        """necessity"""
        if self.__necessity == 1:
            return self.NECESSARILY1(p)
        return self.NECESSARILY2(p)

    def POSSIBLY(self, p:int) -> int:
        """necessity"""
        return self.NOT(self.NECESSARILY(self.NOT(p)))

    def SIMP(self, p:int, q:int) -> int:
        """strict implication"""
        return self.NECESSARILY(self.IMP(p, q))

    def SEQU(self, p:int, q:int) -> int:
        """strict equivalence"""
        return self.NECESSARILY(self.EQU(p, q))

    @property
    def _necessity(self):
        """return the necessity type"""
        return self.__necessity

    @_necessity.setter
    def _necessity(self, necessity):
        """change the necessity operator"""
        self.__necessity = necessity
        assert self.__necessity in self._NECESSITIES

    def is_true(self, p:int, var="p") -> bool:
        """returns True if the statement is true in this world"""
        self.defined(p, var)
        return p & 1 == 1

    def is_false(self, p:int, var="p") -> bool:
        """returns True if the statement is false in this world"""
        self.defined(p, var)
        return p & 1 == 0

    def is_necessary(self, p:int, var="p") -> bool:
        """returns True if the statement is true in all worlds"""
        self.defined(p, var)
        return p == self.__maxp

    def is_contradictory(self, p:int, var="p") -> bool:
        """returns True if the statement is false in all worlds"""
        self.defined(p, var)
        return p == 0

    def is_contingent(self, p:int, var="p") -> bool:
        """returns True if the statement is true in some worlds"""
        self.defined(p, var)
        return p > 0

    @property
    def T(self):
        """the tautological constant"""
        return self.__maxp

def test_unary(op:callable, df:callable, values:list, expected:list,
               w=2, pv="p"):
    """test a unary operator"""
    first = "   "
    rest = ""
    for p in values:
        df(p)
        rest = rest + f"{p:{w}}"
    print(first + rest)
    print(first + "-" * len(rest))
    rest = ""
    for p in values:
        v = op(p)
        try:
            df(v)
        except ValueError:
            assert False, f"{p} --> {v} UNDEFINED!"
        expected = exp[p]
        assert v == expected, f"{p} --> {v} (exp={expected})"
        rest = rest + f"{v:{w}}"
    print(first + rest)

def test_binary(op:callable, df:callable, values:list, expected:list,
                w=2, pv="p", qv="q"):
    """test a binary operator"""
    filler = " "
    first = f"{qv:>{w}} "
    rest = ""
    for p in values:
        df(p)
        rest = rest + f"{p:{w}}"
    print(filler*(len(first) + len(rest)//2) + pv)
    print(filler*len(first) + rest)
    print(first + "-" * len(rest))
    for q in values:
        first = f"{q:{w}} "
        rest = ""
        for p in values:
            v = op(p,q)
            try:
                df(v)
            except ValueError:
                assert False, f"{p}, {q} --> {v} UNDEFINED!"
            expected = exp[p][q]
            assert v == expected, f"{p}, {q} --> {v} (exp={expected})"
            rest = rest + f"{v:{w}}"
        print(first + rest)

if __name__ == "__main__":
        # TESTS
    print("Testing boolean logic in a two-world universe")
    print("0 - False in both worlds")
    print("1 - True in this world, but not the other")
    print("2 - True in the other world, but not this one")
    print("3 - True in both worlds")
    w2 = BooleanLogic(2)     # two possible worlds

    print("defined(p)...")
    values = range(4)
    for p in values:
        w2.defined(p)
    try:
        w2.defined(-1)
        raise RuntimeError('Error -1')
    except ValueError:
        pass
    try:
        w2.defined(4)
        raise RuntimeError('Error 4')
    except ValueError:
        pass

    print()
    print("Testing boolean operators...")
    print("NOT(p):")
    exp = [3, 2, 1, 0]
    test_unary(w2.NOT, w2.defined, values, exp)

    print("AND(p,q):   (conjunction)")
    exp = [[0, 0, 0, 0],
           [0, 1, 0, 1],
           [0, 0, 2, 2],
           [0, 1, 2, 3]]
    test_binary(w2.AND, w2.defined, values, exp)

    print("OR(p,q):    (disjunction)")
    exp = [[0, 1, 2, 3],
           [1, 1, 3, 3],
           [2, 3, 2, 3],
           [3, 3, 3, 3]]
    test_binary(w2.OR, w2.defined, values, exp)

    print("XOR(p,q):   (exclusive disjunction)")
    exp = [[0, 1, 2, 3],
           [1, 0, 3, 2],
           [2, 3, 0, 1],
           [3, 2, 1, 0]]
    test_binary(w2.XOR, w2.defined, values, exp)

    print("IMP(p,q):   (material implication)")
    exp = [[3, 3, 3, 3],
           [2, 3, 2, 3],
           [1, 1, 3, 3],
           [0, 1, 2, 3]]
    test_binary(w2.IMP, w2.defined, values, exp)

    print("EQU(p,q):   (material equivalence)")
    exp = [[3, 2, 1, 0],
           [2, 3, 0, 1],
           [1, 0, 3, 2],
           [0, 1, 2, 3]]
    test_binary(w2.EQU, w2.defined, values, exp)

    print()
    print("Testing modal operators (Brouwer S6-type systems)...")
    print("Every statement is necessarily possibly possible.")
    print("No statement is necessarily necessary.")

    print("SQU(p):    (necessity)")
    exp = [0, 0, 0, 1]
    test_unary(w2.NECESSARILY, w2.defined, values, exp)

    print("DIA(p):    (possibility)")
    exp = [2, 3, 3, 3]
    test_unary(w2.POSSIBLY, w2.defined, values, exp)

    print("SIMP(p,q):  (strict implication)")
    exp = [[1, 1, 1, 1],
           [0, 1, 0, 1],
           [0, 0, 1, 1],
           [0, 0, 0, 1]]
    test_binary(w2.SIMP, w2.defined, values, exp)

    print("SEQU(p,q):  (strict equivalence)")
    exp = [[1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1]]
    test_binary(w2.SEQU, w2.defined, values, exp)

    print("DIA ∘ DIA:    (possibly possibly operator)")
    PP = lambda p: w2.POSSIBLY(w2.POSSIBLY(p))
    exp = [3, 3, 3, 3]
    test_unary(PP, w2.defined, values, exp)

    print("SQU ∘ SQU:    (necessarily necessarily operator)")
    MM = lambda p: w2.NECESSARILY(w2.NECESSARILY(p))
    exp = [0, 0, 0, 0]
    test_unary(MM, w2.defined, values, exp)
    
    print()
    print("Testing modal operators (Lewis S4-type systems)...")
    print("Impossible statements are not possibly possible.")
    print("Necessary statements are necessarily necessary.")
    w2._necessity = 0

    print("SQU(p):    (necessity)")
    exp = [0, 0, 0, 3]
    test_unary(w2.NECESSARILY, w2.defined, values, exp)

    print("DIA(p):    (possibility)")
    exp = [0, 3, 3, 3]
    test_unary(w2.POSSIBLY, w2.defined, values, exp)

    print("SIMP(p,q):  (strict implication)")
    exp = [[3, 3, 3, 3],
           [0, 3, 0, 3],
           [0, 0, 3, 3],
           [0, 0, 0, 3]]
    test_binary(w2.SIMP, w2.defined, values, exp)

    print("SEQU(p,q):  (strict equivalence)")
    exp = [[3, 0, 0, 0],
           [0, 3, 0, 0],
           [0, 0, 3, 0],
           [0, 0, 0, 3]]
    test_binary(w2.SEQU, w2.defined, values, exp)

    print("DIA ∘ DIA:    (possibly possibly operator)")
    exp = [0, 3, 3, 3]
    test_unary(PP, w2.defined, values, exp)

    print("SQU ∘ SQU:    (necessarily necessarily operator)")
    exp = [0, 0, 0, 3]
    test_unary(MM, w2.defined, values, exp)

    print("OK!")
