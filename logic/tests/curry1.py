"""
logic.tests.curry1 - combinatory logic exercises in Rosenbloom
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Combinatory logic as laid out here was developed by Haskell Curry.
    (I am following the presentation as given in Rosenbloom [1].)

    The system, which we will call CL consists of a set of constants 𝕮,
    a binary operator "|" called either "the stroke" or application, and
    an equivalence relation "=" on 𝕮 called equality.  (The name 𝕮 for
    the set of constants is a bold script C (often called "Gothic", but
    that's a misnomer.  We use that font for the set of constants and
    reserve normal typeface letters for constants.)

    The axioms, as given in Rosenbloom fall into three groups:

                Rules of Formation
        R0. If a and be are in 𝕮, then |ab is a uniquely determined
            member of 𝕮.

                Definition of Equality
        E1. If a is in 𝕮, then a=a.
        E2. If a and b are in 𝕮 and a=b, then b=a.
        E3. For all a, b, and c are in 𝕮, if a=b and b=c, then a=c.
        E4. For all a, b, c, and d in 𝕮, if a=b and c=d, then |ac=|bd.
        E5. For all a and b in 𝕮, if |ac=|bc for every c in 𝕮, then
            a=b.

                Primitive Constants
        C0. A and K are in 𝕮.
        C1. If a, b, and c are in 𝕮, then |||Aabc = ||ac|bc.
        C2. If a and b are in 𝕮, then ||Kab = a.

    We can think of the stroke | as function application:

        |fx = f(x).

    The key difference here is that, if f(x) is undefined, we have a
    uniquely determined constant which represents some undefined value.
    There is no distinction being made here between constants which
    represent operators and those which represent operands,

    The constant K is a binary projection operator which discards its
    second argument:

        ||Kab = K(a,b) = a.

    Rosenbloom calls K the constancy operator.  (I prefer to think of it
    as a simple projection, so my name for it is the projector.)

    The constant A is a ternary operator which takes two unary functions
    and a value:
        ||Afgx = F(x, g(x)) = ||fx|gx.

BASIC DEFINED CONSTANTS

    The set of constants is denumerably infinite.  Here are some of the
    more interesting ones (see Rosenbloom [1, page 113].

        I = ||AKK.                               indentificator
            |Ia = |||AKKa
                = ||Ka|Ka               (C1)
                = a                     (C2)
        B = ||A|KAK                              compositor
            |Ba = |||A|KAKa
                = |||KAa|Ka             (C1)
                = |A|Ka                 (C2)
            |||Babc = |||A|Kabc         (Ba)
                    = |||Kac|bc         (C1)
                    = |a|bc             (C2)

            The B combinator represents function composition:
                |||Bfgx = |f|gx = f(g(x))

        W = ||AA|AK                               duplicator
            ||Wab = ||||AA|AKab
                  = |||Aa||AKab         (C1)
                  = ||ab|||AKab         (C1)
                  = ||ab||Kb|ab         (C1)
                  = ||abb               (C2)

            Think of a and b as functions...
                |||Wfgx = |||fggx = f(g(g(x)))

        D = |BB
            |||||BBabcd = |||B|abcd     (Babc)
                        = ||ab|cd       (Babc)

        C = ||A|DA|KK                              permutator
            |||||A|DA|KKabc
                = |||||DAa||KKabc       (C1)
                = |||Aa|||KKabc         (Dabcd)
                = ||ac||||KKabc         (C1)
                = ||ac||Kbc             (C2)
                = ||acb                 (C2)

        T = |CI
            |||CIab = ||Iba             (Cabc)
                    = |ba               (Ia)

OTHER RESULTS

    Reduction is useful but some proofs require E5.  For example:

    Prove: |BI = I
    Proof:
        Let a and b be arbitrary elements of 𝕮.
        Then:
            |||BIab = |I|ab = |ab.            by reduction
            |||BIab = |ab.                    by transitivity (E3)
        Also:
              ||Iab = |ab.                    by reduction
                |ab = ||Iab.                  by symmetry (E2)
        Thus:
            |||BIab = ||Iab.                  by transitivity (E3)
        Now b and a are both arbitrary, so:
              ||BIa = |Ia.                    by E5
                |BI = I.                      by E5
                            Q.E.D.

    Combinatory logic goes much deeper than this.  Rosenbloom shows that
    it is adequate for much of arithmetic.

REFERENCES

    [1] Paul Rosenbloom. Elements of Mathematical Logic. New York (Dover,
        1950).

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
from logic.curry import *

axioms = """AXIOMS

                Rules of Formation
        R0. If a and be are in 𝕮, then |ab is a uniquely determined
            member of 𝕮.

                Definition of Equality
        E1. If a is in 𝕮, then a=a.
        E2. If a and b are in 𝕮 and a=b, then b=a.
        E3. For all a, b, and c are in 𝕮, if a=b and b=c, then a=c.
        E4. For all a, b, c, and d in 𝕮, if a=b and c=d, then |ac=|bd.
        E5. For all a and b in 𝕮, if |ac=|bc for every c in 𝕮, then
            a=b.

                Primitive Constants
        C0. A and K are in 𝕮.
        C1. If a, b, and c are in 𝕮, then |||Aabc = ||ac|bc.
        C2. If a and b are in 𝕮, then ||Kab = a.

                    See: Rosenbloom 1950, page 112.
