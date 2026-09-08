"""
logic.deductions - to evaluate rules of transformation
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

from logic.wff import WFF, Constant, Variable

_TRUE = 1                           # true in this world
_NECESSARY = 2                      # true in all world
_MAPPINGS = {_TRUE:'⊢', _NECESSARY:'⊨'}
_SEP = {'if':"If", ',':',', 'and':'and', 'then':'then', '.':'.'}

class Rule(object):
    """rules of transformation (deductions)"""

    __slots__ = ("__args", "__name")

    @staticmethod
    def TRUE(wff:WFF) -> tuple:
        """create a (TRUE, wff) pair"""
        return (_TRUE, wff)

    @staticmethod
    def NECESSARY(wff:WFF) -> tuple:
        """create a (NECESSARY, wff) pair"""
        return (_NECESSARY, wff)

    def __init__(self, *args, name=None):
        """constructor

        The arguments consist of zero or more premises followed by one conclusion.
        Each argument is an ordered pair consisting of an argument type (TRUE or
        NECESSARY) followed by a wff.

        For example, consider modus ponens for material implication:

            MP: If ⊢ X⊃Y and ⊢ X, then ⊢ Y.

        This rule says that if X⊃Y and X are both true, then Y must also be
        true.  To encode this rule, we have as arguments:

            (TRUE, X⊃Y), (TRUE, X), (TRUE, Y)

        In practice, since we treat propositional variables as propostional schemata,
        the encoding will be:

            (TRUE, p⊃q), (TRUE, p), (TRUE, q)

        For a second example, consider, modus tollens:

            MT: If ⊢ X⊃Y and ⊢ ~Y, then ⊢ ~X.

        Our typical encoding would be:

            (TRUE, p⊃q), (TRUE, ~q), (TRUE, ~p)

        Now consider the necessitation rule for Lewis's system S1:

            N(S1): If X is a tautology, then ⊢ □X.

        Our typical encoding would be:

            (NECESSARY, p), (TRUE, □p)
        """
        assert len(args) > 0
        self.__args = args
        self.__name = name

    @property
    def premises(self) -> tuple:
        """return the premises"""
        return self.__args[:-1]

    @property
    def conclusion(self) -> tuple:
        """returns the conclusion"""
        return self.__args[-1]

    @staticmethod
    def fmt(pair:tuple) -> str:
        """format a (type, wff) pair"""
        typ, wff = pair
        return f"{_MAPPINGS[typ]}{str(wff)}"

    @property
    def fmt_all(self) -> str:
        """format the hypotheses for a rule"""
        premises = self.premises
        if len(premises) == 0:
            return str()
        if len(premises) == 1:
            premise = premises[0]
            s = _SEP['if'] + ' ' + self.fmt(premise)
            s += _SEP[','] + ' ' + _SEP['then'] + ' '
            s += self.fmt(self.conclusion) + _SEP['.']
            return s
        if len(premises) == 2:
            premise1 = premises[0]
            premise2 = premises[1]
            s = _SEP['if'] + ' ' + self.fmt(premise1)
            s += ' ' + _SEP['and'] + ' ' + self.fmt(premise2)
            s += _SEP[','] + ' ' + _SEP['then'] + ' '
            s += self.fmt(self.conclusion) + _SEP['.']
            return s
        head = premises[:-1]
        tail = premises[-1]
        s = _SEPARATORS['if'] + ' '
        for premise in head:
            s += self.fmt(premise) + _SEP[','] + ' '
        s += _SEP['and'] + ' ' + self.fmt(tail) + _SEP[','] + ' '
        s += self.fmt(self.conclusion) + _SEP['.']
        return s

    def __str__(self):
        """returns the string"""
        return self.fmt_all

    @property
    def name(self) -> str:
        """returns the name"""
        return self.__name

    @name.setter
    def name(self, new_name:str):
        """sets the name"""
        self.__name = new_name

    @property
    def vars(self) -> tuple:
        """get the variables, sorted lexically"""
        vset = set()
        for pair in self.__args:
            typ, wff = pair
            # print("\twff:", wff)
            if type(wff) == Constant:
                pass
            elif type(wff) == Variable:
                vset.add(wff)
            elif type(wff) == WFF:
                vset |= set(wff.vars)
        return tuple(sorted(vset))

from functools import partial
from itertools import product

def f_generator(A:list, B:list):
    """generates all functions from A to B

    Ricardo Bucco
        https://stackoverflow.com/questions/60932181/ -
            representing-set-of-functions-from-finite-set-to-finite-set
    """
    def f_template(d, x):
        return d[x]
    for b_values in product(B, repeat=len(A)):
        yield partial(f_template, dict(zip(A, b_values)))

if __name__ == "__main__":
        # TESTING
    from logic.boolean import BooleanLogic as BL
    TRUE = Rule.TRUE
    MUST = Rule.NECESSARY

    def pr(rule):
        """display a rule"""
        if rule.name:
            s = str(rule)
            n = len(s) + len(rule.name)
            fill = " " * (79-n)
            print(s + fill + rule.name)
        else:
            print(rule)

    def center(text):
        """display centered text"""
        n = len(text)
        print(" " * ((79-n)//2), text)

    cpc = BL()          # classical propositional calculus
    values = (0, 1)
    center("MODUS PONENS")
    p = Variable("p", owner=cpc)
    q = Variable("q", owner=cpc)
    Cpq = WFF(owner=cpc)
    Cpq.wff = Cpq.IMP(p, q)
    modus_ponens = Rule(TRUE(Cpq), TRUE(p), TRUE(q), name="modus ponens")
    pr(modus_ponens)
    variables = modus_ponens.vars
    print("    variables:", *variables)
    assert variables == (p, q)
    for f in f_generator(variables, values):
        p.value = f(p)
        q.value = f(q)
        head = f"\t{str(p)}={f(p)}, {str(q)}={f(q)}:"
        if Cpq.value != 1:
            print(head, f"{str(Cpq)}={Cpq.value}   (false premise)")
            continue
        if p.value != 1:
            print(head, f"{str(p)}={p.value}       (false premise)")
            continue
        if q.value != 1:
            print(head, f"{str(q)}={q.value}       (INVALID RULE)")
            raise ValueError("Invalid rule")
        else:
            print(head, f"{str(q)}={q.value}       (true conclusion)")
    print("    RULE IS VALID")

    center("MODUS TOLLENS")
    Nq = WFF(owner=cpc)
    Nq.wff = Nq.NOT(q)
    Np = WFF(owner=cpc)
    Np.wff = Np.NOT(p)
    modus_tollens = Rule(TRUE(Cpq), TRUE(Nq), TRUE(Np), name="modus tollens")
    pr(modus_tollens)
    variables = modus_tollens.vars
    print("    variables:", *variables)
    assert variables == (p, q)
    for f in f_generator(variables, values):
        p.value = f(p)
        q.value = f(q)
        head = f"\t{str(p)}={f(p)}, {str(q)}={f(q)}:"
        if Cpq.value != 1:
            print(head, f"{str(Cpq)}={Cpq.value}   (false premise)")
            continue
        if Nq.value != 1:
            print(head, f"{str(Nq)}={Nq.value}       (false premise)")
            continue
        if Np.value != 1:
            print(head, f"{str(Np)}={Np.value}       (INVALID RULE)")
            raise ValueError("Invalid rule")
        else:
            print(head, f"{str(Np)}={Np.value}       (true conclusion)")
    print("    RULE IS VALID")


    center("HYPOTHETICAL SYLLOGISM")
    r = Variable("r", owner=cpc)
    Cqr = WFF(owner=cpc)
    Cqr.wff = Cqr.IMP(q, r)
    Cpr = WFF(owner=cpc)
    Cpr.wff = Cpr.IMP(p, r)
    hypsyll = Rule(TRUE(Cpq), TRUE(Cqr), TRUE(Cpr), name="hypothetical syllogism")
    pr(hypsyll)
    variables = hypsyll.vars
    print("    variables:", *variables)
    assert variables == (p, q, r)
    for f in f_generator(variables, values):
        p.value = f(p)
        q.value = f(q)
        r.value = f(r)
        head = f"\t{str(p)}={f(p)}, {str(q)}={f(q)}, {str(r)}={f(r)}:"
        if Cpq.value != 1:
            print(head, f"{str(Cpq)}={Cpq.value}   (false premise)")
            continue
        if Cqr.value != 1:
            print(head, f"{str(Cqr)}={Cqr.value}   (false premise)")
            continue
        if Cpr.value != 1:
            print(head, f"{str(Cpr)}={Cpr.value}   (INVALID RULE)")
            raise ValueError("Invalid rule")
        else:
            print(head, f"{str(Cpr)}={Cpr.value}   (true conclusion)")
    print("    RULE IS VALID")

    center("NECESSITATION")
    print("setting up the two world calculus...")
    modal2 = BL(2)
    p = Variable("p", owner=modal2)
    Mp = WFF(owner=modal2)
    Mp.wff = Mp.NECESSARILY(p)
    values = tuple(range(4))
    print("setting up the rule...")
    nec = Rule(MUST(p), TRUE(Mp), name="necessitation")
    pr(nec)
    variables = nec.vars
    print("    variables:", *variables)
    assert variables == (p, )
    for f in values:
        p.value = f
        head = f"\t{str(p)}={f}:"
        if p.value != modal2.T:
            print(head, f"{str(p)}={p.value}    (possibly false premise)")
            continue
        if Mp.value & 1 == 0:
            print(head, f"{str(Mp)}={Mp.value}   (INVALID RULE)")
            raise ValueError("Invalid rule")
        else:
            print(head, f"{str(Mp)}={Mp.value}   (true conclusion)")
    print("    RULE IS VALID")
