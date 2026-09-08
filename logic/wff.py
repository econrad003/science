"""
logic.wff - well-formed formulas in propositional calculus
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

    # forward references

LogicDef = 'LogicDefinitions'
TruthValue = 'TruthValue'
Operator = 'Operator'
WFFx = 'WFF'

class Constant(object):
    """a nullary operator with a fixed value"""

    __slots__ = ("__name", "__value")

    def __init__(self, name:str, value:TruthValue, owner:LogicDef=None):
        """constructor"""
        if owner:
            owner.defined(value)        # make sure the value is defined
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        """name getter"""
        return self.__name

    @property
    def value(self) -> TruthValue:
        """value getter"""
        return self.__value

    def __str__(self):
        """string value for printing a wff"""
        return self.__name

class Variable(object):
    """a nullary operator whose value must be set and can be changed"""

    __slots__ = ("__name", "__value", "__owner")

    def __init__(self, name:str, owner:callable=None):
        """constructor"""
        self.__name = name
        self.__owner = owner

    @property
    def name(self) -> str:
        """name getter"""
        return self.__name
        return 

    @property
    def value(self) -> TruthValue:
        """value getter

        A ValueError exception is raised if the value is not set.
        """
        try:
            return self.__value
        except NameError:
            raise ValueError(f"variable {self.name} is undefined")

    @value.setter
    def value(self, result:TruthValue):
        """value setter"""
        if self.__owner:
            self.__owner.defined(result)    # make sure the value is defined
        self.__value = result

    @value.deleter
    def value(self):
        del self.__value

    def __str__(self):
        """string value for printing a wff"""
        return self.__name

    def __lt__(self, other):
        """lexical order"""
        return str(self) < str(other)

class UnaryOperator(object):
    """a unary operator"""

    __slots__ = ("__name", "__op", "__owner", "__arg")

    def __init__(self, name:str, op:TruthValue,
                 arg:WFFx, owner:LogicDef=None):
        """constructor"""
        self.__name = name
        self.__op = op
        self.__arg = arg
        self.__owner = owner

    @property
    def name(self) -> str:
        """name getter"""
        return self.__name

    @property
    def value(self) -> TruthValue:
        """value getter"""
        value = self.__op(self.__arg.value)
        if self.__owner:
            self.__owner.defined(value, var=str(self))
        return value

    def __str__(self):
        """string value for printing a wff"""
        return self.__name + str(self.__arg)

    @property
    def arg(self):
        """return the argument"""
        return self.__arg

class BinaryOperator(object):
    """a Binary operator"""

    __slots__ = ("__name", "__op", "__arg1", "__arg2", "__owner")

    def __init__(self, name:str, op:TruthValue,
                 arg1:WFFx, arg2:WFFx, owner:LogicDef=None):
        """constructor"""
        self.__name = name
        self.__op = op
        self.__arg1 = arg1
        self.__arg2 = arg2
        self.__owner = owner

    @property
    def name(self) -> str:
        """name getter"""
        return self.__name

    @property
    def value(self) -> TruthValue:
        """value getter"""
        value = self.__op(self.__arg1.value, self.__arg2.value)
        if self.__owner:
            self.__owner.defined(value, var=str(self))
        return value

    def __str__(self):
        """string value for printing a wff"""
        return '(' + str(self.__arg1) + self.__name + str(self.__arg2) + ')'

    @property
    def arg1(self):
        """return the first argument"""
        return self.__arg1

    @property
    def arg2(self):
        """return the second argument"""
        return self.__arg2

_EXPRS = (Constant, Variable, UnaryOperator, BinaryOperator)

class WFF(object):
    """well-formed formulas"""

    NUMBER = 0
    PREFIX = 'wff'
    EXPRS = _EXPRS

    __slots__ = ("__wff", "__vars", "__owner", "__name", "__number") 

    def __init__(self, owner, name:str=None,
                 number:int=None, prefix:str=None):
        """constructor"""
        if number == None:
            number = self.new_number()
        if prefix == None:
            prefix = self.PREFIX
        self.__number = str(prefix) + str(number)
        self.__owner = owner
        self.__name = name if name else str()

    @classmethod
    def new_number(cls) -> int:
        """get the next number"""
        cls.NUMBER += 1
        return cls.NUMBER

    def constant(self, name, value) -> Constant:
        """make a constant"""
        return Constant(name, value, self.__owner)

    @property
    def number(self) -> str:
        """get the number"""
        return self.__number

    @property
    def owner(self):
        """returns the owner (or parent) object"""
        return self.__owner

    @property
    def name(self) -> str:
        """get the name"""
        return self.__name

    @property
    def wff(self) -> _EXPRS:
        """returns the wff object"""
        return self.__wff

    def extract_vars(self):
        """collect the variables in the wff"""
        self.__vars = set()
        stack = []
        stack.append(self.wff)
        while(stack):
            top = stack.pop()
            self.extract_top(top, stack)

    def extract_top(self, top, stack):
        """process the top of stack for extract_vars"""
        # print("\t>", top)               # for testing
        if type(top) == BinaryOperator:
            stack.append(top.arg1)
            stack.append(top.arg2)
            return
        if type(top) == UnaryOperator:
            stack.append(top.arg)
            return
        if type(top) == Variable:
            self.__vars.add(top)
            return
        if type(top) == Constant:
            return              # nothing to do
        raise TypeError("Unknown expression type (extract_vars)")

    @property
    def vars(self):
        """return the variables in the exression"""
        return list(self.__vars)

    @wff.setter
    def wff(self, expr:WFFx):
        """sets the wff object"""
        if not isinstance(expr, self.EXPRS):
            raise TypeError("Invalid WFF")
        self.__wff = expr
        self.extract_vars()

    def __str__(self):
        """string form"""
        return str(self.__wff)

    def NOT(self, expr) -> WFFx:
        """Negate an expression"""
        if not isinstance(expr, self.EXPRS):
            raise TypeError("Invalid WFF")
        return UnaryOperator('~', self.owner.NOT, expr, self.owner)

    def NECESSARILY(self, expr) -> WFFx:
        """Necessitate an expression (Lewis)"""
        if not isinstance(expr, self.EXPRS):
            raise TypeError("Invalid WFF")
        return UnaryOperator('□', self.owner.NECESSARILY, expr, self.owner)

    def POSSIBLY(self, expr) -> WFFx:
        """Make an expression contingent (Lewis)"""
        if not isinstance(expr, self.EXPRS):
            raise TypeError("Invalid WFF")
        return UnaryOperator('◇', self.owner.POSSIBLY, expr, self.owner)

    def STRUE(self, expr) -> WFFx:
        """Necessitate an expression (Tarski)"""
        if not isinstance(expr, self.EXPRS):
            raise TypeError("Invalid WFF")
        return UnaryOperator('S', self.owner.STRUE, expr, self.owner)

    def WTRUE(self, expr) -> WFFx:
        """Make an expression possible (Tarski)"""
        if not isinstance(expr, self.EXPRS):
            raise TypeError("Invalid WFF")
        return UnaryOperator('W', self.owner.WTRUE, expr, self.owner)

    def AND(self, expr1, expr2) -> WFFx:
        """Conjunction"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('∧', self.owner.AND, expr1, expr2, self.owner)

    def OR(self, expr1, expr2) -> WFFx:
        """Disjunction"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('∨', self.owner.OR, expr1, expr2, self.owner)

    def XOR(self, expr1, expr2) -> WFFx:
        """Exclusive disjunction"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('⊻', self.owner.XOR, expr1, expr2, self.owner)

    def IMP(self, expr1, expr2) -> WFFx:
        """Material implication"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('⊃', self.owner.IMP, expr1, expr2, self.owner)

    def EQU(self, expr1, expr2) -> WFFx:
        """Material equivalence"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('≡', self.owner.EQU, expr1, expr2, self.owner)

    def DEF(self, expr1, expr2) -> WFFx:
        """definition"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator(' := ', self.owner.EQU, expr1, expr2, self.owner)

    def SIMP(self, expr1, expr2) -> WFFx:
        """Strict implication"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('→', self.owner.SIMP, expr1, expr2, self.owner)

    def SEQU(self, expr1, expr2) -> WFFx:
        """Strict equivalence"""
        if not isinstance(expr1, self.EXPRS):
            raise TypeError("Invalid WFF 1")
        if not isinstance(expr2, self.EXPRS):
            raise TypeError("Invalid WFF 2")
        return BinaryOperator('⇔', self.owner.SEQU, expr1, expr2, self.owner)

    @property
    def value(self):
        """returns the truth value"""
        return self.wff.value