"""
print(axioms)

notes = """NOTES

    The computer-generated proofs are abbreviated.  We give each
    expression, but we don't write the equality symbols.  Most of the
    proofs follow one of two patterns -- reduction or parallel
    reduction.

    We use R0, C0 and E1 through E5 implicitly.  Many of the proofs are
    by reduction:

          ||||FOOabcd = ... = ||||BARabcd  by reduction rules

    The reductions are mainly axioms C1 and C2, and theorems T1 and T3
    though T7.  Axioms E1 through E5 are used implicitly in the reductions.

    To go from FOOabcd = BAabcd to FOO = BAR, we use the "for every c in 𝕮"
    part of E5 to remove the arbitrary variable on the right hand side of
    the stroke operation.  Note that to be arbitary, the variable on the
    right and side must be alone on the right side of the stroke and appear
    nowhere on the left side of the stroke.

          ||||FOOabcd = ||||BARabcd        by E3, repeated as needed
            |||FOOabc = BARabc             by E5, since d is arbitrary
              ||FOOab = BARab              by E5, since c is arbitrary
                |FOOa = BARa               by E5, since b is arbitrary

    Sometimes we use parallel reduction:

          ||||FOOabcd = ... = BAZ          by reduction rules
          ||||BAZabcd = ... = BAZ          by reduction rules

    To show that ||||FOOabcd = ||||BARabcd we use E2 and E3:

           |||BARabcd = BAZ                by E3, repeated as needed
                  BAZ = ||BARabcd          by E2
          ||||FOOabcd = ||||BARabcd        by E3, repeated as needed
                  FOO = BAR                by E5, repeated as before
"""
print()
print(notes)

references = """REFERENCES

    [1] Paul Rosenbloom. Elements of Mathematical Logic. New York (Dover,
    1950).
