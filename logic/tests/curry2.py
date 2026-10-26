"""
logic.tests.curry2 - combinatory logic arithmetic exercises in Rosenbloom
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Combinatory logic as laid out here was developed by Haskell Curry.
    (I am following the presentation as given in Rosenbloom [1].)

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

    Rosenbloom defines several elements of 𝕮 and denonstrates that each
    of these elements is a associated with a reduction rule similar
    to Axioms C1 and C2:

              Definition                Reduction rule
        D1. I = ||AKK.               T1.       |Ia = a.
        D2. B = ||A|KAK.             T3.   |||Babc = |a|bc.
        D3. W = ||AA|AK.             T4.     ||Wab = ||abb.
        D4. D = |BB.                 T5. ||||Dabcd = ||ab|cd.
        D5. C = ||A|DA|KK.           T6.   |||Cabc = ||acb.
        D6. T = |CI.                 T7.     ||Tab = |ba.

    Axiom schema E5 can be replaced by the following four theorems:

        T8b. ||AB|KI = I.
        T9b. ||BA|BK = K.
        T11. ||A|DB|KK = ||B|BKI.
        T13. ||A|D||BA||B|BAA|KA = ||B|BA||WI|BA.

    Note that Axiom schema E5 is a rule which can take infinitely many
    forms and is part of the metalanguage for CL=(𝕮,T(𝕮),{A,K},=).
    (T(𝕮) is the set of theorems that can be expressed using only
    symbols from the set {A, K. |, =}.)

    Although Theorems T8b, T9b, T11, and T13 might look complicated,
    they are finitely many (specifically four!) statements in the T(𝕮).

    A remarkable fact is that T(𝕮) is rich enough to act as a language
    for arithmetic.  But the language is also weak in the sense that
    there is no way to represent quantifiers in the language.

    Script module logic.tests.curry1 develops basic theorems of CL.
    This module, logic.tests.curry2 develops arithmetic inside CL.

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

axioms = """ARITHMETIC IN CL=(𝕮,T(𝕮),{A,K},=)

    The set of natural numbers is denoted ℕ.  We make the following
    definitions:

        D7. 0 = |KI.
        D8. S = |A||BAK.

    We define ℕ as inductively as a subset of 𝕮:

        N1. 0 is in ℕ.
        N2. If n is in ℕ, then |Sn is in ℕ.

    In this definition, we exclude from ℕ anything which cannot be
    derived finitely by applying Rules N1 and N2.