if __name__ == "__main__":
    from fractions import Fraction
    from logic.lukasiewicz import LukasiewiczLogic as LL

    def center(text:str, cols=80):
        """center text in a line"""
        n = len(text)
        filler = " " * ((cols-n) // 2)
        print(filler + text)

    def justify(left:str, right:str, cols=80):
        """fill the middle"""
        if right:
            n = len(left) + len(right)
            filler = " " * (cols - n - 1)
            print(left + filler + right)
        else:
            print(left)

    def pr(wff):
        """display the wff"""
        expr = str(wff)
        if expr[0] == '(':
            expr = expr[1:-1]
        justify(f"{wff.number}. {expr}", wff.name)

    def permutations(expr, values):
        """generate the permutations"""
        m = len(expr.vars)
        k = len(values)
        n = k**m
        settings = list()
        for i in range(n):
            h = i
            setting = list()
            for x in expr.vars:
                j = h % k
                pair = x, values[j]
                setting.append(pair)
                h //= k
            settings.append(setting)
            # print(i, setting)
        return settings

    def print_permutations(expr, values, VALUES):
        """display the settings - for testing"""
        # print(values)
        # print(VALUES)
        settings = permutations(expr, values)
        for setting in settings:
            s = "\t"
            for pair in setting:
                x, t = pair
                s += str(x) + ':' + VALUES.get(t, str(t)) + ", "
            print(s[:-2])

    def is_weakly_valid(expr, values, VALUES, truth=1):
        """test whether a statement is always true in this world"""
        settings = permutations(expr, values)
        for setting in settings:
            for pair in setting:
                x, t = pair
                x.value = t         # set the variable
            value = expr.wff.value
            if value[0] == truth:
                continue
            s = "\t>"
            for pair in setting:
                x, t = pair
                s += str(x) + ':' + VALUES.get(t, str(t)) + ", "
            s +=  "expr:" + VALUES.get(value, str(value))
            print(s)
            return False
        return True

    def is_strongly_valid(expr, values, VALUES, truth=1):
        """test whether a statement is always necessarily true"""
        settings = permutations(expr, values)
        for setting in settings:
            for pair in setting:
                x, t = pair
                x.value = t         # set the variable
            value = expr.wff.value
            ok = True
            for item in value:
                if item != truth:
                    ok = False
                    break
            if ok:
                continue
            s = "\t>"
            for pair in setting:
                x, t = pair
                s += str(x) + ':' + VALUES.get(t, str(t)) + ", "
            s +=  f"{str(expr)}:" + VALUES.get(value, str(value))
            print(s)
            return False
        return True

    print("successfully compiled...")

    print()
    print("="*79)
    print()

    center("Ł₃ — Łukasiewicz 3-valued logic")
    L3 = LL()
    print("declaring propositional constants...")
    half = Fraction(1,2)
    VALUES = {(0,):'F', (half,):'I', (1,):'T'}
    values = [(0,), (half,), (1,)]
    eff = Constant("ϝ", (0,))

    print("declaring propositional variables...")
    p = Variable("p", L3)
    q = Variable("q", L3)
    r = Variable("r", L3)
    print(f"variables: {p}, {q}, {r}")
    print("primitive operators: '⊃'")

    print("definitions...")
    df1 = WFF(L3, prefix="Df", number=1, name="negation")
    df1.wff = df1.DEF(df1.NOT(p), df1.IMP(p, eff))
    pr(df1)
    # print("variables:", *tuple(str(x) for x in df1.vars))   # for testing
    assert set(df1.vars) == {p}

    df2 = WFF(L3, prefix="Df", number=2, name="disjunction")
    df2.wff = df2.DEF(df2.OR(p, q), df2.IMP(df2.IMP(p, q), q))
    pr(df2)
    # print("variables:", *tuple(str(x) for x in df2.vars))   # for testing
    assert set(df2.vars) == {p, q}

    df3 = WFF(L3, prefix="Df", number=3, name="conjunction")
    df3.wff = df3.DEF(df3.AND(p, q), df3.NOT(df3.OR(df3.NOT(p), df3.NOT(q))))
    pr(df3)

    df4 = WFF(L3, prefix="Df", number=4, name="material equivalence")
    df4.wff = df4.DEF(df4.EQU(p, q), df4.AND(df4.IMP(p, q), df4.IMP(q, p)))
    pr(df4)

    definitions = [df1, df2, df3, df4]
    for df in definitions:
        assert is_strongly_valid(df, values, VALUES), f'ERROR: {str(df)}'
    print("\t\t> definitions... OK!")

    print("declaring axioms (Wajsberg, 1931)...")
    ax1 = WFF(L3, prefix="Ax", number=1, name="simplification (exported)")
    ax1.wff = ax1.IMP(p, ax1.IMP(q, p))
    pr(ax1)

    ax2 = WFF(L3, prefix="Ax", number=2, name="hypothetical syllogism")
    ax2.wff = ax2.IMP(ax2.IMP(p, q), ax2.IMP(ax2.IMP(q, r), ax2.IMP(p, r)))
    pr(ax2)
    # print_permutations(ax2, values, VALUES)             # for testing

    ax3 = WFF(L3, prefix="Ax", number=3, name="Ł₃-Pierce")
    ax3.wff = ax3.IMP(ax3.IMP(ax3.IMP(p, ax3.NOT(p)), p), p)
    pr(ax3)

    ax4 = WFF(L3, prefix="Ax", number=4, name="contrapositive")
    ax4.wff = ax4.IMP(ax4.IMP(ax4.NOT(q), ax4.NOT(p)), ax4.IMP(p, q))
    pr(ax4)

    axioms = [ax1, ax2, ax3, ax4]
    for ax in axioms:
        assert is_strongly_valid(ax, values, VALUES), f'ERROR: {str(ax)}'
    print("\t\t> axioms... OK!")

    print("some theorems...")
    th1 = WFF(L3, prefix="Th", number=1, name="identity")
    th1.wff = th1.IMP(p, p)
    pr(th1)

    th2 = WFF(L3, prefix="Th", number=2)
    th2.wff = th2.IMP(th2.IMP(th2.IMP(p, q), q), th2.IMP(th2.IMP(q, p), p))
    pr(th2)

    th3 = WFF(L3, prefix="Th", number=3, name="exportation")
    th3.wff = th3.IMP(th3.IMP(th3.AND(p,q),r),th3.IMP(p,th3.IMP(q,r)))
    pr(th3)

    d1 = WFF(L3, prefix="D", number=1, name="distributivity")
    d1.wff = d1.EQU(d1.AND(p,d1.OR(q,r)),d1.OR(d1.AND(p,q),d1.AND(p,r)))
    pr(d1)

    d2 = WFF(L3, prefix="D", number=2, name="distributivity")
    d2.wff = d2.EQU(d2.OR(p,d2.AND(q,r)),d2.AND(d2.OR(p,q),d2.OR(p,r)))
    pr(d2)

    theorems = [th1, th2, th3, d1, d2]
    for th in theorems:
        assert is_strongly_valid(th, values, VALUES), f'ERROR: {str(th)}'
    print("\t\t> theorems... OK!")

    print("some important contingent wffs...")
    wff1 = WFF(L3, name="excluded middle")
    wff1.wff = wff1.OR(p, wff1.NOT(p))
    pr(wff1)

    wff2 = WFF(L3, name="reductio ad absurdum")
    wff2.wff = wff2.IMP(wff2.IMP(p, wff2.NOT(p)), wff2.NOT(p))
    pr(wff2)

    wff3 = WFF(L3, name="importation")
    wff3.wff = wff3.IMP(wff3.IMP(p, wff3.IMP(q,r)), wff3.IMP(wff3.AND(p,q),r))
    pr(wff3)

    d3 = WFF(L3, prefix="D", number=3, name="distributivity")
    d3.wff = d3.IMP(d3.IMP(p,d3.IMP(q,r)),d3.IMP(d3.IMP(p,q),d3.IMP(p,r)))
    pr(d3)
    print("\tNOTE: D3 and Ax1 are important for proving a deduction theorem.")

    nontheorems = [wff1, wff2, wff3, d3]
    for wef in nontheorems:
        assert not is_strongly_valid(wef, values, VALUES), f'ERROR: {str(wef)}'
    print("\t\t> contingent expressions... OK!")

    print()
    print("NOTE:")
    print("    Ł₃ does not support \"natural\" deduction.")
    print("    For example:")
    hyp1 = WFF(L3)
    hyp1.wff = hyp1.IMP(p,hyp1.IMP(q,r))
    hyp2 = WFF(L3)
    hyp2.wff = hyp2.IMP(p,q)
    print(f"        Assume that {hyp1}, {hyp2} and {p} are true.")
    imp3 = WFF(L3)
    imp3.wff = imp3.IMP(q,r)
    print(f"        Since {p} is true, by modus ponens, {imp3} and {q} are true.")
    print(f"        Then, since {q} is true, by modus ponens, {r} is also true.")
    print(f"    We have verified the following deduction:")
    justify(f"        If {hyp1}, {hyp2} and {p} are true, then {r} is also true.",
            "(1)")
    print(f"    With natural deduction, we would have:")
    imp4 = WFF(L3)
    imp4.wff = imp4.IMP(p,r)
    justify(f"        If {hyp1} and {hyp2} are true, then {imp4} is also true.",
            "(2)")
    imp5 = WFF(L3)
    imp5.wff = imp5.IMP(imp5.IMP(q,r),imp5.IMP(p,r))
    justify(f"        If {hyp1} is true, then {imp5} is also true.",
            "(3)")
    justify(f"        {d3} is true.",
            "(4)")
    print(f"    But {d3} [D3] is not valid in Ł₃.")
    print(f"    If {p} and {q} are intermediate and {r} is false, then",
          "D3 is intermediate.")

    print()
    print("REMARK:")
    print("    A system containing Ax1, D3 and modus ponens supports",
          "natural deduction.")

    print()
    print("="*79)
    print()

    del L3
    center("Ł₃/2 — Łukasiewicz 3-valued logic")
    center("two worlds satisfying the Brouwerian axiom")
    L3b = LL(n=2)
    print("declaring propositional constants...")
    VALUES = {(0,0):'FF', (0,half):'FI', (0,1):'FT',
              (half,0):'IF', (half,half):'II', (half,1):'IT',
              (1,0):'TF', (1,half):'TI', (1,1):'TT'}
    values = [(0,0), (0,half), (0,1),
              (half,0), (half,half), (half,1),
              (1,0), (1,half), (1,1)]
    eff = Constant("ϝ", (0,0))

    print("declaring propositional variables...")
    p = Variable("p", L3b)
    q = Variable("q", L3b)
    r = Variable("r", L3b)
    print(f"variables: {p}, {q}, {r}")
    print("primitive operators: '⊃', '□'")

    print("definitions...")
    df1 = WFF(L3b, prefix="Df", number=1, name="negation")
    df1.wff = df1.DEF(df1.NOT(p), df1.IMP(p, eff))
    pr(df1)
    # print("variables:", *tuple(str(x) for x in df1.vars))   # for testing
    assert set(df1.vars) == {p}

    df2 = WFF(L3b, prefix="Df", number=2, name="disjunction")
    df2.wff = df2.DEF(df2.OR(p, q), df2.IMP(df2.IMP(p, q), q))
    pr(df2)
    # print("variables:", *tuple(str(x) for x in df2.vars))   # for testing
    assert set(df2.vars) == {p, q}

    df3 = WFF(L3b, prefix="Df", number=3, name="conjunction")
    df3.wff = df3.DEF(df3.AND(p, q), df3.NOT(df3.OR(df3.NOT(p), df3.NOT(q))))
    pr(df3)

    df4 = WFF(L3b, prefix="Df", number=4, name="material equivalence")
    df4.wff = df4.DEF(df4.EQU(p, q), df4.AND(df4.IMP(p, q), df4.IMP(q, p)))
    pr(df4)

    df5 = WFF(L3b, prefix="Df", number=5, name="strict implication")
    df5.wff = df5.DEF(df5.SIMP(p, q), df5.NECESSARILY(df5.IMP(p, q)))
    pr(df5)

    df6 = WFF(L3b, prefix="Df", number=6, name="strict equivalence")
    df6.wff = df6.DEF(df6.SEQU(p, q), df6.AND(df6.SIMP(p, q), df6.SIMP(q, p)))
    pr(df6)

    df7 = WFF(L3b, prefix="Df", number=5, name="possibility")
    df7.wff = df7.DEF(df7.POSSIBLY(p), df7.NOT(df7.NECESSARILY(df7.NOT(p))))
    pr(df7)

    definitions = [df1, df2, df3, df4, df5, df6, df7]
    for df in definitions:
        assert is_strongly_valid(df, values, VALUES), f'ERROR: {str(df)}'
    print("\t\t> definitions... OK!")

    print("declaring Ł₃ axioms (Wajsberg, 1931)...")
    ax1 = WFF(L3b, prefix="Ax", number=1, name="simplification (exported)")
    ax1.wff = ax1.IMP(p, ax1.IMP(q, p))
    pr(ax1)

    ax2 = WFF(L3b, prefix="Ax", number=2, name="hypothetical syllogism")
    ax2.wff = ax2.IMP(ax2.IMP(p, q), ax2.IMP(ax2.IMP(q, r), ax2.IMP(p, r)))
    pr(ax2)
    # print_permutations(ax2, values, VALUES)             # for testing

    ax3 = WFF(L3b, prefix="Ax", number=3, name="Ł₃-Pierce")
    ax3.wff = ax3.IMP(ax3.IMP(ax3.IMP(p, ax3.NOT(p)), p), p)
    pr(ax3)

    ax4 = WFF(L3b, prefix="Ax", number=4, name="contrapositive")
    ax4.wff = ax4.IMP(ax4.IMP(ax4.NOT(q), ax4.NOT(p)), ax4.IMP(p, q))
    pr(ax4)

    axioms = [ax1, ax2, ax3, ax4]
    for ax in axioms:
        assert is_strongly_valid(ax, values, VALUES), f'ERROR: {str(ax)}'
    print("\t\t> axioms... OK!")

    print("candidate Ł₃/2 axioms...")

    ax5 = WFF(L3b, prefix="X", number=5, name="simplification (exported)")
    ax5.wff = ax5.SIMP(p, ax5.SIMP(q, p))
    pr(ax5)
    assert not is_weakly_valid(ax5, values, VALUES)
    print('\t> NOT VALID!')

    lw1 = WFF(L3b, prefix='Lw', number=1, name="simplification")
    lw1.wff = lw1.SIMP(lw1.AND(p,q), p)
    pr(lw1)
    assert is_weakly_valid(lw1, values, VALUES)
    print('\t> VALID!')

    lw2 = WFF(L3b, prefix='Lw', number=2, name="commutativity")
    lw2.wff = lw2.SIMP(lw2.AND(p,q), lw2.AND(q,p))
    pr(lw2)
    assert is_weakly_valid(lw2, values, VALUES)
    print('\t> VALID!')

    lw3 = WFF(L3b, prefix='Lw', number=3, name="associativity")
    lw3.wff = lw3.SIMP(lw3.AND(p,lw3.AND(q,r)), lw3.AND(lw3.AND(p,q),r))
    pr(lw3)
    assert is_weakly_valid(lw2, values, VALUES)
    print('\t> VALID!')

    ax6 = WFF(L3b, prefix='X', number=6, name="modus ponens (exported)")
    ax6.wff = ax6.SIMP(p, ax6.SIMP(ax6.SIMP(p,q),q))
    pr(ax6)
    assert not is_weakly_valid(ax6, values, VALUES)
    print('\t> NOT VALID!')

    ax7 = WFF(L3b, prefix='X', number=7, name="modus ponens (imported)")
    ax7.wff = ax7.SIMP(ax7.AND(p, ax7.SIMP(p,q)),q)
    pr(ax7)
    assert not is_weakly_valid(ax7, values, VALUES)
    print('\t> NOT VALID!  (but valid in Lewis S2)')

    lw4 = WFF(L3b, prefix="Lw", number=4,
              name="hypothetical syllogism (exported)")
    lw4.wff = lw4.SIMP(lw4.SIMP(p,q), lw4.SIMP(lw4.SIMP(q,r), lw4.SIMP(p,r)))
    pr(lw4)
    assert is_weakly_valid(lw4, values, VALUES)
    print('\t> VALID!')

    lw5 = WFF(L3b, prefix="Lw", number=5,
              name="hypothetical syllogism (imported)")
    lw5.wff = lw5.SIMP(lw5.AND(lw5.SIMP(p,q), lw5.SIMP(q,r)), lw5.SIMP(q, r))
    pr(lw5)
    assert is_weakly_valid(lw5, values, VALUES)
    print('\t> VALID!')

    lw6 = WFF(L3b, prefix="Lw", number=5,
              name="Brouwer")
    lw6.wff = lw6.POSSIBLY(lw6.POSSIBLY(p))
    pr(lw6)
    assert is_weakly_valid(lw6, values, VALUES)
    print('\t> VALID!')

    d1 = WFF(L3b, prefix="D", number=1, name="distributivity")
    d1.wff = d1.SEQU(d1.AND(p,d1.OR(q,r)),d1.OR(d1.AND(p,q),d1.AND(p,r)))
    pr(d1)
    assert is_weakly_valid(d1, values, VALUES)
    print('\t> VALID!')

    d2 = WFF(L3b, prefix="D", number=2, name="distributivity")
    d2.wff = d2.SEQU(d2.OR(p,d2.AND(q,r)),d2.AND(d2.OR(p,q),d2.OR(p,r)))
    pr(d2)
    assert is_weakly_valid(d2, values, VALUES)
    print('\t> VALID!')

    print("some theorems...")
    th1 = WFF(L3b, prefix="Th", number=1, name="identity")
    th1.wff = th1.IMP(p, p)
    pr(th1)

    th2 = WFF(L3b, prefix="Th", number=2)
    th2.wff = th2.IMP(th2.IMP(th2.IMP(p, q), q), th2.IMP(th2.IMP(q, p), p))
    pr(th2)

    theorems = [th1, th2]
    for th in theorems:
        assert is_strongly_valid(th, values, VALUES), f'ERROR: {str(th)}'
    print("\t\t> theorems... OK!")

    print("some important contingent wffs...")
    wff1 = WFF(L3b, name="excluded middle", number=1)
    wff1.wff = wff1.OR(p, wff1.NOT(p))
    pr(wff1)

    wff2 = WFF(L3b, name="reductio ad absurdum", number=2)
    wff2.wff = wff2.IMP(wff2.IMP(p, wff2.NOT(p)), wff2.NOT(p))
    pr(wff2)

    wff3 = WFF(L3b, name="importation", number=3)
    wff3.wff = wff3.IMP(wff3.IMP(p, wff3.IMP(q,r)), wff3.IMP(wff3.AND(p,q),r))
    pr(wff3)

    d3 = WFF(L3b, prefix="D", number=3, name="distributivity")
    d3.wff = d3.IMP(d3.IMP(p,d3.IMP(q,r)),d3.IMP(d3.IMP(p,q),d3.IMP(p,r)))
    pr(d3)
    print("\tNOTE: D3 and Ax1 are important for proving a deduction theorem.")

    nontheorems = [wff1, wff2, wff3, d3]
    for wef in nontheorems:
        assert not is_strongly_valid(wef, values, VALUES), f'ERROR: {str(wef)}'
    print("\t\t> contingent expressions... OK!")

    print()
    print("REMARK:")
    print("   The notes above about natural deduction in Ł₃ apply here as well.")

    print()
    print("="*79)
    print()

    print("SUCCESS!")