"""
print()
print(references)

print
print("Rosenbloom 1950, page 113.")

print()
print("D1. I = ||AKK.         (identificator)")
print("T1. |Ia = a.")
expr = "|||AKKa"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, rule_set=AK_reduction, maxlen=50)
assert str(tree) == 'a', str(tree)

print()
print("D2. B = ||A|KAK.       (compositor)")
print("T2. |Ba = |A|Ka.")
expr = "|||A|KAKa"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, rule_set=AK_reduction, maxlen=50)
assert str(tree) == '|A|Ka', str(tree)

print("T3. |||Babc = |a|bc.")
expr = "|||||A|KAKabc"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, rule_set=AK_reduction, maxlen=50) 
assert str(tree) == '|a|bc', str(tree)

print()
print("D3. W = ||AA|AK.       (duplicator)")
print("T4. |Wab = ||abb.")
expr = "||||AA|AKab"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, rule_set=AK_reduction, maxlen=50)
assert str(tree) == '||abb', str(tree)

print()
print("D4. D = |BB.")
print("T5. ||||Dabcd = ||ab|cd.")
expr = "|||||BBabcd"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '||ab|cd', str(tree)

print()
print("D5. C = ||A|DA|KK.     (permutator)")
print("T5. |||Cabc = ||acb.")
expr = "|||||A|DA|KKabc"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||acb', str(tree)

print()
print("D6. T = |CI.")
print("T5. ||Tab = |ba.")
expr = "|||CIab"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ba', str(tree)

print()
print("Rosenbloom 1950, page 114.")
print("  (*) The statements T8b, T9b, T11, and T13 can replace")
print("      the statement schema E5.")

print()
print("Lemma 8a. ||A|KaI = a.")
expr = "|||A|KaIb"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, rule_set=AKI_reduction, maxlen=50)
assert str(tree) == '|ab', str(tree)

print()
msg = "T8b. ||AB|KI = I."
print("Proof by parallel reduction:")
print(msg + " " * (70-len(msg)) + "(*)")
expr = "||||AB|KIab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "||Iab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=AKI_reduction, maxlen=50)
assert str(tree) == '|ab', str(tree)

print()
print("Proof using Lemma 8a:")
expr = "|||AB|KIa"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||BaI', str(tree)
print("     ||BaI = ||A|KaI      by T2")
print("           = a            by Lemma 8a")
print("           = |Ia          by T1")

print()
print("Lemma 9a. ||A||A|KKab = a.")
expr = "|||A||A|KKabc"
print(f"{0:3}: {expr}")
tree = Reducer.on(expr, rule_set=AK_reduction, maxlen=50)
assert str(tree) == '|ac', str(tree)

print()
msg = "T9b. ||BA|BK = K."
print("Proof by parallel reduction:")
print(msg + " " * (70-len(msg)) + "(*)")
expr = "|||||BA|BKabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ac', str(tree)
expr = "|||Kabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=AKI_reduction, maxlen=50)
assert str(tree) == '|ac', str(tree)

print()
print("Proof using Lemma 9a:")
expr = "||||BA|BKab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||A||BKab', str(tree)
print("     ||A||BKab = |||A||A|KKab      by T2")
print("               = a                 by Lemma 9a")
print("               = ||Kab             by Axiom C2")

print()
print("Lemma 10. ||A|Ka|Kb = |K|ab.")
expr = "|||A|Ka|Kbc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=AK_reduction, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "||K|abc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=AK_reduction, maxlen=50)
assert str(tree) == '|ab', str(tree)

print()
msg = "T11. ||A|DB|KK = ||B|BKI."
print(msg + " " * (70-len(msg)) + "(*)")
print("Proof by parallel reduction:")
expr = "|||||A|DB|KKabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "|||||B|BKIabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)

print()
print("Proof using Lemma 10:")
expr = "||||A|DB|KKab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||Ba|Kb', str(tree)
print("     ||Ba|Kb = ||A|Ka|Kb         by T2")
print("             = |K|ab             by Lemma 10")
print("     ... But:")
expr = "||||B|BKIab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|K|ab', str(tree)

print()
print("Lemma 12. ||A||Aac||Abc = ||A||A||BAabc.")
expr = "|||A||Aac||Abcd"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=AK_reduction, maxlen=50)
assert str(tree) == '|||ad|cd||bd|cd', str(tree)
expr = "|||A||A||BAabcd"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|||ad|cd||bd|cd', str(tree)

print()
msg = "T13. ||A|D||BA||B|BAA|KA = ||B|BA||WI|BA."
print(msg + " " * (70-len(msg)) + "(*)")
print("Proof using Lemma 11:")
expr = "|||||A|D||BA||B|BAA|KAabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||A||Aac||Abc', str(tree)
print(f"     {str(tree)} is the LHS of Lemma 11.  But...")
expr = "|||||B|BA||WI|BAabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
print(f"     {str(tree)} is the RHS of Lemma 11.  Q.E.D.")

print()
print("Note 1) in Rosenbloom 1950, page 114, T13...")
print("        The last expression has a typo (missing stroke).")

print()
print("Proof from scratch:")
expr = "||||||A|D||BA||B|BAA|KAabcd"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|||ad|cd||bd|cd', str(tree)
expr = "||||||B|BA||WI|BAabcd"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|||ad|cd||bd|cd', str(tree)

print()
print("Note 2) The default for the maximum number of reductions")
print("        in logic.curry.Reducer.on() is 10.  So just squeaked")
print("        by in reducing the LHS.  (You can increase or")
print("        this limit by setting ``max_steps''.")

print()
print("Rosenbloom 1950, pages 115-116.")
print("  Here throughout we replace |BB with D.")

print()
print("T14,T19. |BI = I = ||CBI.")
expr = "|||BIab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "||Iab"
print(f"MHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "||||CBIab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)

print()
print("Note: We can also combine this with T8b:")
print("          ||CBI = |BI = ||AB|KI = I.")
print("      Also see T23 and T29.")

print()
print("T15. ||C|D|DBB = ||BDB.")
expr = "||||||C|D|DBBabcd"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a|b|cd', str(tree)
expr = "||||||BDBabcd"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a|b|cd', str(tree)

print()
print("T16. ||C|D|DBC = ||B|BC|DB.")
expr = "||||||C|D|DBCabcd"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a||bdc', str(tree)
expr = "||||||B|BC|DBabcd"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a||bdc', str(tree)

print()
print("T17. ||C|DBW = ||B|BW|DB.")
expr = "|||||C|DBWabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a||bcc', str(tree)
expr = "|||||B|BW|DBabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a||bcc', str(tree)

print()
print("T18. ||C|DBK = ||B|BKI.")
expr = "|||||C|DBKabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "|||||B|BKIabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)

print()
print("T19. CBI = I.  (See T14 above.)")

print()
print("T20. ||B||B|BCCD = |DC.")
expr = "||||||B||B|BCCDabcd"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||ad|bc', str(tree)
expr = "|||||DCabcd"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||ad|bc', str(tree)

print()
print("Note 3) in Rosenbloom 1950, page 116, T21...")
print("        There are errors in the LHS of the expression, and")
print("        in the sketch of the proof.  I am assuming that the")
print("        RHS (i.e. ||BBW, here as |DW) is correct.")
print("           The corrected LHS is a correction I wrote down in")
print("        my copy of Elememts of Mathematical Logic sometime in the")
print("        1970s.  The reduction of the RHS is easy, so I am sure")
print("        that I worked out the correct reduced form.  But working")
print("        out the correct form of the LHS is not trivial -- did I")
print("        find it in some Errata, or did I derive it myself from")
print("        the lambda expressions?")

print()
print("T21. ||B||B||B|BWW|BC|DD = |DW.")
expr = "|||||B||B||B|BWW|BC|DDabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||a|bc|bc', str(tree)
expr = "||||DWabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '||a|bc|bc', str(tree)

print()
print("T22. |DK = ||BKK.")
expr = "||||DKabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == 'a', str(tree)
expr = "|||||BKKabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == 'a', str(tree)

print()
print("T23. ||BCC = I.")
expr = "|||||BCCabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '||abc', str(tree)
expr = "|||Iabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=AKI_reduction, maxlen=50)
assert str(tree) == '||abc', str(tree)

print()
print("T24. ||B||B|BCC|BC = ||B||BC|BCC.")
expr = "||||||B||B|BCC|BCabcd"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|||adcb', str(tree)
expr = "||||||B||BC|BCCabcd"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|||adcb', str(tree)

print()
print("T25. ||B||B|BWC|BC = ||BCW.")
expr = "|||||B||B|BWC|BCabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|||accb', str(tree)
expr = "|||||BCWabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|||accb', str(tree)

print()
print("T26. ||BCK = |BK.")
expr = "|||||BCKabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "||||BKabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|ab', str(tree)

print()
print("T27. ||BWC = W.")
expr = "||||BWCab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '||abb', str(tree)
expr = "||Wab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '||abb', str(tree)

print()
print("T28. ||BW|BW = ||BWW.")
expr = "||||BW|BWab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|||abbb', str(tree)
expr = "||||BWWab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|||abbb', str(tree)

print()
print("T29. ||BWK = I.")
expr = "||||BWKab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, rule_set=BCWK_reduction, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "||Iab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, rule_set=AKI_reduction, maxlen=50)
assert str(tree) == '|ab', str(tree)

print("SUCCESS!")
