"""
logic.lukasiewicz - many-valued Łukasiewicz logic
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    In a basic Łukasiewicz algebra, we have a closed range of numbers in the
    interval [0,1].  In the finite finite case, with n+1 values, these will
    be the rational numbers 0, 1/n, 2/n, ..., (n-1)/n, 1.  Material implication
    is defined as follows:

        p⊃q = min(1, 1-p+q)                 material implication

    The remaining logical connectives can be defined using material implication
    and the constant 0:

        ~p = p⊃0 = 1-p                      logical negation
        p∨q = (p⊃q)⊃q                       disjunction (logical addition)
        p∧q = ~(~p∨~q)                      conjunction (logical multiplication)

    In the two-valued case, these reduce to the corresponding Boolean operators.

    In addition, we have the Tarski modal operators which, to distinguish them
    from the Lewis operators, we notate as:

        Sp = 1 if p=1 else 0                strongly true
        Wp = 0 if p=0 else 1                weakly true

    By vectoring these values, we can create a multiple worlds scenarion which
    generalizes Boolean multiple worlds.

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
from fractions import Fraction
from math import log10, floor

class LukasiewiczLogic(object):
    """Łukasiewicz multiple worlds logic"""

    _NECESSITIES = {0, 1}

    __slots__ = ("__m", "__n", "__necessity", "__width")

    def __init__(self, m:int=3, n:int=1, necessity=1):
        """constructor

        ARGUMENTS
            m - number of truth values
            n - number of worlds (default:1)
        """
        if m == float('inf'):
            pass
        else:
            if type(m) != int:
                raise TypeError("levels (m) must be an integer or infinity")
            if m < 2:
                raise ValueError("levels (m) must be at least two")
        if type(n) != int:
            raise TypeError("number of worlds (n) must be an integer")
        if n < 1:
            raise ValueError("number of worlds (n) must be a positive integer")
        self.__m = m
        self.__n = n
        self._necessity = necessity
        if type(m) == int:
            self.__width = floor(log10(m-1.0))

    def defined(self, p:('Number', tuple), var:str='p'):
        """check whether a truth value is defined"""
        p = self._to_vector(p)
        return self._tuple_defined(p, var)

    def _tuple_defined(self, p:tuple, var):
        """check the vector"""
        # print(var, p)
        if len(p) != self.__n:
            raise ValueError("The number of components in {var} must be {self.__n}")
        for i in range(self.__n):
            self._truth_defined(p[i], var, i)

    def _truth_defined(self, p:'Number', var:str, i:int):
        """check the component"""
        if 0 <= p <= 1:
            pass
        else:
            raise ValueError("Component {i} in {var} must be in [0,1]")
        if self.__n == float('inf'):
            return
        q = p * (self.__m-1)
        if q.denominator == 1:
            return
        smallest = f"1/{self.__m-1}"
        print("---  ERROR VECTOR:", p, var, i, q, self.__m-1, smallest)
        raise ValueError(f"Component {i} in {var} must be a multiple of {smallest}")

    def _to_vector(self, p):
        """convert to vector"""
        if type(p) == tuple:
            return p
        if type(p) == list:
            return tuple(p)
        return tuple([p])

    def NOT(self, p:tuple) -> tuple:
        """logical negation"""
        return tuple((1 - p[i]) for i in range(self.__n))

    def AND(self, p:tuple, q:tuple) -> tuple:
        """conjunction"""
        return tuple(min(p[i], q[i]) for i in range(self.__n))

    def NAND(self, p:tuple, q:tuple) -> tuple:
        """negated conjunction"""
        return self.NOT(self.AND(p,q))

    def OR(self, p:tuple, q:tuple) -> tuple:
        """inclusive disjunction"""
        return tuple(max(p[i], q[i]) for i in range(self.__n))

    def NOR(self, p:tuple, q:tuple) -> tuple:
        """negated disjunction"""
        return self.NOT(self.OR(p,q))

    def IMP(self, p:tuple, q:tuple) -> tuple:
        """material implication"""
        return tuple(min(1, 1-p[i]+q[i]) for i in range(self.__n))

    def EQU(self, p:tuple, q:tuple) -> tuple:
        """material equivalence"""
        return self.AND(self.IMP(p, q), self.IMP(q, p))

    def NEQ(self, p:tuple, q:tuple) -> tuple:
        """negated material equivalence"""
        return self.NOT(self.EQU(p, q))

    def XOR(self, p:tuple, q:tuple) -> tuple:
        """exclusive disjunction"""
        return self.AND(self.OR(p,q), self.NAND(p,q))

    def STRUE(self, p:tuple) -> tuple:
        """Tarski strongly true"""
        return tuple((1 if p[i]==1 else 0) for i in range(self.__n))

    def WTRUE(self, p:tuple) -> tuple:
        """Tarski weakly true"""
        return tuple((0 if p[i]==0 else 1) for i in range(self.__n))

    def NECESSARILY1(self, p:tuple) -> tuple:
        """necessity (weak)

        Returns the minimum truth level in this world.  In other words,
        the level of truth in the real world for ▫p is the minimum level
        of truth for p in all worlds.  In the other worlds, ▫p is false.

        This can be used with modality STRUE to suppress intermediate
        truth levels.
        """
        level = min(p)
        return tuple([level] + [0]*(len(p)-1))

    def NECESSARILY2(self, p:tuple) -> tuple:
        """necessity (strong)

        Returns the minimum truth level into all worlds.  In other words,
        the level of truth in all worlds for ▫p is the minimum level
        of truth for p in all worlds.

        This can be used with modality STRUE to suppress intermediate
        truth levels.
        """
        level = min(p)
        return tuple([level]*len(p))

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

    def is_true(self, p:tuple, var="p") -> bool:
        """returns True if the statement is true in this world"""
        self.defined(p, var)
        return p[0] == 1

    def is_likely_true(self, p:tuple, var="p") -> bool:
        """returns True if the statement is more than half true in this world"""
        self.defined(p, var)
        return p[0] > Fraction(1,2)

    def is_likely_false(self, p:tuple, var="p") -> bool:
        """returns True if the statement is less than half true in this world"""
        self.defined(p, var)
        return p[0] < Fraction(1,2)

    def is_false(self, p:tuple, var="p") -> bool:
        """returns True if the statement is false in this world"""
        self.defined(p, var)
        return p[0] == 0

    def is_necessary(self, p:tuple, var="p") -> bool:
        """returns True if the statement is true in all worlds"""
        self.defined(p, var)
        level = min(p)
        return level == 1

    def is_likely_necessary(self, p:tuple, var="p") -> bool:
        """returns True if the statement is more than half true in all worlds"""
        self.defined(p, var)
        level = min(p)
        return level > Fraction(1,2)

    def is_contradictory(self, p:tuple, var="p") -> bool:
        """returns True if the statement is false in all worlds"""
        self.defined(p, var)
        level = max(p)
        return level == 0

    def is_likely_contradictory(self, p:tuple, var="p") -> bool:
        """returns True if the statement is less than half true in all worlds"""
        self.defined(p, var)
        level = max(p)
        return level < Fraction(1,2)

    def is_contingent(self, p:tuple, var="p") -> bool:
        """returns True if the statement is true in some worlds"""
        self.defined(p, var)
        level = max(p)
        return level == 1

    @property
    def T(self):
        """the tautological constant"""
        return tuple([1]*self.__n)

    @property
    def denominator(self):
        """returns the denominator of the smallest possible truth level"""
        return self.__m - 1

    @property
    def width(self):
        """returns the width of the largest possible numerator

        An exception is raised if this numerator is infinity.
        """
        return self.__width

    @property
    def worlds(self):
        """returns the number of worlds"""
        return self.__n

def pack_levels(obj:callable, p:tuple) -> int:
    """pack a truth value"""
    obj.defined(p)
    d = obj.denominator
    w = obj.width           # exception when undefined
    s = ""
    for x in p:
        s += f"{int(x*d):{w}}"
    return s

def test_unary(obj:callable, op:callable, values:list, exp:list,
               pv="p"):
    """test a unary operator"""
    w = obj.width * obj.worlds
    first = "   "
    rest = ""
    for p in values:
        obj.defined(p)
        rest = rest + pack_levels(obj, p) + " "
    print(first + rest)
    print(first + "-" * len(rest))
    rest = ""
    for i in range(len(values)):
        p = values[i]
        v = op(p)
        try:
            obj.defined(v)
        except ValueError:
            assert False, f"{i}: {p} --> {v} UNDEFINED!"
        expected = exp[i]
        assert v == expected, f"{i}: {p} --> {v} (exp={expected})"
        rest = rest + pack_levels(obj, v) + " "
    print(first + rest)

def test_binary(obj:callable, op:callable, values:list, exp:list,
                pv="p", qv="q"):
    """test a binary operator"""
    w = obj.width * obj.worlds
    filler = " "
    first = f" {qv:>{w}} "
    rest = ""
    for p in values:
        obj.defined(p)
        rest = rest + pack_levels(obj, p) + " "
    print(filler*(len(first) + len(rest)//2) + pv)
    print(filler*len(first) + rest)
    print(first + "-" * len(rest))
    for i in range(len(values)):
        q = values[i]
        first = pack_levels(obj, q) + " "
        rest = ""
        for j in range(len(values)):
            p = values[j]
            v = op(p,q)
            try:
                obj.defined(v)
            except ValueError:
                assert False, f"{i},{j}: {p}, {q} --> {v} UNDEFINED!"
            expected = exp[i][j]
            assert v == expected, f"{i},{j}: {p}, {q} --> {v} (exp={expected})"
            rest = rest + pack_levels(obj, v) + " "
        print(first + rest)

if __name__ == "__main__":

            # USEFUL FOR DEVELOPMENT

    def literal(foo):
        x, y = int(foo[0]), int(foo[1])
        d = {0:'F', 1:'I', 2:'T'}
        return d[x] + d[y]

    def dump_unary(obj, op, values, exp):
        s = "["
        for p in values:
            s = s + literal(pack_levels(obj, op(p))) + ", "
        s = s[:-2] + "]"
        print(s)

    def dump_binary(obj, op, values, exp):
        print("[")
        for q in values:
            s = "["
            for p in values:
                s = s + literal(pack_levels(obj, op(p, q))) + ", "
            s = s[:-2] + "],"
            print(s)
        print("]")

            # TESTS

    print("Testing Łukasiewicz 3-logic in a two-world universe")
    print("  T I F = 1 1/2 0")
    print("        This world")
    print("        F    I    T")
    print("       --------------+   Other world")
    print("        FF   IF   TF |        F")
    print("        FI   II   TI |        I")
    print("        FT   IT   TT |        T")
    print("    0 or F - False")
    print("  1/2 or I - Intermediate (neither true nor false)")
    print("    1 or T - True")
    w2 = LukasiewiczLogic(3,2)     # two possible worlds

    print("defined(p)...")
    T, I, F = 1, Fraction(1,2), 0
    values = [(F,F), (I,F), (T,F),
              (F,I), (I,I), (T,I),
              (F,T), (I,T), (T,T)]
    assert len(set(values)) == 9

    for p in values:
        w2.defined(p)
    try:
        p = (-1, 0)
        w2.defined(p)
        raise RuntimeError('Error -1')
    except ValueError:
        pass
    try:
        p = (0, Fraction(3,2))
        w2.defined(p)
        raise RuntimeError('Error 3/2')
    except ValueError:
        pass
    try:
        p = (0, Fraction(1,3))
        w2.defined(p)
        raise RuntimeError('Error 1/3')
    except ValueError:
        pass

    print("packed truth levels:")
    FIT = {0:'F', Fraction(1,2):'I', 1:'T'}
    for p in values:
        # print(p)
        print(pack_levels(w2, p), FIT[p[0]]+FIT[p[1]], p)

    print("truth levels")
    for p in values:
        x, y = p
        assert w2.is_true(p) == (x == 1)
        assert w2.is_false(p) == (x == 0)
        assert w2.is_necessary(p) == (x == 1 == y)
        assert w2.is_contradictory(p) == (x == 0 == y)
        
    print()
    print("Testing logical operators...")
    print("NOT(p):")
    exp = [(T,T), (I,T), (F,T),
           (T,I), (I,I), (F,I),
           (T,F), (I,F), (F,F)]
    test_unary(w2, w2.NOT, values, exp)

    print("STRUE(p):")
    exp = [(F,F), (F,F), (T,F),
           (F,F), (F,F), (T,F),
           (F,T), (F,T), (T,T)]
    test_unary(w2, w2.STRUE, values, exp)

    print("WTRUE(p):")
    exp = [(F,F), (T,F), (T,F),
           (F,T), (T,T), (T,T),
           (F,T), (T,T), (T,T)]
    test_unary(w2, w2.WTRUE, values, exp)

    FF, IF, TF = (F,F), (I,F), (T,F)
    FI, II, TI = (F,I), (I,I), (T,I)
    FT, IT, TT = (F,T), (I,T), (T,T)
    print("AND(p,q):   (conjunction)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[FF, FF, FF,  FF, FF, FF,  FF, FF, FF], # FF
           [FF, IF, IF,  FF, IF, IF,  FF, IF, IF], # IF
           [FF, IF, TF,  FF, IF, TF,  FF, IF, TF], # TF
        # -------------------------------------------------
           [FF, FF, FF,  FI, FI, FI,  FI, FI, FI], # FI
           [FF, IF, IF,  FI, II, II,  FI, II, II], # II
           [FF, IF, TF,  FI, II, TI,  FI, II, TI], # TI
        # -------------------------------------------------
           [FF, FF, FF,  FI, FI, FI,  FT, FT, FT], # FT
           [FF, IF, IF,  FI, II, II,  FT, IT, IT], # IT
           [FF, IF, TF,  FI, II, TI,  FT, IT, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.AND, values, exp)

    print("OR(p,q):    (disjunction)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[FF, IF, TF,  FI, II, TI,  FT, IT, TT], # FF
           [IF, IF, TF,  II, II, TI,  IT, IT, TT], # IF
           [TF, TF, TF,  TI, TI, TI,  TT, TT, TT], # TF
        # -------------------------------------------------
           [FI, II, TI,  FI, II, TI,  FT, IT, TT], # FI
           [II, II, TI,  II, II, TI,  IT, IT, TT], # II
           [TI, TI, TI,  TI, TI, TI,  TT, TT, TT], # TI
        # -------------------------------------------------
           [FT, IT, TT,  FT, IT, TT,  FT, IT, TT], # FT
           [IT, IT, TT,  IT, IT, TT,  IT, IT, TT], # IT
           [TT, TT, TT,  TT, TT, TT,  TT, TT, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.OR, values, exp)

    print("IMP(p,q):   (material implication)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[TT, IT, FT,  TI, II, FI,  TF, IF, FF], # FF
           [TT, TT, IT,  TI, TI, II,  TF, TF, IF], # IF
           [TT, TT, TT,  TI, TI, TI,  TF, TF, TF], # TF
        # -------------------------------------------------
           [TT, IT, FT,  TT, IT, FT,  TI, II, FI], # FI
           [TT, TT, IT,  TT, TT, IT,  TI, TI, II], # II
           [TT, TT, TT,  TT, TT, TT,  TI, TI, TI], # TI
        # -------------------------------------------------
           [TT, IT, FT,  TT, IT, FT,  TT, IT, FT], # FT
           [TT, TT, IT,  TT, TT, IT,  TT, TT, IT], # IT
           [TT, TT, TT,  TT, TT, TT,  TT, TT, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.IMP, values, exp)

    print("EQU(p,q):   (material equivalence)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[TT, IT, FT,  TI, II, FI,  TF, IF, FF], # FF
           [IT, TT, IT,  II, TI, II,  IF, TF, IF], # IF
           [FT, IT, TT,  FI, II, TI,  FF, IF, TF], # TF
        # -------------------------------------------------
           [TI, II, FI,  TT, IT, FT,  TI, II, FI], # FI
           [II, TI, II,  IT, TT, IT,  II, TI, II], # II
           [FI, II, TI,  FT, IT, TT,  FI, II, TI], # TI
        # -------------------------------------------------
           [TF, IF, FF,  TI, II, FI,  TT, IT, FT], # FT
           [IF, TF, IF,  II, TI, II,  IT, TT, IT], # IT
           [FF, IF, TF,  FI, II, TI,  FT, IT, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.EQU, values, exp)
    print("NEQ(p,q):   (not equivalent)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[FF, IF, TF,  FI, II, TI,  FT, IT, TT], # FF
           [IF, FF, IF,  II, FI, II,  IT, FT, IT], # IF
           [TF, IF, FF,  TI, II, FI,  TT, IT, FT], # TF
        # -------------------------------------------------
           [FI, II, TI,  FF, IF, TF,  FI, II, TI], # FI
           [II, FI, II,  IF, FF, IF,  II, FI, II], # II
           [TI, II, FI,  TF, IF, FF,  TI, II, FI], # TI
        # -------------------------------------------------
           [FT, IT, TT,  FI, II, TI,  FF, IF, TF], # FT
           [IT, FT, IT,  II, FI, II,  IF, FF, IF], # IT
           [TT, IT, FT,  TI, II, FI,  TF, IF, FF]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.NEQ, values, exp)

    print("XOR(p,q):   (exclusive disjunction)")
#    print("\t\t(diffs)")
#    for p in values:
#        for q in values:
#            XOR = w2.XOR(p, q)
#            NEQ = w2.NEQ(p, q)
#            if XOR != NEQ:
#                print("\tp="+pack_levels(w2, p)+",",
#                      "q="+pack_levels(w2, q)+",",
#                      "XOR="+pack_levels(w2, XOR)+",",
#                      "NEQ="+pack_levels(w2, NEQ))
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[FF, IF, TF,  FI, II, TI,  FT, IT, TT], # FF
           [IF, IF, IF,  II, II, II,  IT, IT, IT], # IF
           [TF, IF, FF,  TI, II, FI,  TT, IT, FT], # TF
        # -------------------------------------------------
           [FI, II, TI,  FI, II, TI,  FI, II, TI], # FI
           [II, II, II,  II, II, II,  II, II, II], # II
           [TI, II, FI,  TI, II, FI,  TI, II, FI], # TI
        # -------------------------------------------------
           [FT, IT, TT,  FI, II, TI,  FF, IF, TF], # FT
           [IT, IT, IT,  II, II, II,  IF, IF, IF], # IT
           [TT, IT, FT,  TI, II, FI,  TF, IF, FF]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.XOR, values, exp)

    print()
    print("Testing modal operators (Brouwer S6-type systems)...")
    print("Every statement is necessarily possibly possible.")
    print("No statement is necessarily necessary.")

    print("SQU(p):    (necessity)")
    exp = [FF, FF, FF, FF, IF, IF, FF, IF, TF]
    test_unary(w2, w2.NECESSARILY, values, exp)

    print("DIA(p):    (possibility)")
    exp = [FT, IT, TT, IT, IT, TT, TT, TT, TT]
    test_unary(w2, w2.POSSIBLY, values, exp)

    print("SIMP(p,q):  (strict implication)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[TF, IF, FF,  IF, IF, FF,  FF, FF, FF], # FF
           [TF, TF, IF,  IF, IF, IF,  FF, FF, FF], # IF
           [TF, TF, TF,  IF, IF, IF,  FF, FF, FF], # TF
        # -------------------------------------------------
           [TF, IF, FF,  TF, IF, FF,  IF, IF, FF], # FI
           [TF, TF, IF,  TF, TF, IF,  IF, IF, IF], # II
           [TF, TF, TF,  TF, TF, TF,  IF, IF, IF], # TI
        # -------------------------------------------------
           [TF, IF, FF,  TF, IF, FF,  TF, IF, FF], # FT
           [TF, TF, IF,  TF, TF, IF,  TF, TF, IF], # IT
           [TF, TF, TF,  TF, TF, TF,  TF, TF, TF]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.SIMP, values, exp)

    print("SEQU(p,q):  (strict equivalence)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[TF, IF, FF,  IF, IF, FF,  FF, FF, FF], # FF
           [IF, TF, IF,  IF, IF, IF,  FF, FF, FF], # IF
           [FF, IF, TF,  FF, IF, IF,  FF, FF, FF], # TF
        # -------------------------------------------------
           [IF, IF, FF,  TF, IF, FF,  IF, IF, FF], # FI
           [IF, IF, IF,  IF, TF, IF,  IF, IF, IF], # II
           [FF, IF, IF,  FF, IF, TF,  FF, IF, IF], # TI
        # -------------------------------------------------
           [FF, FF, FF,  IF, IF, FF,  TF, IF, FF], # FT
           [FF, FF, FF,  IF, IF, IF,  IF, TF, IF], # IT
           [FF, FF, FF,  FF, IF, IF,  FF, IF, TF]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.SEQU, values, exp)

    print("DIA ∘ DIA:    (possibly possibly operator)")
    PP = lambda p: w2.POSSIBLY(w2.POSSIBLY(p))
    exp = [TT, TT, TT, TT, TT, TT, TT, TT, TT]
    test_unary(w2, PP, values, exp)

    print("SQU ∘ SQU:    (necessarily necessarily operator)")
    MM = lambda p: w2.NECESSARILY(w2.NECESSARILY(p))
    exp = [FF, FF, FF, FF, FF, FF, FF, FF, FF]
    test_unary(w2, MM, values, exp)

    print()
    print("Testing modal operators (Lewis S4-type systems)...")
    print("Impossible statements are not possibly possible.")
    print("Necessary statements are necessarily necessary.")
    w2._necessity = 0

    print("SQU(p):    (necessity)")
    exp = [FF, FF, FF, FF, II, II, FF, II, TT]
    test_unary(w2, w2.NECESSARILY, values, exp)

    print("DIA(p):    (possibility)")
    exp = [FF, II, TT, II, II, TT, TT, TT, TT]
    test_unary(w2, w2.POSSIBLY, values, exp)

    print("SIMP(p,q):  (strict implication)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[TT, II, FF,  II, II, FF,  FF, FF, FF], # FF
           [TT, TT, II,  II, II, II,  FF, FF, FF], # IF
           [TT, TT, TT,  II, II, II,  FF, FF, FF], # TF
        # -------------------------------------------------
           [TT, II, FF,  TT, II, FF,  II, II, FF], # FI
           [TT, TT, II,  TT, TT, II,  II, II, II], # II
           [TT, TT, TT,  TT, TT, TT,  II, II, II], # TI
        # -------------------------------------------------
           [TT, II, FF,  TT, II, FF,  TT, II, FF], # FT
           [TT, TT, II,  TT, TT, II,  TT, TT, II], # IT
           [TT, TT, TT,  TT, TT, TT,  TT, TT, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.SIMP, values, exp)

    print("SEQU(p,q):  (strict equivalence)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  


    exp = [[TT, II, FF,  II, II, FF,  FF, FF, FF], # FF
           [II, TT, II,  II, II, II,  FF, FF, FF], # IF
           [FF, II, TT,  FF, II, II,  FF, FF, FF], # TF
        # -------------------------------------------------
           [II, II, FF,  TT, II, FF,  II, II, FF], # FI
           [II, II, II,  II, TT, II,  II, II, II], # II
           [FF, II, II,  FF, II, TT,  FF, II, II], # TI
        # -------------------------------------------------
           [FF, FF, FF,  II, II, FF,  TT, II, FF], # FT
           [FF, FF, FF,  II, II, II,  II, TT, II], # IT
           [FF, FF, FF,  FF, II, II,  FF, II, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.SEQU, values, exp)

    print("DIA ∘ DIA:    (possibly possibly operator)")
    exp = [FF, II, TT, II, II, TT, TT, TT, TT]
    test_unary(w2, PP, values, exp)

    print("SQU ∘ SQU:    (necessarily necessarily operator)")
    exp = [FF, FF, FF, FF, II, II, FF, II, TT]
    test_unary(w2, MM, values, exp)

    print("OK!")