"""
print(axioms)

print()
print("Adding rule 'zero_reduction' as Rule 0.")

def zero_reduction(tree:ParseTree, parent, child=-1):
    """perform a 0 reduction: ||0ab = b"""
    node = tree.validate_parentage(parent, child)
    if type(node) == str or node[0] != '|':
        return False
    Za, b = node[1], node[2]
    if type(Za) == str or Za[0] != '|' or Za[1] != '0':
        return False
    result = b
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

Reducer.add_rule(zero_reduction, '0')

print()
print("D7. 0 = |KI.                 (Zero)")
expr = "||0ab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == 'b', str(tree)
expr = "|||KIab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == 'b', str(tree)

print()
print("Adding rule 'successor_reduction' as Rule 0.")

def S_reduction(tree:ParseTree, parent, child=-1):
    """perform a successor reduction: |||Sabc = |b||abc"""
    node = tree.validate_parentage(parent, child)
    if type(node) == str or node[0] != '|':
        return False
    Sab, c = node[1], node[2]
    if type(Sab) == str or Sab[0] != '|':
        return False
    Sa, b = Sab[1], Sab[2]
    if type(Sa) == str or Sa[0] != '|' or Sa[1] != 'S':
        return False
    a = Sa[2]
    result = ['|', b, ['|', ['|', a, b], c]]    # ||b||abc
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

Reducer.add_rule(S_reduction, 'S')

print()
print("D8. S = |A||BAK.             (Successor)")
expr = "|||Sabc"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|b||abc', str(tree)
expr = "||||A||BAKabc"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|b||abc', str(tree)

print()
print("TN1: |S0 = I.                (One)")
expr = "||Iab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)
expr = "|||S0ab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|ab', str(tree)

print()
print("Note: Using our definition of 0 and S, 1=|S0=I.")

print()
print("Adding rules for two through ten...")

digits = {2:"two", 3:"three", 4:"four", 5:"five",
          6:"six", 7:"seven", 8:"eight", 9:"nine", 10:"ten"}

def make_n_reduction(n):
    """create reduction rules for 2 through 10"""
    op = str(n)[0]       # op for 10 is "1"
    def f(tree:ParseTree, parent, child=-1):
        """perform a %s reduction: ||%sab = %sb"""
        node = tree.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|':
            return False
        fa, b = node[1], node[2]
        if type(fa) == str or fa[0] != '|' or fa[1] != op:
            return False
        a = fa[2]
        result = b
        for i in range(n):
            result = ['|', a, result]
        if parent == None:
            tree.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result
    name = digits[n]
    prefix = "|a|" * n
    f.__doc__ = f.__doc__ % (name, op, prefix)
    print("Adding rule '%s_reduction':" % name)
    print("  " + f.__doc__)
    Reducer.add_rule(f, str(n))

for i in range(2,11):
    make_n_reduction(i)
    
print()
print("D9. 2 = |SI.                 (Two)")
expr = "||2ab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a|ab', str(tree)
expr = "|||SIab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a|ab', str(tree)

print()
print("TN2. 2 = ||ABI.")
expr = "||||ABIab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a|ab', str(tree)
print("   = ||2ab from above")

print()
print("D9. 3 = |S2 = |S|SI.             (Three)")
expr = "||3ab"
print(f"LHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a|a|ab', str(tree)
expr = "|||S2ab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=50)
assert str(tree) == '|a|a|ab', str(tree)

print()
print("""NOTES

    ℕ = {0, 1, 2, 3, 4, ...}
      = {0, |S0, |S|S0, |S|S|S0, |S|S|S|S0, ...
      = {|KI, I, ||ABI, ||A||BAK||ABI, ||A||BAK||A||BAK||ABI, ...}

     Entity   Reduction         Lagrange notation
    ||0fx   = x               = x
    ||1fx   = |fx             = f(x)
    ||2ab   = |f|fx           = f(f(x))
    ||3ab   = |f|f|fx         = f(f(f(x)))
    ||4ab   = |f|f|f|fx       = f(f(f(f(x))))
     ...       ...               ...
""")

print("ADDITION")

print()
print("""    There are many entities which could be used as definitions
    of addition.  One such operator is + = ||BAD.  We start with a few
    examples.
""")

print("3 + 5 = 8 = 5 + 3:                    (commutativity)")
plus = lambda x, y: f"||||BAD{x}{y}"
expr = "||" + plus(3, 5) + "ab"
LHS = str(Reducer.on(expr, maxlen=50, trace=False))
print(f"\t||||+35ab = {expr} = {LHS}")
expr = "||8ab"
MHS = str(Reducer.on(expr, maxlen=50, trace=False))
print(f"\t{expr} = {MHS}")
expr = "||" + plus(5, 3) + "ab"
RHS = str(Reducer.on(expr, maxlen=50, trace=False))
print(f"\t||||+53ab {expr} = {RHS}")
assert LHS == MHS == RHS

print()
print("(1 + 3) + 5 = 9 = 1 + (3 + 5):        (associativity)")
expr = "||" + plus(plus('I', 3), 5) + "ab"
LHS = str(Reducer.on(expr, maxlen=50, trace=False))
print(f"\t||||+||+I35ab = {expr} = {LHS}")
expr = "||9ab"
MHS = str(Reducer.on(expr, maxlen=50, trace=False))
print(f"\t{expr} = {MHS}")
expr = "||" + plus('I', plus(3, 5)) + "ab"
RHS = str(Reducer.on(expr, maxlen=50, trace=False))
print(f"\t||||+I||+35 = {expr} = {RHS}")
assert LHS == MHS == RHS

print("""
    To verify that ||BAD is a correct implementation of addition,
    we need to check that it works for all members of ℕ. An addition
    operator in CL should satisfy the following requirements:

        If m and n are members of ℕ, then:
            add1. 0+n = n; and
            add2. (m+1)+n = (m+n)+1.

    In fact ||BAD works very nicely as we can show it satisfies
    both conditions for all m and n in 𝕮.
""")

print("add1. If n is a member of ℕ, then ||+0n = n.")
print("  or: If n is a member of ℕ, then ||||BAD0n = n.")
expr = "||" + plus(0, "n") + "ab"
print("LHS:", expr)
tree = Reducer.on(expr, maxlen=50)
print()
print("    In fact, ||||BAD0n = n for every n in 𝕮.")

print()
print("add2. If m and n are members of ℕ, then ||+|Smn = |S||+mn.")
print("  or: If m and n are members of ℕ, then ||||BAD|Smn = |S||||BADmn.")
expr1 = plus("|Sm", "n")
expr = "||" + expr1 + "ab"
print("LHS:", expr)
tree = Reducer.on(expr, maxlen=50)
expr2 = "|S" + plus("m", "n")
expr = "||" + expr2 + "ab"
print("RHS:", expr)
tree = Reducer.on(expr, maxlen=50)

print("""
    Let's prove some basic facts about addition (using ||BAD)...
""")

print("TN3. (Identity) If m is in ℕ, then 0+m = m = m+0.")
expr = "||" + plus(0, "m") + "ab"
print("LHS:", expr)
tree = Reducer.on(expr, maxlen=50)
LHS = str(tree)
MHS = "||mab"
print("MHS:", expr)
expr = "||" + plus(0, "m") + "ab"
print("RHS:", expr)
tree = Reducer.on(expr, maxlen=50)
RHS = str(tree)
assert LHS == MHS == RHS
print()
print("    The reductions prove something stronger:")
print("         (a) If m in 𝕮, then ||||BAD0m = m = ||||BADm0;")
print("         (b) moreover, |||BAD0 = I.")

print()
print("TN4. (Associativity.) If k, m, and n are in ℕ, then k+(m+n) = (k+m)+n.")
expr = "||" + plus("k", plus("m", "n")) + "ab"
print("LHS:", expr)
tree = Reducer.on(expr, maxlen=50)
LHS = str(tree)
expr = "||" + plus(plus("k", "m"), "n") + "ab"
print("RHS:", expr)
tree = Reducer.on(expr, maxlen=50)
RHS = str(tree)
assert LHS == RHS
print()
print("    The reductions prove the ||BAD operator is associative in 𝕮.")
print("    In other words, writing '+' for '||BAD':")
print("        if k, m, and n are in 𝕮, then ||+k||+mn = ||+||+kmn.")

print("""
    The |||BAD operator is commutative in ℕ, but not in 𝕮.  So verifying
    commutativity is harder,  To see the difficulty we need to take a
    look at ||(m+n)ab and ||(n+m)ab:
""")
expr = "||" + plus("m", "n") + "ab"
print("    ", "||||+mnab")
print("   =", expr)
tree = Reducer.on(expr, maxlen=50)
print()
print("        ||(m+n)ab = ||ma||nab")
print("        ||(n+m)ab = ||na||mab")

print()
print("    We can show noncommutativity by setting -- m=K, n=I")
expr = "||Ka||Iab"
print("A)", expr, "= a")
tree = Reducer.on(expr, maxlen=50)
expr = "||Ia||Kab"
print("B)", expr, "= |aa")
tree = Reducer.on(expr, maxlen=50)

print()
print("    Since I is in ℕ, assuming we can show that ||BAD is")
print("    commutative in ℕ, then K is not in ℕ.")

print()
print("    From associativity, if m and n are in ℕ:")
print("        m+(n+1) = (m+n)+1")
print("    But we really need to verify that:")
print("        ||+1m = |Sm = ||+m1")
print()
print("TN5. If m is in ℕ, then 1+m = |Sm = m+1.")
print("To verify: ||BADIm = |Sm = ||BADmI.")
expr = "||" + plus("I", "m") + "ab"
print("LHS:", expr)
tree = Reducer.on(expr, maxlen=50)
LHS = str(tree)
expr = "||" + "|Sm" + "ab"
print("MHS:", expr)
tree = Reducer.on(expr, maxlen=50)
MHS = str(tree)
assert LHS == MHS

print("    --- The problem is on the right hand side: ---")
expr = "||" + plus("m", "I") + "ab"
print("RHS:", expr)
tree = Reducer.on(expr, maxlen=50)
RHS = str(tree)

print("    --- So we induce on m...")
print("Basis: m = 0.")
expr = "||" + "|S" + plus(0, "I") + "ab"
print("MHS(0):", expr)
tree = Reducer.on(expr, maxlen=50)
MHS = str(tree)
expr = "||" + plus("|S0", "I") + "ab"
print("RHS(0):", expr)
tree = Reducer.on(expr, maxlen=50)
RHS = str(tree)
assert MHS == RHS

print("Induction hypothesis: |Sm = m+1")
print("  To prove: |S|Sm = |Sm+1")
expr = plus("|Sm", "I")
print("RHS(m):", expr)
expr = "|S" + plus("m", "I") 
print("      =", expr, "            by (add2)")
expr = "|S" + "|Sm"
print("      =", expr, "                  by induction hypothesis.  Q.E.D.")

print("""
    (a) By reduction, 1+m := ||||BADIm = |Sm for m in 𝕮.
    (b) By induction, m+1 := ||||BADmI = |Sm for m in ℕ.

    But ||||BADmI = |Sm is not valid in 𝕮.  From the note above, we can
    see that K is not a member of ℕ.

    We can now prove commutativity of addition (using ||BAD) in ℕ.
""")

print("TN6. (Commutativity) If m and n are in ℕ, then m+n = n+m.")
print("  By induction on m...")
print("    True for m=0 and all n by TN3.")
print("    Suppose true for all n in ℕ for some given m in ℕ.")
expr = plus("m", "n") + " = " + plus("n", "m")
print("  Induction hypothesis:", expr)
lhs = plus("|Sm", "n")
rhs = plus("n", "|Sm")
print("  To prove:", lhs, "=", rhs)
expr = lhs
print("LHS:", expr)
expr = "|S" + plus("m", "n")
print("   =", expr, "             by (add2)")
expr = "|S" + plus("n", "m")
print("   =", expr, "             by induction hypothesis")
expr = plus(plus("n", "m"), "I")
print("   =", expr, "       by TN4")
expr = plus("n", plus("m", "I"))
print("   =", expr, "       by associativity")
expr = plus("n", "Sm")
print("   =", expr, "       by TN4.  Q.E.D.")

print()
print("MULTIPLICATION")

print()
print("""    There are many entities which could be used as definitions
    of multiplication.  One such operator is x = B.
""")

print("3 x 5 = 15 = 5 x 3:                   (commutativity)")
times = lambda x, y: f"||B{x}{y}"
expr = "||" + times(3, 5) + "ab"
LHS = str(Reducer.on(expr, maxlen=50, trace=False))
print(f"\t ||||.35ab = {expr} = {LHS}")
expr = "||" + plus("1", 5) +"ab"
MHS = str(Reducer.on(expr, maxlen=50, trace=False))
print("   --- Note: ||+15 means 10+5=15")
print(f"\t||||+15ab = {expr} = {MHS}")
expr = "||" + times(5, 3) + "ab"
RHS = str(Reducer.on(expr, maxlen=50, trace=False))
print(f"\t||||.53 = {expr} = {RHS}")
assert LHS == MHS == RHS
aaaa = RHS[:-1].replace("|", "")
print("Note:")
print(f"    '{RHS}' has {len(aaaa)} a's.")

print()
print("(2 x 3) x 4 = 24 = 2 x (3 x 4):       (associativity)")
expr = "||" + times(times(2, 3), 4) + "ab"
LHS = str(Reducer.on(expr, maxlen=72, max_steps=15, trace=False))
print(f"\t||||.||.234ab = {expr}")
print(f"\t\t = {LHS}")
print("   --- Note: ||+||+114 means (10+10)+4=24")
expr = "||" + plus(plus("1", "1"), 4) +"ab"
MHS = str(Reducer.on(expr, maxlen=72, trace=False))
print(f"\t||||+||+114ab = {expr}")
print(f"\t\t = {MHS}")
expr = "||" + times(2, times(3, 4)) + "ab"
RHS = str(Reducer.on(expr, maxlen=72, max_steps=15, trace=False))
print(f"\t||||.2||.34ab = {expr}")
print(f"\t\t = {RHS}")
assert LHS == MHS == RHS

aaaa = RHS[:-1].replace("|", "")
print("Note:")
print(f"    '{RHS}' has {len(aaaa)} a's.")

print()
print("2 x (3 + 4) = 14 = (3 + 4) x 2:       (distributive property)")
times = lambda x, y: f"||B{x}{y}"
expr = "||" + times(2, plus(3, 4)) + "ab"
LHS = str(Reducer.on(expr, maxlen=72, max_steps=15, trace=False))
print(f"\t||||.2||+34ab = {expr}")
print(f"\t\t = {LHS}")
expr = "||" + plus("1", 4) +"ab"
MHS = str(Reducer.on(expr, maxlen=72, trace=False))
print("   --- Note: ||+14 means 10+4=14")
print(f"\t||||+14ab = {expr} = {MHS}")
expr = "||" + times(plus(3, 4), 2) + "ab"
RHS = str(Reducer.on(expr, maxlen=72, max_steps=15, trace=False))
print(f"\t||||.||+342ab = {expr}")
print(f"\t\t = {RHS}")
assert LHS == MHS == RHS

aaaa = RHS[:-1].replace("|", "")
print("Note:")
print(f"    '{RHS}' has {len(aaaa)} a's.")

print("""
    We now sketch proofs of basic properties of multiplication.
""")

print("TN7. (Zero.) If m is in ℕ, then 0 x m = 0 = m x 0.")
expr = f"||{times(0,'m')}ab"
LHS = str(Reducer.on(expr, maxlen=72, trace=False))
print(f"\t||||.0mab = {expr} = {LHS}")
expr = "||0ab"
MHS = str(Reducer.on(expr, maxlen=72, trace=False))
print(f"\t{expr} = {MHS}")
expr = f"||{times('m',0)}ab"
RHS = str(Reducer.on(expr, maxlen=72, trace=False))
print(f"\t||||.m0ab = {expr} = {RHS}")
assert LHS == MHS
print("""
    The first equality is valid over 𝕮.  The second equality needs
    an induction proof.  The second equality is indeed valid over
    ℕ, but not over 𝕮.
""")
print("Basis: (m=0)")
print("    ||0|0ab = |||KI||0ab = b, by K-reduction.")
print("Induction: Assume ||m|0ab = b.")
expr = "|||Sm|0ab"
print(f"  0: {expr}")
result = str(Reducer.on(expr, maxlen=72))
assert result == "||m|0ab", result
print("   = b, by the induction hypothesis.")

print()
print("TN8. (Identity.) If m is in ℕ, then 1 x m = m = m x 1.")
expr = f"||{times('I','m')}ab"
LHS = str(Reducer.on(expr, maxlen=72, trace=False))
print(f"\t||||.0mab = {expr} = {LHS}")
expr = f"||{times('m','I')}ab"
RHS = str(Reducer.on(expr, maxlen=72, trace=False))
print(f"\t||||.m0ab = {expr} = {RHS}")
assert LHS == "||mab" == RHS
print("""
    Both equalities are valid over 𝕮.
""")

print()
print("TN9. (Associativity.) If k, m, and n are in ℕ, then k(mn) = (km)n.")
expr = "||" + times("k", times("m", "n")) + "ab"
print("LHS:", expr)
tree = Reducer.on(expr, maxlen=50)
LHS = str(tree)
expr = "||" + times(times("k", "m"), "n") + "ab"
print("RHS:", expr)
tree = Reducer.on(expr, maxlen=50)
RHS = str(tree)
assert LHS == RHS
print("""
    The reductions prove the B operator is associative in 𝕮.
    In other words, writing '.' for 'B:
        if k, m, and n are in 𝕮, then ||.k||.mn = ||.||.kmn.
""")

# ======================= RIGHT DISTRIBUTIVE LAW

print("TN10. (Right Distributivity)")
print("      If k, m, and n are in ℕ, (m+n)k = mk+nk.")
print("LHS: ||||.||+mnkab")
expr = f"||{times(plus('m','n'),'k')}ab"
print("   =", expr)
LHS = str(Reducer.on(expr, maxlen=72))
print("RHS: ||||+||.mk||.nk")
expr = f"||{plus(times('m','k'),times('n','k'))}ab"
print("   =", expr)
RHS = str(Reducer.on(expr, maxlen=72))
assert LHS == RHS

print("""
    The reductions are valid for all k, m, and n in 𝕮.
    If k, m, and n are in 𝕮, then:
        ||B||||BADmnk = ||.||+mnk
                      = ||+||.mk||.nk = ||||BAD||Bmk||Bnk.
    The corresponding left distributive law is valid in ℕ, but
    not generally in 𝕮.
""")

print("TN11. (Left Successor I)")
print("      If m, and n are in ℕ, (m+1)n = n+mn.")
print("LHS: ||||.|Smnab")
expr = f"||{times('|Sm','n')}ab"
print("   =", expr)
LHS = str(Reducer.on(expr, maxlen=72))
print("RHS: ||||+n||.mn")
expr = f"||{plus('n',times('m','n'))}ab"
print("   =", expr)
RHS = str(Reducer.on(expr, maxlen=72))
assert LHS == RHS

print("""
    The reductions are valid for all m and n in 𝕮.
    If m, and n are in 𝕮, then:
        ||B|Smn = ||.|Smn = ||+n||.mn = ||||BADn||Bmn.
    The addition combinator is not commutative in 𝕮, but it is
    commutative in ℕ, so we have the following corollary.
""")

print("TN11b. (Left Successor II)")
print("       If m, and n are in ℕ, then (m+1)n = mn+n, i.e.:")
print("             ||B|Smn = ||.|Smn = ||+||.mnn = ||||BAD||Bmnn.")

print("")
print("DI Lemma.  |DI=B.")
print("   Proof: ||||DIabc = ||Ia|bc = |a|bc = |||Babc.")

print()
print("TN12. (Right Successor.)")
print("      If m and n are in ℕ, then m(n+1) = m+mn.")

print("Proof by induction:")
print("Basis: m=0.")
print("    0(0+1) = 0 = 0+0, or in combinators:")
print("       ||.0I = 0 = |+00, by TN7 and TN3.")
print("Induction: Assume m(n+1) = m+mn where m is given, i.e.")
print("       ||.m|Sn = ||+||.mn.")

expr = f"||{times('m','|Sn')}ab"
print("LHS:", expr)
expr = f"||{times('m',plus('I','n'))}ab"
print("   =", expr)
LHS = str(Reducer.on(expr, maxlen=72))
expr = f"||{plus('m',times('m','n'))}ab"
print("RHS:", expr)
RHS = str(Reducer.on(expr, maxlen=72))
print("  Assumption implies:", LHS, "=", RHS + ".\t\t(*)")

print("  Show that: ||.Sm|Sn = ||+|Sm|||Smn.")

expr = f"||{times('|Sm','|Sn')}ab"
print("LHS:", expr)
expr = f"||{times('|Sm',plus('I','n'))}ab"
print("   =", expr)
LHS = str(Reducer.on(expr, maxlen=72))
LHS = "|a||na||ma||m|nab"
print(f"   = {LHS}\t\t\t\t\t(*)")

print("\tClaim: LHS = ||(I+(n+(m+mn)))ab:")
expr = "||" + plus('I', plus('n', plus('m', times('m','n')))) + 'ab'
print("alt:", expr)
LHS2 = str(Reducer.on(expr, maxlen=72, max_steps=11))
assert LHS == LHS2


expr = f"||{plus('|Sm',times('|Sm','n'))}ab"
print("RHS:", expr)
RHS = str(Reducer.on(expr, maxlen=72))
print("\tClaim: RHS = ||(I+(m+(n+mn)))ab:")
print("\t  11 step reduction is similar to (alt) above.")
print("\tClaim: LHS = RHS:")
print("\t  Use associativity (TN4) and commutativity (TN6) of addition.")

# ======================= LEFT DISTRIBUTIVE LAW

print("""
TN13. (Left Distributivity)
      If k, m, and n are in ℕ, k(m+n) = km+kn.
Proof by induction on k:
Basis: k=0.
LHS: ||||.0||+mnab""")
expr = f"||{times(0,plus('m','n'))}ab"
print("   =", expr)
LHS = str(Reducer.on(expr, maxlen=72))
print("RHS: ||||+||.0m||.0nab")
expr = f"||{plus(times(0,'m'),times(0,'n'))}ab"
print("   =", expr)
RHS = str(Reducer.on(expr, maxlen=72))
assert LHS == RHS

print("Induction: Assume k(m+n) = km+kn for some given k, i.e.")
print("\t\t||.k||+mn = ||+||.km||.kn.")
expr = f"||{times('k',plus('m','n'))}ab"
print("LHS:", expr)
LHS = str(Reducer.on(expr, maxlen=72))
expr = f"||{plus(times('k','m'),times('k','n'))}ab"
print("RHS:", expr)
RHS = str(Reducer.on(expr, maxlen=72))
print("   We can use: ||k|||Dma|nab = ||k|ma||k|nab.")
print("To prove: ||.|Sk||+mn = ||+||.|Skm||.|Skn.")
expr = f"||{times('|Sk',plus('m','n'))}ab"
print("LHS:", expr)
LHS = str(Reducer.on(expr, maxlen=72))
print("   = ||ma||na||k|ma||k|nab  <--- induction hypothesis")
print("   = ||(m + n + km + kn)ab  <--- cf. claim in previous proof")
expr = f"||{plus(times('|Sk','m'),times('|Sk','n'))}ab"
print("RHS:", expr)
RHS = str(Reducer.on(expr, maxlen=72))
print("   = ||(m + kn + n + kn)ab  <--- cf. claim in previous proof")
print("Then LHS = RHS by TN4 and TN6.")

# ======================= RIGHT DISTRIBUTIVE LAW

print("""
TN14. (Right Distributivity)
      If k, m, and n are in ℕ, (m+n)k = mk+nk.
Does it work in general?""")
expr = f"||{times(plus('m','n'),'k')}ab"
print("LHS: ||||.||+mnkab")
print("   =", expr)
LHS = str(Reducer.on(expr, maxlen=72))
print("RHS: ||||+||.mk||.nkab")
expr = f"||{plus(times('m','k'),times('n','k'))}ab"
print("   =", expr)
RHS = str(Reducer.on(expr, maxlen=72))
print("LHS == RHS?", LHS==RHS)

# ======================= COMMUTATIVITY

print("""
TN15. (Commutativity of multiplication)
      If m, and n are in ℕ, mn = nm.
Proof by induction on k:
Basis: m=0.
   Then mn=0n = 0 = n0 = nm, by TN7.
Induction hypothesis: Let m be given and assume mn=nm, i.e.
                            ||Bmn = ||.mn = ||.nm = ||Bnm.
""")
expr = f"||{times('m','n')}ab"
print("LHS:", expr)
LHS = str(Reducer.on(expr, maxlen=72))
expr = f"||{times('n','m')}ab"
print("RHS:", expr)
RHS = str(Reducer.on(expr, maxlen=72))
print("  Then ||m|nab = ||n|mab.")
print("""
  We want to verify that:
      ||.|Smn = ||.n|Sm.""")
print("LHS: ||.Smn           i.e. ||((1+m)n)ab")
expr = "||" + times("|Sm", "n") + "ab"
print("LHS:", expr)
LHS = str(Reducer.on(expr, maxlen=72))
print("   = ||na||n|mab, by the induction hypothesis")
LHS = "||na||n|mab"

print("MHS: ||||.n||+Imab     i.e.: ||(n(1+m))ab")
expr = "||" + plus(times("n","I"),times("n", "m")) + "ab"
print("  =", expr)
MHS = str(Reducer.on(expr, maxlen=72))
assert LHS == MHS

print("RHS: ||||.n|Sm         i.e.: ||(n(1+m))ab")
expr = "||" + times("n","|Sm") + "ab"
print("  =", expr)
RHS = str(Reducer.on(expr, maxlen=72))

print("LHS = MHS, by reduction.")
print("MHS = RHS, by the right successor property (TN12).")
print()
print("    Note that both equalities are valid for ℕ, but not for 𝕮.")

print("""
                          SUMMARY
     ----------------------------------------------------------------
                                                           Validity                                            
     Property             Theorem                          𝕮      ℕ⊂𝕮
     ----------------------------------------------------------------
Zero:            0 := |KI
Successor:       S := |A||BAK
One:             I = |S0 
Addition:        + := ||BAD
     Left identity        TN3. ||+0m = m                   Yes    Yes
     Right identity       TN3. ||+m0 = m                   Yes    Yes
     Associative          TN4. ||+k||+mn = ||+||+kmn       Yes    Yes
     Left successor       TN5. ||+Im = |Sm                 Yes    Yes
     Right successor      TN5. ||+mI = |Sm                 No     Yes
     Commutative          TN6. ||+mn = ||+nm               No     Yes
Multiplication:  . = ||B
     Left zero            TN7. ||.0m = 0                   Yes    Yes
     Right zero           TN7. ||.m0 = 0                   No     Yes
     Left identity        TN8. ||.Im = m                   Yes    Yes
     Right identity       TN8. ||.mI = m                   Yes    Yes
     Associative          TN9. ||.k||.mn = ||.||.kmn       Yes    Yes
     Right distributive  TN10. ||.||+mnk = ||+||.mk||.nk   Yes    Yes
     Distributive laws:
        left successor   TN11. ||.|Smn = ||+n||.mn         Yes    Yes
        left successor         ||.|Smn = ||+||.mnn         No     Yes
        right successor  TN12. ||.m|sn = ||+m||.mn         No     Yes
        left             TN13. ||.k||+mn = ||+||.km||.kn   No     Yes
        right            TN14. ||.||+mnk = ||+||.mk||.nk   Yes    Yes
     Commutative         TN15. ||.mn = ||.nm               No     Yes
""")

print()
print("EXPONENTIATION")

print()
print("""    There are many entities which could be used as definitions
    of exponentiation.  One such operator is ^ = T.  Since ||Tmn = |nm,
    |nm is a representation in CL of m^n.
""")

print("2^3 = 8:")
power = lambda x, y: f"||T{x}{y}"
expr = "||" + power(2, 3) + "ab"
print(f"LHS: {expr}   (i.e. ||(2^3)ab)")
tree = Reducer.on(expr, maxlen=72)
LHS = str(tree)
expr = "||8ab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=72)
RHS = str(tree)
assert LHS == RHS

print()
print("3^2 = 9:")
power = lambda x, y: f"||T{x}{y}"
expr = "||" + power(3, 2) + "ab"
print(f"LHS: {expr}   (i.e. ||(3^2)ab)")
tree = Reducer.on(expr, maxlen=72)
LHS = str(tree)
expr = "||9ab"
print(f"RHS: {expr}")
tree = Reducer.on(expr, maxlen=72)
RHS = str(tree)
assert LHS == RHS

print()
print("2^4 = 16 = 4^2:")
power = lambda x, y: f"||T{x}{y}"
expr = "||" + power(2, 4) + "ab"
print(f"LHS: {expr}   (i.e. ||(2^4)ab)")
tree = Reducer.on(expr, maxlen=72, max_steps=20)
LHS = str(tree)
expr = "||" + times(4, 4) + "ab"
print(f"RHS: {expr}    (using 4 x 4 = 16)")
tree = Reducer.on(expr)
MHS = str(tree)
expr = "||" + power(4, 2) + "ab"
print(f"RHS: {expr}   (i.e. ||(4^2)ab)")
tree = Reducer.on(expr, maxlen=72)
RHS = str(tree)
assert LHS == MHS == RHS

print("SUCCESS!")
