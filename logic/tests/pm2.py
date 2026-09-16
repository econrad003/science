"""
logic.tests.pm2 - test against Principia Mathematica axioms (2nd version)
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    As a module, this program provides a method (test) which tests
    a logic system against the assumptions underlying the axiom system
    for the classical propositional calculus.

    As a main program (or demo), this program tests several different
    systems of propositional logic.

DIFFERENCES FROM PM1

    Except for the DivisorLogic module, this is essentially the same as
    logic.tests.pm1.  Depending on how well this model seems to work,
    there may be some additional tests in the database.

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
from itertools import product     # Cartesian product
from logic.wff import WFF, Constant, Variable, UnaryOperator, BinaryOperator
from logic.deductions import Rule

s_name = "PM (Principia Mathematica, 1910)"

    # primitives: Np, Apq
    # definitions
d_and = ("conjunction", ":KpqNANpNq")
d_imp = ("implication", ":CpqANpq")
d_equ = ("equivalence", ":EpqKCpqCqp")
definitions = (d_and, d_imp, d_equ)

    # axioms
a_tautology = ("tautology", "CAppp")
a_addition = ("addition", "CqApq")
a_permutation = ("permutation", "CApqAqp")
a_association = ("association", "CApAqrAqApr")
a_summation = ("summation", "CCqrCApqApr")
axioms = (a_tautology, a_addition, a_permutation,
          a_association, a_summation)

    # primitive rules
def modus_ponens(engine):
    """make a modus ponens rule"""
    TRUE = Rule.TRUE
    p = Variable("p", owner=engine)
    q = Variable("q", owner=engine)
    Cpq = WFF(owner=engine)
    Cpq.wff = Cpq.IMP(p, q)
    return Rule(TRUE(Cpq), TRUE(p), TRUE(q), name="modus ponens")

rules = (modus_ponens,)

    # other rules

def adjunction(engine):
    """make the rule"""
    TRUE = Rule.TRUE
    p = Variable("p", owner=engine)
    q = Variable("q", owner=engine)
    Kpq = WFF(owner=engine)
    Kpq.wff = Kpq.AND(p, q)
    return Rule(TRUE(p), TRUE(q), TRUE(Kpq), name="adjunction")

def modus_tollens_1(engine):
    """make the rule"""
    TRUE = Rule.TRUE
    p = Variable("p", owner=engine)
    q = Variable("q", owner=engine)
    Cpq = WFF(owner=engine)
    Cpq.wff = Cpq.IMP(p, q)
    Np = WFF(owner=engine)
    Np.wff = Np.NOT(p)
    Nq = WFF(owner=engine)
    Nq.wff = Np.NOT(q)
    return Rule(TRUE(Cpq), TRUE(Nq), TRUE(Np), name="modus tollens 1")

def modus_tollens_2(engine):
    """make the rule"""
    TRUE = Rule.TRUE
    p = Variable("p", owner=engine)
    q = Variable("q", owner=engine)
    CNpNq = WFF(owner=engine)
    CNpNq.wff = CNpNq.IMP(CNpNq.NOT(p), CNpNq.NOT(q))
    return Rule(TRUE(CNpNq), TRUE(q), TRUE(p), name="modus tollens 2")

def modus_tollens_3(engine):
    """make the rule"""
    TRUE = Rule.TRUE
    p = Variable("p", owner=engine)
    q = Variable("q", owner=engine)
    CpNq = WFF(owner=engine)
    CpNq.wff = CpNq.IMP(p, CpNq.NOT(q))
    Np = WFF(owner=engine)
    Np.wff = Np.NOT(p)
    return Rule(TRUE(CpNq), TRUE(q), TRUE(Np), name="modus tollens 3")

def modus_tollens_4(engine):
    """make the rule"""
    TRUE = Rule.TRUE
    p = Variable("p", owner=engine)
    q = Variable("q", owner=engine)
    CNpq = WFF(owner=engine)
    CNpq.wff = CNpq.IMP(CNpq.NOT(p), q)
    Nq = WFF(owner=engine)
    Nq.wff = Nq.NOT(q)
    return Rule(TRUE(CNpq), TRUE(Nq), TRUE(p), name="modus tollens 4")

def contradiction_1(engine):
    """make the rule"""
    TRUE = Rule.TRUE
    p = Variable("p", owner=engine)
    CNpp = WFF(owner=engine)
    CNpp.wff = CNpp.IMP(CNpp.NOT(p), p)
    return Rule(TRUE(CNpp), TRUE(p), name="contradiction 1")

def contradiction_2(engine):
    """make the rule"""
    TRUE = Rule.TRUE
    p = Variable("p", owner=engine)
    CpNp = WFF(owner=engine)
    CpNp.wff = CpNp.IMP(p, CpNp.NOT(p))
    Np = WFF(owner=engine)
    Np.wff = Np.NOT(p)
    return Rule(TRUE(CpNp), TRUE(Np), name="contradiction 2")

more_rules = (adjunction, modus_tollens_1,
              modus_tollens_2, modus_tollens_3, modus_tollens_4, # added
              contradiction_1,
              contradiction_2)                                   # added

    # theorems
t_reflex = ("reflexivity", "Epp")
t_symm = ("symmetry", "CEpqEqp")
t_trans = ("transitivity", "CEpqCEqrEpr")
t_monotony = ("monotony", "CEpqCNpNq",
              "CEpqCAprAqr", "CEqrCApqApr",
              "CEpqCKprKqr", "CEqrCKpqKpr",
              "CEpqCCprCqr", "CEqrCCpqCpr")

t_importC = ("importation", "CCpCqrCCpqCpr")
t_reflexC = ("identity", "Cpp")
t_antisymmC = ("antisymmetry", "CCpqCCqpEpq")
t_transC = ("transitivity", "CCpqCCqrCpr", "CEpqCEqrEpr")

t_Pierce = ("Pierce", "CCCpqpp")
t_dilemma = ("dilemma", "CCprCCqrCApqr", "CCprCCqsCApqArs")
t_import = ("importation", "CCpCqrCKpqr")
t_export = ("exportation", "CCKpqrCpCqr")

t_exclm = ("tertium non datur", "ApNp", "ACpqCqp")
t_contrad = ("contradiction", "NKpNp")
t_raa = ("reductio ad absurdum", "CCpNpNp", "CCNppp")

t_contrap = ("contraposition", "CCpqCNqNp", "CCNpNqCqp",
             "CCpNqCqNp", "CCNpqCNqp")      # added #4, #5
t_dn = ("double negation", "CpNNp", "CNNpp", "EpNNp",
        "CNNNpNp")                          # added #5

t_tautology = ("tautology", "EpApp", "EpKpp")
t_simp = ("simplification", "CpApq", "CKpqp")
t_comm = ("commutation", "EApqAqp", "EKpqKqp")
t_assoc = ("association", "EApAqrAApqr", "EKpKqrKKpqr")

t_distrib = ("distribution", "EKpAqrAKpqKpr", "EApKqrKApqApr")
t_absorp = ("absorption", "EApKpqp", "EKpApqp")

t_subset = ("subset", "CCpqEpKpq", "CEpKpqCpq",
            "CCpqEqApq", "CEqApqCpq")
t_binding = ("binding", "EApFp", "EKpTp", "ECpFNp")
t_alt = ("alternate def: Apq", "EApqCCpqq")


theorems = (t_reflex, t_symm, t_trans, t_monotony,
            t_importC, t_reflexC, t_antisymmC, t_transC,
            t_Pierce, t_dilemma, t_import, t_export,
            t_exclm, t_contrad, t_raa,
            t_contrap, t_dn,
            t_tautology, t_simp, t_comm, t_assoc,
            t_distrib, t_absorp, t_subset, t_binding, t_alt)

def test(name, engine, false, true, values, verified=None):
    """test a scenario against the assumptions"""
    print("-" * 79)
    print("     Target Engine:", name)
    print("Source Expressions:", s_name)
    print()
        # Define the operators
    NOT = engine.NOT
    AND = engine.AND
    OR = engine.OR
    IMP = engine.IMP
    EQU = engine.EQU
    DEF = engine.EQU
    F = Constant("F", false, owner=engine)
    T = Constant("T", true, owner=engine)
    p = Variable("p", owner=engine)
    q = Variable("q", owner=engine)
    r = Variable("r", owner=engine)
    s = Variable("s", owner=engine)
    atoms = {'F':F, 'T':T, 'p':p, 'q':q, 'r':r, 's':s}
    unaries = {'N':NOT}
    binaries = {'K':AND, 'A':OR, 'C':IMP, 'E':EQU, ':':DEF}
    names = {'N':'~', 'K':'∧', 'A':'∨', 'C':'⊃', 'E':'≡', ':':' := '}

    if verified == None:
        verified = lambda value: value == true

    def parse(expr, name, number, prefix):
        """create a wff"""
        wff = WFF(engine, name, number, prefix)
        stack = list()
        rpn = list(reversed(expr))
        for char in rpn:
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
                    e_defs += 1
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

if __name__ == "__main__":
        # DEMO CODE
        #   Use this as a guide to running your own tests against
        #   this database

    from fractions import Fraction
    half = Fraction(1,2)
    third = Fraction(1,3)
    twothirds = Fraction(2,3)

        # IMPORT LOGIC ENGINES

    from logic.lukasiewicz import LukasiewiczLogic as LMVPC
    from logic.godel_dummett import GodelLogic as GDMVPC
    from logic.divisors2 import DivisorLogic        # note change
        # Changes
        #   divisors1 uses the gcd as the failure handler for
        #       material implication.
        #   divisors2 uses the complementary lcm (i.e. top/lcm(p,q))
        #       as the failure handler.
        #
        #   In divisors1, in multiworld scenarios (more than 1 prime
        #   factor), material equivalence failed to be an equivalence
        #   relation.  (Transitivity failed.)
        #
        #   Primary question: Will the change save transitivity?
        #       Answer: No!
        #
        #   Observations for this setup:
        #       (1) In multiworld scenarios, PM Axiom 5 fails.
        #       (2) Transitivity fails both in multivalues (not square-free)
        #           and multiworld (more than one prime) scenarios.
        #       (3) T24.2 (lattice partial order) fails in multiworld
        #           scenarios.
        #
        #   For further study:
        #       Can we develop a more robust implication operator based
        #       on the properties grouped under T24?
        #
        #   An analysis of the results of a study of transitivity
        #   suggests that we want |top ⊃ q| = q.  This implies that
        #   divisor1 is a better candidate than divisor2.

        # PART 1. Classical propositional calculus

    name = "Ł₂ (Ł₂ ≅ PM, 2-valued Łukasiewicz algebra)"
    values = {(0,):'F', (1,):'T'}
    false = (0,)
    true = (1,)
    engine = LMVPC(m=2)
    test(name, engine, false, true, values)

        # PART 2. 3-valued Łukasiewicz algebra

    name = "Ł₃ (Ł₃ ≇ PM, 3-valued Łukasiewicz algebra)"
    values = {(0,):'F', (half,):'I', (1,):'T'}
    false = (0,)
    true = (1,)
    engine = LMVPC(m=3)
    test(name, engine, false, true, values)

        # PART 3. 4-valued Łukasiewicz algebra

    name = "Ł₄ (Ł₄ ≇ PM, 4-valued Łukasiewicz algebra)"
    values = {(0,):'F', (third,):'I', (twothirds,):'J', (1,):'T'}
    false = (0,)
    true = (1,)
    engine = LMVPC(m=4)
    test(name, engine, false, true, values)

        # PART 4. 3-valued Gödel-Dummett algebra

    name = "G₃ (G₃ ≇ PM, 3-valued Gödel-Dummett algebra)"
    values = {(0,):'F', (half,):'I', (1,):'T'}
    false = (0,)
    true = (1,)
    engine = GDMVPC(m=3)
    test(name, engine, false, true, values)

        # PART 5. 4-valued Gödel-Dummett algebra

    name = "G₄ (G₄ ≇ PM, 4-valued Gödel-Dummett algebra)"
    values = {(0,):'F', (third,):'I', (twothirds,):'J', (1,):'T'}
    false = (0,)
    true = (1,)
    engine = GDMVPC(m=4)
    test(name, engine, false, true, values)

        # PART 6. Divisor lattice for n=4
        #
        #                   4
        #                   |
        #                   2
        #                   |
        #                   1
        

    name = "ℒ(4) (lattice of divisors of 4, i.e. {1, 2, 4})"
    values = {}
    for value in {1,2,4}:
        values[value] = str(value)
    false = 1
    true = 4
    engine = DivisorLogic(4)
    test(name, engine, false, true, values) 

        # PART 7. Divisor lattice for n=6
        #
        #                   6
        #                  / \
        #                 2   3
        #                  \ /
        #                   1

    name = "ℒ(6) (lattice of divisors of 6, i.e. {1, 2, 3, 6})"
    values = {}
    for value in {1,2,3,6}:
        values[value] = str(value)
    false = 1
    true = 6
    engine = DivisorLogic(6)
    test(name, engine, false, true, values) 

        # PART 8. Divisor lattice for n=30
        #
        #   top            30
        #                 / | \
        #   coprimes     6 10 15 
        #                |\/ \/|
        #                |/\ /\|
        #   primes       2  3  5
        #                 \ | /
        #                  \|/
        #   bottom          1

    name = "ℒ(30) (lattice of divisors of 30)"
    values = {}
    false = 1
    true = 30
    engine = DivisorLogic(30)
    for value in engine.lattice:
        values[value] = str(value)
    test(name, engine, false, true, values) 

        # PART 9. Divisor lattice for n=60
        #
        #   top            60
        #                 / | \
        #   coprimes    12 20 30
        #               /\   \/ \     also 4-->20, 6-->30
        #   planes     4  6  10 15 
        #               \/ \  \ /     also 2-->10, 3-->15
        #   primes       2  3  5
        #                 \ | /
        #                  \|/
        #   bottom          1

    name = "ℒ(60) (lattice of divisors of 60)"
    values = {}
    false = 1
    true = 60
    engine = DivisorLogic(60)
    for value in engine.lattice:
        values[value] = str(value)
    test(name, engine, false, true, values) 
