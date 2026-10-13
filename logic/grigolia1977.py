"""
logic.grigolia1977 - axioms for finitely many-valued Łukasiewicz logic
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

BACKGROUND

    In a basic Łukasiewicz algebra, we have a closed range of numbers in
    the interval [0,1].  In the finite finite case, with n+1 values, these
    will be the rational numbers 0, 1/n, 2/n, ..., (n-1)/n, 1.  Material
    implication is defined as follows:

        p⊃q = min(1, 1-p+q)                 material implication

    The remaining logical connectives can be defined using material
    implication and the constant 0:

        ~p := p⊃0 = 1-p                    D1 logical negation
        p∨q := (p⊃q)⊃q                     D2 disjunction
        p∧q := ~(~p∨~q)                    D3 conjunction

    In the two-valued case, these reduce to the corresponding Boolean
    operators.

    In a 1930 paper, Łukasiewicz and Tarski conjectured that, along with
    modus ponens, the following axiom schemas are characterize the
    infinite-valued logic: (see [1], page 40)

        p⊃(q⊃p)                            A1 tautology
        (p⊃q)⊃((q⊃r)⊃(p⊃r))                A2 hypothetical syllogism
        (p∨q)⊃(q∨p)                        A3 commutativity
        (~q⊃~p)⊃(p⊃q)                      A4 contraposition
        ((p⊃q)⊃(q⊃p))⊃(q⊃p)                A5

    The conjecture was confirmed by Wajsberg in 1931, but apparently
    not published.  Rose and Rosser published a proof in 1958. (ibid.)

GRIGOLIA'S AXIOMS FOR Ł₃

    Several axiomatizations of the finitely many-valued systems have
    been published.  Mentioned [1] on page 40 is a 1977 axiomatization
    by R Grigolia.

    For additional definitions are used.  The first two are different
    generalizations of disjunction and conjunction:

        p+q := ~p⊃q                        D4 join2
        p•q := ~(p⊃~q)                     D5 meet2

    (I refer to them as join2 and meet2 to distinguish then from
    disjunction [or join] and conjunction [or meet] which are mathematical
    maximum and minimum operations.)

    Note that p+q and p•q are commutative and related by DeMorgan's Laws.

    From these two, we have repetition and exponentiation:

        kp := p + p + ... + p              D6 repetition
            1p := p
            (k+1)p := kp + p
        pᵏ := p • p • ... • p              D7 exponentiation
            p¹ := p
            pᵏ⁺¹ := pᵏ • p

    (We can define 0p = ~(p⊃p) = 0 and p⁰ = (p⊃p) = 1.)

    For the three-valued logic Ł₃, letting F=0, I=1/2 and T=1, we have
    the following tables:

                q               q               q
        p⊃q | F I T     p∨q | F I T     p∧q | F I T
        ----+-------    ----+-------    ----+-------
          F | T T T       F | F I T       F | F F F
        p I | I T T     p I | I I T     q I | F I I
          T | F I T       T | T T T       T | F I T

                        p+q | F I T     p•q | F I T
                        ----+-------    ----+-------
                          F | F I T       F | F F F
                        p I | I T T     p I | F F I
                          T | T T T       T | F I T

    Note that p∨q and p+q only differ when p=q=I.  The same holds for
    p∧q and p•q.

    We then add a set of axioms to obtain Łₙ.  The first deals with join2:

        np ⊃ (n-1)p                        A6

    Note that this will imply:

        np ≡ (n-1)p

    For Ł₃, we have the axiom:

        3p ⊃ 2p                            A6(Ł₃)

    Here is a table for "multiples" of p:

        p 0p 1p 2p 3p
        --------------       Note that 2p≡3p is a theorem in Ł₃.
        F  F  F  F  F
        I  F  I  T  T
        T  F  T  T  T

    Then, for each j such that 1<j<n-1 and j does not divide n-1, we add
    the following schema:

        (n-1)((~p)ʲ + (p•(j-1)p))         A7(j)

    For Ł₃, n=3, n-1=2, so there are no values of j that require axioms.

    Also note that 2p=F if and only if p=F and otherwise T, so 2p is
    Tarski's possibility operator for Ł₃

    Let's look at the exponents (even though we don't get any axioms
    using them:

        p p⁰ p¹ p²
        -----------
        F T  F  F
        I T  I  F
        T T  T  T

    Note that p²=T if and only if p=T and otherwise F, so p² is Tarski's
    necessity operator for Ł₃

GRIGOLIA'S AXIOMS FOR Ł₄

    Letting F=0, I=1/3, J=2/3 and T=1, here are the relevant tables for
    Ł₄:

                 q                 q                 q
        p⊃q | F I J T     p∨q | F I J T     p∧q | F I J T
        ----+---------    ----+---------    ----+---------
          F | T T T T       F | F I J T       F | F F F F
        p I | J T T T     p I | I I J T     q I | F I I I
          J | I J T T       J | J J J T       J | F I J J
          T | F I J T       T | T T T T       T | F I J T

                          p+q | F I J T     p•q | F I J T
                          ----+---------    ----+---------
                            F | F I J T       F | F F F F
                          p I | I J T T     p I | F F F I
                            J | J T T T       J | F F I J
                            T | T T T T       T | F I J T

        p 0p 1p 2p 3p 4p
        -----------------
        F  F  F  F  F  F
        I  F  I  J  T  T
        J  F  J  T  T  T
        T  F  T  T  T  T

    Axiom 6 clearly holds:

        4p ⊃ 3p                            A6(Ł₄)

    Of course we also have 4p≡3p. 3p is the Tarski possibility operator
    for Ł₄

    Look at values of j between 1 and n-1=3:

        2 does not divide n-1=3.

    Thus the schema A7 reduces to this schema
    
        3((~p)² + (p•1p))                  A7(Ł₄, 2)

    1p is just p and (p•p) is just p², so we can write this as follows:

        3((~p)² + p²)                      A7'(Ł₄, 2)

    Here is a table for the exponents:

        p p⁰ p¹ p² p³
        --------------
        F T  F  F  F
        I T  I  F  F
        J T  J  I  F
        T T  T  T  T

    p³ is the Tarski necessity operator for Ł₄.  Here is a table for A7:

        p=1p ~p p² (~p)² (~p)²+p²  3((~p)²+p²)
         F    T F    T       T          T
         I    J F    I       I          T
         J    I I    F       I          T
         T    F T    F       T          T

POLISH NOTATION

    The Polish notation decoder needs to be able to understand the
    additional operators.  The classical operators are:

        proposition letters         p, q, r, ...
        negation                    ~X                NX
        material implication        (X⊃Y)             CXY
        disjunction                 (X∨Y)             Axy
        conjunction                 (X∧Y)             Kxy
        material equivalence        (X≡Y)             Exy

    We treat the proposition letters as schemas to avoid writing down
    a complicated substitution rule.

    The Lewis-like many-worlds extensions are as follows:

        necessity                    □X               MX
        possibility                  ◇X               PX
        strict implication           (X⥽Y)            IXY
        strict equivalence           (X=Y)            =XY

    The additional binary operators are:

        join2                        (X+Y)            +XY
        meet2                        (X•Y)            .XY

    The repeated forms use:
        joins     _(decimal)_X, e.g. "_123_X" for 123X
        meets     ^(decimal)^X, e.g. "^123^X" for X¹²³

    To mark a definitions, we use ":" .  We treat this the same as
    material equivalence.  Prefix form ":XY" in infix form is:
        X := Y

REFERENCE

    [1] Grzegorz Malinowski.  Many-valued Logics.  Clarendon Press (Oxford,
        1993)

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
from logic.lukasiewicz import LukasiewiczLogic
from logic.wff import WFF, Constant, Variable, UnaryOperator, BinaryOperator
from logic.deductions import Rule

class GrigoliaExtensions(LukasiewiczLogic):
    """extended operator set

    The extensions can all be defined using negation and material
    implication.
    """

    def JOIN2(self, p:tuple, q:tuple) -> tuple:
        """a disjunction-like operator

        (p+q) := (~p⊃q)
        """
        return self.IMP(self.NOT(p), q)

    def MEET2(self, p:tuple, q:tuple) -> tuple:
        """a conjunction-like operator

        (p•q) := ~(p⊃~q)
        """
        r = self.IMP(p, self.NOT(q))
        return self.NOT(r)

    def coefficient(self, j:str, p:tuple):
        """repeated join2 operations"""
        j = int(j)
        assert j>=0
        if j == 0:
            return self.F
        if j == 1:
            return p
        if j >= self.denominator:
            return self.WTRUE(p)        # Tarski's possibility
        result = list()
        for i in range(self.worlds):
            if p[i] == 0:
                result.append(0)
                continue
            q = p[i] * j
            result.append(min(q,1))
        return tuple(result)

    def exponent(self, j:str, p:tuple):
        """repeated meet2 operations"""
        q = self.NOT(p)
        return self.NOT(self.coefficient(j, q))

WFFx = "GWFF"

class CoefficientOperator(UnaryOperator):
    """Handles operators involving coefficients"""

    __slots__ = ("__fmt", "__op", "__j", "__arg", "__owner", "__prefixed")

    def __init__(self, fmt:str, op:callable, j:int, arg:WFFx, owner,
                 prefixed:bool):
        """constructor"""
        j = int(j)
        self.__fmt = fmt
        self.__op = op
        self.__j = j
        self.__arg = arg
        self.__owner = owner
        self.__prefixed = prefixed

    @property
    def fmt(self) -> str:
        """name getter"""
        return self.__fmt

    @property
    def value(self) -> "TruthValue":
        """value getter"""
        value = self.__op(self.__j, self.__arg.value)
        self.__owner.defined(value, var=str(self))
        return value

    def __str__(self):
        """string value for printing a wff"""
        if self.__prefixed:
            return self.__fmt % (self.__j, self.__arg)
        return self.__fmt % (self.__arg, self.__j)

    @property
    def j(self):
        """return the first argument"""
        return self.__j

    @property
    def arg(self):
        """return the second argument"""
        return self.__arg

class GWFF(WFF):
    """well-formed formulas for the Grigolia extensions

    Note that these extensions are just abbreviations for more
    complicated existing operators.
    """
    
    def JOIN2(self, expr1, expr2) -> WFFx:
        """the plus operator"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('+', self.owner.JOIN2, expr1, expr2, self.owner)

    def MEET2(self, expr1, expr2) -> WFFx:
        """the plus operator"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('•', self.owner.MEET2, expr1, expr2, self.owner)

    def coefficient(self, j:int, expr) -> WFFx:
        """the coefficient operator"""
        if not isinstance(expr, self.EXPRS):
            raise TypeError("Invalid WFF")
        fmt = "(%d%s)"
        return CoefficientOperator(fmt, self.owner.coefficient, j, expr,
                                   self.owner, True)

    def exponent(self, j:int, expr) -> WFFx:
        """the exponent operator"""
        if not isinstance(expr, self.EXPRS):
            raise TypeError("Invalid WFF")
        if isinstance(expr, (Variable, BinaryOperator)):
            fmt = "(%s^%d)"
        else:
            fmt = "((%s)^%d)"
        return CoefficientOperator(fmt, self.owner.exponent, j, expr,
                                   self.owner, False)

#    def _validate_type(self, expr:WFFx):
#        """validate the type of an expression"""
#        if isinstance(expr, CoefficientOperator):
#            return
#        super()._validate_type(expr)

    def extract_top(self, top, stack):
        """process the top of stack for extract_vars"""
        if type(top) == CoefficientOperator:
            stack.append(top.arg)
            return
        super().extract_top(top, stack)

if __name__ == "__main__":
    """check the operators"""
    from fractions import Fraction
    g = GrigoliaExtensions(m=4)
    F = 0
    I = Fraction(1,3)
    J = Fraction(2,3)
    T = 1
    ps = [(F,), (I,), (J,), (T,)]
    qs = [(F,), (I,), (J,), (T,)]
    v = {(F,):'F', (I,):'I', (J,):'J', (T,):'T'}

    print("---------- DISJUNCTION ----------")
    s = "p∨q |"
    for q in qs:
        s += f" {v[q]}"
    s += "     "
    s += "p+q |"
    for q in qs:
        s += f" {v[q]}"
    print(s)
    print("----+" + "-" * 9 + "    " + "----+" + "-" * 9)
    for p in ps:
        s = f"  {v[p]} |"
        for q in qs:
            s += f" {v[g.OR(p,q)]}"
        s += "     "
        s += f"  {v[p]} |"
        for q in qs:
            s += f" {v[g.JOIN2(p,q)]}"
        print(s)
    print()


    print("---------- CONJUNCTION ----------")
    s = "p∧q |"
    for q in qs:
        s += f" {v[q]}"
    s += "     "
    s += "p•q |"
    for q in qs:
        s += f" {v[q]}"
    print(s)
    print("----+" + "-" * 9 + "    " + "----+" + "-" * 9)
    for p in ps:
        s = f"  {v[p]} |"
        for q in qs:
            s += f" {v[g.AND(p,q)]}"
        s += "     "
        s += f"  {v[p]} |"
        for q in qs:
            s += f" {v[g.MEET2(p,q)]}"
        print(s)
    print()

    print("Check that + is true in the lower triangle.")
    print("  The strict upper triangle should never be true...")
    print()
    print("Check that • is false in the upper triangle.")
    print("  The strict lower triangle should never be false...")
    print()

    print("---- COEFFICIENTS ----")
    s = "p"
    for j in range(10):
        s += f" {j}"
    print(s)
    print("-" * 22)
    for p in ps:
        s = f"{v[p]}"
        for j in range(10):
            q = g.coefficient(j, p)
            s += f" {v[q]}"
        print(s)
    print()

    print("----- EXPONENTS ------")
    s = "p"
    for j in range(10):
        s += f" {j}"
    print(s)
    print("-" * 22)
    for p in ps:
        s = f"{v[p]}"
        for j in range(10):
            q = g.exponent(j, p)
            s += f" {v[q]}"
        print(s)
    print()

    def vars(wff):
        """list the variables"""
        x = list(str(t) for t in wff.vars)
        y = ", ".join(x)
        return y

    print("Begin verification...")

    print("Checking + and •...")
    for p in ps:
        for q in qs:
            r = g.JOIN2(p, q)
            s = g.MEET2(p, q)
            x, y = min(p[0], q[0]), max(p[0], q[0])
            msg = f"+{v[p]}{v[q]} = {v[r]}"
            if x+y >= 1:
                assert r[0] == T, msg
            else:
                assert r[0] == x+y, msg
            msg = f"•{v[p]}{v[q]} = {v[s]}"
            if x+y <= 1:
                assert s[0] == F, msg
            else:
                assert s[0] == x+y-1, msg
            
    print("Checking coefficients...")
    for p in ps:
        for j in range(10):
            q = g.coefficient(j, p)
            msg = f"{j}{v[p]} = {v[q]}"
            if j == 0:
                assert q[0] == F, msg
            elif j!=1 and p[0]==0:
                assert q[0] == F, msg
            else:
                r = (min(1, p[0] + Fraction(j-1, 3)),)
                assert q == r, msg

    print("Checking exponents...")
    for p in ps:
        for j in range(10):
            q = g.exponent(j, p)
            msg = f"{v[p]}^{j} = {v[q]}"
            if j == 0:
                assert q[0] == T, msg
            elif j!=1 and p[0]==T:
                assert q[0] == T, msg
            else:
                r = (max(0, p[0] - Fraction(j-1, 3)),)
                assert q == r, msg

    print("Checking Axiom 6...")
    P = Variable("p", owner=g)
    fourP = GWFF(g)
    fourP.wff = fourP.coefficient(4, P)
    print("\t4p =", fourP.strip, "\t\tvariables =", vars(fourP))
    threeP = GWFF(g)
    threeP.wff = threeP.coefficient(3, P)
    print("\t3p =", threeP.strip, "\t\tvariables =", vars(threeP))
    ax6 = GWFF(g)
    ax6.wff = ax6.IMP(fourP.wff, threeP.wff)
    print("\t4p⊃3p =", ax6.strip, "\tvariables =", vars(ax6))
    for p in ps:
        P.value = p
        q = ax6.value
        print(f"\t    {str(P)} = {v[p]} ⮕ {str(ax6.strip)} = {v[q]}")
        assert q == (T,)
    print()

    print("Checking Axiom 7...")
    notP = UnaryOperator("~", g.NOT, P, g)
    notPsq = CoefficientOperator("((%s)^%d)", g.exponent, 2, notP,
                                 g, False)      # suffixed!
    Psq = CoefficientOperator("(%s^%d)", g.exponent, 2, P,
                              g, False)         # suffixed!
    sumsq = BinaryOperator("+", g.JOIN2, notPsq, Psq, g)
    threeTimes = GWFF(g)
    threeTimes.wff = threeTimes.coefficient(3, sumsq)
    for p in ps:
        P.value = p
        q = sumsq.value
        r = threeTimes.value
        print(f"\t    {str(P)} = {v[p]} ⮕ {str(sumsq)} = {v[q]}",
              f"⮕ {threeTimes.strip} = {v[r]}")
        assert r == (T,)
    
    
#        3((~p)² + p²)                      A7'(Ł₄, 2)

    print("Verification complete!")
    print("SUCCESS!")
