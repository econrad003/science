"""
logic.tests.luk2 - test against axioms for Łukasiewicz algebras (second version)
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    As a module, this program provides a method (test) which tests
    a logic system against the assumptions axiom systems
    for the Łukasiewicz algebras.

    As a main program (or demo), this program tests several different
    systems of propositional logic.

REFERENCES

    [1] Alistair Urquhart.  Basic many-valued logic.  Offprint (received 2026).
        Published in: Handbook of Philosophical Logic.  Springer (2001),
        pp 249-295.  (ISBN-13) 978-94-017-0452-6.

    [2] Grzegorz Malinowski. Many-valued Logics.  Oxford (1993), p 40.
        (ISBN) 0-19-853787-5.

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
references = """
[1] Alistair Urquhart, "Basic Many-Valued Logic", in the
    Handbook of Philosophical Logic, Springer (2001), Section 2.6. An
    offprint of the Urquhart article is available as a free download.
[2] Grzegorz Malinowski. Many-valued Logics.  Oxford (1993), p 40.
"""
from itertools import product     # Cartesian product
from logic.wff import WFF, Constant, Variable, UnaryOperator, BinaryOperator
from logic.deductions import Rule
from logic.grigolia1977 import GrigoliaExtensions, CoefficientOperator
from logic.grigolia1977 import GWFF
from logic.tests.luk1 import definitions as defns
from logic.tests.luk1 import rules
from logic.tests.luk1 import theorems, more_rules, Axioms

def make_axioms() -> list:
    """Wajsberg's axioms for Ł ͚and Ł₃"""
    ax1 = ("positive paradox", "CpCqp")
    ax2 = ("hypothetical syllogism", "CCpqCCqrCpr")
    ax3 = ("contraposition", "CCNpNqCqp")
    ax4 = ("commutativity", "CApqAqp")
    ax5 = ("excluded middle 2", "CCCpqCqpCqp")
    ax6 = ("Ł₃ axiom 4", "CCCpNppp")
    return [ax1, ax2, ax3, ax4, ax5, ax6]

axioms = make_axioms()

