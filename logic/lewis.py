"""
logic.lewis - calculus of strict implementation (Lewis/Langford modal systems)
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

class NullaryOperator(object):
    """a nullary operator (constant or variable)"""

    __slots = ("__name", "__value")

    def __init__(self, name:str):
        """constructor"""
        self.__name = name

    @property
    def value(self):
        """current value"""
        return self.__value

    @value.setter
    def value(self, value):
        """new value"""
        self.__value = value

    def eval(self, _model:any):
        """returns the current value"""
        return self.value

    def __str__(self):
        """returns the name"""
        return self.__name

class UnaryOperation(object):
    """a unary operation"""

    INFIXES = {'N':'~', 'M':'▫', 'P':'◇'}

    __slots__ = ("__op", "__p")

    def __init__(self, op:str, p:any):
        """constructor"""
        self.__op = op
        self.__p = p

    def eval(self, model:callable):
        """evaluates the expression"""
        p = self.__p.eval(model)
        if self.__op == 'N':
            return model.NOT(p)             # logical negation
        if self.__op == 'M':
            return model.NECESSARILY(p)     # necessity operator
        if self.__op == 'P':
            return model.POSSIBLY(p)        # possibility operator
        raise NotImplementedError

    def __str__(self):
        """returns the string form"""
        p = str(self.__p)
        return self.INFIXES[self.__op] + p

class BinaryOperation(object):
    """a binary operation"""

    INFIXES = {'K':'∧', 'A':'∨', '+':'+', 'C':'⊃',
               'E':'≡', 'G':'⇒', 'H':'='}

    __slots__ = ("__op", "__p", "__q")

    def __init__(self, op:str, p:any, q:any):
        """constructor"""
        self.__op = op
        self.__p = p
        self.__q = q

    def eval(self, model:callable):
        """evaluates the expression"""
        p = self.__p.eval(model)
        q = self.__q.eval(model)
        if self.__op == 'K':
            return model.AND(p, q)          # conjunction
        if self.__op == 'A':
            return model.OR(p, q)           # disjunction (alternation)
        if self.__op == '+':
            return model.XOR(p, q)          # possibility operator
        if self.__op == 'C':
            return model.IMP(p, q)          # material implication
        if self.__op == 'E':
            return model.EQU(p, q)          # material equivalence
        if self.__op == 'G':
            return model.SIMP(p, q)         # strict implication
        if self.__op == 'H':
            return model.SEQU(p, q)         # strict equivalence
        raise NotImplementedError

    def __str__(self):
        """returns the string form"""
        p = str(self.__p)
        q = str(self.__q)
        infix = self.INFIXES[self.__op]
        return "(" + p + infix + q + ")"

class Statement(object):
    """a proposition"""

    __slots__ = ("__vars", "__f")

    def __init__(self, *args):
        """a propostion

        ARGUMENTS

            p1, p2, ..., pk
                propositional variables

            f(p1,p2,...,pk)
                the statement (tree form)
        """
        self.__vars = args[:-1]
        self.__f = args[-1]

    def __str__(self):
        """returns the string form"""
        s = str(self.__f)
        return s[1:-1] if s[0] == '(' else s

    def eval(self, model:callable):
        """evaluates the statement"""
        return self.__f.eval(model)

    @property
    def vars(self) -> list:
        """the referenced variables"""
        return list(self.__vars)

    @property
    def tree(self):
        """returns the statement tree"""
        return self.__f

    # Propositional constants
class T_Value(NullaryOperator):
    """tautological constant"""

    def eval(self, model):
        """returns the current value"""
        return model.T

T = T_Value('T')

    # Propositional variables
p = NullaryOperator('p')
q = NullaryOperator('q')
r = NullaryOperator('r')

    # Unary Operators
N = lambda x: UnaryOperation('N', x)            # logical negation
M = lambda x: UnaryOperation('M', x)            # necessity
P = lambda x: UnaryOperation('P', x)            # possibility

    # Binary Operators
K = lambda x, y: BinaryOperation('K', x, y)     # conjunction
A = lambda x, y: BinaryOperation('A', x, y)     # inclusive disjunction
C = lambda x, y: BinaryOperation('C', x, y)     # material implication
G = lambda x, y: BinaryOperation('G', x, y)     # strict implication
E = lambda x, y: BinaryOperation('E', x, y)     # material equivalence
H = lambda x, y: BinaryOperation('H', x, y)     # strict equivalence
Plus = lambda x, y: BinaryOperation('+', x, y)  # exclusive disjunction

Operators = {'T':T, 'p':p, 'q':q, 'r':r, 'N':N, 'M':M, 'P':P,
             'K':K, 'A':A, 'C':C, 'G':G, 'E':E, 'H':H, '+':Plus}

    # Axioms
A1 = Statement(p, q, G(K(p,q), K(q,p)))         # commutativity
A2 = Statement(p, q, G(K(p,q), p))              # simplification
A3 = Statement(p, G(p, K(p,p)))                 # tautology
A4 = Statement(p, q, r,
               G(K(K(p,q),r), K(p,K(q,r))))     # associativity
A5 = Statement(p, G(p, N(N(p))))                # double negation (dependent)
A6 = Statement(p, q, r,
               G(K(G(p,q), G(q,r)), G(p,r)))    # hypothetical syllogism
A7 = Statement(p, q, G(K(p, G(p,q)), q))        # modus ponens
A8 = Statement(p, q, G(P(K(p,q)), P(p)))        # S2 axiom
A9 = Statement(p, q, G(G(p,q), G(P(p),P(q))))   # S3 axiom
C10 = Statement(p, G(M(p), M(M(p))))            # S4 axiom
C11 = Statement(p, G(P(p), M(P(p))))            # S5 axiom
C12 = Statement(p, G(p, M(P(p))))               # S5 axiom (equivalent to C12)
C13 = Statement(p, P(P(p)))                     # Brouwerian axiom (S6, S7, S8)

Axioms = [A1, A2, A3, A4, A5, A6, A7, A8, A9, C10, C11, C12, C13]

    # Rules

if __name__ == "__main__":
        # Testing
    print(' A1:', A1)
    print(' A2:', A2)
    print(' A3:', A3)
    print(' A4:', A4)
    print(' A5:', A5, "\t\t\tDEPENDENT")
    print(' A6:', A6)
    print(' A7:', A7)
    print(' A8:', A8)
    print(' A9:', A9)
    print('C10:', C10)
    print('C11:', C11)
    print('C12:', C12)
    print('C13:', C13)

    from logic.boolean import BooleanLogic as BL

    def test(axiom, valid, model, debug=False):
        is_valid = True
        is_tautology = True
        if debug: print(str(axiom) + ':')
        stack = list()
        top = [axiom.vars[0], iter(values)]
        stack.append(top)
        n = len(axiom.vars)
        skip = False
        while(stack):
            x, y = stack[-1]
            try:
                x.value = next(y)
                if debug: print(x, '=', x.value)
            except StopIteration:
                stack.pop()
                continue
            k = len(stack)
            if k < n:
                x = axiom.vars[k]
                top = [axiom.vars[k], iter(values)]
                stack.append(top)
                continue
            value = axiom.eval(model)
            if value < model.T:
                is_tautology = False
            if not valid(value):
                is_valid = False
                break
        if is_valid:
            return is_valid, is_tautology, None
        error = str(axiom)+":\tNOT VALID\t"
        while(stack):
            x, y = stack.pop()
            error = error + str(x) + "=" + str(x.value) + ", "
        error = error + "VALUE=" + str(axiom.eval(model))
        return is_valid, is_tautology, error

    values = range(8)

    print()
    print("MODEL 3; weak, valid if true in real world...")
    model = BL(3)
    valid = lambda x: x%2 == 1
    for axiom in Axioms:
        is_valid, is_tautology, error = test(axiom, valid, model)
        if is_tautology:
            print(str(axiom)+":\tTAUTOLOGY")
        elif is_valid:
            print(str(axiom)+":\tVALID")
        else:
            print(error)

    print()
    print("MODEL 3; strong...")
    model._necessity = 0
    for axiom in Axioms:
        is_valid, is_tautology, error = test(axiom, valid, model)
        if is_tautology:
            print(str(axiom)+":\tTAUTOLOGY")
        elif is_valid:
            print(str(axiom)+":\tVALID")
        else:
            print(error)

    class LewisS2(BL):
        """model to show independence of A9
        Lewis & Langford Appendix III p 507
        """

        def NECESSARILY(self, p):
            """weird NECESSITY function"""
            if p == self.T:
                return p-1
            if p == self.T - 1:
                return 2
            return 0

    print()
    print(LewisS2.__doc__)
    model = LewisS2(3)
    valid = lambda x: x in {6, 7}
    for axiom in Axioms:
        is_valid, is_tautology, error = test(axiom, valid, model)
        if is_tautology:
            print(str(axiom)+":\tTAUTOLOGY")
        elif is_valid:
            print(str(axiom)+":\tVALID")
        else:
            print(error)
