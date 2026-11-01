"""
logic.tests.curry1 - combinatory logic exercises in Rosenbloom
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Exercises from pages 130-131.

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
import logic.curry_arithmetic as CLA
import logic.curry_lambda as LCL
import logic.curry_recursive as LCR

CLA.add_rules()
LCR.add_rules()

print("*" * 72)
LCR.all_reductions()
LCR.test_standard()
LCR.all_filters()
LCR.test_alpha_replacement()
print("*" * 72)

# ======================================================================
LCR._title("LEFT BRACKET REDUCTION")

print("\nEx.3a) [ := λxλyλz||z|Kyx = |C||BC||BTK.")

expr = "|||" + "|C||BC||BTK" + "xyz"
print(f"{expr=}")
result = str(Reducer.on(expr, maxlen=50))
assert result == "||z|Kyx"

expr = "|||" + "[" + "xyz"
print(f"{expr=}")
result = str(Reducer.on(expr, maxlen=50))
assert result == "||z|Kyx"

print("\nEx.5a) |||[ab0 = a.")

expr = "|||[ab0"
print("LHS:", expr)
result = str(Reducer.on(expr, maxlen=50))
assert result == "a"

print("\nEx.5b) |||[ab|Sn = b.")

expr = "|||[ab|Sn"
print("LHS:", expr)
result = str(Reducer.on(expr, maxlen=50))
assert result == "b"

# ======================================================================
LCR._title("ALPHA REDUCTION")

print("""
    NOTE

        |||[abz is a Kronecker delta function which returns a if z=0
        or b if z=|Sn for some entity n.

        This effectively implies that 0 cannot be expressed as |Sn.
        Note that we don't have a universal quantifier in CL...
        Since CL is consistent, we can say:

            There are no n in 𝕮 such that 0 = |Sn.

        But this is a statement in the meta language.  There is no
        way to express this as a statement in CL.
""")

print("\nEx.3b) α := λx||[|S|x0|x0 = ||B|W||B[S|T0.")

# ||[|S|x0|x0
#   a = |x0 = ||T0x
# ||[|Saa
#   b = |[|Sa = |||B[Sa
# |ba
# ||||B[Saa
#   c = ||B[S
# ||caa
# ||Wca
# ||Wc||T0x
#   d = |Wc = |W||B[s
#   e = |T0
# |d|ex
# |||Bdex
#   ||Bde = ||B|W||B[S|T0

expr = "|" + "||B|W||B[S|T0" + "x"
print(f"{expr=}")
result = str(Reducer.on(expr, maxlen=50))
assert result == "||[|S|x0|x0"

expr = "|αx"
print("LHS:", expr)
result = str(Reducer.on(expr, maxlen=50))
assert result == "||[|S|x0|x0"

print("\nEx.5c) If n is in ℕ, then |||nα|K00 = n.")
print("Basis: n=0.")
expr = "|||0α|K00"
print("LHS:", expr)
result = str(Reducer.on(expr, maxlen=50))
assert result == '0'
print("Induction: Assume |||nα|K00 = n. Show: ||||Snα|K00 = |Sn.")
expr = "||||Snα|K00"
print("LHS:", expr)
result = str(Reducer.on(expr, maxlen=50))
assert result == "|S" + "|||nα|K00"

result = LCR.alpha_replacement(result, "n", verbose=False)
assert str(result) == "|Sn", str(result)
print("   =", "|S" + "n, by the induction hypothesis.")

# ===

print("\Corr.5c) If n is in ℕ, then |||nα|K0I = |Pn.")

print("\n   This corollary follows from (Ex.5c) and the following reductions:")

print()
expr = "|||0α|K0I"
print("LHS:", expr)
result = str(Reducer.on(expr, maxlen=50))
assert result == "0"

print()
expr = "||||Snα|K0I"
print("LHS:", expr)
result = str(Reducer.on(expr, maxlen=50))
assert result == "|||nα|K00"


# ======================================================================
LCR._title("PREDECESSOR REDUCTION")

print("\nEx.3c) P := λx|||xα|K0I = ||C||C|Tα|K0I.")

# ||(|xα)|K0I
# |(||Tαx|K0)I
# | | ||C|Tα|K0 x I
# |||C||C|Tα|K0Ix

expr = "|" + "||C||C|Tα|K0I" + "x"
print(f"{expr=}")
result = str(Reducer.on(expr, maxlen=50))

expr = "|Px"
print(f"{expr=}")
result = str(Reducer.on(expr, maxlen=50))

print("\nEx.5d) P0 = 0.")

expr = "|P0"
print(f"{expr=}")
result = str(Reducer.on(expr, maxlen=50))
assert result == '0'

print("\nEx.5e) If n is in ℕ, then P|Sn = n.")

expr = "|P|Sn"
print(f"{expr=}")
result = str(Reducer.on(expr, maxlen=50))

assert result == "|||nα|K00"
result = LCR.alpha_replacement(result, "n", verbose=False)
assert str(result) == "n", str(result)
print("   = n, whenever n is in ℕ (by Ex.5c).")


# ======================================================================
LCR._title("BETA REDUCTION")

print("\nEx.3d) β := λxλyλzλw||||[|Kx|y|Pww|z|Pw")

print()
expr1 = "||||[|Kx|y|Pww|z|Pw"
print(f"λxλyλzλw{expr1}")
lambdas = "λxλyλzλw"
expr = expr1
while lambdas:
    variable = lambdas[-1]
    lambdas = lambdas[:-2]
    expr = LCL.AKI_eliminate(variable, str(expr))
    LCL.prune_AK(expr)
    expr = str(expr)
    expr = expr.replace('|BB', 'D')
    expr = expr.replace("||A|KAK", "B")
    expr = expr.replace('||AKK', 'I')
    expr = expr.replace("|BI", "I")
    expr = expr.replace("|DI", "B")
    expr = expr.replace("||AA|AK", "W")
    expr = expr.replace("||A|DA|AK", "C")
    expr = expr.replace("||BA|BK", "K")
    expr = expr.replace("||A|DB|KK", "||B|BKI")
    print("=", lambdas + str(expr))
letters = set(expr)
print("constants = ", letters)

expr2 = "||||" + expr +"xyzw"
print("Applying last expression to xyzw...")
expr3 = Reducer.on(expr2, max_steps=50, trace=False, rule_set=AKIBCW_reduction)
print(expr1, "=", expr3, "...", end="")
assert expr1 == str(expr3)
print("ok!")

# Can we improve the ugly expression?
# λxλyλzλw||||[|Kx|y|Pww|z|Pw
# |z|Pw = |||BzPw
# |y|Pw = |||ByPw
# λxλyλzλw||||[|Kx|||ByPww|||BzPw

print()
expr = "||||[|Kx|||ByPww|||BzPw"
lambdas = "λxλyλzλw"

BWCreduce = {ParseTree.B_reduce, ParseTree.W_reduce, ParseTree.C_reduce}
assert expr1 == str(Reducer.on(expr, rule_set=BWCreduce, trace=False))

print("β = ", lambdas, ParseTree(expr), sep='')

prunings = 0
shavings = 0
while lambdas:
    variable = lambdas[-1]
    lambdas = lambdas[:-2]
    expr = LCL.AKI_eliminate(variable, str(expr))
    n_ = len(str(expr))
    LCL.prune_AK(expr)
    m_ = len(str(expr))
    prunings += n_ - m_
    expr = str(expr)
    expr = expr.replace('|BB', 'D')
    expr = expr.replace("||A|KAK", "B")
    expr = expr.replace('||AKK', 'I')
    expr = expr.replace("|BI", "I")
    expr = expr.replace("|DI", "B")
    expr = expr.replace("||AA|AK", "W")
    expr = expr.replace("||A|DA|AK", "C")
    expr = expr.replace("||BA|BK", "K")
    expr = expr.replace("||A|DB|KK", "||B|BKI")
    print("=", lambdas + str(expr))
    n_ = len(str(expr))
    prunings += m_ - n_
print("Savings:", f"pruning: {prunings}", f"shaving: {shavings}", sep="\n\t")

# Can we improve the ugly expression?
# λxλyλzλw | | ||[|Kx|||ByPw  w |||BzPw
# λxλyλzλw | | |||B|[|Kx||ByPw  w |||BzPw
#          1 2 345454543454321  0 123210-
#            1 234343432343210  -
#              12323232123210-
# λxλyλzλw | || ||B|[|Kx||ByP w  w |||BzPw
# λxλyλzλw | ||W||B|[|Kx||ByP w |||BzPw
# λxλyλzλw | | |W||B|[|Kx||ByP w |||BzPw
# λxλyλzλw | ||C |W||B|[|Kx||ByP  |||BzPw w
# λxλyλzλw |  |     |C|W||B|[|Kx||ByP  |||BzP   w w
#             |     a                   |b      c
# λxλyλzλw |  ||| B |C|W||B|[|Kx||ByP    ||BzP  w w
#          1  234 3 43434545454345432    34321  0 -
# λxλyλzλw || ||B|C|W||B|[|Kx||ByP||BzP  w w
#          || a                          b b
# λxλyλzλw ||W||B|C|W||B|[|Kx||ByP||BzP  w

print()
expr = "||W||B|C|W||B|[|Kx||ByP||BzPw"
lambdas = "λxλyλzλw"
print(lambdas, expr, sep="")
expr = "|W||B|C|W||B|[|Kx||ByP||BzP"
lambdas = "λxλyλz"
print("=", lambdas, expr, sep="")
expr2 = str(Reducer.on("|"+expr+"w", rule_set=BWCreduce, trace=False))
assert expr1 == expr2, f"\n{expr1}\n{expr2}"

prunings = 0
shavings = 0
while lambdas:
    variable = lambdas[-1]
    lambdas = lambdas[:-2]
    expr = LCL.AKI_eliminate(variable, str(expr))
    n_ = len(str(expr))
    LCL.prune_AK(expr)
    m_ = len(str(expr))
    prunings += n_ - m_
    expr = str(expr)
    expr = expr.replace('|BB', 'D')
    expr = expr.replace("||A|KAK", "B")
    expr = expr.replace('||AKK', 'I')
    expr = expr.replace("|BI", "I")
    expr = expr.replace("|DI", "B")
    expr = expr.replace("||AA|AK", "W")
    expr = expr.replace("||A|DA|AK", "C")
    expr = expr.replace("||BA|BK", "K")
    expr = expr.replace("||A|DB|KK", "||B|BKI")
    print("=", lambdas + str(expr))
    n_ = len(str(expr))
    prunings += m_ - n_
print("Savings:", f"pruning: {prunings}", f"shaving: {shavings}", sep="\n\t")

# print(ParseTree(expr1).tree)


print("\nEx.5g) ||||βagf0 = a.")

expr = "||||βagf0"
print("LHS:", expr)
Reducer.on(expr, maxlen=50)

print("\nEx.5g) If n is in ℕ, then ||||βagf|Sn = ||gn|fn.")

print("\n  from (Ex.5c) If n is in ℕ, then |||nα|K00 = n.\n")

expr = "||||βagf|Sn"
print("LHS:", expr)
Reducer.on(expr, max_steps=4, maxlen=50)
print("   = ||gn|fn, by (Ex.5e)")


# ======================================================================
LCR._title("THETA REDUCTION")

print("\nEx.3e) ϑ := λx||W|Bx|W|Bx = ||B||B|WIWB")

theta = "||B||B|WIWB"
expr = "|" + theta + "x"
print("|ϑx=", expr)
Reducer.on(expr, max_steps=4, maxlen=50)

print("\nEx.5f) |ϑa = |a|ϑa.")

expr = "||W|Ba|W|Ba"
print("|ϑa=", expr)
Reducer.on(expr, max_steps=2, maxlen=50)
print("   = |a|ϑa")

theta_rule = LCR.recursives['th'][0]

print("""
    NOTE
        This is an ascending recurrence:
            |ϑa = |a|ϑa = |a|a|ϑa = |a|a|a|ϑa = ...
""")

    # test
result = Reducer.on("|ϑa", rule_set=theta_rule, max_steps=1, trace=False)
assert str(result) == "|a|ϑa"
result = Reducer.on("|ϑa", rule_set=theta_rule, max_steps=2, trace=False)
assert str(result) == "|a|a|ϑa"

#                       R
# ======================================================================
LCR._title("RECURSION REDUCTION - the R operator")

print("\nEx.3f) R := λxλy|ϑ||βxy = ||B|Bϑβ")

expr = "||Rxy"
print("LHS:", expr)
LHS = str(Reducer.on(expr, maxlen=50, max_steps=1))

expr = "||" + "||B|Bϑβ" + "xy"
print("RHS:", expr)
RHS = str(Reducer.on(expr, maxlen=50))

assert LHS == RHS, f"{LHS} == {RHS}"

print("""
Ex.5i) Let f = ||Rag.  Then:
           (i)   f = |||βagf;
           (ii)  |f0 = a; and
           (iii) if n is in ℕ, then f|Sn = ||gn|fn.