def test(name, engine, false, true, values, verified=None):
    """test a scenario against the assumptions"""
    print("-" * 79)
    print("     Target Engine:", name)
    print(f"             Class:", engine.__class__.__name__)
    print()
    if not isinstance(engine, GrigoliaExtensions):
        message = f"engine class {engine.__class__.__name__} is not\n" \
            + f"supported in module {__file__}"
        raise NotImplementedError(message)

        # Define the operators
    NOT = engine.NOT
    AND = engine.AND
    OR = engine.OR
    IMP = engine.IMP
    EQU = engine.EQU
    DEF = engine.EQU
    JOIN2 = engine.JOIN2
    MEET2 = engine.MEET2
    F = Constant("F", false, owner=engine)
    T = Constant("T", true, owner=engine)
    p = Variable("p", owner=engine)
    q = Variable("q", owner=engine)
    r = Variable("r", owner=engine)
    s = Variable("s", owner=engine)
    atoms = {'F':F, 'T':T, 'p':p, 'q':q, 'r':r, 's':s}
    unaries = {'N':NOT}
    binaries = {'K':AND, 'A':OR, 'C':IMP, 'E':EQU, ':':DEF,
                '+':JOIN2, '.':MEET2}
    names = {'N':'~', 'K':'∧', 'A':'∨', 'C':'⊃', 'E':'≡', ':':' := ',
             '+':'+', '.':'•'}

    definitions = list(defns)
    d_join2 = ("join (2)", ":+pqCNpq")
    definitions.append(d_join2)
    d_meet2 = ("meet (2)", ":.pqNCpNq")
    definitions.append(d_meet2)
    pair = ("multiple 2", ":_2_p+pp")
    definitions.append(pair)
    pair = ("multiple 3", ":_3_p+_2_pp")
    definitions.append(pair)
    pair = ("multiple 4", ":_4_p+_3_pp")
    definitions.append(pair)
    pair = ("exponent 2", ":^2^p.pp")
    definitions.append(pair)
    pair = ("exponent 3", ":^3^p.^2^pp")
    definitions.append(pair)
    pair = ("exponent 4", ":^4^p.^3^pp")
    definitions.append(pair)

    if verified == None:
        verified = lambda value: value == true

    def parse(expr, name, number, prefix):
        """create a wff"""
        wff = GWFF(engine, name, number, prefix)
        stack = list()
        rpn = list(reversed(expr))
        digits = False
        d1 = 0
        d2 = 1
        for char in rpn:
            if digits:
                if char == "_":
                    arg = stack.pop()
                    result = CoefficientOperator("(%d%s)",
                                                 engine.coefficient, d1,
                                                 arg, engine, True)
                    stack.append(result)
                    digits = False
                    d1 = 0
                    d2 = 1
                    continue
                if char == "^":
                    arg = stack.pop()
                    fmt = "(%s^%d)" \
                        if isinstance(arg, (Variable, BinaryOperator)) \
                        else "((%s)^%d)"
                    result = CoefficientOperator(fmt,
                                                 engine.exponent, d1,
                                                 arg, engine, False)
                    stack.append(result)
                    digits = False
                    d1 = 0
                    d2 = 1
                    continue
                d1 += int(char) * d2
                d2 *= 10
                continue
            if char in atoms:
                stack.append(atoms[char])
                continue
            if char in unaries:
                name = names[char]
                op = unaries[char]
                arg1 = stack.pop()
                result = UnaryOperator(name, op, arg1, engine)
                stack.append(result)
                continue
            if char in binaries:
                name = names[char]
                op = binaries[char]
                arg1 = stack.pop()
                arg2 = stack.pop()
                result = BinaryOperator(name, op, arg1, arg2, engine)
                stack.append(result)
                continue
            if char in {"^", "_"}:
                digits = True
                continue
            raise ValueError(f"parse: unrecognized {char=}, {expr=}")
        if len(stack) != 1:
            raise ValueError(f"parse: stack error {len(stack)=}, {expr=}")
        wff.wff = stack.pop()
        return wff

    def print_expr(wff, expr):
        """print an expression"""
        s = f"{str(wff.number):>6}: "
        w = str(wff)
        if w[0] == '(':
            w = w[1:-1]
        s += w
        padding = 45-len(s)
        filler = " " * padding
        s += filler + expr
        padding = 79 - len(s) - len(wff.name)
        filler = " " * padding
        s += filler + wff.name
        print(s)

    def print_rule(tag, rule):
        """print a rule"""
        s = f"{str(tag):>6}: {str(rule)}"
        padding = 79 - len(s) - len(rule.name)
        filler = " " * padding
        s += filler + rule.name
        print(s)

    def is_true(result, true) -> bool:
        """is the statement true"""
        return result == true
    errors = 0

    print("Definitions:")
    e_defs = 0
    n = 1
    for item in definitions:
        name, expr = item                   # unpack
        # print(f"{name}: {expr}")            # debugging
        wff = parse(expr, name, n, "D")     # tag: D1, D2, D3, etc.
        print_expr(wff, expr)
        variables = wff.vars                # variables in the expression
        k = len(variables)
        args_in = tuple(values.keys() for _ in range(k))
        args_out = product(*args_in)
        # print(list(args_out))               # debugging
        for target in args_out:
            s = "\t"
            for i in range(k):
                x = variables[i]
                v = target[i]
                x.value = v
                s += f"|{str(x)}|={values[v]}, "
            result = wff.value
            if not is_true(result, true):
                s += f"result={values[result]}"
                print("\tnot valid:", s[1:])
                e_defs += 1
                break
        n += 1
    if e_defs > 0:
        errors += e_defs
        if e_defs == 1:
            print("\t--> One definition is not valid.")
        else:
            print(f"\t--> {e_defs} definitions are not valid.")
    else:
        print("\t--> All the definitions are valid.")

    print("Axiom Schemas:")
    e_axioms = 0
    n = 1
    for item in axioms:
        name = item[0]                      # start unpacking
        rest = item[1:]
        while rest:
            expr = rest[0]                      # continue unpacking
            rest = rest[1:]
            # print(f"{name}: {expr}")            # debugging
            wff = parse(expr, name, n, "A")     # tag: A1, A2, A3, etc.
            print_expr(wff, expr)
            variables = wff.vars                # variables in the expression
            k = len(variables)
            args_in = tuple(values.keys() for _ in range(k))
            args_out = product(*args_in)
            # print(list(args_out))               # debugging
            for target in args_out:
                s = "\t"
                for i in range(k):
                    x = variables[i]
                    v = target[i]
                    x.value = v
                    s += f"|{str(x)}|={values[v]}, "
                result = wff.value
                if not is_true(result, true):
                    s += f"result={values[result]}"
                    print("\tnot valid:", s[1:])
                    e_axioms += 1
                    break
        n += 1
    if e_axioms > 0:
        errors += e_axioms
        if e_axioms == 1:
            print("\t--> One axiom schema is not valid.")
        else:
            print(f"\t--> {e_axioms} axiom schemas are not valid.")
    else:
        print("\t--> All the axiom schemas are valid.")

    print("Rules of Transformation:")
    print("\tTo avoid stating a complicated rule for substitution of variables,")
    print("\twe treat our wffs as schemas.")
    e_rules = 0
    n = 1
    for maker in rules:
        rule = maker(engine)
        tag = f"R{n}"
        print_rule(tag, rule)
        variables = rule.vars               # variables in the expression
        k = len(variables)
        args_in = tuple(values.keys() for _ in range(k))
        args_out = product(*args_in)
        # print(list(args_out))               # debugging
        for target in args_out:
            s = "\t"
            for i in range(k):
                x = variables[i]
                v = target[i]
                x.value = v
                s += f"|{str(x)}|={values[v]}, "
            bypass = False
            # print(s)                    # debugging
            for premise in rule.premises:
                result = premise[1].value
                # print("\tPremise", premise[1], "=", values[result],
                #       "when", s[:-2]+".")   # debugging
                if not is_true(result, true):
                    bypass = True
                    break
            if bypass:
                # print("\tBypass!")          # debugging
                continue                    # does not apply to this assignment
            conclusion = rule.conclusion
            result = conclusion[1].value
            if not is_true(result, true):
                print("\t Conclusion", conclusion[1], "=", values[result],
                      "when", s[1:-2], "and premises hold.")
                e_rules += 1                # rule fails
                break
        n += 1
    if e_rules > 0:
        errors += e_rules
        if e_rules == 1:
            print("\t--> One transformation is not valid.")
        else:
            print(f"\t--> {e_rules} transformations are not valid.")
    else:
        print("\t--> All the transformations are valid.")

    print("Theorem Schemas:")
    e_theorems = 0
    n = 1
    for item in theorems:
        name = item[0]                      # start unpacking
        rest = item[1:]
        while rest:
            expr = rest[0]                      # continue unpacking
            rest = rest[1:]
            # print(f"{name}: {expr}")            # debugging
            wff = parse(expr, name, n, "T")     # tag: T1, T2, T3, etc.
            print_expr(wff, expr)
            variables = wff.vars                # variables in the expression
            k = len(variables)
            args_in = tuple(values.keys() for _ in range(k))
            args_out = product(*args_in)
            # print(list(args_out))               # debugging
            for target in args_out:
                s = "\t"
                for i in range(k):
                    x = variables[i]
                    v = target[i]
                    x.value = v
                    s += f"|{str(x)}|={values[v]}, "
                result = wff.value
                if not is_true(result, true):
                    s += f"result={values[result]}"
                    print("\tnot valid:", s[1:])
                    e_theorems += 1
                    break
        n += 1
    if e_theorems > 0:
        errors += e_theorems
        if e_theorems == 1:
            print("\t--> One theorem schema is not valid.")
        else:
            print(f"\t--> {e_theorems} theorem schemas are not valid.")
    else:
        print("\t--> All the theorem schemas are valid.")

    print("Derived Rules:")
    e_rules = 0
    n = 1
    for maker in more_rules:
        rule = maker(engine)
        tag = f"DR{n}"
        print_rule(tag, rule)
        variables = rule.vars               # variables in the expression
        k = len(variables)
        args_in = tuple(values.keys() for _ in range(k))
        args_out = product(*args_in)
        # print(list(args_out))               # debugging
        for target in args_out:
            s = "\t"
            for i in range(k):
                x = variables[i]
                v = target[i]
                x.value = v
                s += f"|{str(x)}|={values[v]}, "
            bypass = False
            # print(s)                    # debugging
            for premise in rule.premises:
                result = premise[1].value
                # print("\tPremise", premise[1], "=", values[result],
                #       "when", s[:-2]+".")   # debugging
                if not is_true(result, true):
                    bypass = True
                    break
            if bypass:
                # print("\tBypass!")          # debugging
                continue                    # does not apply to this assignment
            conclusion = rule.conclusion
            result = conclusion[1].value
            if not is_true(result, true):
                print("\t Conclusion", conclusion[1], "=", values[result],
                      "when", s[1:-2], "and premises hold.")
                e_rules += 1                # rule fails
                break
        n += 1
    if e_rules > 0:
        errors += e_rules
        if e_rules == 1:
            print("\t--> One transformation is not valid.")
        else:
            print(f"\t--> {e_rules} transformations are not valid.")
    else:
        print("\t--> All the transformations are valid.")
    print("Total number of invalid items:", errors)

