"""
logic.post - many-valued Post logic
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Post algebras are many-valued generalizations of Boolean algebras.
    The basic operations are meet, join, and a logical rotation.  In
    the two-valued False/True case, the result is that meet is ordinary
    conjunction, join is ordinary disjunction, and the logical rotation
    is logical negation.

    The approach to the subject is a modification of the approach taken
    on pages 52-53 and Exercise 1 page 65 of Rosenbloom's EML [1].  The
    main difference is that meet and join have been interchanged in this
    implementation.  In addition, in order to model modal operators like
    possibility and necessity, we allow for multiple world scenarios.

REFERENCE

    [1] Paul Rosenbloom.  Elements of Mathematical Logic.  Dover, 1950.

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
from math import floor
from fractions import Fraction

_TV = "TruthValue"

def _implies(x, y, maxt):
    """material implication (one world)

    If q > p or q = p, then we treat the statement as true and
    assign the maximum truth value.

    if p < q, we return the negated difference.
    """
    if y >= x:
        return maxt
    return maxt - x + y         # maxt >= x > y

def positive_int(n:int, name:str) -> int:
    """validate a positive integer"""
    n = int(n)
    if n < 1:
        raise ValueError(name, "must be a positive integer")
    return n

class PostLogic(object):
    """Multiple-world Post algebras

    SEMANTICS

        The slotted parameters are interpreted as follows:

            __n = number of possible worlds (a positive integer).  World
                0 is the actual world, worlds 1 through n-1 are the other
                possible worlds.  These worlds need not be isomorphic.
            __maxt = the value (a positive integer) for fully true; 0 is
                the fully false value; values in between are
                proportionately true.
            __debug = a flag to indicate whether there is some logging
            IMPLIES = the material implication operator
            NECESSITY =  the Lewis necessity operator
            __same = indicates whether the different worlds are use the
                same truth value ranges.  If all worlds use the same
                range, they are isomorphic.
    """

    __slots__ = ("__n", "__maxt", "__debug",
                 "__same", "IMPLIES", "NECESSITY")

    def __init__(self, *args, debug=False, necessity=1):
        """constructor

        We allow for three types of constructors:
            a) single world
            b) multiple worlds, each with the same structure
            c) multiple worlds, allowing differences in structure

        USAGES
            PostLogic(maxt)                     single world
            PostLogic(n, maxt)                  multiple isomorphic worlds
            PostLogic(maxts)                    multiple worlds

        POSITIONAL ARGUMENTS

            maxt - a positive integer; the possible truth values range
                from 0 to maxt, inclusive.  (For classical Boolean logic,
                set maxt=1.
            n - a positive integer.  If n=1, this is just a single world
                scenario.
            maxts - a tuple containing at least two (not necessarily
                distinct) maximum truth values.  Each of these must be
                a positive integer.
            necessity - selects one of several Lewis necessity operators

        KEYWORD ARGUMENTS

            debug - if True, print some information about program execution.
        """
        self.__debug = bool(debug)
        self.IMPLIES = _implies         # may be changed, but be careful!
        if len(args) == 1:
            arg = args[0]
            if type(arg) in (tuple, list):
                self.__many_worlds(*arg)
            elif type(arg) == range:
                arg = tuple(arg)        # expand the range
                self.__many_worlds(*arg)
            else:
                self.__one_world(arg)
        elif len(args) == 2:
            n = positive_int(args[0], "n")
            maxt = positive_int(args[1], "maxt")
            arg = tuple([maxt] * n)
            self.__many_worlds(*arg)
        else:
            raise TypeError("PostLogic requires either one or two arguments")
        if necessity == 1:
            self.NECESSITY = self.make_necessity_weak(self)
            if debug:
                print("PostLogic:    weak S6-type necessity")
        else:
            self.NECESSITY = self.make_necessity_strong(self)
            if debug:
                print("PostLogic:    strong S4-type necessity")

            # CONSTRUCTOR HELPERS

    def __one_world(self, maxt:int):
        """one world setup"""
        maxt = positive_int(maxt, "maxt")
        self.__n = 1
        self.__maxt = maxt
        self.__same = True
        if self.__debug:
            print(f"PostLogic: 1 world, truth values [0,{maxt}]")

    def __many_worlds(self, *maxts):
        """many worlds setup"""
        n = len(maxts)
        if n < 2:
            raise ValueError("at least two values must be given")
        minmaxt, maxmaxt = float('inf'), 0
        for k in range(n):
            maxt = positive_int(maxts[k], "maxts[k]")
            minmaxt = min(maxt, minmaxt)
            maxmaxt = max(maxt, maxmaxt)
        self.__n = n
        self.__maxt = maxts
        self.__same = (maxmaxt == minmaxt)
        if self.__debug:
            if minmaxt == maxmaxt:
                print(f"PostLogic: {n} worlds, truth values [0,{maxmaxt}]")
            else:
                print(f"PostLogic: {n} worlds, maximum truth values {maxts}")

    def defined(self, p:('Number', tuple), var:str='p'):
        """check whether a truth value is defined

        DESCRIPTION

            Determine whether a given truth value is admissible
            for this class instance (i.e. "self").

            Returns True if the value is admissible.

            Raises a TypeError or a ValueError exception if the
            value is inadmissible.
        """
        n = self.__n
        if n == 1:
            m = self.__maxt
            if type(p) != int or p < 0 or p > m:
                raise ValueError(f"{var} must be int in [0,{m}]")
        else:
            if type(p) != tuple or len(p) != n:
                raise TypeError(f"{var} must be a/an {n}-tuple")
            for k in range(n):
                pk = p[k]
                mk = self.__maxt[k]
                if type(pk) != int or pk < 0 or pk > mk:
                    raise ValueError(f"{var}[{k}] must be int in [0,{mk}]")
        return True

    def NOT(self, p:_TV) -> _TV:
        """logical negation (inverts the truth value)"""
        n, maxt = self.__n, self.__maxt
        if n == 1:
            return maxt - p
        return tuple((self.__maxt[k] - p[k]) for k in range(n))

    def ROT(self, p:_TV, rotate=1) -> _TV:
        """logical rotation"""
        n, maxt = self.__n, self.__maxt
        if n == 1:
            return (p + rotate) % (maxt + 1)
        return tuple(((p[k] + rotate) % (maxt[k] + 1)) for k in range(n))

    def AND(self, p:_TV, q:_TV) -> _TV:
        """conjunction"""
        n, maxt = self.__n, self.__maxt
        if n == 1:
            return min(p, q)
        return tuple(min(p[k], q[k]) for k in range(n))

    def NAND(self, p:_TV, q:_TV) -> _TV:
        """negated conjunction"""
        return self.NOT(self.AND(p, q))

    def OR(self, p:_TV, q:_TV) -> _TV:
        """disjunction"""
        n, maxt = self.__n, self.__maxt
        if n == 1:
            return max(p, q)
        return tuple(max(p[k], q[k]) for k in range(n))

    def NOR(self, p:_TV, q:_TV) -> _TV:
        """negated disjunction"""
        return self.NOT(self.OR(p, q))

    def IMP(self, p:_TV, q:_TV) -> _TV:
        """material implication

            The details may be changed by changing the function
            self.IMPLIES.  Each world is treated as an independent
            scenario.  A replacement should meet the following
            requirements:

                a) usage: IMPLIES(pk, qk, maxtk)

                b) if qk >= pk, return maxtk

                c) if qk < tk, return a value in [0, maxtk-1]

            To generalize Boolean material implication, in addition,
            we also need:

                d) if qk=0 and tk=maxtk, then return 0

        DEFAULT:
            If q > p or q = p, then we treat the statement as true and
            assign the maximum truth value.

            if p < q, we return the negated difference.
        """
        n, maxt = self.__n, self.__maxt
        IMPLIES = self.IMPLIES
        if n == 1:
            return IMPLIES(p, q, maxt)
        return tuple(IMPLIES(p[k], q[k], maxt[k]) for k in range(n))

    def EQU(self, p:_TV, q:_TV) -> _TV:
        """material equivalence."""
        return self.AND(self.IMP(p, q), self.IMP(q, p))

    def NEQ(self, p:_TV, q:_TV) -> _TV:
        """material equivalence."""
        return self.NOT(self.EQU(p, q))

    def XOR(self, p:_TV, q:_TV) -> _TV:
        """exclusive disjunction"""
        return self.AND(self.OR(p,q), self.NAND(p,q))

            # Tarski-style one-world modalities

    def STRUE(self, p:_TV) -> _TV:
        """Tarski strongly true"""
        n, maxt = self.__n, self.__maxt
        if n == 1:
            return maxt if p==maxt else 0
        return tuple((maxt[k] if p[k]==maxt[k] else 0) for k in range(n))

    def WTRUE(self, p:_TV) -> _TV:
        """Tarski weakly true"""
        n, maxt = self.__n, self.__maxt
        if n == 1:
            return maxt if p>0 else 0
        return tuple((maxt[k] if p[k]>0 else 0) for k in range(n))

            # Support for the Lewis necessity operator
            #   These should be helpful in writing scripts.

    @property
    def isomorphic(self) -> bool:
        """returns True if the worlds are isomorphic"""
        return self.__same

    def fully_true_in(self, world:int=0) -> int:
        """returns the value which indicates "fully true" in the given world

        If no world is given, then the result is true in the "actual" world.

        The world should be a non-negative integer which is less than the
        number of possible worlds.

        Note that is the worlds are all isomorphic, then the actual world
        fully true value will be returned for all possible worlds.
        """
        if self.__n == 0:
            return self.__maxt
        return self.__maxt[world]

    @property
    def worlds(self) -> int:
        """returns the number of possible worlds"""
        return self.__n

    @staticmethod
    def make_necessity_strong(instance) -> "operator":
        """necessity (strong)

        DESCRIPTION

            Creates a strong necessity operator akin to Lewis S4.

            The operator returns the minimum truth level into all worlds.
            In other words, the level of truth in all worlds for ▫p
            is the minimum level of truth for p in all worlds.

            This can be used with modality STRUE to suppress intermediate
            truth levels.

            If the worlds are not isomorphic, proportions are used.  

        EXAMPLE WITH NON-ISOMORPHIC WORLDS

            Suppose with two worlds, the actual world has three truth
            levels (0, 1, 2) and the other world has four truth levels
            (0, 1, 2, 3).  Then there are twelve possible truth values,
            namely the ordered pairs in {0,1,2}x{0,1,2,3}.

                  □p        p[1]
                p[0]      0      1      2      3
                  0     (0,0)  (0,0)  (0,0)  (0,0)
                  1     (0,0)  (0,1)  (1,1)  (1,1)
                  2     (0,0)  (0,1)  (1,2)  (2,2)

            Here are the details for some of the calculations.  In
            each case, we round downward:

                 p      proportions                  min   □p
                (1,1)   (1/2, 1/3)    1/3 < 1/2      1/3   (0,1)
                (1,2)   (1/2, 2/3)    1/2 < 2/3      1/2   (1,1)
                (1,3)   (1/2,  1)     1/2 < 1        1/2   (1,1)   *
                (2,1)   ( 1,  1/3)    1/3 < 1        1/3   (0,1)
                (2,2)   ( 1,  2/3)    2/3 < 1        2/3   (1,2)

            (*) The minimum 1/2 is not expressible as a third, so we
            round downward.  The possibilities are 0, 1/3, 2/3 and 1.
            Of these, 2/3 and 1 are larger than 1/2.  We take the largest
            remaining proportion, 1/3 and use its numerator over 3: thus
            (□p)[1] is 1.  The best possible discrete estimate of
            (1/2,1/2) is (1/2,1/3), □p=(1,1).
        """
        if instance.worlds == 1:
            def strongly_necessary(p:_TV) -> _TV:
                """strong necessity (one world)"""
                return p          # EASY!
            return strongly_necessary

        if instance.isomorphic:
            def strongly_necessary(p:_TV) -> _TV:
                """strong necessity (multiple isomorphic worlds)"""
                necessary = (min(p),)                   # scalar
                return necessary * instance.worlds      # vector
            return strongly_necessary

            # NON-ISOMORPHIC MANY WORLDS
        def strongly_necessary(p:_TV) -> _TV:
            """strongly necessary (multiple worlds, not isomorphic)"""
            worlds = range(instance.worlds)
            proportions = tuple(Fraction(p[k], instance.fully_true_in(k)) for k in worlds)
            proportion = min(proportions)
            return tuple(floor(proportion * instance.fully_true_in(k)) for k in worlds)
        return strongly_necessary

    @staticmethod
    def make_necessity_weak(instance) -> "operator":
        """necessity (strong)

        DESCRIPTION

            Creates a weak necessity operator akin to Lewis S6.

            The operator returns the minimum truth level into actual world.
            In other words, the level of truth in the actual worlds for ▫p
            is the minimum level of truth for p in all worlds.

            The operator returns false in all other worlds.

            This can be used with modality STRUE to suppress intermediate
            truth levels.

            If the worlds are not isomorphic, proportions are used.  

        EXAMPLE WITH NON-ISOMORPHIC WORLDS

            Suppose with two worlds, the actual world has three truth
            levels (0, 1, 2) and the other world has four truth levels
            (0, 1, 2, 3).  Then there are twelve possible truth values,
            namely the ordered pairs in {0,1,2}x{0,1,2,3}.

                  □p        p[1]
                p[0]      0      1      2      3
                  0     (0,0)  (0,0)  (0,0)  (0,0)
                  1     (0,0)  (0,0)  (1,0)  (1,0)
                  2     (0,0)  (0,0)  (1,0)  (2,0)

            The results agree with the strong necessity operator in the
            actual (or first) world.  In other worlds, the result is fully
            false.
        """
        if instance.worlds == 1:
            def weakly_necessary(p:_TV) -> _TV:
                """weak necessity (one world)"""
                return p          # EASY!
            return weakly_necessary

        if instance.isomorphic:
            def weakly_necessary(p:_TV) -> _TV:
                """weak necessity (multiple isomorphic worlds)"""
                necessary = (min(p),)                   # scalar
                other = (0,) * (instance.worlds-1)      # vector
                return necessary + other                # vector
            return weakly_necessary

            # NON-ISOMORPHIC MANY WORLDS
        def weakly_necessary(p:_TV) -> _TV:
            """strongly necessary (multiple worlds, not isomorphic)"""
            proportions = tuple(Fraction(p[k], instance.fully_true_in(k)) for k in range(instance.worlds))
            smallest = min(proportions)                 # scalar, fraction
            estimate = floor(smallest * instance.fully_true_in(0)) # scalar
            return (estimate,) + (0,) * (instance.worlds-1)   # vector
        return weakly_necessary

    def NECESSARILY(self, p:_TV) -> _TV:
        """the necessity operator (hook)"""
        return self.NECESSITY(p)

    def POSSIBLY(self, p:_TV) -> _TV:
        """he possibility operator"""
        return self.NOT(self.NECESSARILY(self.NOT(p)))

    def ACTUALLY(self, p:_TV) -> _TV:
        """he actuality operator"""
        if self.__n == 1:
            return p                            # EASY!
        if self.__same:
            return (p[0],) * self.__n           # vector
                # NON-ISO CASE
        x = p[0]                            # scalar
        d = self.__maxt[0]
        y = (floor(Fraction(x,d)*self.__maxt[k]) for k in range(1, self.__n))
        return (x,) + tuple(y)

def test1():
    """test the one world scenario with n=4"""
    print("\t\t\tPost Algebras")
    print()
    print("REFERENCES:")
    print("\t[1] Paul Rosembloom. Elements of Mathematical Logic.")
    print("\t    1950 (Dover, New York.  Section 4.  Cited as \"EML\".")
    print("\t\tNOTES:")
    print("\t\t\tIn this implementation, we treat as a meet the")
    print("\t\t\tjoin operation in EML, page 52.  Similarly, the")
    print("\t\t\tEML's meet is implemented here as a join.  The")
    print("\t\t\ttruth values range in [0,n-1] instead of [1.n] --")
    print("\t\t\tthis simplifies the Python programming. Duality")
    print("\t\t\tbetween meets and joins holds via DeMorgan's Law.")

    print()
    print("Step 1) Test single world setup:")
    post = PostLogic(3, debug=True)
    truth = tuple(range(4))
    print("Truth values:", truth)
    print("\t\t\tUnary operators")
    print("p  |\t~p\t⪧p\t□p\t◇p\tMp\tPp")
    for p in truth:
        post.defined(p)
        p1 = post.NOT(p)
        p2 = post.ROT(p)
        p3 = post.NECESSARILY(p)
        p4 = post.POSSIBLY(p)
        p5 = post.STRUE(p)
        p6 = post.WTRUE(p)
        print(f"{p}  |\t{p1}\t{p2}\t{p3}\t{p4}\t{p5}\t{p6}")
    try:
        post.defined(4)
        assert False, "4 is not a legitimate value"
    except ValueError as msg:
        print("Message for 4:", msg)

    print("\t\tp∧q  (conjunction)")
    print("p | q:\t0\t1\t2\t3")
    print("--+" + "-" * 32)
    for p in truth:
        line = list([p])
        for q in truth:
            result = post.AND(p, q)
            assert result == min(p, q), f"{p=}, {q=}, p∧q={result}"
            post.defined(result, var=f"({p}∧{q})")
            line.append(result)
        print("%d |\t%d\t%d\t%d\t%d" % tuple(line))

    print("\t\tp∨q  (disunction)")
    print("p | q:\t0\t1\t2\t3")
    print("--+" + "-" * 32)
    for p in truth:
        line = list([p])
        for q in truth:
            result = post.OR(p, q)
            assert result == max(p, q), f"{p=}, {q=}, p∧q={result}"
            post.defined(result, var=f"({p}∨{q})")
            line.append(result)
        print("%d |\t%d\t%d\t%d\t%d" % tuple(line))

    print("\t\tp⊃q  (material implication)")
    print("p | q:\t0\t1\t2\t3")
    print("--+" + "-" * 32)
    imp = lambda x, y: min(3, max(0, 3 - x + y))
    for p in truth:
        line = list([p])
        for q in truth:
            result = post.IMP(p, q)
            assert result == imp(p, q), f"{p=}, {q=}, p⊃q={result}"
            post.defined(result, var=f"({p}⊃{q})")
            line.append(result)
        print("%d |\t%d\t%d\t%d\t%d" % tuple(line))

    print("\t\tp≡q  (material equivalence)")
    print("p | q:\t0\t1\t2\t3")
    print("--+" + "-" * 32)
    for p in truth:
        line = list([p])
        for q in truth:
            result = post.EQU(p, q)
            post.defined(result, var=f"({p}≡{q})")
            line.append(result)
        print("%d |\t%d\t%d\t%d\t%d" % tuple(line))

    print()
    print("Step 2) Look at claims on pages 253-254 of Rosenbloom, EML")
    print("    Summary:")
    print("        a) functional completeness (here verified for 4-valued)")
    print("        b) primitives: rotation and conjunction")
    NOT = lambda x: post.NOT(x)
    ROT = lambda x: post.ROT(x)
    ROT2 = lambda x: post.ROT(x, 2)
    ROT3 = lambda x: post.ROT(x, 3)
    AND = lambda x, y: post.AND(x, y)
    OR = lambda x, y: post.OR(x, y)
    EQU = lambda x, y: post.EQU(x, y)
    print("  P2) ⊦(p∧q)≡(q∧p)\t", end="")
    claim = lambda x, y: EQU(AND(x, y), AND(y, x))
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  P3) ⊦((p∧q)∧r)≡(p∧(q∧r))\t", end="")
    claim = lambda x, y, z: EQU(AND(AND(x, y), z), AND(x, AND(y, z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = claim(p, q, r)
                assert result == 3, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")
    print("  P4) ⊦(p∧p)≡p\t", end="")
    claim = lambda x: EQU(AND(x, x), x)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")
    print("  D3) ⊦(p ∧ ⪧p∧ ⪧⪧p ∧ ⪧⪧⪧p)≡0\t", end="")
    claim = lambda x: EQU(AND(x, AND(ROT(x), AND(ROT2(x), ROT3(x)))), 0)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")
    print("  D4a) ⊦⪧p0≡1\t", end="")
    result = EQU(ROT(0), 1)
    assert result == 3, f"failed: ⪧p0={ROT(0)}, {result=}"
    print("ok!")
    print("  D4b) ⊦⪧p1≡2\t", end="")
    result = EQU(ROT(1), 2)
    assert result == 3, f"failed: ⪧p1={ROT(1)}, {result=}"
    print("ok!")
    print("  D4c) ⊦⪧p2≡3\t", end="")
    result = EQU(ROT(2), 3)
    assert result == 3, f"failed: ⪧p2={ROT(2)}, {result=}"
    print("ok!")
    print("  P5) ⊦⪧p3≡0\t", end="")
    result = EQU(ROT(3), 0)
    assert result == 3, f"failed: ⪧p3={ROT(3)}, {result=}"
    print("ok!")
    print("  D5) φ₀(p) := ⪧⪧⪧(⪧p∧ ⪧⪧p ∧ ⪧⪧⪧p)")
    phi0 = lambda x: ROT3(AND(ROT(x), AND(ROT2(x), ROT3(x))))
    print("  D6a) φ₁(p) := ⪧⪧⪧(⪧⪧⪧(p ∧ 1) ∧ ⪧⪧p)")
    phi1 = lambda x: ROT3(AND(ROT3(AND(x, 1)), ROT2(x)))
    print("  D6b) φ₂(p) := ⪧⪧⪧(⪧⪧⪧(p ∧ 1) ∧ ⪧⪧p)")
    phi2 = lambda x: ROT3(AND(ROT3(AND(x, 1)), ROT3(x)))
    print("\t p\t%d\t%d\t%d\t%d" % truth)
    print("\t" + "-" * 35)
    results = tuple(phi0(p) for p in truth)
    print("\t φ₀(p)\t%d\t%d\t%d\t%d" % results)
    results = tuple(phi1(p) for p in truth)
    print("\t φ₁(p)\t%d\t%d\t%d\t%d" % results)
    results = tuple(phi2(p) for p in truth)
    print("\t φ₂(p)\t%d\t%d\t%d\t%d" % results)
    print("    Negation is not a primitive...  But it takes some work!")
    print("    Negation can be defined in terms of conjunction and rotation!")
    print("  D7) ~p ≡ (φ₀(⪧p) ∧ φ₁(⪧⪧p) ∧ φ₂(⪧⪧⪧p))\t", end="")
    f0 = lambda x: phi0(ROT(p))
    f1 = lambda x: phi1(ROT2(p))
    f2 = lambda x: phi2(ROT3(p))
    claim = lambda x: EQU(NOT(p),AND(AND(f0(x),f1(x)),f2(p)))
    for p in truth:
          result = claim(p)
          assert result == 3, f"\tfailed: {p=}, {result=}"
    print("ok!")
    print("    Disjunction can be defined using DeMorgan's law...")
    print("  D8) ⊦(p∨q)≡~(~p∧~q)\t", end="")
    claim = lambda x, y: EQU(OR(x,y),NOT(AND(NOT(x),NOT(y))))
    for p in truth:
        for q in truth:
            result = claim(p,q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("    Distributive laws hold!")
    print("  P6a) ⊦((p∨q)∧r)≡((p∧r)∨(q∧r))\t", end="")
    claim = lambda x, y, z: EQU(AND(OR(x,y),z), OR(AND(x,z),AND(y,z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = claim(p, q, r)
                assert result == 3, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")
    print("  P6b) ⊦((p∧q)∨r)≡((p∨r)∧(q∨r))\t", end="")
    claim = lambda x, y, z: EQU(OR(AND(x,y),z), AND(OR(x,z),OR(y,z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = claim(p, q, r)
                assert result == 3, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")

    print("   Absorption laws?  Do they hold?  Yes, they do!")
    print("  A1) ⊦((p∧q)∨p)≡p\t", end="")
    claim = lambda x, y: EQU(OR(AND(x,y),x), x)
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  A2) ⊦((p∨q)∧p)≡p\t", end="")
    claim = lambda x, y: EQU(AND(OR(x,y),x), x)
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print()
    print("Step 3) Excluded middle? No!  Excluded fifth? Yes!")
    print("    The excluded middle law fails!")
    print("  E3) ⊦(p∨~p) is not valid!\t", end="")
    claim = lambda x: OR(x, NOT(x))
    ok = False
    for p in truth:
        result = claim(p)
        if result == 3:
            continue
        ok = True
        print(f"ok!: {p=}, {result=}")
        break
    assert ok, "failed!  excluded middle was not falsified!"
    print("    But we have the following analogue -- the excluded fifth:")
    print("  E5) ⊦(p ∨ ⪧p ∨ ⪧⪧p ∨ ⪧⪧⪧p)\t", end="")
    claim = lambda x: OR(OR(x, ROT(x)), OR(ROT2(x), ROT3(x)))
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")
    print("    The excluded fourth fails!")
    print("  E4) ⊦(p ∨ ⪧p ∨ ⪧⪧p) is not valid!\t", end="")
    claim = lambda x: OR(OR(x, ROT(x)), ROT2(x))
    ok = False
    for p in truth:
        result = claim(p)
        if result == 3:
            continue
        ok = True
        print(f"ok!: {p=}, {result=}")
        break
    assert ok, "failed!  excluded fourth was not falsified!"

    print()
    print("Step 4) Exercise 1, page 65 in EML")
    print("\tSome of these have been dualized.  (See the headnote above.)")
    print("\tThese are truth table verifications, not synthetic proofs.")

    print("  a) ⊦(p∨q)≡(q∨p)\t", end="")
    claim = lambda x, y: EQU(OR(x, y), OR(y, x))
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print("  b0) ⊦0(p)≡0(q), i.e. 0(p) is a constant function,")
    print("      where 0(p) := p ∧ ⪧p ∧ ⪧⪧p ∧ ⪧⪧⪧p. \t", end="")
    zero = lambda x: AND(AND(x, ROT(x)), AND(ROT2(x), ROT3(x)))
    claim = lambda x, y: EQU(zero(x), zero(y))
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  b1) ⊦1(p)≡1(q), i.e. 1(p) is a constant function,")
    print("      where 1(p) := ⪧0(p). \t", end="")
    one = lambda x: ROT(zero(x))
    claim = lambda x, y: EQU(one(x), one(y))
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  b2) ⊦2(p)≡2(q), i.e. 2(p) is a constant function,")
    print("      where 2(p) := ⪧1(p). \t", end="")
    two = lambda x: ROT(one(x))
    claim = lambda x, y: EQU(two(x), two(y))
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  b3) ⊦3(p)≡3(q), i.e. 3(p) is a constant function,")
    print("      where 3(p) := ⪧2(p). \t", end="")
    three = lambda x: ROT(two(x))
    claim = lambda x, y: EQU(three(x), three(y))
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  b4) ⊦4(p)≡0(q), where 4(p) := ⪧3(p). \t", end="")
    four = lambda x: ROT(three(x))
    claim = lambda x, y: EQU(four(x), zero(y))
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    
    print("  c1) ⊦(p∧0)≡0\t", end="")
    claim = lambda x: EQU(AND(x, 0), 0)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")
    print("  c2) ⊦(p∨3)≡3\t", end="")
    claim = lambda x: EQU(OR(x, 3), 3)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")

    print("  d, e) absorption laws verified above!")

    print("  f1) ⊦(p∨p)≡p\t", end="")
    claim = lambda x: EQU(OR(x, x), x)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")
    print("  f2) ⊦~~p≡p\t", end="")
    claim = lambda x: EQU(NOT(NOT(x)), x)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")

    print("  g1) ⊦(p∧3)≡p\t", end="")
    claim = lambda x: EQU(AND(x, 4), x)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")
    print("  g2) ⊦(p∨0)≡p\t", end="")
    claim = lambda x: EQU(OR(x, 0), x)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")

    print("  h) ⊦(p∨(q∨r))≡((p∨q)∨r)\t", end="")
    claim = lambda x, y, z: EQU(OR(OR(x, y), z), OR(x, OR(y, z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = claim(p, q, r)
                assert result == 3, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")

    print("  i) distributive ∨ over ∧, see P6b above...")
    print("  j) ⊦⪧⪧⪧⪧p≡p\t", end="")
    claim = lambda x: EQU(ROT(ROT(ROT(ROT(x)))), x)
    for p in truth:
        result = claim(p)
        assert result == 3, f"failed: {p=}, {result=}"
    print("ok!")

    print("  k) ⊦((p∧q)≡p)≡((p∨q)≡q)\t", end="")
    claim = lambda x, y: EQU(EQU(AND(x, y),x), EQU(OR(x, y), y))
    for p in truth:
        for q in truth:
            result = claim(p, q)
            assert result == 3, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print("  l) φ₁(1)≡3\t", end="")
    assert phi1(1) == 3, f"{phi1(1)=} != 3"
    print("ok!")

    print("  m) φ₀(1) = φ₀(2) = φ₀(3) = 3\t", end="")
    assert phi0(1) == phi0(2) == phi0(3) == 3, f"({phi0(1)=},{phi0(2)=},{phi0(3)=} = (3,3,3)"
    print("ok!")

    print("  n) 0 ≡ (φ₀(0)∧3)\t", end="")
    assert 0 == AND(phi0(0), 3), f"({phi0(0)=}"
    print("ok!")

    print("  o0) ~0 ≡ 3\t", end="")
    assert NOT(0) == 3, f"({NOT(0)=}"
    print("ok!")
    print("  o1) ~1 ≡ 2\t", end="")
    assert NOT(1) == 2, f"({NOT(1)=}"
    print("ok!")
    print("  o2) ~2 ≡ 1\t", end="")
    assert NOT(2) == 1, f"({NOT(2)=}"
    print("ok!")
    print("  o3) ~3 ≡ 0\t", end="")
    assert NOT(3) == 0, f"({NOT(3)=}"
    print("ok!")

    print("  p, q) see (f, g) above.")

    print("  r) 0 ≡ φ₀(0)\t", end="")
    assert 0 == phi0(0), f"({phi0(0)=}"
    print("ok!  See also (n) above.")

    print("  s1) 1∧2 = 1∧3 = 1\t", end="")
    assert AND(1,2) == AND(1,3) == 1, "oops!"
    print("ok!")
    print("  s2) 2∨0 = 2∨1 = 2\t", end="")
    assert OR(2,0) == OR(2,1) == 2, "oops!"
    print("ok!")

    print("  t, u, v) See Step 2 above.")
    print("single world test completed successfully.")

def test2():
    """three isomorphic worlds with 5 levels each."""
    class triple(tuple):
        """three-element tuples"""

        def __new__(cls, x, y, z):
            """constructor - phase 1"""
            return super().__new__(cls, (x, y, z))

        def __init__(self, x, y, z):
            """constructor - phase 2"""
            super().__init__()

        def __str__(self):
            """packed string"""
            x, y, z = self[0], self[1], self[2]
            return f"{x}{y}{z}"

        def __repr__(self):
            """packed string"""
            x, y, z = self[0], self[1], self[2]
            return f"{x}{y}{z}"

        @classmethod
        def unpack(cls, s:str) -> tuple:
            """convert a 3-string to a triple"""
            if type(s) != str:
                raise TypeError
            if len(s) != 3:
                raise ValueError
            return triple(int(s[0]), int(s[1]), int(s[2]))

    post = PostLogic(3, 4, debug=True)
    levels = range(5)
    truth = tuple(triple(p,q,r) for p in levels for q in levels for r in levels)
    print("Truth values:", truth)
    assert triple.unpack("123") == (1, 2, 3)
    assert len(truth) == 125
    print()
    print("There are 125 possible truth values (5 levels in each of three worlds),")
    print("*** Verification time for an n-variable expression is proportional to 125^nL,")
    print("where L is the length of the expression.")
    print("*** The associative laws and distributive laws tests each run")
    print("through", 125**3, "cases!")
    print()

    print("verifying the NOT operation...", end="")
    for p in truth:
        q = triple(*post.NOT(p))
        for i in range(3):
            assert q[i] == 4-p[i], f"{p=}, ~p={q}"
    print("ok!")

    print("verifying the AND operation...", end="")
    for p in truth:
        for q in truth:
            r = triple(*post.AND(p, q))
            for i in range(3):
                assert r[i] == min(p[i], q[i]), f"{p=}, {q=}, p∧q={r}"
    print("ok!")

    print("verifying the OR operation...", end="")
    for p in truth:
        for q in truth:
            r = triple(*post.OR(p, q))
            for i in range(3):
                assert r[i] == max(p[i], q[i]), f"{p=}, {q=}, p∨q={r}"
    print("ok!")

    print("verifying the IMP operation...", end="")
    for p in truth:
        for q in truth:
            r = triple(*post.IMP(p, q))
            for i in range(3):
                assert r[i] == _implies(p[i], q[i], 4), f"{p=}, {q=}, p⊃q={r}"
    print("ok!")

    print("verifying the STRUE operation...", end="")
    for p in truth:
        q = triple(*post.STRUE(p))
        for i in range(3):
            assert q[i] == (4 if p[i]==4 else 0), f"{p=}, Mp={q}"
    print("ok!")

    print("verifying the WTRUE operation...", end="")
    for p in truth:
        q = triple(*post.WTRUE(p))
        for i in range(3):
            assert q[i] == (0 if p[i]==0 else 4), f"{p=}, Mp={q}"
    print("ok!")

    print("verifying the Brouwerian S6 NECESSARILY operation...", end="")
    for p in truth:
        q = triple(*post.NECESSARILY(p))
        minq = min(p)
        r = triple(minq, 0, 0)
        assert q == r, f"{p=}, □p={q} expected {r}"
    print("ok!")

    print("verifying the ACTUALLY operation...", end="")
    for p in truth:
        q = triple(*post.ACTUALLY(p))
        r = triple(p[0], p[0], p[0])
        assert q == r, f"{p=}, actually(p)={q} expected {r}"
    print("ok!")

    print("changing the NECESSARILY operation...")
    post.NECESSITY = PostLogic.make_necessity_strong(post)
    print("verifying the Lewis S4 NECESSARILY operation...", end="")
    for p in truth:
        q = triple(*post.NECESSARILY(p))
        minq = min(p)
        r = triple(minq, minq, minq)
        assert q == r, f"{p=}, □p={q} expected {r}"
    print("ok!")

    print("changing the NECESSARILY operation back...")
    post.NECESSITY = PostLogic.make_necessity_weak(post)
    print("verifying the Brouwerian S6 NECESSARILY operation...", end="")
    for p in truth:
        q = triple(*post.NECESSARILY(p))
        minq = min(p)
        r = triple(minq, 0, 0)
        assert q == r, f"{p=}, □p={q} expected {r}"
    print("ok!")

    print("verifying some standard tautologies:")

    always = triple(4, 4, 4)
    really = triple(4, 0, 0)
    never = triple(0, 0, 0)

    NOT = lambda x: post.NOT(x)
    ROT = lambda x: post.ROT(x)
    ROT2 = lambda x: post.ROT(x, 2)
    ROT3 = lambda x: post.ROT(x, 3)
    ROT4 = lambda x: post.ROT(x, 4)
    AND = lambda x, y: post.AND(x, y)
    OR = lambda x, y: post.OR(x, y)
    EQU = lambda x, y: post.EQU(x, y)

    print("\tTop and bottom lattice elements")
    print("  A1) ⊦(p∧0)≡0\t", end="")
    claim = lambda x: EQU(AND(x, never), never)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("  A2) ⊦(p∧4)≡p\t", end="")
    claim = lambda x: EQU(AND(x, always), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("  A3) ⊦(p∨4)≡4\t", end="")
    claim = lambda x: EQU(OR(x, always), always)
    for p in truth:
        result = claim(p)
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("  A4) ⊦(p∨0)≡p\t", end="")
    claim = lambda x: EQU(OR(x, never), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("\tIdempotency")
    print("  B1) ⊦(p∧p)≡p\t", end="")
    claim = lambda x: EQU(AND(x, x), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("  B2) ⊦(p∨p)≡p\t", end="")
    claim = lambda x: EQU(OR(x, x), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("\tCommutativity")
    print("  C1) ⊦(p∧q)≡(q∧p)\t", end="")
    claim = lambda x, y: EQU(AND(x, y), AND(y, x))
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print("  C2) ⊦(p∨q)≡(q∨p)\t", end="")
    claim = lambda x, y: EQU(OR(x, y), OR(y, x))
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print("\tAssociativity [be patient!]")
    print("  D1) ⊦((p∧q)∧r)≡(p∧(q∧r))\t", end="")
    claim = lambda x, y, z: EQU(AND(AND(x, y), z), AND(x, AND(y, z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = triple(*claim(p, q, r))
                assert result == always, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")

    print("  D2) ⊦((p∨q)∨r)≡(p∨(q∨r))\t", end="")
    claim = lambda x, y, z: EQU(OR(OR(x, y), z), OR(x, OR(y, z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = triple(*claim(p, q, r))
                assert result == always, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")

    print("\tAbsorptivity")
    print("  E1) ⊦((p∧q)∨p)≡p\t", end="")
    claim = lambda x, y: EQU(OR(AND(x,y),x), x)
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  E2) ⊦((p∨q)∧p)≡p\t", end="")
    claim = lambda x, y: EQU(AND(OR(x,y),x), x)
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print("\tDistributivity [be patient!]")
    print("  F1) ⊦((p∨q)∧r)≡((p∧r)∨(q∧r))\t", end="")
    claim = lambda x, y, z: EQU(AND(OR(x,y),z), OR(AND(x,z),AND(y,z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = triple(*claim(p, q, r))
                assert result == always, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")
    print("  F2) ⊦((p∧q)∨r)≡((p∨r)∧(q∨r))\t", end="")
    claim = lambda x, y, z: EQU(OR(AND(x,y),z), AND(OR(x,z),OR(y,z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = triple(*claim(p, q, r))
                assert result == always, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")

    print("\tDeMorgan's Laws")
    print("  G1) ⊦(p∨q)≡~(~p∧~q)\t", end="")
    claim = lambda x, y: EQU(OR(x,y),NOT(AND(NOT(x),NOT(y))))
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  G2) ⊦(p∧q)≡~(~p∨~q)\t", end="")
    claim = lambda x, y: EQU(AND(x,y),NOT(OR(NOT(x),NOT(y))))
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  G3) ⊦~~p≡p\t", end="")
    claim = lambda x: EQU(NOT(NOT(x)), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("multiple isomorphic worlds test completed successfully.")

def test3():
    """multiple words, non-isomorphic"""
    class triple(tuple):
        """three-element tuples"""

        def __new__(cls, x, y, z):
            """constructor - phase 1"""
            return super().__new__(cls, (x, y, z))

        def __init__(self, x, y, z):
            """constructor - phase 2"""
            super().__init__()

        def __str__(self):
            """packed string"""
            x, y, z = self[0], self[1], self[2]
            return f"{x}{y}{z}"

        def __repr__(self):
            """packed string"""
            x, y, z = self[0], self[1], self[2]
            return f"{x}{y}{z}"

        @classmethod
        def unpack(cls, s:str) -> tuple:
            """convert a 3-string to a triple"""
            if type(s) != str:
                raise TypeError
            if len(s) != 3:
                raise ValueError
            return triple(int(s[0]), int(s[1]), int(s[2]))

    post = PostLogic((3, 2, 4), debug=True)
    level0 = range(4)
    print("Truth levels for the actual world (world 0):", tuple(level0))
    level1 = range(3)
    print("Truth levels for the other world 1:", tuple(level1))
    level2 = range(5)
    print("Truth levels for the other world 2:", tuple(level2))
    maxlevels = triple(3, 2, 4)

    truth = tuple(triple(p,q,r) for p in level0 for q in level1 for r in level2)
    print("Truth values:", truth)
    assert triple.unpack("123") == (1, 2, 3)
    assert len(truth) == 60
    print()
    print("There are 60 possible truth values (5 levels in each of three worlds),")
    print("*** Verification time for an n-variable expression is proportional to 60^nL,")
    print("where L is the length of the expression.")
    print("*** The associative laws and distributive laws tests each run")
    print("through", 60**3, "cases!")
    print()

    print("verifying the NOT operation...", end="")
    for p in truth:
        q = triple(*post.NOT(p))
        for i in range(3):
            assert q[i] == maxlevels[i]-p[i], f"{p=}, ~p={q}"
    print("ok!")

    print("verifying the AND operation...", end="")
    for p in truth:
        for q in truth:
            r = triple(*post.AND(p, q))
            for i in range(3):
                assert r[i] == min(p[i], q[i]), f"{p=}, {q=}, p∧q={r}"
    print("ok!")

    print("verifying the OR operation...", end="")
    for p in truth:
        for q in truth:
            r = triple(*post.OR(p, q))
            for i in range(3):
                assert r[i] == max(p[i], q[i]), f"{p=}, {q=}, p∨q={r}"
    print("ok!")

    print("verifying the IMP operation...", end="")
    for p in truth:
        for q in truth:
            r = triple(*post.IMP(p, q))
            for i in range(3):
                top = maxlevels[i]
                assert r[i] == _implies(p[i], q[i], top), f"{p=}, {q=}, p⊃q={r}"
    print("ok!")

    print("verifying the STRUE operation...", end="")
    for p in truth:
        q = triple(*post.STRUE(p))
        for i in range(3):
            top = maxlevels[i]
            assert q[i] == (top if p[i]==top else 0), f"{p=}, Mp={q}"
    print("ok!")

    print("verifying the WTRUE operation...", end="")
    for p in truth:
        q = triple(*post.WTRUE(p))
        for i in range(3):
            top = maxlevels[i]
            assert q[i] == (0 if p[i]==0 else top), f"{p=}, Mp={q}"
    print("ok!")

    print("verifying the Brouwerian S6 NECESSARILY operation...", end="")
    for p in truth:
        q = triple(*post.NECESSARILY(p))
        r = (Fraction(p[0],3), Fraction(p[1],2), Fraction(p[2],4))
        r0 = min(r)
        s0 = floor(r0*3)
        s = triple(s0, 0, 0)
        # print(f"{p=}, {q=}, r=({r[0]},{r[1]},{r[2]}), r0={r0}, {s0=}, {s=}")
        assert q == s, f"{p=}, □p={q} expected {s}"
    print("ok!")

    print("  Example 1: p=111 □p=000 since 1/4<1/3<1/2")
    q = post.NECESSARILY(triple(1, 1, 1))
    assert q == triple(0, 0, 0), q

    print("  Example 2: p=112 □p=100 since 1/3<1/2=2/4")
    q = post.NECESSARILY(triple(1, 1, 2))
    assert q == triple(1, 0, 0), q

    print("  Example 3: p=213 □p=100 since 1/2<2/3<3/4 and 1/2>1/3")
    q = post.NECESSARILY(triple(1, 2, 3))
    assert q == triple(1, 0, 0), q

    print("  Table for NECESSARILY: (always false in other worlds!)")
    print("\tp=0** or *0* or **0, □p=000")
    for p in truth:
        if 0 in p:
            continue
        q = triple(*post.NECESSARILY(p))
        print(f"\t{p=}, □p={q}")

    print("Brouwerian axiom for Lewis S6-S8")
    print("    ⊦◇◇p\t", end="")
    claim = lambda x: post.POSSIBLY(post.POSSIBLY(x))
    for p in truth:
        result = triple(*claim(p))
        assert result == maxlevels, f"failed: {p=}, {result=}"
    print("ok!")
    
    print("Axiom for Lewis S4")
    print("    ⊦□p⊃□□p\t(this sometimes fails)")
    claim = lambda x: post.IMP(post.NECESSARILY(x), post.NECESSARILY(post.NECESSARILY(x)))
    ok = False
    for p in truth:
        result = triple(*claim(p))
        if result != maxlevels:
            print(f"ok!  (fails for {p=}, {result=})")
            ok = True
    assert ok, "oops!  This should fail!"

    print("verifying the ACTUALLY operation...", end="")
    for p in truth:
        q = triple(*post.ACTUALLY(p))
        r0 = p[0]
        r1 = floor(Fraction(r0,3) * 2)
        r2 = floor(Fraction(r0,3) * 4)
        r = triple(r0, r1, r2)
        assert q == r, f"{p=}, actually(p)={q} expected {r}"
    print("ok!")

    print("  Table for ACTUALLY:  (other world levels are ignored)")
    for p in level0:
        pxx = triple(p,0,0)
        q = triple(*post.ACTUALLY(pxx))
        print(f"\tp={p}**  actually(p)={q}")

    print("changing the NECESSARILY operation...")
    post.NECESSITY = PostLogic.make_necessity_strong(post)
    print("verifying the Lewis S4 NECESSARILY operation...", end="")
    for p in truth:
        q = triple(*post.NECESSARILY(p))
        r = (Fraction(p[0],3), Fraction(p[1],2), Fraction(p[2],4))
        r0 = min(r)
        s0 = floor(r0*3)
        s1 = floor(r0*2)
        s2 = floor(r0*4)
        s = triple(s0, s1, s2)
        # print(f"{p=}, {q=}, r=({r[0]},{r[1]},{r[2]}), r0={r0}, {s0=}, {s=}")
        assert q == s, f"{p=}, □p={q} expected {s} r0={r0}"
    print("ok!")

    print("  Table for S4-style NECESSARILY:")
    print("\tp=0** or *0* or **0, □p=000")
    for p in truth:
        if 0 in p:
            continue
        q = triple(*post.NECESSARILY(p))
        print(f"\t{p=}, □p={q}")

    print("Brouwerian axiom for Lewis S6-S8")
    print("    ⊦◇◇p\t(this sometimes fails)")
    claim = lambda x: post.POSSIBLY(post.POSSIBLY(x))
    ok = False
    for p in truth:
        result = triple(*claim(p))
        if result != maxlevels:
            print(f"ok!  (fails for {p=}, {result=})")
            ok = True
    assert ok, "oops!  This should fail!"
    
    print("Axiom for Lewis S4")
    print("    ⊦□p⊃□□p\t(this can fail with intermediate values)")
    claim = lambda x: post.IMP(post.NECESSARILY(x), post.NECESSARILY(post.NECESSARILY(x)))
    ok = 0
    for p in truth:
        result = triple(*claim(p))
        if result != maxlevels:
            print(f"ok!  (fails for {p=}, {result=})")
            ok += 1
    print(f"Warning: Fails in {ok} cases!")

    print("changing the NECESSARILY operation back...")
    post.NECESSITY = PostLogic.make_necessity_weak(post)
    print("verifying the Brouwerian S6 NECESSARILY operation...", end="")
    for p in truth:
        q = triple(*post.NECESSARILY(p))
        r = (Fraction(p[0],3), Fraction(p[1],2), Fraction(p[2],4))
        r0 = min(r)
        s0 = floor(r0*3)
        s = triple(s0, 0, 0)
        # print(f"{p=}, {q=}, r=({r[0]},{r[1]},{r[2]}), r0={r0}, {s0=}, {s=}")
        assert q == s, f"{p=}, □p={q} expected {s}"
    print("ok!")


    NOT = lambda x: post.NOT(x)
    ROT = lambda x: post.ROT(x)
    ROT2 = lambda x: post.ROT(x, 2)
    ROT3 = lambda x: post.ROT(x, 3)
    ROT4 = lambda x: post.ROT(x, 4)
    AND = lambda x, y: post.AND(x, y)
    OR = lambda x, y: post.OR(x, y)
    EQU = lambda x, y: post.EQU(x, y)

    always = triple(3, 2, 4)
    really = triple(3, 0, 0)
    never = triple(0, 0, 0)

    print("\tTop and bottom lattice elements")
    print("  A1) ⊦(p∧0)≡0\t", end="")
    claim = lambda x: EQU(AND(x, never), never)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("  A2) ⊦(p∧4)≡p\t", end="")
    claim = lambda x: EQU(AND(x, always), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("  A3) ⊦(p∨4)≡4\t", end="")
    claim = lambda x: EQU(OR(x, always), always)
    for p in truth:
        result = claim(p)
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("  A4) ⊦(p∨0)≡p\t", end="")
    claim = lambda x: EQU(OR(x, never), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("\tIdempotency")
    print("  B1) ⊦(p∧p)≡p\t", end="")
    claim = lambda x: EQU(AND(x, x), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("  B2) ⊦(p∨p)≡p\t", end="")
    claim = lambda x: EQU(OR(x, x), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("\tCommutativity")
    print("  C1) ⊦(p∧q)≡(q∧p)\t", end="")
    claim = lambda x, y: EQU(AND(x, y), AND(y, x))
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print("  C2) ⊦(p∨q)≡(q∨p)\t", end="")
    claim = lambda x, y: EQU(OR(x, y), OR(y, x))
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print("\tAssociativity [be patient!]")
    print("  D1) ⊦((p∧q)∧r)≡(p∧(q∧r))\t", end="")
    claim = lambda x, y, z: EQU(AND(AND(x, y), z), AND(x, AND(y, z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = triple(*claim(p, q, r))
                assert result == always, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")

    print("  D2) ⊦((p∨q)∨r)≡(p∨(q∨r))\t", end="")
    claim = lambda x, y, z: EQU(OR(OR(x, y), z), OR(x, OR(y, z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = triple(*claim(p, q, r))
                assert result == always, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")

    print("\tAbsorptivity")
    print("  E1) ⊦((p∧q)∨p)≡p\t", end="")
    claim = lambda x, y: EQU(OR(AND(x,y),x), x)
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  E2) ⊦((p∨q)∧p)≡p\t", end="")
    claim = lambda x, y: EQU(AND(OR(x,y),x), x)
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")

    print("\tDistributivity [be patient!]")
    print("  F1) ⊦((p∨q)∧r)≡((p∧r)∨(q∧r))\t", end="")
    claim = lambda x, y, z: EQU(AND(OR(x,y),z), OR(AND(x,z),AND(y,z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = triple(*claim(p, q, r))
                assert result == always, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")
    print("  F2) ⊦((p∧q)∨r)≡((p∨r)∧(q∨r))\t", end="")
    claim = lambda x, y, z: EQU(OR(AND(x,y),z), AND(OR(x,z),OR(y,z)))
    for p in truth:
        for q in truth:
            for r in truth:
                result = triple(*claim(p, q, r))
                assert result == always, f"failed: {p=}, {q=}, {r=}, {result=}"
    print("ok!")

    print("\tDeMorgan's Laws")
    print("  G1) ⊦(p∨q)≡~(~p∧~q)\t", end="")
    claim = lambda x, y: EQU(OR(x,y),NOT(AND(NOT(x),NOT(y))))
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  G2) ⊦(p∧q)≡~(~p∨~q)\t", end="")
    claim = lambda x, y: EQU(AND(x,y),NOT(OR(NOT(x),NOT(y))))
    for p in truth:
        for q in truth:
            result = triple(*claim(p, q))
            assert result == always, f"failed: {p=}, {q=}, {result=}"
    print("ok!")
    print("  G3) ⊦~~p≡p\t", end="")
    claim = lambda x: EQU(NOT(NOT(x)), x)
    for p in truth:
        result = triple(*claim(p))
        assert result == always, f"failed: {p=}, {result=}"
    print("ok!")

    print("multiple non-isomorphic worlds test completed successfully.")

def main(argv):
    """argument parser"""
    import argparse

    DESC = "Post Algebra implementation testing"
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("args", nargs="*", type=str, \
        help="the tests to be run (1, 2, 3 or all)." \
        + "  The value 'all' is equivalent to '1 2 3'.)" \
        + "  If no arguments are supplied, then '1' is assumed.")
    args = parser.parse_args(argv)
    print("Testing:", args.args)
    print("-"*72)
    if len(args.args) == 0:
        test1()
        print("-"*72)
        print("SUCCESS!")
        return
    for arg in args.args:
        if arg == "1":
            test1()
        elif arg == "2":
            test2()
        elif arg == "3":
            test3()
        elif arg[0].lower() == "a":
            test1()
            print("-"*72)
            test2()
            print("-"*72)
            test3()
        else:
            raise Argparse.NotImplementedError("unknown argument")
        print("-"*72)
        print("SUCCESS!")

if __name__ == "__main__":
        # TESTING
    import sys

    main(sys.argv[1:])
