"""
logic.godel_dummett - many-valued Gödel-Dummett logic
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    In a basic Gödel-Dummett algebra, we have a closed range of numbers in the
    interval [0,1].  In the finite finite case, with n+1 values, these will
    be the rational numbers 0, 1/n, 2/n, ..., (n-1)/n, 1.  Material implication
    is defined as follows:

               ┏
               ┃  1 if p≥q
        p⊃q = ━┫                            material implication
               ┃  |q| if q<p
               ┗

    Negation (or impossibility) is defined as:

                    ┏
                    ┃  1 if p≥q
        ~p = p⊃0 = ━┫                      logical negation
                    ┃  |q| if q<p
                    ┗

    Disjunction and conjunction are defined in the usual manner:

        p∨q = (p⊃q)⊃q                       disjunction (logical addition)
        p∧q = ~(~p∨~q)                      conjunction (logical multiplication)

    In the two-valued case, these reduce to the corresponding Boolean operators.

    Gödel-Dummett logics (or Gödel logics or Dummett logics) are interesting
    in part because they interpolate between classical propositional calculus
    and the intuitionistic propositional calculus.

    The infinite Gödel-Dummett algebra can be axiomatized by adding as an
    axiom the following wff to a set of axioms for the intuitionistic
    propositional calculus:

        (p⊃q)∨(q⊃p)

    Note that DeMorgan's laws do not hold in the Gödel-Dummett logics unless
    the only truth values are 0 and 1.

    By vectoring these values, we can create a multiple worlds scenarion which
    generalizes Boolean multiple worlds.

IMPLEMENTATION

    In our implementation, we derive the logic class GodelLogic from class
    LukasiewiczLogic by redefining negation and material implication.

    We also redefine the Lewis possibility operator as a primitive. 

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

class GodelLogic(LukasiewiczLogic):
    """Gödel-Dummett many worlds logic"""

    def NOT(self, p:tuple) -> tuple:
        """logical negation"""
        neg = lambda x: 1 if x == 0 else 0
        return tuple(neg(p[i]) for i in range(self.worlds))

    def IMP(self, p:tuple, q:tuple) -> tuple:
        """material implication"""
        imp = lambda x, y: 1 if x <= y else y
        return tuple(imp(p[i], q[i]) for i in range(self.worlds))

    def POSSIBLY1(self, p:tuple) -> tuple:
        """necessity (weak)

        Returns the maximum truth level in this world.  In other words,
        the level of truth in the real world for ◇p is the maximum level
        of truth for p in all worlds.  In the other worlds, ◇p is false.

        This can be used with modality STRUE to suppress intermediate
        truth levels.
        """
        level = max(p)
        return tuple([level] + [1]*(len(p)-1))

    def POSSIBLY2(self, p:tuple) -> tuple:
        """necessity (strong)

        Returns the maximum truth level into all worlds.  In other words,
        the level of truth in all worlds for ◇p is the maximum level
        of truth for p in all worlds.

        This can be used with modality STRUE to suppress intermediate
        truth levels.
        """
        level = max(p)
        return tuple([level]*len(p))

    def POSSIBLY(self, p:int) -> int:
        """possibility"""
        if self._necessity == 1:
            return self.POSSIBLY1(p)
        return self.POSSIBLY2(p)

if __name__ == "__main__":
    from fractions import Fraction
    from logic.lukasiewicz import pack_levels
    from logic.lukasiewicz import test_unary
    from logic.lukasiewicz import test_binary

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

    print("Testing Godel 3-logic in a two-world universe")
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
    w2 = GodelLogic(3,2)     # two possible worlds

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
    exp = [(T,T), (F,T), (F,T),
           (T,F), (F,F), (F,F),
           (T,F), (F,F), (F,F)]
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
    exp = [[TT, FT, FT,  TF, FF, FF,  TF, FF, FF], # FF
           [TT, TT, IT,  TF, TF, IF,  TF, TF, IF], # IF
           [TT, TT, TT,  TF, TF, TF,  TF, TF, TF], # TF
        # -------------------------------------------------
           [TT, FT, FT,  TT, FT, FT,  TI, FI, FI], # FI
           [TT, TT, IT,  TT, TT, IT,  TI, TI, II], # II
           [TT, TT, TT,  TT, TT, TT,  TI, TI, TI], # TI
        # -------------------------------------------------
           [TT, FT, FT,  TT, FT, FT,  TT, FT, FT], # FT
           [TT, TT, IT,  TT, TT, IT,  TT, TT, IT], # IT
           [TT, TT, TT,  TT, TT, TT,  TT, TT, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.IMP, values, exp)

    print("EQU(p,q):   (material equivalence)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[TT, FT, FT,  TF, FF, FF,  TF, FF, FF], # FF
           [FT, TT, IT,  FF, TF, IF,  FF, TF, IF], # IF
           [FT, IT, TT,  FF, IF, TF,  FF, IF, TF], # TF
        # -------------------------------------------------
           [TF, FF, FF,  TT, FT, FT,  TI, FI, FI], # FI
           [FF, TF, IF,  FT, TT, IT,  FI, TI, II], # II
           [FF, IF, TF,  FT, IT, TT,  FI, II, TI], # TI
        # -------------------------------------------------
           [TF, FF, FF,  TI, FI, FI,  TT, FT, FT], # FT
           [FF, TF, IF,  FI, TI, II,  FT, TT, IT], # IT
           [FF, IF, TF,  FI, II, TI,  FT, IT, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.EQU, values, exp)
    print("NEQ(p,q):   (not remotely equivalent)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[FF, TF, TF,  FT, TT, TT,  FT, TT, TT], # FF
           [TF, FF, FF,  TT, FT, FT,  TT, FT, FT], # IF
           [TF, FF, FF,  TT, FT, FT,  TT, FT, FT], # TF
        # -------------------------------------------------
           [FT, TT, TT,  FF, TF, TF,  FF, TF, TF], # FI
           [TT, FT, FT,  TF, FF, FF,  TF, FF, FF], # II
           [TT, FT, FT,  TF, FF, FF,  TF, FF, FF], # TI
        # -------------------------------------------------
           [FT, TT, TT,  FF, TF, TF,  FF, TF, TF], # FT
           [TT, FT, FT,  TF, FF, FF,  TF, FF, FF], # IT
           [TT, FT, FT,  TF, FF, FF,  TF, FF, FF]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.NEQ, values, exp)

    print("XOR(p,q):   (exclusive disjunction)")
#    foo = GodelLogic()
#    foobar = {'F':(0,), 'I':(Fraction(1,2),), 'T':(1,)}
#    barfoo = {(0,):'F', (Fraction(1,2),):'I', (1,):'T'}
#    print('   F  I  T')
#    for xxx in ['F', 'I', 'T']:
#        line = str(xxx)
#        for yyy in ['F', 'I', 'T']:
#            zzz = barfoo[foo.XOR(foobar[xxx], foobar[yyy])]
#            line += "  " + zzz
#        print(line)
#         F  I  T
#      F  F  I  T
#      I  I  F  F
#      T  T  F  F
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[FF, IF, TF,  FI, II, TI,  FT, IT, TT], # FF
           [IF, FF, FF,  II, FI, FI,  IT, FT, FT], # IF
           [TF, FF, FF,  TI, FI, FI,  TT, FT, FT], # TF
        # -------------------------------------------------
           [FI, II, TI,  FF, IF, TF,  FF, IF, TF], # FI
           [II, FI, FI,  IF, FF, FF,  IF, FF, FF], # II
           [TI, FI, FI,  TF, FF, FF,  TF, FF, FF], # TI
        # -------------------------------------------------
           [FT, IT, TT,  FF, IF, TF,  FF, IF, TF], # FT
           [IT, FT, FT,  IF, FF, FF,  IF, FF, FF], # IT
           [TT, FT, FT,  TF, FF, FF,  TF, FF, FF]] # TT
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
    exp = [[TF, FF, FF,  FF, FF, FF,  FF, FF, FF], # FF
           [TF, TF, IF,  FF, FF, FF,  FF, FF, FF], # IF
           [TF, TF, TF,  FF, FF, FF,  FF, FF, FF], # TF
        # -------------------------------------------------
           [TF, FF, FF,  TF, FF, FF,  IF, FF, FF], # FI
           [TF, TF, IF,  TF, TF, IF,  IF, IF, IF], # II
           [TF, TF, TF,  TF, TF, TF,  IF, IF, IF], # TI
        # -------------------------------------------------
           [TF, FF, FF,  TF, FF, FF,  TF, FF, FF], # FT
           [TF, TF, IF,  TF, TF, IF,  TF, TF, IF], # IT
           [TF, TF, TF,  TF, TF, TF,  TF, TF, TF]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.SIMP, values, exp)

    print("SEQU(p,q):  (strict equivalence)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[TF, FF, FF,  FF, FF, FF,  FF, FF, FF], # FF
           [FF, TF, IF,  FF, FF, FF,  FF, FF, FF], # IF
           [FF, IF, TF,  FF, FF, FF,  FF, FF, FF], # TF
        # -------------------------------------------------
           [FF, FF, FF,  TF, FF, FF,  IF, FF, FF], # FI
           [FF, FF, FF,  FF, TF, IF,  FF, IF, IF], # II
           [FF, FF, FF,  FF, IF, TF,  FF, IF, IF], # TI
        # -------------------------------------------------
           [FF, FF, FF,  IF, FF, FF,  TF, FF, FF], # FT
           [FF, FF, FF,  FF, IF, IF,  FF, TF, IF], # IT
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
    exp = [[TT, FF, FF,  FF, FF, FF,  FF, FF, FF], # FF
           [TT, TT, II,  FF, FF, FF,  FF, FF, FF], # IF
           [TT, TT, TT,  FF, FF, FF,  FF, FF, FF], # TF
        # -------------------------------------------------
           [TT, FF, FF,  TT, FF, FF,  II, FF, FF], # FI
           [TT, TT, II,  TT, TT, II,  II, II, II], # II
           [TT, TT, TT,  TT, TT, TT,  II, II, II], # TI
        # -------------------------------------------------
           [TT, FF, FF,  TT, FF, FF,  TT, FF, FF], # FT
           [TT, TT, II,  TT, TT, II,  TT, TT, II], # IT
           [TT, TT, TT,  TT, TT, TT,  TT, TT, TT]] # TT
        # -------------------------------------------------
    test_binary(w2, w2.SIMP, values, exp)

    print("SEQU(p,q):  (strict equivalence)")
    #       FF  IF  TF   FI  II  TI   FT  IT  TT  
    exp = [[TT, FF, FF,  FF, FF, FF,  FF, FF, FF], # FF
           [FF, TT, II,  FF, FF, FF,  FF, FF, FF], # IF
           [FF, II, TT,  FF, FF, FF,  FF, FF, FF], # TF
        # -------------------------------------------------
           [FF, FF, FF,  TT, FF, FF,  II, FF, FF], # FI
           [FF, FF, FF,  FF, TT, II,  FF, II, II], # II
           [FF, FF, FF,  FF, II, TT,  FF, II, II], # TI
        # -------------------------------------------------
           [FF, FF, FF,  II, FF, FF,  TT, FF, FF], # FT
           [FF, FF, FF,  FF, II, II,  FF, TT, II], # IT
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