def run(m):
    """run a test for a given value of m"""
    from fractions import Fraction
    L = GrigoliaExtensions(m=m)
    values = dict()
    for n in range(m):
        values[(Fraction(n,m-1),)] = n
    test(f"Ł({m})", L, (0,), (1,), values)

def one_time(f):
    added = set()
    def wrapper(m):
        m = int(m)
        if m not in added:
            result = f(m)
            added.add(m)
    return wrapper

# axiom6_added = set()

@one_time
def make_axiom6(m):
    """make the sixth axiom for Ł(m)"""
#    m = int(m)
#    if m in axiom6_added:
#        return
#    axiom6_added.add(m)
    name = f"Ł({m}) ax6"
    value = f"C_{m}_p_{m-1}_p"
    print(f"Adding axiom: {name}={value}")
    pair = (name, value)
    axioms.append(pair)

@one_time
def make_axioms7(m):
    """make all seventh axioms for Ł(m)"""
    if m < 4:
        return                  # too small
    for j in range(2, m-1):
        if (m-1)%j == 0:
            continue            # j divides m-1
        name = f"Ł({m}) ax7/{j}"
        value = f"_{m-1}_+^{j}^Np.p_{j-1}_p"
        print(f"Adding axiom: {name}={value}")
        pair = (name, value)
        axioms.append(pair)

def main(argv):
    """argument parser"""
    import argparse
    from fractions import Fraction

    def int2(m):
        """integers larger than 1"""
        m = int(m)
        if m < 2:
            raise ValueError(f"must be at least 2 (entered {m}")
        return m

    DESC = "Łukasiewicz algebras test"
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("-t", "--test", type=int2, nargs="*", \
        metavar="m", default=(3, 4), \
        help="Ł-algebras to test (integers m=2, 3, 4, ...)")
    parser.add_argument("-a", "--axioms", type=int2, nargs="*", \
        metavar="m", default=(2, 3, 4, 5), \
        help="additional Ł-algebra axioms (integers m=2, 3, 4, ...)")
    args = parser.parse_args(argv)
    # print(args)
    args.axioms = sorted(set(args.test) | set(args.axioms))
    print(args)
    for m in args.axioms:
        make_axiom6(m)
        make_axioms7(m)
    for m in args.test:
        name = f"Łukasiewicz-algebra Ł({m})"
        engine = GrigoliaExtensions(m)
        false, true = (0,), (1,)
        values = dict()
        for j in range(m):
            v = Fraction(j, m-1)
            values[(v,)] = j
        test(name, engine, false, true, values, verified=None)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
