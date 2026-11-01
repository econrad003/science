"""
logic.tests.curry_arithmetic - combinatory arithmetic definitions
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Includes the following reduction rules:

          method                  rule                    note
        zero_reduction         ||0ab = b                0 = |KI
        S_reduction            |||Smab = |a||mab        S = |A||BAK
        plus_reduction         ||||+mnab = ||ma||nab    + = ||BAD
        times_reduction        |||.mna = |m|na          . = B
                               ||||.mnab = ||m|nab
        power_reduction        ||^mn = |nm              ^ = T
                               ||||^mnab = |||nmab

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
from logic.curry import full_reduction

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

def plus_reduction(tree:ParseTree, parent, child=-1):
    """perform an addition reduction: ||||+mnab = |ma||nab

    The name for the operation is given as "m+n" as an aid in tracing.
    """
    node = tree.validate_parentage(parent, child)
    if type(node) == str or node[0] != '|':
        return False
    Pmna, b = node[1], node[2]
    if type(Pmna) == str or Pmna[0] != '|':
        return False
    Pmn, a = Pmna[1], Pmna[2]
    if type(Pmn) == str or Pmn[0] != '|':
        return False
    Pm, n = Pmn[1], Pmn[2]
    if type(Pm) == str or Pm[0] != '|' or Pm[1] != '+':
        return False
    m = Pm[2]
    # print(f"{m=}, {n=}, {a=}, {b=}")
    nab = ['|', ['|', n, a], b]
    result = ['|', ['|', m, a], nab]        # ||ma||nab
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def times_reduction(tree:ParseTree, parent, child=-1):
    """perform an multiplication reduction: |||.mna = |m|na

    This is a synonym for B-reduction.  For ease in typesetting,
    we use a period as the entity, but we use a bold center dot
    (•) in the name for the operation ("m•n").
    """
    node = tree.validate_parentage(parent, child)
    if type(node) == str or node[0] != '|':
        return False
    Mmn, a = node[1], node[2]
    if type(Mmn) == str or Mmn[0] != '|':
        return False
    Mm, n = Mmn[1], Mmn[2]
    if type(Mm) == str or Mm[0] != '|' or Mm[1] != '.':
        return False
    m = Mm[2]
    # print(f"{m=}, {n=}, {a=}")
    na = ['|', n, a]
    result = ['|', m, na]                   # |m|na
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def power_reduction(tree:ParseTree, parent, child=-1):
    """perform an exponentiation reduction: ||^mn = |nm

    This is a synonym for T-reduction.  For ease in typesetting,
    we use a caret as the entity, but we use a superscript (ⁿ) in the
    name for the operation ("mⁿ").
    """
    node = tree.validate_parentage(parent, child)
    if type(node) == str or node[0] != '|':
        return False
    Tm, n = node[1], node[2]
    if type(Tm) == str or Tm[0] != '|' or Tm[1] != '^':
        return False
    m = Tm[2]
    # print(f"{m=}, {n=}")
    result = ['|', n, m]
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result


def add_rules(rule_set:set=full_reduction):
    """add the rules to the rule set"""
    Reducer.add_rule(zero_reduction, name='0', rule_set=rule_set)
    Reducer.add_rule(S_reduction, name='S(m)', rule_set=rule_set)
    Reducer.add_rule(plus_reduction, name='m+n', rule_set=rule_set)
    Reducer.add_rule(times_reduction, name='m•n', rule_set=rule_set)
    Reducer.add_rule(power_reduction, name='mⁿ', rule_set=rule_set)

if __name__ == "__main__":
    print("Testing additional rules")
    add_rules()
    print("0 = |KI.")
    lhs = "||0ab"
    LHS = str(Reducer.on(lhs, trace=False))
    rhs = "|||KIab"
    RHS = str(Reducer.on(rhs, trace=False))
    assert LHS==RHS, f"{lhs}={LHS}, {rhs}={RHS}"

    print("S = |A||BAK")
    lhs = "||" + "|Sm" + "ab"
    LHS = str(Reducer.on(lhs, trace=False))
    rhs = "||" + "||A||BAKm" + "ab"
    RHS = str(Reducer.on(rhs, trace=False))
    assert LHS==RHS, f"{lhs}={LHS}, {rhs}={RHS}"

    print("+ = ||BAD")
    lhs = "||" + "||+mn" + "ab"
    LHS = str(Reducer.on(lhs, trace=False))
    rhs = "||" + "||||BADmn" + "ab"
    RHS = str(Reducer.on(rhs, trace=False))
    assert LHS==RHS, f"{lhs}={LHS}, {rhs}={RHS}"

    print("• = B")
    lhs = "|" + "||.mn" + "a"
    LHS = str(Reducer.on(lhs, trace=False))
    rhs = "|" + "||Bmn" + "a"
    RHS = str(Reducer.on(rhs, trace=False))
    assert LHS==RHS, f"{lhs}={LHS}, {rhs}={RHS}"
    lhs = "||" + "||.mn" + "ab"
    LHS = str(Reducer.on(lhs, trace=False))
    rhs = "||" + "||Bmn" + "ab"
    RHS = str(Reducer.on(rhs, trace=False))
    assert LHS==RHS, f"{lhs}={LHS}, {rhs}={RHS}"

    print("ⁿ = T")
    lhs = "||^mn"
    LHS = str(Reducer.on(lhs, trace=False))
    rhs = "||Tmn"
    RHS = str(Reducer.on(rhs, trace=False))
    assert LHS==RHS, f"{lhs}={LHS}, {rhs}={RHS}"
    lhs = "||" + "||^mn" + "ab"
    LHS = str(Reducer.on(lhs, trace=False))
    rhs = "||" + "||Tmn" + "ab"
    RHS = str(Reducer.on(rhs, trace=False))
    assert LHS==RHS, f"{lhs}={LHS}, {rhs}={RHS}"

    print()
    print("All in one (example)...")
    succ = lambda x: "|S" + str(x)
    plus = lambda x, y: "||+" + str(x) + str(y)
    times = lambda x, y: "||." + str(x) + str(y)
    power = lambda x, y: "||^" + str(x) + str(y)

    expr = "||" + plus(succ('m'), times('n', power('p', 'q'))) + "ab"
    print(f"{expr=}")
    EXPR = str(Reducer.on(expr, maxlen=50))
    assert EXPR == "|a||ma||n||qpab"
    print("SUCCESS!")
