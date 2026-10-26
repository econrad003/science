"""
logic.curry - combinatory logic
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Combinatory logic as laid out here was developed by Haskell Curry.
    (I am following the presentation as given in Rosenbloom [1].)

    The system, which we will call CL consists of a set of constants 𝕮,
    a binary operator "|" called either "the stroke" or application, and
    an equivalence relation "=" on 𝕮 called equality.  (The name 𝕮 for
    the set of constants is a bold script C (often called "Gothic", but
    that's a misnomer.  We use that font for the set of constants and
    reserve normal typeface letters for constants.)

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

    We can think of the stroke | as function application:

        |fx = f(x).

    The key difference here is that, if f(x) is undefined, we have a
    uniquely determined constant which represents some undefined value.
    There is no distinction being made here between constants which
    represent operators and those which represent operands,

    The constant K is a binary projection operator which discards its
    second argument:

        ||Kab = K(a,b) = a.

    Rosenbloom calls K the constancy operator.  (I prefer to think of it
    as a simple projection, so my name for it is the projector.)

    The constant A is a ternary operator which takes two unary functions
    and a value:
        ||Afgx = F(x, g(x)) = ||fx|gx.

BASIC DEFINED CONSTANTS

    The set of constants is denumerably infinite.  Here are some of the
    more interesting ones (see Rosenbloom [1, page 113].

        I = ||AKK.                               indentificator
            |Ia = |||AKKa
                = ||Ka|Ka               (C1)
                = a                     (C2)
        B = ||A|KAK                              compositor
            |Ba = |||A|KAKa
                = |||KAa|Ka             (C1)
                = |A|Ka                 (C2)
            |||Babc = |||A|Kabc         (Ba)
                    = |||Kac|bc         (C1)
                    = |a|bc             (C2)

            The B combinator represents function composition:
                |||Bfgx = |f|gx = f(g(x))

        W = ||AA|AK                               duplicator
            ||Wab = ||||AA|AKab
                  = |||Aa||AKab         (C1)
                  = ||ab|||AKab         (C1)
                  = ||ab||Kb|ab         (C1)
                  = ||abb               (C2)

            Think of a and b as functions...
                |||Wfgx = |||fggx = f(g(g(x)))

        D = |BB
            |||||BBabcd = |||B|abcd     (Babc)
                        = ||ab|cd       (Babc)

        C = ||A|DA|KK                              permutator
            |||||A|DA|KKabc
                = |||||DAa||KKabc       (C1)
                = |||Aa|||KKabc         (Dabcd)
                = ||ac||||KKabc         (C1)
                = ||ac||Kbc             (C2)
                = ||acb                 (C2)

        T = |CI
            |||CIab = ||Iba             (Cabc)
                    = |ba               (Ia)

OTHER RESULTS

    Reduction is useful but some proofs require E5.  For example:

    Prove: |BI = I
    Proof:
        Let a and b be arbitrary elements of 𝕮.
        Then:
            |||BIab = |I|ab = |ab.            by reduction
            |||BIab = |ab.                    by transitivity (E3)
        Also:
              ||Iab = |ab.                    by reduction
                |ab = ||Iab.                  by symmetry (E2)
        Thus:
            |||BIab = ||Iab.                  by transitivity (E3)
        Now b and a are both arbitrary, so:
              ||BIa = |Ia.                    by E5
                |BI = I.                      by E5
                            Q.E.D.

    Combinatory logic goes much deeper than this.  Rosenbloom shows that
    it is adequate for much of arithmetic.

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

__all__ = list()

class ParseTree(object):
    """manage a parse tree for the expression"""

    def __init__(self, expr:str):
        """build the parse tree"""
        self.tree = expr

    @property
    def tree(self):
        """return the parse tree"""
        return self.__tree

    @tree.setter
    def tree(self, expr:str):
        """parse the expression"""
        stack = list()
        reversed_expr = expr[::-1]
        for c in reversed_expr:
            if c == "|":
                a = stack.pop()
                b = stack.pop()
                node = ["|", a, b]
                stack.append(node)
            else:
                stack.append(c)
        if len(stack) != 1:
            raise ValueError(f"{expr} is ill-formed: {len(stack)=}")
        self.__tree = stack[0]

    def validate_parentage(self, parent, child):
        """validation to catch errors in reduction"""
        if parent == None:
            return self.tree
        if type(parent) != list:
            raise TypeError("Invalid parent node; expected a list", type(parent))
        if parent[0] != '|':
            raise RuntimeError("Invalid parent node; expected '|'")
        if 0 < child < 3:
            return parent[child]
        raise ValueError(f"invalid child; expected [1,2]")

    def A_reduce(self, parent, child:int=-1):
        """perform an A reduction: |||Aabc = ||ac|bc"""
        node = self.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|':
            return False
        Aab, c = node[1], node[2]
        if type(Aab) == str or Aab[0] != '|':
            return False
        Aa, b = Aab[1], Aab[2]
        if type(Aa) == str or Aa[0] != '|' or Aa[1] != 'A':
            return False
        a = Aa[2]
        bc = ['|', b, c]
        ac = ['|', a, c]
        result = ['|', ac, bc]
        if parent == None:
            self.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result

    def K_reduce(self, parent, child:int=-1):
        """perform a K reduction: ||Kab = a"""
        node = self.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|':
            return False
        Ka, b = node[1], node[2]
        if type(Ka) == str or Ka[0] != '|' or Ka[1] != 'K':
            return False
        result = Ka[2]
        if parent == None:
            self.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result

    def I_reduce(self, parent, child:int=-1):
        """perform an I reduction: |Ia = a"""
        node = self.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|' or node[1] != 'I':
            return False
        result = node[2]
        if parent == None:
            self.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result

    def B_reduce(self, parent, child:int=-1):
        """perform a B reduction: |||Babc = |a|bc"""
        node = self.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|':
            return False
        Bab, c = node[1], node[2]
        if type(Bab) == str or Bab[0] != '|':
            return False
        Ba, b = Bab[1], Bab[2]
        if type(Ba) == str or Ba[0] != '|' or Ba[1] != 'B':
            return False
        a = Ba[2]
        bc = ['|', b, c]
        result = ['|', a, bc]
        if parent == None:
            self.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result

    def W_reduce(self, parent, child:int=-1):
        """perform a W reduction: ||Wab = ||abb"""
        node = self.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|':
            return False
        Wa, b = node[1], node[2]
        if type(Wa) == str or Wa[0] != '|' or Wa[1] != 'W':
            return False
        a = Wa[2]
        ab = ['|', a, b]
        result = ['|', ab, b]
        if parent == None:
            self.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result

    def D_reduce(self, parent, child:int=-1):
        """perform a D reduction: ||||Dabcd = ||ab|cd"""
        node = self.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|':
            return False
        Dabc, d = node[1], node[2]
        if type(Dabc) == str or Dabc[0] != '|':
            return False
        Dab, c = Dabc[1], Dabc[2]
        if type(Dab) == str or Dab[0] != '|':
            return False
        Da, b = Dab[1], Dab[2]
        if type(Da) == str or Da[0] != '|' or Da[1] != 'D':
            return False
        a = Da[2]
        ab = ['|', a, b]
        cd = ['|', c, d]
        result = ['|', ab, cd]
        if parent == None:
            self.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result

    def C_reduce(self, parent, child:int=-1):
        """perform a C reduction: |||Cabc = ||abc"""
        node = self.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|':
            return False
        Cab, c = node[1], node[2]
        if type(Cab) == str or Cab[0] != '|':
            return False
        Ca, b = Cab[1], Cab[2]
        if type(Ca) == str or Ca[0] != '|' or Ca[1] != 'C':
            return False
        a = Ca[2]
        ac = ['|', a, c]
        result = ['|', ac, b]
        if parent == None:
            self.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result

    def T_reduce(self, parent, child:int=-1):
        """perform a T reduction: ||Tab = |ba"""
        node = self.validate_parentage(parent, child)
        if type(node) == str or node[0] != '|':
            return False
        Ta, b = node[1], node[2]
        if type(Ta) == str or Ta[0] != '|' or Ta[1] != 'T':
            return False
        a = Ta[2]
        result = ['|', b, a]
        if parent == None:
            self.tree = result                  # surgery
        else:
            parent[child] = result              # surgery
        return result

    @property
    def depth(self):
        """return the maximum depth of a leaf node

        The root has depth 0.
        """
        max_depth = 0
        stack = list()
        stack.append((max_depth, self.tree))
        while stack:
            d, node = stack.pop()
            max_depth = max(d, max_depth)
            if type(node) == list:
                d += 1
                for subnode in node[1:]:
                    stack.append((d, subnode))
        return max_depth

    @classmethod
    def node_to_str(cls, node:(str, tuple)) -> str:
        """express a node as a string"""
        if type(node) == str:
            return node
        if type(node) != list:
            raise TypeError("Unkknown type for node")
        s = str(node[0])
        for subnode in node[1:]:
            s += cls.node_to_str(subnode)
        return s

    def __str__(self):
        """express the current tree as a string"""
        return self.node_to_str(self.tree)

__all__.append("ParseTree")

class named_set(set):
    """a set with its own name"""
    def __init__(self, name, *args):
        super(named_set,self).__init__(*args)
        self.__name__ = name

    # Rosenbloom's primitives
AK_reduction = named_set("AK_reduction")
AK_reduction.add(ParseTree.A_reduce)
AK_reduction.add(ParseTree.K_reduce)
__all__.append("AK_reduction")

    # Rosenbloom's lambda primitives
AKI_reduction = named_set("AKI_reduction")
AKI_reduction.add(ParseTree.A_reduce)
AKI_reduction.add(ParseTree.K_reduce)
AKI_reduction.add(ParseTree.I_reduce)
__all__.append("AKI_reduction")

    # Curry's primitives
BCWK_reduction = named_set("BCWK_reduction")
BCWK_reduction.add(ParseTree.B_reduce)
BCWK_reduction.add(ParseTree.C_reduce)
BCWK_reduction.add(ParseTree.W_reduce)
BCWK_reduction.add(ParseTree.K_reduce)
__all__.append("BCWK_reduction")

    # all defined above
full_reduction = AKI_reduction | BCWK_reduction
full_reduction.add(ParseTree.D_reduce)
full_reduction.add(ParseTree.T_reduce)

    # short names for the rules
names = {}
names[ParseTree.A_reduce] = "A"
names[ParseTree.K_reduce] = "K"
names[ParseTree.I_reduce] = "I"
names[ParseTree.B_reduce] = "B"
names[ParseTree.C_reduce] = "C"
names[ParseTree.W_reduce] = "W"
names[ParseTree.D_reduce] = "D"
names[ParseTree.T_reduce] = "T"
names[None] = "FAIL"
names[False] = "FAIL"

class Reducer(object):
    """reduce an expression"""

    @staticmethod
    def name(rule:callable):
        """return the name of a rule"""
        return names.get(rule, "unregistered rule")

    @staticmethod
    def rename(rule:callable, name:str):
        """name a rule"""
        names[rule] = name

    @staticmethod
    def add_rule(rule:callable, name:str=None, rule_set:set=full_reduction):
        """add a rule to a rule set"""
        rule_set.add(rule)
        if name:
            Reducer.rename(rule, name)

    @staticmethod
    def apply_rule(tree:ParseTree, where:list=None, child=-1,
                   rule_set:set=full_reduction):
        """returns either None or the rule that was applied"""
        for rule in rule_set:
            result = rule(tree, where, child)
            if result not in (None, False):
                return rule

    @classmethod
    def search_and_apply(cls, tree:ParseTree, rule_set:set=full_reduction):
        """search for a place where a rule can be applied

        If a place is found, apply and return the rule.  Otherwise
        return None.
        """
            # try the top level
        rule = cls.apply_rule(tree, rule_set=rule_set)
        if rule != None:
            return rule
        stack = list()
        stack.append(tree.tree)
        while stack:
            top = stack.pop()
            if type(top) != list:
                continue        # atomic expression
            rule = cls.apply_rule(tree, top, 1, rule_set)
            if rule != None:
                return rule
            rule = cls.apply_rule(tree, top, 2, rule_set)
            if rule != None:
                return rule
            stack.append(top[2])
            stack.append(top[1])

    @classmethod
    def on(cls, expr:str, rule_set:set=full_reduction,
           max_steps=10, trace=True, maxlen=72):
        """parse and reduce"""
        tree = ParseTree(expr)
        results = list()
        steps = 0

        def log(reason:str):
            """log the result"""
            expr2 = str(tree)
            result = (steps, expr2, reason)
            results.append(result)
            if trace:
                msg1 = f"{steps:3}: {expr2} "
                filler = " " * (maxlen - len(msg1))
                print(msg1 + filler + reason)
        results.append((str(tree), "Start"))
        
        while steps < max_steps:
            steps += 1
            rule = cls.search_and_apply(tree, rule_set)
            if rule == None:
                break
            log(cls.name(rule))
        
        return tree

__all__.append("Reducer")

if __name__ == "__main__":
    print("__all__:", ", ".join( __all__))

    print()
    print("Example 1: I reduction")
    expr = "|||AKKa"
    tree = ParseTree(expr)
    print("         expr =", tree)
    print("         tree =", tree.tree)
    print("        depth =", tree.depth)
    assert str(tree) == expr, str(tree)
    tree.A_reduce(None)
    print("   A reduction:", tree)
    tree.K_reduce(None)
    print("   K reduction:", tree)
    assert str(tree) == "a", str(tree)
        # test different ways of doing reductions
    expr = "|Ia"
    tree = ParseTree(expr)
    tree.I_reduce(None)
    assert str(tree) == "a", str(tree)
    tree = ParseTree(expr)
    ParseTree.I_reduce(tree, None)                # extended syntax
    assert str(tree) == "a", str(tree)
    tree = ParseTree(expr)
    rule = Reducer.apply_rule(tree)               # extended syntax
    assert str(tree) == "a", str(tree)
    assert Reducer.name(rule) == "I"
        # epidermal surgery #1
    expr = "||Iab"
    tree = ParseTree(expr)
    tree.I_reduce(tree.tree, 1)
    assert str(tree) == "|ab", str(tree)
    tree = ParseTree(expr)
    Reducer.apply_rule(tree, tree.tree, 1)        # extended syntax
    assert str(tree) == "|ab", str(tree)
    tree = ParseTree(expr)
    rule = Reducer.apply_rule(tree, tree.tree, 1) # extended syntax
    assert str(tree) == "|ab", str(tree)
    assert Reducer.name(rule) == "I"
        # epidermal surgery #2
    expr = "|a|Ib"
    tree = ParseTree(expr)
    tree.I_reduce(tree.tree, 2)
    assert str(tree) == "|ab", str(tree)
    tree = ParseTree(expr)
    ParseTree.I_reduce(tree, tree.tree, 2)        # extended syntax
    assert str(tree) == "|ab", str(tree)
    tree = ParseTree(expr)
    rule = Reducer.apply_rule(tree, tree.tree, 2) # extended syntax
    assert str(tree) == "|ab", str(tree)
    assert Reducer.name(rule) == "I"
        # interal surgery #1
    expr = "|||Iabc"
    tree = ParseTree(expr)
    tree.I_reduce(tree.tree[1], 1)
    assert str(tree) == "||abc", str(tree)
    tree = ParseTree(expr)
    ParseTree.I_reduce(tree, tree.tree[1], 1)     # extended syntax
    assert str(tree) == "||abc", str(tree)
    tree = ParseTree(expr)
    rule = Reducer.apply_rule(tree, tree.tree[1], 1) # extended syntax
    assert str(tree) == "||abc", str(tree)
    assert Reducer.name(rule) == "I"
        # internal surgery #2
    expr = "||a|Ibc"
    tree = ParseTree(expr)
    tree.I_reduce(tree.tree[1], 2)
    assert str(tree) == "||abc", str(tree)
    tree = ParseTree(expr)
    ParseTree.I_reduce(tree, tree.tree[1], 2)     # extended syntax
    assert str(tree) == "||abc", str(tree)
    tree = ParseTree(expr)
    rule = Reducer.apply_rule(tree, tree.tree[1], 2) # extended syntax
    assert str(tree) == "||abc", str(tree)
    assert Reducer.name(rule) == "I"
        # interal surgery #3
    expr = "|a||Ibc"
    tree = ParseTree(expr)
    tree.I_reduce(tree.tree[2], 1)
    assert str(tree) == "|a|bc", str(tree)
    tree = ParseTree(expr)
    ParseTree.I_reduce(tree, tree.tree[2], 1)     # extended syntax
    assert str(tree) == "|a|bc", str(tree)
    tree = ParseTree(expr)
    rule = Reducer.apply_rule(tree, tree.tree[2], 1) # extended syntax
    assert str(tree) == "|a|bc", str(tree)
    assert Reducer.name(rule) == "I"
        # internal surgery #4
    expr = "|a|b|Ic"
    tree = ParseTree(expr)
    tree.I_reduce(tree.tree[2], 2)
    assert str(tree) == "|a|bc", str(tree)
    tree = ParseTree(expr)
    ParseTree.I_reduce(tree, tree.tree[2], 2)     # extended syntax
    assert str(tree) == "|a|bc", str(tree)
    tree = ParseTree(expr)
    rule = Reducer.apply_rule(tree, tree.tree[2], 2) # extended syntax
    assert str(tree) == "|a|bc", str(tree)
    assert Reducer.name(rule) == "I"

    print()
    print("Example 2: B reduction")
    expr = "|||A|Kabc"
    tree = ParseTree(expr)
    print("         expr =", tree)
    print("         tree =", tree.tree)
    print("        depth =", tree.depth)
    assert str(tree) == expr, str(tree)
    tree.A_reduce(None)
    print("   A reduction:", tree)
    tree.K_reduce(tree.tree, 1)
    print("   K reduction:", tree)
    assert str(tree) == "|a|bc", str(tree)
    expr = "|||Babc"
    tree = ParseTree(expr)
    tree.B_reduce(None)
    assert str(tree) == "|a|bc", str(tree)

    print()
    print("Example 3: W reduction")
    expr = "||||AA|AKab"
    tree = ParseTree(expr)
    print("         expr =", tree)
    print("         tree =", tree.tree)
    print("        depth =", tree.depth)
    assert str(tree) == expr, str(tree)
    tree.A_reduce(tree.tree, 1)
    print("   A reduction:", tree)
    tree.A_reduce(None)
    print("   A reduction:", tree)
    tree.A_reduce(tree.tree, 2)
    print("   A reduction:", tree)
    tree.K_reduce(tree.tree, 2)
    print("   K reduction:", tree)
    expr = "|||Wfgx"
    tree = ParseTree(expr)
    tree.W_reduce(tree.tree, 1)
    assert str(tree) == "|||fggx", str(tree)
    print("SUCCESS!")

    print()
    print("Example 4: D reduction")
    expr = "|||||BBabcd"
    tree = ParseTree(expr)
    print("         expr =", tree)
    print("         tree =", tree.tree)
    print("        depth =", tree.depth)
    assert str(tree) == expr, str(tree)
    tree.B_reduce(tree.tree[1], 1)
    print("   B reduction:", tree)
    tree.B_reduce(None)
    print("   B reduction:", tree)
    assert str(tree) == "||ab|cd", str(tree)
    expr = "||||Dabcd"
    tree = ParseTree(expr)
    tree.D_reduce(None)
    assert str(tree) == "||ab|cd", str(tree)

    print()
    print("Example 5: C reduction")
    expr = "|||||A|DA|KKabc"
    tree = ParseTree(expr)
    print("         expr =", tree)
    print("         tree =", tree.tree)
    print("        depth =", tree.depth)
    assert str(tree) == expr, str(tree)
    tree.A_reduce(tree.tree[1], 1)
    print("   A reduction:", tree)
    tree.D_reduce(tree.tree, 1)
    print("   D reduction:", tree)
    tree.A_reduce(None)
    print("   A reduction:", tree)
    tree.K_reduce(tree.tree[2][1], 1)
    print("   K reduction:", tree)
    tree.K_reduce(tree.tree, 2)
    print("   K reduction:", tree)
    assert str(tree) == "||acb", str(tree)
    expr = "|||Cabc"
    tree = ParseTree(expr)
    tree.C_reduce(None)
    assert str(tree) == "||acb", str(tree)

    print()
    print("Example 6: T reduction")
    expr = "|||CIab"
    tree = ParseTree(expr)
    print("         expr =", tree)
    print("         tree =", tree.tree)
    print("        depth =", tree.depth)
    assert str(tree) == expr, str(tree)
    tree.C_reduce(None)
    print("   C reduction:", tree)
    tree.I_reduce(tree.tree, 1)
    print("   I reduction:", tree)
    assert str(tree) == "|ba", str(tree)
    expr = "||Tab"
    tree = ParseTree(expr)
    tree.T_reduce(None)
    assert str(tree) == "|ba", str(tree)

    print()
    print("Example 7: Prove: |BI = I")
    expr = "|||BIab"
    tree = ParseTree(expr)
    s1 = "        " + expr + " = "
    s2 = "        " + expr + " = "
    print("         expr =", tree)
    tree.B_reduce(None)
    print("   B reduction:", tree)
    s1 += str(tree) + " = "
    tree.I_reduce(None)
    print("   I reduction:", tree)
    s1 += str(tree) + "."
    s2 += str(tree) + "."
    assert str(tree) == "|ab", str(tree)
    expr = "||Iab"
    tree = ParseTree(expr)
    print("         expr =", tree)
    s3 = "        " + expr + " = "
    s4 = " = " + expr + "."
    tree.I_reduce(tree.tree, 1)
    print("   I reduction:", tree)
    s3 += str(tree) + "."
    s4 = "        " + str(tree) + s4
    assert str(tree) == "|ab", str(tree)
    filler = 40 - len(s1)
    print(s1, " "*filler, "by reduction")
    filler = 40 - len(s2)
    print(s2, " "*filler, "by transitivity (E3)")
    filler = 40 - len(s3)
    print(s3, " "*filler, "by reduction")
    filler = 40 - len(s4)
    print(s4, " "*filler, "by symmetry (E2)")
    s = "        |||BIab = ||Iab."
    filler = 40 - len(s)
    print(s, " "*filler, "by transitivity (E3)")
    s = "        ||BIa = |Ia."
    filler = 40 - len(s)
    print(s, " "*filler, "by E5 since b is arbitrary")
    s = "        |BI = I.             QED."
    filler = 40 - len(s)
    print(s, " "*filler, "by E5 since a is arbitrary")

    print("Example 8")
    items = expr1, expr2 = "||C||BBBK", "||B|BK||BCC"
    print(f"Show that {expr1} = {expr2}")
    for item in items:
        expr = "||||" + item + "abcd"
        print("expr:", expr, " --> BCWK_reduction")
        tree = Reducer.on(expr, rule_set=BCWK_reduction)
        print("result:", tree)

