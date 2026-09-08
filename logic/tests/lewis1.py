"""
logic.tests.lewis - calculus of strict implementation (Lewis/Langford modal systems)
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

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

from logic.boolean import BooleanLogic as BL
from logic.wff import WFF, Constant, Variable, UnaryOperator
from logic.deductions import Rule

letters = set("abcdefghijklmnopqrstuvwxyz")

class BasicParser(object):
    """makes wffs"""

    def __init__(self, engine, Tarski=False, false=0, debug=False):
        """set up the wffer"""
        self.engine = engine
        self.Tarski = Tarski            # Are the Tarski operators supported
        self.false = Constant("ϝ", false, owner=self.engine)
        true = self.engine.NOT(false)
        self.true = Constant("𝜏", true, owner=self.engine)
        self.variables = {}
        self.debug = debug

    def make_wff(self, statement, name=None, number=None, prefix=None):
        """create a wff (main entry point)"""
        wff = WFF(self.engine, name=name, number=number, prefix=prefix)
        self.tokens = list(statement)
        self.stack = list()
        if self.debug:
            print("Statement:", statement)
        while self.tokens:
            self.token = self.tokens.pop()
            if self.debug:
                print("\tToken:", self.token)
            if self.unary(wff):
                continue                # unary operator token processed
            if self.binary(wff):
                continue                # binary operator token processed
            if self.constant():
                continue                # constant token processed
            if self.letter():
                continue                # variable token processed
            raise ValueError(f"bad token {self.token}")
        if len(self.stack) != 1:
            print("Statement parse error:", statement)
            raise ValueError(f"stack length = {len(self.stack)} != 1")
        wff.wff = self.stack.pop()
        return wff

    def unary(self, wff) -> bool:
        """process a unary operator

        If the active token is a unary operator, it is processed, the
        updated wff is pushed, and True is returned.

        Otherwise the token is ignored and False is returned.

        Operators:
            N - negation
            M, P - necessity, possibility (multiple worlds - Lewis)
            S, W - necessity, possibility (multivalued - Tarski)
        """
        if self.token == 'N':           # NOT
            arg = self.stack.pop()
            arg = wff.NOT(arg)
            self.stack.append(arg)
            return True
        if self.token == 'M':           # NECESSARILY (Lewis)
            arg = self.stack.pop()
            arg = wff.NECESSARILY(arg)
            self.stack.append(arg)
            return True
        if self.token == 'P':           # POSSIBLY (Lewis)
            arg = self.stack.pop()
            arg = wff.POSSIBLY(arg)
            self.stack.append(arg)
            return True
        if not self.Tarski:
            return False
        if self.token == 'S':           # STRUE (necessary - Tarski)
            arg = stack.pop()
            arg = wff.STRUE(arg)
            self.stack.append(arg)
            return True
        if self.token == 'W':           # WTRUE (possible - Tarski)
            arg = self.stack.pop()
            arg = wff.WTRUE(arg)
            self.stack.append(arg)
            return True
        return False

    def binary(self, wff) -> bool:
        """process a binary operator

        If the active token is a binary operator, it is processed, the
        updated wff is pushed, and True is returned.

        Otherwise the token is ignored and False is returned.

        Operators:
            K, A, X - conjunction, disjunction, exclusive disjunction
            C, E - material implication and equivalence
            : - a definition (treated as a material equivalence)
                intended mainly for notational purposes
            S, = - strict implication and equivalence
        """
        if self.token == 'K':           # AND (conjunction)
            arg1 = self.stack.pop()
            arg2 = self.stack.pop()
            arg = wff.AND(arg1, arg2)
            self.stack.append(arg)
            return True
        if self.token == 'A':           # OR (disjunction, alternation)
            arg1 = self.stack.pop()
            arg2 = self.stack.pop()
            arg = wff.OR(arg1, arg2)
            self.stack.append(arg)
            return True
        if self.token == 'X':           # XOR (exclusive disjunction)
            arg1 = self.stack.pop()
            arg2 = self.stack.pop()
            arg = wff.XOR(arg1, arg2)
            self.stack.append(arg)
            return True
        if self.token == 'C':           # IMP (material implication)
            arg1 = self.stack.pop()
            arg2 = self.stack.pop()
            arg = wff.IMP(arg1, arg2)
            self.stack.append(arg)
            return True
        if self.token == 'E':           # EQU (material equivalence)
            arg1 = self.stack.pop()
            arg2 = self.stack.pop()
            arg = wff.EQU(arg1, arg2)
            self.stack.append(arg)
            return True
        if self.token == ':':           # DEF (definition - material equivalence)
            arg1 = self.stack.pop()
            arg2 = self.stack.pop()
            arg = wff.DEF(arg1, arg2)
            self.stack.append(arg)
            return True
        if self.token == 'I':           # SIMP (strict implication)
            arg1 = self.stack.pop()
            arg2 = self.stack.pop()
            arg = wff.SIMP(arg1, arg2)
            self.stack.append(arg)
            return True
        if self.token == '=':           # SEQU (strict implication)
            arg1 = self.stack.pop()
            arg2 = self.stack.pop()
            arg = wff.SEQU(arg1, arg2)
            self.stack.append(arg)
            return True
        return False

    def constant(self):
        """propositional constants

        Operators:
            F - false in all worlds
            T - true in all worlds
        """
        if self.token == "F":
            self.stack.append(self.false)
            return True
        if self.token == "T":
            self.stack.append(self.true)
            return True
        return False

    def letter(self):
        """propositional variables

        Lower case letters are accepted.
        """
        if self.token not in letters:
            return False
        if self.token not in self.variables:
            self.variables[self.token] = Variable(self.token, self.engine)
        self.stack.append(self.variables[self.token])
        return True

def self_test(debug=False):
    """quick check to make sure things are in reasonable working order"""
    if debug:
        print("Selftest...")
    boole = BL(1)
    parser = BasicParser(boole, debug=debug)
    wff = parser.make_wff("p")
    assert str(wff) == "p"
    wff = parser.make_wff("Cpq")
    assert str(wff) == "(p⊃q)"
    wff = parser.make_wff("EKpqNANpNq")
    assert str(wff) == "((p∧q)≡~(~p∨~q))"
    wff = parser.make_wff(":IpqMCpq")
    assert str(wff) == "((p→q) := □(p⊃q))"
    wff = parser.make_wff("=MpNPNp")
    assert str(wff) == "(□p⇔~◇~p)"
    print("lewis1: selftest passed!")

def positive_int(n:str) -> int:
    """validates a positive integer"""
    n = int(n)
    if n < 1:
        raise ValueError("must be positive")
    return n

def build_logic(args):
    """builds the logic model"""
    if args.necessary >= 2 ** args.worlds:
        print("necessary value exceeds maximum, assuming maximum")
        args.necessary >= 2 ** args.worlds - 1
    if args.necessary % 2 != 1:
        raise ValueError("necessary value is even, □p won't be actually true")
    class MyBL(BL):
        """modify the necessity operator"""
        def NECESSARILY(self, p:int) -> int:
            """necessity"""
            return args.necessary if p==self.T else 0
    return MyBL(args.worlds)

wffs = {'A1':('commutativity', "IKpqKqp"),
        'A2':('simplification', "IKpqp"),
        'A3':('tautology', "IpKpp"),
        'A4':('associativity', "IKKpqrKpKqr"),
        'A5':('double negation', "IpNNp"),
        'A6':('hypothetical syllogism', "IKIpqIqrIpr"),
        'A7':('modus ponens', "IKpIpqq"),
        'A8':('consistency (S2)', "IPKpqPp"),
        'B8':('consistency (S3)', "IIpqIPpPq"),
        'C0':('axiom (S4)', "IMpMMp"),
        'C1':('axiom (S5)', "IPpMPp"),
        'C2':('axiom (S5)', "IpMPp"),
        'C3':('Brouwer (S6/S7/S8)', "PPp"),
        'D1':('disjunction', ":ApqNKNpNq"),
        'D2':('material implication', ":CpqNKpNq"),
        'D3':('material equivalence', ":EpqKCpqCqp"),
        'D4':('strict implication', ":IpqNPKpNq"),
        'D5':('strict equivalence', ":=pqKIpqIqp"),
        'D6':('necessity', ":MpNPNp"),
    }

def parse_args(argv):
    """parse command line arguments"""
    import argparse

    DESC = "Many worlds modelling"
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("-n", "--worlds", type=positive_int, default=3,
                        help="number of worlds [3]")
    parser.add_argument("--necessary", type=positive_int, default=1,
                        help="return value for □p when p is necessary [1]")
    args = parser.parse_args(argv)
    print(args)
    return args

def pr(label, wff, str_Polish, name):
    """print the wff"""
    def padding(s, n):
        """pad with spaces"""
        if len(s) >= n:
            return s + " "
        return s + " " * (n - len(s))
    sw = str(wff)
    if sw[0] == "(":
        sw = sw[1:-1]           # remove outer parentheses
    s = label + ": " + sw
    s = padding(s, 35) + str_Polish
    filler = " " * (79 - len(s) - len(name))
    print(s + filler + name)

def process_wff(parser, name, str_Polish, label):
    """build a wff for testing"""
    prefix, number = label[0], int(label[1:])
    wff = parser.make_wff(str_Polish,
                          name=name, prefix=prefix, number= number)
    pr(label, wff, str_Polish, name)

def process_args(args, model=build_logic, Parser=BasicParser):
    """process the arguments"""
    engine = model(args)            # the basic logic model
    parser = Parser(engine)         # the wff builder
    axioms = list(sorted(wffs.keys()))
    for axiom in axioms:
        name, str_Polish = wffs[axiom]
        process_wff(parser, name, str_Polish, axiom) 

if __name__ == "__main__":
    import sys

    self_test(False)
    process_args(parse_args(sys.argv[1:]))
    print("lewis1: done!")
