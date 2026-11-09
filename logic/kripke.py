"""
logic.kripke - Kripke models
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A Kripke model (see [1], Ex 19 p29) is a triple 𝕸=(Ω,≤,S) where:
        (1) Ω is a non empty set;
        (2) ≤ is a binary relation between members of Ω; and
        (3) S is a function which maps members of Ω to proposition
            letters;
    such that for each α, β and γ in Ω:
        (4) α≤α;
        (5) if α≤β and β≤γ, then α≤γ; and
        (6) if α≤β, then S(α)⊆S(β).

    I'll refer to Ω as the multiverse, its members as universes, and the
    members of S as supports. The relation ≤ is the partial order on the
    multiverse. (This terminology is strictly my own.  It is used here
    as a convenience to minimize the typing of unicode characters.)

    Given a Kripke model 𝕸, a universe α in 𝕸, and a proposition P, the
    relation (𝕸|α) ⊧ P is defined inductively.  For the intuitionistic
    propositional calculus:

        (1) for a proposition letter p:
                (𝕸|α) ⊧ p  if and only if p is in S(α);
        (2) for the propositional constant F:
                (𝕸|α) ⊧ F is false;
        (3) for propositions X and Y:
            (a) (𝕸|α) ⊧ X∧Y if and only if both (𝕸|α) ⊧ X and (𝕸|α) ⊧ Y;
            (b) (𝕸|α) ⊧ X∨Y if and only if both (𝕸|α) ⊧ X or (𝕸|α) ⊧ Y; and
            (c) (𝕸|α) ⊧ X⊃Y if and only if for every β≥α:
                    if (𝕸|β) ⊧ X then (𝕸|β) ⊧ Y.

    Note that negation is defined by:

        ~X := X⊃F.

    Then given a model 𝕸, a universe α, and a proposition X:

        (𝕸|α) ⊧ ~X if and only if for every universe β≥α:
                (𝕸|β) ⊧ X is false.

    As an example, consider Exercise 20 ([1], page 30) where we are
    given exactly two universes α and β with support:

        S(α) = ∅; and
        S(β) = {p}

    From the definitions above, it follows that β≥α.  We have the
    following valuations:

        proposition        valuations
        ----------- -------------------------
            X       (𝕸|α) ⊧ X       𝕸|β) ⊧ X            notes
        -------------------------------------  -------------------------
            p          false           true    true when p in S(*)
            ~p         false           false   F in β, so F in α 
           ~p∨p        false           true    F for both in α
           ~~p         true            true    ~p is F in both
          ~~p⊃p        false           true    in α: T⊃F

    𝕸|β) ⊧ X is true if X is a classically valid proposition in p.
    (The converse is not true! For example, 𝕸|β) ⊧ p is true, but p
    is not classically valid as p can be false.)  The propositions
    ~p∨p and ~~p⊃p are both classically valid.

    𝕸|α) ⊧ X is not necessarily true for classically valid propositions
    in p.  Neither of the propositions ~p∨p and ~~p⊃p are are
    intuitionistically valid, so they fail in some (but not all!) Kripke
    models.

NOTES

    Look at the code in the '__main__' part of the model to see some
    applications.  (And run the module as '__main__' to see some results.)

    Parts of the code make use of recursive programming. In particular,
    all invocations of 'displayForm' and '_eval' are recursive.  Depending
    on your application you may need to increase the maximum recursion
    depth.

REFERENCES

    [1] Joel W Robbin.  Mathematical logic, a first course.
        W A Benjamin (1967, 1997).  Dover Edition (2006).

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
from collections import defaultdict

class KripkeModel(object):
    """a many-valued Kripke model"""

    __slots__ = ("__n", "__true", "__constants", "__values",
                 "__supports", "__multiverses", "__settings")

        # Reserved symbols
        #   prefix symbol -> (infix symbol, number of operands)
    RESERVED = {'N':('¬', 1), 'A':('∨', 2), 'K':('∧', 2), 'C':('⊃',2),
                'E':('≡', 2), 'M':('□', 1), 'P':('◊', 1)}

    def __init__(self, true:int=1, *constants):
        """constructor

        POSITIONAL ARGUMENTS

            truth (default=1) - a positive integer which indicates
                absolute truth.  The truth values are:
                        0 (false), 1, ..., true

            constants - these are ordered pairs of the form:
                        (<character>, <value>)
                where <character> is a character which is not reserved
                and <value> is a truth value.  Digits 0 through 9 in
                range(true+1) are predefined.

        EXAMPLE 1 - A three-valued Kripke model

            For a three-valued model, we set up the model as follows:

                    M = KripkeModel(2)

            Three constants, 0 (for false), 1, and 2 (for true) are
            predefined.

        EXAMPLE 2 - A twelve-valued model

            For a twelve valued model, we have truth values in the range:

                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

            The constants 0 through 9 are predefined.  We need names for
            10 and 11.  Lower case letters that we don't use as
            propositional variables are safe, but any character that isn't
            reserved can be used as constants.  One possibility is:

                    M = KripkeModel(12, ('a',10), ('b',11))

        RESERVED CHARACTERS

            Input for valuations uses Polish notation.  Infix notation
            is used when displaying results.  The following capital
            letters are reserved:

                    N - for negation
                    A - for disjunction (alternation)
                    K - for conjunction
                    C - for material implication (conditional)
                    E - for material equivalence
                    M - for necessity (German müssen = must)
                    P - for possibility

            M and P are not implemented here, but they are reserved.
        """
        if type(true) != int:
            raise TypeError("'true' must be an integer")
        if true <= 0:
            raise ValueError("'true' must be a positive integer")
        self.__true = true
        self.__n = true+1                           # number of values
        self.__constants = dict()
        self.__values = dict()
        for value in range(self.__n):
            if value > 9:
                break
            self.__constants[str(value)] = value
            self.__values[value] = str(value)
        for packet in constants:
            if not isinstance(packet, (tuple, list)) or len(packet) != 2:
                raise TypeError("each 'constants' argument must be an ordered pair")
            constant, value = packet
            if type(constant) != str or type(value) != int:
                raise TypeError("each 'constants' argument must be (str, int)")
            if len(constant) != 1:
                raise ValueError("constant must be a single character")
            if value < 0 or value > true:
                raise ValueError(f"value must be in range {self.__n}")
            if constant in self.RESERVED:
                raise ValueError(f"constant name '{constant}' is reserved")
            self.__constants[constant] = value
            self.__values[value] = constant
        self.__supports = dict()
        self.__multiverses = dict()
        self.__settings = dict()

            # customizations
        self.initialize()
        self.configure()

    def initialize(self):
        """initialization (stub)"""
        pass

    def configure(self):
        """configuration (stub)"""
        pass

    @property
    def true(self):
        """return the value 'true'"""
        return self.__true

    @property
    def n(self):
        """return the number of truth values"""
        return self.__n

    def constant(self, c:str) -> int:
        """find the value of a constant"""
        return self.__constants[str(c)]

    def value(self, v:int) -> str:
        """find the value of a constant"""
        return self.__values[int(v)]

    def new_support(self, universe:str, *pvs):
        """create a support for a universe"""
        for pv in pvs:
            if type(pv) != str or len(pv) != 1:
                raise TypeError("a propositional variable must be a string of length 1")
            if pv in self.RESERVED:
                raise ValueError(f"propositional variable name '{pv}' is reserved")
            if pv in self.__constants:
                raise ValueError(f"propositional variable name '{pv}' is a name for a constant")
        self.__supports[universe] = set(pvs)

    def support(self, universe:str) -> frozenset:
        """return the supports for a universe"""
        return frozenset(self.__supports[universe])

    def new_multiverse(self, name:str, *universes):
        """create a multiverse"""
        for universe in universes:
            if universe not in self.__supports:
                raise ValueError(f"universe {universe} does not have a support")
        self.__multiverses[name] = set(universes)

    def multiverse(self, name:str) -> frozenset:
        """return the named multiverse"""
        return frozenset(self.__multiverses[name])

    def leq(self, universe1, universe2):
        """determine whether universe1 precedes universe 2"""
        return self.support(universe1).issubset(self.support(universe2))

    def lt(self, universe1, universe2):
        """determine whether universe1 precedes universe 2"""
        return self.support(universe1) < self.support(universe2)

    def geq(self, universe1, universe2):
        """determine whether universe1 follows universe 2"""
        return self.support(universe2).issubset(self.support(universe1))

    def gt(self, universe1, universe2):
        """determine whether universe1 precedes universe 2"""
        return self.support(universe1) > self.support(universe2)

    @staticmethod
    def powerset(*args) -> list:
        """generate a power set

        ARGUMENTS

            The arguments must be hashable and may not include any
            duplicates.
        """
        n = len(args)
        if n != len(set(args)):
            raise ValueError("Duplicates are not permitted")
        result = list()
        for i in range(2 ** n):
            q = i
            subset = list()
            for j in range(n):
                q, r = divmod(q, 2)
                if r == 1:
                    subset.append(args[j])
            result.append(set(subset))
        return result

    def setvars(self, multiverse, **kwargs):
        """set the values of the variabels in a given multiverse

        USAGE

            The default is to set the supported variables to true
            and unsupported variables to false:

                    model.setvars(multiverse)

            To set a supported variable to some value other than
            true (but not false), include the value in the setting,
            for example:

                    model.setvars(multiverse, p=3, q=7)

            Unsupported variables are always set to false.

            If setvars hasn't been invoked, then all supported
            variables are treated as true.

            This function is only useful when there are more than
            two truth values.
        """
        for key in kwargs:
            assert len(key) == 1, f"{key=}: length != 1"
            assert key not in self.__constants, f"{key=}: constant"
            assert key not in self.RESERVED, f"{key=}: reserved"
            assert type(kwargs[key]) == int, f"{key=}: integers only"
            assert 0 < kwargs[key] <= self.true, f"{key=}, {kwargs[key]=}: truth value, not false"
        self.__settings[multiverse] = kwargs

    def getvars(self, multiverse, universe) -> dict:
        """retrieve the current variable presets"""
        settings = dict()
        support = self.support(universe)
        updates = self.__settings.get(multiverse, dict())
        for variable in support:
            settings[variable] = updates.get(variable, self.__true)
        return settings

    def topology(self, multiverse) -> dict:
        """determine the multiverse topology"""
        Tau = dict()
        for universe1 in self.__multiverses[multiverse]:
            Tau[universe1] = list()
            for universe2 in self.__multiverses[multiverse]:
                if M2.lt(universe1, universe2):
                    Tau[universe1].append(universe2)
        return Tau

    @classmethod
    def displayForm(cls, tree) -> str:
        """generate the infix form of a wff (recursive)"""
        #print("displayForm:", tree)
        if type(tree) == str:
            return tree
        op, infix, n = tree[:3]
        rest = tree[3:]
        if n == 0:              # for subclasses
            return infix
        if n == 1:
            return infix + cls.displayForm(rest[0])
        if n == 2:
            op1 = cls.displayForm(rest[0])
            op2 = cls.displayForm(rest[1])
            return f"({op1}{infix}{op2})"
                # Lagrange functional form for subclasses
        args = [cls.displayForm(item) for item in rest]
        s = infix + "(" + ",".join(args) + ")"
        return s

    @classmethod
    def parse_wffs(cls, wffs:str, verbose:bool=False,
                   debug:bool=False) -> "tree":
        """generate parse trees for several wffs

        EXCEPTIONS

            IndexError - indicates a syntax error
                * pop from empty stack
        """
        if verbose:
            print("\tParsing:", wffs)
        stack = list()
        for symbol in reversed(wffs):
            if symbol in cls.RESERVED:
                infix, n = cls.RESERVED[symbol]
                if debug:
                    print(f"parse {symbol}/{infix}:",
                          f"requires {n} operands,",
                          f"stack size={len(stack)}->{len(stack)-n+1}")
                node = [symbol, infix, n]
                for _ in range(n):
                    node.append(stack.pop())
                stack.append(tuple(node))
            else:
                if debug:
                    print(f"parse {symbol}: constant or variable",
                          f"stack size={len(stack)}->{len(stack)+1}")
                stack.append(symbol)
        stack = tuple(reversed(stack))
        if debug:
            print(stack)
        if verbose:
            if len(stack) == 0:
                print("\tParsed: empty input")
            else:
                print("\tParsed:")
            for i in range(len(stack)):
                infixForm = cls.displayForm(stack[i])
                if infixForm[0] == '(':
                    infixForm = infixForm[1:-1]
                print(f"\t  {i+1}:", infixForm)
        return stack

    @classmethod
    def parse(cls, wff:str, verbose:bool=False,
              debug:bool=False) -> "tree":
        """generate the parse tree for a wff

        EXCEPTIONS

            IndexError - indicates a syntax error
                * pop from empty stack
                * number of items on the the stack at end is not on
        """
        tree = cls.parse_wffs(wff, verbose, debug)
        if len(tree) != 1:
            raise IndexError(f"syntax error, stack size={len(stack)}")
        return tree

    def evaluate(self, multiverse, wffs, verbose=False, debug=False) -> dict:
        """returns a dictionary mapping each expression to a value"""
        Tau = self.topology(multiverse)
        ranked = defaultdict(list)
        ranks = set()
        settings = dict()
        universes = self.__multiverses[multiverse]
        for universe in universes:
            # print(universe, Tau[universe])
            rank = len(Tau[universe])
            ranked[rank].append(universe)
            ranks.add(rank)
            settings[universe] = self.getvars(multiverse, universe)
        ranks = sorted(ranks)
        results = dict()
        trees = self.parse_wffs(wffs, verbose)
        # print(Tau)
        for i in range(len(trees)):
            tree = trees[i]
            results[i] = self.displayForm(tree)
            nodes = dict()
            for rank in ranks:
                for universe in ranked[rank]:
                    # print("--->", rank, universe)
                    results[i,universe] \
                        = self._eval(tree, universe, Tau, settings, nodes)
        return results

    def OR(self, tree, universe, Tau, settings, nodes) -> int:
        """disjunction"""
        arg1 = self._eval(tree[3], universe, Tau, settings, nodes)
        arg2 = self._eval(tree[4], universe, Tau, settings, nodes)
        return max(arg1, arg2)

    def AND(self, tree, universe, Tau, settings, nodes) -> int:
        """conjunction"""
        arg1 = self._eval(tree[3], universe, Tau, settings, nodes)
        arg2 = self._eval(tree[4], universe, Tau, settings, nodes)
        return min(arg1, arg2)

    def NOT(self, tree, universe, Tau, settings, nodes) -> int:
        """negation"""
        arg1 = self._eval(tree[3], universe, Tau, settings, nodes)
        result = self.true - arg1           # local estimate
        for cover in Tau[universe]:
            arg = nodes[cover, tree]
            # print(f"{universe}:{cover}:{arg}", tree)
            result = min(result, arg)       # necessary
        # print(f"{universe}:{result}", tree)
        nodes[universe, tree] = result
        return result

    def IMP(self, tree, universe, Tau, settings, nodes) -> int:
        """material implication"""
        arg1 = self._eval(tree[3], universe, Tau, settings, nodes)
        arg2 = self._eval(tree[4], universe, Tau, settings, nodes)
        result= min(self.true, self.true + arg2 - arg1)  # local
        for cover in Tau[universe]:
            arg = nodes[cover, tree]
            # print(f"{universe}:{cover}:{arg}", tree)
            result = min(result, arg)       # necessary
        # print(f"{universe}:{result}", tree)
        nodes[universe, tree] = result
        return result

    def EQU(self, tree, universe, Tau, settings, nodes) -> int:
        """material equivalence"""
        arg1 = self._eval(tree[3], universe, Tau, settings, nodes)
        arg2 = self._eval(tree[4], universe, Tau, settings, nodes)
        result = min(self.true + arg1 - arg2, self.true + arg2 - arg1) #local
        for cover in Tau[universe]:
            arg = nodes[cover, tree]
            # print(f"{universe}:{cover}:{arg}", tree)
            result = min(result, arg)       # necessary
        # print(f"{universe}:{result}", tree)
        nodes[universe, tree] = result
        return result

    def NEC(self, tree, universe, Tau, settings, nodes) -> int:
        """necessity"""
        arg1 = self._eval(tree[3], universe, Tau, settings, nodes)
        result = arg1    # local estimate
        for cover in Tau[universe]:
            arg = nodes[cover, tree]
            # print(f"{universe}:{cover}:{arg}", tree)
            result = min(result, arg)       # necessary
        # print(f"{universe}:{result}", tree)
        nodes[universe, tree] = result
        return result

    def POSS(self, tree, universe, Tau, settings, nodes) -> int:
        """possibility"""
        arg1 = self._eval(tree[3], universe, Tau, settings, nodes)
        result = arg1    # local estimate
        for cover in Tau[universe]:
            arg = nodes[cover, tree]
            # print(f"{universe}:{cover}:{arg}", tree)
            result = max(result, arg)       # possible
        # print(f"{universe}:{result}", tree)
        nodes[universe, tree] = result
        return result

    def _eval(self, tree, universe, Tau, settings, nodes) -> int:
        """recursively evaluate an expression"""
        if type(tree) == str:
            try:
                return self.constant(tree)
            except KeyError:
                return settings[universe].get(tree, 0)
        if tree[0] == 'A':          # disjunction
            return self.OR(tree, universe, Tau, settings, nodes)
        if tree[0] == 'K':          # conjunction
            return self.AND(tree, universe, Tau, settings, nodes)
        if tree[0] == 'N':
            return self.NOT(tree, universe, Tau, settings, nodes)
        if tree[0] == 'C':
            return self.IMP(tree, universe, Tau, settings, nodes)
        if tree[0] == 'E':
            return self.EQU(tree, universe, Tau, settings, nodes)
        if tree[0] == 'M':
            return self.NEC(tree, universe, Tau, settings, nodes)
        if tree[0] == 'P':
            return self.POSS(tree, universe, Tau, settings, nodes)
        raise NotImplementedError(f"node type {tree[0]}")

if __name__ == "__main__":
            # self-test

            # 36 defined here, enough for 5 support variables
            #   variables       letters needed      support variables
            #       0                1
            #       1                2              p
            #       2                4              p, q
            #       3                8              p, q, r
            #       4               16              p, q, r, s
            #       5               32              p, q, r, s, t
            #       6               64              p, q, r, s, t, u
    greek = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι',
             'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ',
             'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'ϝ', 'ϛ', 'ͱ',
             'ϳ', 'ϻ', 'ϟ', 'ϙ', 'ϡ', 'ͳ', 'ϸ', 'ͷ', 'ά']
    alpha, beta, gamma = greek[0:3]
    delta, epsilon, zeta = greek[3:6]
    eta, theta, iota = greek[6:9]
    kappa, lambdax, mu = greek[9:12]    # 'lambda' is a reserved word
    nu, xi, omicron = greek[12:15]
    pi, rho, sigma = greek[15:18]
    tau, upsilon, phi = greek[18:21]
    chi, psi, omega = greek[21:24]
        # archaic and additional letters
    digamma, stigma, heta = greek[24:27]
    yot, san, koppa = greek[27:30]      # koppa, qoppa: variants (koppa)
    qoppa, sampi, zampi = greek[30:33]  # sampi, zampi: variants (sampi)
    sho, tigamma, atonos = greek[33:36] # digamma, tigamma: variants (digamma)
    
    def tsort(model, *supports):
        """topological sort -- nothing fancy here"""
        n = len(supports)
        D = dict()
        for x in supports:
            D[x] = list()
            for y in supports:
                if model.lt(x, y):
                    D[x].append(y)

        ranked = defaultdict(list)
        for x in D:
            ranked[len(D[x])].append(x)
        ranks = sorted(ranked.keys(), reverse=True)

        s = list()
        for r in ranks:
            ranked[r] = sorted(ranked[r])
            for x in ranked[r]:
                s.append(x)
        return s

    def tag(tags:list, items:list):
        """tag the items"""
        tagging = dict()
        lookup = dict()
        for i in range(len(items)):
            tagging[tags[i]] = items[i]
            lookup[items[i]] = tags[i]
        s = list()
        for item in items:
            tag = lookup[item]
            s.append(f"{tag}:{item}")
        print("    directory:")
        print("     ", ", ".join(s))
        return tagging, lookup

    print("Testing Kripke models...")
    variables = ('p', 'q', 'r')
    powerset = KripkeModel.powerset(*variables)
    expected = [set(), {'p'}, {'q'}, {'p', 'q'}, {'r'}, {'p', 'r'},
                {'q', 'r'}, {'p', 'q', 'r'}]
    assert powerset == expected
    print("  Two-valued models:")
    M2 = KripkeModel(1)
    assert M2.true == 1
    assert M2.n == 2

        # generate the supports
    print("    generating the supports...")
    universes = set()
    for subset in powerset:
        pvs = sorted(list(subset))
        universe = "S(" + "".join(pvs) + ")"
        M2.new_support(universe, *pvs)
        assert M2.support(universe) == subset
        universes.add(universe)
    assert len(universes) == 8
    supports = tsort(M2, *universes)
    print("    supports =", ", ".join(supports))
    tags, lookup = tag(greek, supports)

    print("    testing the precedes relationship...")
    x = set(item for item in universes if M2.leq("S()", item))
    assert len(x) == 8
    x = set(item for item in universes if M2.leq("S(p)", item))
    assert len(x) == 4
    x = set(item for item in universes if M2.leq("S(qr)", item))
    assert len(x) == 2
    x = set(item for item in universes if M2.leq("S(pqr)", item))
    assert len(x) == 1

    print("    testing the follows relationship...")
    x = set(item for item in universes if M2.geq("S()", item))
    assert len(x) == 1
    x = set(item for item in universes if M2.geq("S(p)", item))
    assert len(x) == 2
    x = set(item for item in universes if M2.geq("S(qr)", item))
    assert len(x) == 4
    x = set(item for item in universes if M2.geq("S(pqr)", item))
    assert len(x) == 8

    print("    testing the parsing...")
    assert KripkeModel.parse_wffs("pq", verbose=True) == ('p', 'q')
    assert KripkeModel.parse_wffs("Cpq", verbose=True) == (('C', '⊃', 2, 'p', 'q'),)
    KripkeModel.parse_wffs("CpCqp", verbose=True)
    KripkeModel.parse_wffs("ApNp", verbose=True)
    assert len(KripkeModel.parse_wffs("ApNpANppCNNppCpNNp", verbose=True))==4
    assert len(KripkeModel.parse_wffs("CCpqCCqrCprCEpqKCpqCqp", verbose=True))==2

    def display_setup(M, exercise, T, tags):
        """display the setup"""
        print(f"  settings:\n\t(false=0, true={M2.true})")
        for tag in T:
            s = M.getvars(exercise, tags[tag])
            vs = list()
            for v in ['p', 'q', 'r']:
                vs.append(f"{v}={s.get(v,0)}")
            print(f"    {tag}:", ", ".join(vs), f"  \t{tags[tag]}")

    def topology(M, exercise, lookup):
        """display the topology"""
        print("  topology:")
        Tau = M.topology(exercise)
        inequalities = list()
        for s1 in Tau:
            tag1 = lookup[s1]
            for s2 in Tau[s1]:
                tag2 = lookup[s2]
                inequalities.append(f"{tag1} < {tag2}")
        inequalities = sorted(inequalities)
        for n in range(0, len(inequalities), 8):
             print("   ", ", ".join(inequalities[n:n+8]))
        print(f"\t{len(inequalities)} proper subset relations")

    def simulate(M, exercise, wffs, T, tags, indent, control=""):
        """run the exercise"""
        results = M.evaluate(exercise, wffs, verbose=False, debug=False)
        # print(results)
        key = 0
        if control:
            print(f"  control: ({control})")
        else:
            print("  results:")
        while wff := results.get(key):
            if wff[0] == '(':
                wff = wff[1:-1]
            # print(f"    {key+1}: {wff}")
            s = f"    {key+1}: {wff}"
            if len(s) < indent:
                s += " " * (indent-len(s))
            notvalid = ""
            for letter in T:
                universe = tags[letter]
                result = results[key, universe]
                s += f" {letter}:{result}"
                if result < M.true:
                    notvalid = "*** not valid ***"
            if notvalid:
                s += "  " + notvalid
            print(s)
            key += 1

            # intuitionist propositional calculus axioms
    axioms = ["CpCqp", "CCpCqrCCpqCpr",
              "CKpqp", "CKpqp", "CpCqKpq",
              "CpApq", "CqApq", "CCprCCqrCApqr",
              "C0p"]

    definitions = ["ENpCp0", "EEpqKCpqCqp"]

    mp = "CKCpqpq"

        # Exercise 20 on page 30 of [1]
    print()
    print("Joel Robbin (2006): Exercise 20 on page 30...")
    T = (alpha, beta)
    S = (tags[alpha], tags[beta])
    exercise = "Ex20"
    M2.new_multiverse(exercise, *S)
    assert M2.multiverse(exercise) == set(S)
    display_setup(M2, exercise, T, tags)
    topology(M2, exercise, lookup)
    wffs = "".join(["ApNp", "CNNpp", "CCNpNqCqp", "ACpqCqp", "CCCpqpp"])
    simulate(M2, exercise, wffs, T, tags, 20)

    print("""
          NOTES:
              All five are not intuitionistically valid.  This particular
              Kripke Model verifies that fact for the law of the excluded
              middle (1), one form of double negation (2), and Pierce's
              Law (5).

              The converses of (2) and the contrapositive law (3) are
              both valid in the IPC (= intuitionistic propositional
              calclus).

              (5) is valid in every Gödel-Dummett algebra, but fails in
              the IPC.
          """)
    #simulate(M2, exercise, "".join(axioms), T, tags, 30,
    #         control="axioms")
    #simulate(M2, exercise, "".join(definitions), T, tags, 30,
    #         control="definitions")
    #simulate(M2, exercise, mp, T, tags, 30,
    #         control="modus ponens")

        # Exercise 21 on page 30 of [1]
    print()
    print("Joel Robbin (2006): Exercise 21 on page 30...")
    T = (gamma, epsilon)
    S = (tags[gamma], tags[epsilon])
    exercise = "Ex20"
    M2.new_multiverse(exercise, *S)
    assert M2.multiverse(exercise) == set(S)
    display_setup(M2, exercise, T, tags)
    topology(M2, exercise, lookup)
    wffs = "".join(["CCNpNqCqp", "CCqpCNpNq", "ACpqCqp", "CCCpqpp"])
    simulate(M2, exercise, wffs, T, tags, 20)
    print("""
          NOTES:
              This particular model verifies that the contrapositive
              law (1) is not valid in the IPC.  It's converse (2) is,
              however, valid -- it cannot be falsified in any standard
              Kripke model.
          """)
    #simulate(M2, exercise, "".join(axioms), T, tags, 30,
    #         control="axioms")
    #simulate(M2, exercise, "".join(definitions), T, tags, 30,
    #         control="definitions")
    #simulate(M2, exercise, mp, T, tags, 30,
    #         control="modus ponens")

        # Exercise 22 on page 30 of [1]
    print()
    print("Joel Robbin (2006): Exercise 22 on page 30-31...")
    T = (alpha, beta, gamma)
    S = (tags[alpha], tags[beta], tags[gamma])
    exercise = "Ex20"
    M2.new_multiverse(exercise, *S)
    assert M2.multiverse(exercise) == set(S)
    display_setup(M2, exercise, T, tags)
    topology(M2, exercise, lookup)
    wffs = "".join(["ACpqCqp", "CCCpqpp"])
    simulate(M2, exercise, wffs, T, tags, 20)
    print("""
          NOTES:
              This particular model verifies that (p⊃q)∨(q⊃p) (1)
              is not valid in the IPC.  This wff is satisfied in
              every linearly ordered model.  (Proof remains as
              an exercise.)

              Note that Pierce's Law (2) is satisfied in this model
              with multiverse {{}, {p}, {q}} even though fails in
              the multiverse {{}, {p}} of Exercise 20 above.  Expanding
              the multiverse doesn't preserve the physics.
          """)
    #simulate(M2, exercise, "".join(axioms), T, tags, 30,
    #         control="axioms")
    #simulate(M2, exercise, "".join(definitions), T, tags, 30,
    #         control="definitions")
    #simulate(M2, exercise, mp, T, tags, 30,
    #         control="modus ponens")

        # Exercise 23(a) on page 30 of [1]
    print()
    print("Joel Robbin (2006): Exercise 23(a) on page 30-31...")
    print("\tFind a model in which Pierce's Law fails...")
    print("\t    See exercise 20 above")

        # Exercise 23(b) on page 30 of [1]
    print()
    print("Joel Robbin (2006): Exercise 23(b) on page 30-31 (part)...")
    print("\tFind a model in which (¬p⊃q)⊃((p⊃q)⊃q) fails...")
    T = (alpha, beta)
    S = list(tags[letter] for letter in T)
    exercise = "23a Pierce"
    M2.new_multiverse(exercise, *S)
    assert M2.multiverse(exercise) == set(S)
    display_setup(M2, exercise, T, tags)
    topology(M2, exercise, lookup)
    wffs = "".join(["CCNpqCCpqq", "CCNppCCppp"])
    simulate(M2, exercise, wffs, T, tags, 20)

    print("""
          NOTES:
              To make the more specific one fail, we have:
                  α: p=0
                  β: p=1
              That suggests we try:
                  α: p=q=0
                  γ: p=0 and q=1
                  ε: p=q=1
          """)

    T = (alpha, gamma, epsilon)
    S = list(tags[letter] for letter in T)
    exercise = "23a Pierce"
    M2.new_multiverse(exercise, *S)
    assert M2.multiverse(exercise) == set(S)
    display_setup(M2, exercise, T, tags)
    topology(M2, exercise, lookup)
    simulate(M2, exercise, wffs, T, tags, 20)

        # Check the controls against the full model

    print()
    print("Verify controls...")
    T = greek[:8]
    S = list(tags[letter] for letter in T)
    exercise = "Verify"
    M2.new_multiverse(exercise, *S)
    assert M2.multiverse(exercise) == set(S)
    display_setup(M2, exercise, T, tags)
    topology(M2, exercise, lookup)
    simulate(M2, exercise, "".join(axioms), T, tags, 30,
             control="axioms")
    simulate(M2, exercise, "".join(definitions), T, tags, 30,
             control="definitions")
    simulate(M2, exercise, mp, T, tags, 30,
             control="modus ponens")
    wffs = ["ApNp", "CNNpp", "CCNpNqCqp", "ACpqCqp",
            "CCCpqpp", "CCCpNppp",
            "CCNpqCCpqq", "CCNppCCppp"]
    simulate(M2, exercise, "".join(wffs[:4]), T, tags, 20,
             control="not valid")
    simulate(M2, exercise, "".join(wffs[4:6]), T, tags, 20,
             control="Pierce's Law")
    simulate(M2, exercise, "".join(wffs[6:]), T, tags, 25,
             control="not valid")
    
    print("\nSUCCESS!")