""")

print("(i) f = |||βagf.")

expr = "||Rag"
print("LHS:", expr)
LHS = str(Reducer.on(expr, maxlen=50))
LHS = str(Reducer.on(LHS, maxlen=50, max_steps=1, rule_set=theta_rule))
print("   = |||βag||Rag, since ||Rag=|ϑ||βag;")
print("   = |||βagf, since f=||Rag, by hypothesis.")

print("\n(ii) |f0 = a.")

print("    From (i), f=|||βagf.")
expr1 = "|" + "|||βagf" + "0"
print("|f0=", expr1)
Reducer.on(expr1, maxlen=50)

print("\n(iii) If n is in ℕ, then |f|Sn = ||gn|fn.")

print("    From (i), f=|||βagf.")
expr1 = "|" + "|||βagf" + "|Sn"
print("|f|Sn=", expr1)
result = str(Reducer.on(expr1, max_steps=4, maxlen=50))
expr2 = result.replace('|P|Sn', 'n')
assert expr2 == "||gn|fn", f"result = {str(result)} = {expr2}"
print(f"   = {expr2}, by (Ex.5e), since n is in ℕ.")



### MU
# ======================================================================
LCR._title("MU REDUCTION")

print("\nEx.3g) μ := |ϑ λxλyλz|||[z ||xy|Sz|yz")

# μ := |ϑM where:
# M=λxλyλz |||[z ||xy|Sz     |yz
#                ||||DxySz
#                |||C|DxSyx
#                ||||||BCDxSyz
goal = "|||[z||xy|Sz|yz"
expr = "|||[z||||||BCDxSyz|yz"
print("LHS =", expr)
result = str(Reducer.on(expr, rule_set=AKIBCW_reduction))
assert goal == result, f"{goal} = {result}"

lambdas = "λxλyλz"
print(lambdas, expr, sep="") 
prunings = 0
shavings = 0
while lambdas:
    variable = lambdas[-1]
    lambdas = lambdas[:-2]
    expr = LCL.AKI_eliminate(variable, str(expr))
    n_ = len(str(expr))
    LCL.prune_AK(expr)
    m_ = len(str(expr))
    prunings += n_ - m_
    expr = str(expr)
    expr = expr.replace('|BB', 'D')
    expr = expr.replace("||A|KAK", "B")
    expr = expr.replace('||AKK', 'I')
    expr = expr.replace("|BI", "I")
    expr = expr.replace("|DI", "B")
    expr = expr.replace("||AA|AK", "W")
    expr = expr.replace("||A|DA|AK", "C")
    expr = expr.replace("||BA|BK", "K")
    expr = expr.replace("||A|DB|KK", "||B|BKI")
    print("=", lambdas + str(expr))
    n_ = len(str(expr))
    prunings += m_ - n_
print("Savings:", f"pruning: {prunings}", f"shaving: {shavings}", sep="\n\t")

xyzexpr = "|||" + expr + "xyz"
print("LHS= ", xyzexpr)
expr = Reducer.on(xyzexpr, max_steps=50, rule_set=AKIBCW_reduction)
result = str(expr)
assert result == goal

print(expr.tree)

mu_rule = LCR.recursives["mu"][0]

print("\nEx.5j)  ||μfn = |||[n||μf|Sn|fn.")

LHS = "||μfn"
print("LHS:", LHS)
RHS = str(Reducer.on(LHS, max_steps=1, maxlen=50, rule_set=mu_rule))
assert RHS == "|||[n||μf|Sn|fn"
print("ok!")

print("\nEx.5k)  If |f0 = 0, then ||μf0 = 0.")

expr = "||μf0"
print("LHS:", expr)
expr = str(Reducer.on(expr, max_steps=1, maxlen=50, rule_set=mu_rule))
expr = expr.replace('|f0', '0')
print("  2: ", expr, ", by hypothesis.", sep="")
expr = str(Reducer.on(expr, maxlen=50))

assert expr == "0"

print("\nEx.5l)  If |f0 in ℕ but |f0 ≠ 0, then ||μf0 = ||μfI.")

print("    We show something stronger:")
print("        If |f0 = |Sn, then ||μf0 = ||μfI.")

expr = "||μf0"
print("LHS:", expr)
expr = str(Reducer.on(expr, max_steps=1, maxlen=50, rule_set=mu_rule))
expr = expr.replace('|f0', '|Sn')
print("  2: ", expr, ", by hypothesis.", sep="")
expr = expr.replace('|S0', 'I')
print("  3: ", expr, ", since |S0=I.", sep="")
expr = str(Reducer.on(expr, maxlen=50))


print("\nEx.5m)  If |fn = 0, then ||μfn = n.")

expr = "||μfn"
print("LHS:", expr)
expr = str(Reducer.on(expr, max_steps=1, maxlen=50, rule_set=mu_rule))
expr = expr.replace('|fn', '0')
print("  2: ", expr, ", by hypothesis.", sep="")
expr = str(Reducer.on(expr, maxlen=50))

assert expr == "n"


print("\nEx.5n)  If |fn = |Sm, then ||μfn = ||μf|Sn.")

expr = "||μfn"
print("LHS:", expr)
expr = str(Reducer.on(expr, max_steps=1, maxlen=50, rule_set=mu_rule))
expr = expr.replace('|fn', '|Sm')
print("  2: ", expr, ", by hypothesis.", sep="")
expr = str(Reducer.on(expr, maxlen=50))

assert expr == "||μf|Sn"

print("\nEx.5p) Suppose |fx in in ℕ whenever x is in ℕ.")
print("       If there exists n≥m in ℕ such that |fn = 0, then")
print("       ||μfm is the smallest such n.")

print("Suppose |fn=0 and |fk=|Sn for k such that n>k≥m.")
print("Claim: ||μfk = ||μfn for all k in ℕ whenever n ≥ k ≥ m.")
print("Proof: By induction on k.")
print("  Basis: If k=n, the claim is trivially true.")
print("  Induction: Suppose the claim holds for some fixed k≥m.")
print("    Let j=k-1, i.e. k=|Sj.  Then |fj is not 0.")
print("      ||μfj = ||μf|Sj, by (Ex.5n),")
print("            = ||μfk = ||μfn by the induction hypothesis.")

print("\nEx.5o) Suppose |fx in in ℕ whenever x is in ℕ.")
print("       If there exists n in ℕ such that |fn = 0, then")
print("       ||μf0 is the smallest such n.")

print("True by (Ex.5p) for m=0.")

### DEFINING one-sided and symmetric subtraction
# ======================================================================
LCR._title("SUBTRACTION - Phase I")

print("""
Ex.6a)  Define an operator ∸ for which m∸n = m-n if m≥n and m∸n = n-m
        if m<n.  (The operator is known as symmetric subtraction.

        Using integers, we want m∸n = |m-n| where |*| denotes the absolute
        value of *.

        Now suppose we define subtraction recursively as follows:
            m - 0  = m                    ||-m0 = m
            m - Sn = P(m - n)             ||-m|Sn = |P||-mn
                                                  = |||BP|-mn
                                                  = |||B|BP-mn

        Then:
            m-n is ordinary subtraction wnen m≥n and 0 otherwise.
        This version of subtraction is someimes called one-sided
        subtraction.

        Then we have the symmetric difference as:
            m ∸ n = (m - n) + (n - m)     ||∸mn = ||+||-mn||-nm

        The question that arises is roughly this...  How do we use
        the operator R to define a dyadic operator X so that:
            ||Xm0 = |am                     a = I, X=-
            ||Xm|Sn = ||hmn

        If ||Xmn reduces:
            ||fnm
            ||||Ragnm                       f = ||Rag
                = |am if n=0
                = |||gn|fnm

        If a = I, then ||f0m = |am = |Im = m.
        Also ||Xm|Sn = |||gn|fnm.
        We want |||gn|fnm = |P||fnm
                          = |||BP|fnm
                          = ||K|BPn|fnm.    g = |K|BP
        ||fnm = ||∸mn = |||C-nm.            - = |Cf.
            
""")

print("  We begin by working out the sort of recursion described above...")
print()

expr = "|||C||Ragmn"
print("LHS: ||Xmn")
print("   =", expr)
result = str(Reducer.on(expr))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))

print()
result0 = result.replace('n', '0')
print("LHS: ||Xm0            <-- base case")
print("   =", result0)
result0 = str(Reducer.on(result0))
assert result0 == "|am"

print()
print("LHS: ||Xm|Sn           <-- recursive case (n in ℕ)")
resultS = expr.replace('n', '|Sn')
print("   =", resultS)
resultS = str(Reducer.on(resultS, max_steps=1))
assert resultS == "||||Rag|Snm"
print("   = ||gn|fn, if n is in ℕ, by (Ex.5i) above.")

def recurse_on_n(name:str, X:str, a:str, g:str):
    """define a reduction rule for a function X such that:
        f = ||Rag
        ||Xm0 = |am
        ||Xmn = |||gn|fnm whenever n is in ℕ.
    """
    assert len('X') == 1
    aT = ParseTree(a).tree
    gT = ParseTree(g).tree
    fT = ['|', ['|', 'R', aT], gT]
    
    def Xag(tree:ParseTree, parent, child=-1):
        """binary function #X# -- #name#
            f = ||R#a##g#
            ||#X#m0 = |#a#m 
            ||#X#mn = |||#g#n|fnm whenever n is in ℕ.
        """
        node = ParseTree.validate_parentage(tree, parent, child)
        if type(node) != list or node[0] != '|':
            return
        Xm, n = node[1], node[2]
        if type(Xm) != list or Xm[0] != '|' or Xm[1] != X:
            return
        m = Xm[2]
        nN = LCR.in_N(n)
        if type(nN) == int:
            if nN == 0:
                result = ['|', aT, m]          # |am
            else:
                Pn = LCR.to_N(nN-1)
                gn = ['|', gT, Pn]
                fn = ['|', fT, Pn]
                gnfn = ['|', gn, fn]
                result = ['|', gnfn, m]             # |||g|Pn||f|Pnm
        else:
            fn = ['|', fT, n]
            result = ['|', fn, m]                   # ||||Ragnm
        assert type(result) == list
        if parent == None:
            tree.tree = result
        else:
            parent[child] = result
        return result

    Xag. __name__ = name
    doc = Xag.__doc__.replace("#name#", name)
    doc = doc.replace('#X#', X)
    doc = doc.replace('#a#', a)
    Xag.__doc__ = doc.replace('#g#', g)
    return Xag

Xreduce = recurse_on_n("X reduce", 'X', 'a', 'g')
assert Xreduce.__name__ == "X reduce"
print()
print("       X_reduce documentation")
help(Xreduce)

print()
print("       Test cases")
expr = "||Xm0"
print("  0:", expr, "   <-- base case")
result = Reducer.on(expr, rule_set={Xreduce}, maxlen=40)
assert str(result) == "|am"

expr = "||XmI"
print("  0:", expr, "   <-- one recursive step")
result = str(Reducer.on(expr, rule_set={Xreduce}, maxlen=40))
assert str(result) == "|||g0|||Rag0m"

expr = "||Xm|SI"
print("  0:", expr, "   <-- two recursive steps")
result = str(Reducer.on(expr, rule_set={Xreduce}, maxlen=40))
assert str(result) == "|||gI|||RagIm"

expr = "||Xm|S|SI"
print("  0:", expr, "   <-- three recursive steps")
result = str(Reducer.on(expr, rule_set={Xreduce}, maxlen=40))
assert str(result) == "|||g|SI|||Rag|SIm"


# ======================================================================
LCR._title("SUBTRACTION - Phase II")

    
print()
takeaway = recurse_on_n("one-sided subtraction", '-', 'I', '|K|BP')
help(takeaway)

four = "|S|S|SI"
three = "|S|SI"
two = "|SI"
one = "I"
zero = "0"

print()
print("       Test cases")
expr = "||-%s%s" % (three, zero)
print("  0:", expr, "   <-- 3 - 0 = 3")
result = str(Reducer.on(expr, rule_set={takeaway}, maxlen=40))
result = str(Reducer.on(result))
assert str(result) == three

print()
expr = "||-%s%s" % (three, one)
print("  0:", expr, "   <-- 3 - 1 = 2")
result = str(Reducer.on(expr, rule_set={takeaway}, maxlen=40))
result = str(Reducer.on(result))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = Reducer.on(result)
result = LCR.alpha_replacement(result, two, verbose=True)
assert str(result) == two


print()
expr = "||-%s%s" % (three, two)
print("  0:", expr, "   <-- 3 - 2 = 1")
result = str(Reducer.on(expr, rule_set={takeaway}, maxlen=40))
result = str(Reducer.on(result))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = str(Reducer.on(result, max_steps=7))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = Reducer.on(result, max_steps=17)
result = str(LCR.alpha_replacement(result, two, verbose=True))
assert str(result) == "|P%s" % two
print("   = I")


print()
expr = "||-%s%s" % (three, three)
print("  0:", expr, "   <-- 3 - 3 = 0")
result = str(Reducer.on(expr, rule_set={takeaway}, maxlen=40))
result = str(Reducer.on(result))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = str(Reducer.on(result, max_steps=2))
result = result.replace("|P|SI", "I")
print("   =", result, "    <-- |P|SI = I")
result = str(Reducer.on(result))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = str(Reducer.on(result, max_steps=7))
result = result.replace("|PI", "0")
print("   =", result, "    <-- |PI = 0")
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = str(Reducer.on(result, max_steps=2))
result = result.replace("|P0", "0")
print("   =", result, "    <-- |P0 = 0")
result = Reducer.on(result, max_steps=40)
result = str(LCR.alpha_replacement(result, two, verbose=True))
assert result == zero

print()
expr = "||-%s%s" % (three, four)
print("  0:", expr, "   <-- 3 - 4 = 0")
result = str(Reducer.on(expr, rule_set={takeaway}, maxlen=40))
result = str(Reducer.on(result))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = str(Reducer.on(result, max_steps=2))
result = result.replace("|P|S|SI", "|SI")
print("   =", result, "    <-- |P|S|SI = |SI")
result = result.replace("||K|BP|SI", "|BP")
print("   =", result, "    <-- ||K|BP|SI = |BP")
result = str(Reducer.on(result))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = str(Reducer.on(result, max_steps=2))
result = result.replace("|P|SI", "I")
print("   =", result, "    <-- |P|SI = I")
result = str(Reducer.on(result, max_steps=5))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = str(Reducer.on(result, max_steps=2))
result = result.replace("|PI", "0")
print("   =", result, "    <-- |PI = 0")
result = str(Reducer.on(result))
result = str(Reducer.on(result, rule_set=theta_rule, max_steps=1))
result = str(Reducer.on(result, max_steps=1))
result = result.replace("||K|BP|P0", "|BP")
print("   =", result, "    <-- ||K|BP|P0 = |BP")
result = result.replace("|KI", "0")
print("   =", result, "    <-- |KI = 0")
result = result.replace("|P0", "0")
print("   =", result, "    <-- |P0 = 0")
result = Reducer.on(result)
result = str(LCR.alpha_replacement(result, one, verbose=True))
result = Reducer.on(result, max_steps=7)
result = str(LCR.alpha_replacement(result, one, verbose=True))
result = result.replace("|PI", "0")
print("   =", result, "    <-- |PI = 0")
result = str(LCR.alpha_replacement(result, zero, verbose=True))
assert result == "|P0"
result = result.replace("|P0", "0")
print("   =", result, "    <-- |P0 = 0")




# CAPITAL LAMBDA (Λ)
LCR._title("MAJUSCULE LAMBDA (Λ) REDUCTION")

print("""
Ex.3h) Λ := λxλy|||Py||B|μxS||μx0 = ||B|C||B|T0||BC||BW|||D|C|DD||CBSPμ.
""")

#    After a lot of manual labor, we arrive at a 13-step reduction:
#  0 λxλy|||Py||B|μxS||μx0
#  1 λxλy||||D|Py||B|μxS|μx0
#  2 λxλy||||D|Py|||CBS|μx|μx0
#  3 λxλy||||||DD|Py||CBS|μx|μx0
#  4 λxλy|||W|||DD|Py||CBS|μx0
#  5 λxλy|||C|W|||DD|Py||CBS0|μx
#  6 λxλy|||T0|C|W|||DD|Py||CBS|μx
#  7 λxλy|||T0|C|W|||C|DD||CBS|Py|μx
#  8 λxλy|||T0|C|W||||D|C|DD||CBSPy|μx
#  9 λxλy|||T0|C|||BW|||D|C|DD||CBSPy|μx
# 10 λxλy|||T0|||BC||BW|||D|C|DD||CBSPy|μx
# 11 λxλy||||B|T0||BC||BW|||D|C|DD||CBSPy|μx
# 12 λxλy|||C||B|T0||BC||BW|||D|C|DD||CBSP|μxy
# 13 λxλy||||B|C||B|T0||BC||BW|||D|C|DD||CBSPμxy

# |||C||B|T0||BC||BW|||D|C|DD||CBSP|μxy
# |   |     |C||B|T0||BC||BW|||D|C|DD||CBSP    |μx    y
# |   |     a                                  |bc    y
# |   |||B  |C||B|T0||BC||BW|||D|C|DD||CBSP     μx    y

rule = {ParseTree.B_reduce, ParseTree.C_reduce, ParseTree.D_reduce,
        ParseTree.T_reduce, ParseTree.W_reduce}
exprLambda = "||B|C||B|T0||BC||BW|||D|C|DD||CBSPμ"
expr = '||' + exprLambda + 'xy'
print(expr)
result = str(Reducer.on(expr, rule_set=rule, max_steps=100))
assert result == "|||Py||B|μxS||μx0"

print()
expr = "||Λxy"
print("  Λ:", expr)
result = str(Reducer.on(expr, max_steps=1))
assert result == "|||Py||B|μxS||μx0"

print()
print("Ex.5q) ||Λa1 = ||μa0.")

expr = "||Λa0"
print("LHS:", expr)
result = str(Reducer.on(expr))

print()
print("Ex.5q) ||Λa|S|Sn = ||μa|S||Λa|S|Sn.")


expr = "||Λa|S|Sn"
print("LHS:", expr)
LHS = str(Reducer.on(expr, max_steps=20))

expr = "||μa|S||Λa|Sn"
print("RHS:", expr)
RHS = str(Reducer.on(expr))

assert LHS == RHS


print()
print("-" * 72)
print("""
    For many purposes, the expression 0⁰ is undefined.  In particular,
    given two functions f(x) and g(x) that approach 0 as x
    approaches 0, the limit of f(x) raised to g(x) may be undefined,
    infinite, or even some fixed real or complex value.

    But there are some applications where it is useful to define 0⁰=1.
    For example, if we are working with power series, we often get more
    compact expressions for common series of functions f(x) when f(x)=1.
    As an example consider the power series for exp(x):
                           2      3
                          x      x
        exp(x) = 1 + x + ---- + ---- + ...
                          2      6

                           n          n
                          x          x
               = 1 +  𝝨  ---- =  𝝨  ---- 
                     n>1  n!    n>1  n!

    Another place where we often set 0⁰=1, is when working with integers.
    Nevertheless, one should use caution when defining 0⁰=1.
""")

print("Ex.5t) |00=I.  ||Sn0=0.")

print("\nLemma: 0⁰=1.  Using combinators: ||^00 := ||T00 = |00 = I.")
expr = "||||^00ab"
print("LHS:", expr)
LHS = str(Reducer.on(expr))
expr = "||||T00ab"
print("MHS:", expr)
MHS = str(Reducer.on(expr))
expr = "||Iab"
print("RHS:", expr)
RHS = str(Reducer.on(expr))
assert LHS == MHS == RHS

print("""
    This is a special case of a general result about entities which
    follows from the definition 0 := KI.
""")
print("Lemma: n⁰=1.  Using combinators: ||^n0 := ||Tn0 = |0n = I.")

expr = "||||^n0ab"
print("LHS:", expr)
LHS = str(Reducer.on(expr))
expr = "||Iab"
print("RHS:", expr)
RHS = str(Reducer.on(expr))
assert LHS == RHS

print("\nLemma: 0ⁿ=0 if n=|Sm.")

expr = "||||^0|Snab"
print("LHS:", expr)
LHS = str(Reducer.on(expr))
expr = "||0ab"
print("RHS:", expr)
RHS = str(Reducer.on(expr))
assert LHS == RHS



