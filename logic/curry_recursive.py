"""
logic.curry_recursive - recursive combinator rules in Rosenbloom
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module will add straightfoward arithmetic rules to the
    default full rule set. In addition, recursive rules are placed
    in their own rule sets.

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
from logic.curry import full_reduction as _full_set
from logic.curry import names as _names
import logic.curry_arithmetic as CLA
CLA.add_rules()

__all__ = ("combinators", "recursives", "add_rules",
           "all_reductions", "test_standard", "test_recursive",
           "new_standard_rule", "new recursive_rule",
           "show_all", "filters", "all_filters",
           "alpha_replacement", "test_alpha_replacement")

class Settings(object):
    """settings for handling of arithmetic operators"""

    settings = dict()
    DEFAULT = "use default"
    ARITHMETIC = "use integers"
    SHORTCUTS = "use shortcuts"

    def __init__(self, *args, **kwargs):
        """initializer (not implemented"""
        raise NotImplementedError("Do not instantiate class ArithmeticSettings")

    @classmethod
    def _set(cls, name:str, value:"any", types:("Type", tuple)):
        """set a setting"""
        if not isinstance(value, types):
            raise TypeError(f"'value' for {name} must be instance of {types}")
        cls.settings[name] = value

    @classmethod
    def _fetch(cls, name:str, default) -> "value":
        """retrieve a setting"""
        if cls.default():
            return default
        return cls.settings.get(name, default)

    @classmethod
    def default(cls, value:bool=None) -> bool:
        """use default settings"""
        if value != None:
            cls._set(cls.DEFAULT, value, bool)
        return cls.settings.get(cls.DEFAULT, False)

    @classmethod
    def arithmetic(cls, value:bool=None) -> bool:
        """use default settings"""
        if value != None:
            cls._set(cls.ARITHMETIC, value, bool)
        return cls._fetch(cls.ARITHMETIC, False)

    @classmethod
    def shortcuts(cls, value:bool=None) -> bool:
        """use default settings"""
        if value != None:
            cls._set(cls.SHORTCUTS, value, bool)
        return cls._fetch(cls.SHORTCUTS, False)

combinators = dict()
combinators['A'] = ('|||Afgx', '||fx|gx', "substitutor")
combinators['B'] = ('|||Bfgx', '|f|gx', "compositor|multiplication")
combinators['C'] = ('|||Cfxy', '||fyx', "permutator")
combinators['D'] = ('||||Dfxgy', '||fx|gy', "?")
combinators['I'] = ('|Ix', 'x', "identity|one") 
combinators['K'] = ('||Kxy', 'x', "projector") 
combinators['T'] = ('||Txy', '|yx', "commutator|exponentiation")
combinators['W'] = ('||Wfx', '||fxx', 'duplicator')
combinators['0'] = ('||0ab', 'b', 'zero')
combinators['S'] = ('|||Snab', '|a||nab', 'successor')
combinators['+'] = ('||||+mnab', '||ma||nab', 'addition')
combinators['.'] = ('||||.mnab', '||m|nab', 'multiplication')
combinators['^'] = ('||||^mnab', '|||nmab', 'exponentiation')

recursives = dict()

filters = dict()

def show_all():
    """display the '__all__' tuple"""
    print("methods:", __all__)

def _title(title:str, maxline=72):
    """display a title"""
    print()
    filler = '=' * (maxline // 2)
    s = filler + '  ' + title + '  ' + filler
    chop = (len(s) - maxline) // 2
    s = s[:-chop]
    chop = len(s) - maxline
    s = s[chop:]
    print(s)    

def all_reductions(maxline=72):
    """display all defined reductions"""
    from logic.curry import names

    _title("All Reductions", maxline)
    print(f"{'Method':20} Short name")
    print("-" * maxline)
    for method in names:
        if callable(method):
            name = names[method]
            f = method.__name__
            print(f"{f:30} {name}")

def all_filters(verbose=False, maxline=72):
    """check the installed filtered rules"""
    on_or_off = lambda x: "on" if x else "off"
    default = Settings.default()
    arithmetic = Settings.arithmetic()
    shortcuts = Settings.shortcuts()
    Settings.default(False)
    Settings.arithmetic(True)
    Settings.shortcuts(True)
    _title("All Filtered Rules", maxline)
    print(f"      defaults? {on_or_off(Settings.default())}")
    print(f"    arithmetic? {on_or_off(Settings.arithmetic())}")
    print(f"     shortcuts? {on_or_off(Settings.shortcuts())}")
    for key in filters:
        tests = filters[key]
        print(f"{key.__name__}:")
        for test in tests:
            pattern, expect = test
            if verbose:
                print("  0:", pattern)
            result = Reducer.on(pattern, trace=verbose, maxlen=50)
            error = ""
            if expect == None:
                pass
            elif type(expect) == int:
                n = in_N(result.tree)
                if n == None:
                    error == f"Domain:{expect}"
                else:
                    result = n
                    if n != expect:
                        error = f"Range:{expect}"
            else:
                if str(result) != expect:
                    error = f"expected={expect}"
            result = str(result)
            print(f"     {pattern:20} {result:20} {error}")
    print("Restoring settings:")
    Settings.arithmetic(arithmetic)
    Settings.shortcuts(shortcuts)
    print(f"    arithmetic? {on_or_off(Settings.arithmetic())}")
    print(f"     shortcuts? {on_or_off(Settings.shortcuts())}")
    Settings.default(default)
    print(f"      defaults? {on_or_off(Settings.default())}")

def test_standard(verbose=False, maxline=72, rule_set:set=_full_set):
    """test the defined combinators"""
    keys = sorted(combinators.keys())
    errors = 0
    
    _title("Standard Reductions", maxline)
    print(f"Key  {'Expression':10} {'Result':15} {'Expected':15} Description")
    print("-" * maxline)
    for key in keys:
        expr, expect, name = combinators[key]
        if verbose:
            print("  0:", expr)
        result = str(Reducer.on(expr, trace=verbose, maxlen=50,
                                rule_set=rule_set, max_steps=1))
        error = "" if result == expect else expect
        errors += 1 if error else 0
        print(f" {key:3} {expr:10} {result:15} {error:15} {name}")
    if errors:
        if errors > 1:
            print(f"\n{errors} errors were detected.")
        else:
            print(f"\nOne error was detected.")

def test_recursive(verbose=False, maxline=72):
    """test the defined recursive (or self-referential) combinators"""
    keys = sorted(recursives.keys())
    errors = 0
    
    _title("Recursive Reductions", maxline)
    print(f"Key  {'Expression':10} {'Result':15} {'Expected':15} Description")
    print("-" * maxline)
    for key in keys:
        rule_set, expr, expect, name = recursives[key]
        if verbose:
            print("  0:", expr)
        result = str(Reducer.on(expr, trace=verbose, maxlen=50,
                                max_steps=1, rule_set=rule_set))
        error = "" if result == expect else expect
        errors += 1 if error else 0
        print(f" {key:3} {expr:10} {result:15} {error:15} {name}")
    if errors:
        if errors > 1:
            print(f"\n{errors} errors were detected.")
        else:
            print(f"\nOne error was detected.")

def new_standard_rule(op:str, method:callable, expr:str, expect:str,
                      description:str="?", verbose=True, max_steps=1,
                      maxline=50, rule_set:set=_full_set):
    """enter a new rule into the standard set"""
    if verbose:
        print(f"Adding a standard rule for {op=}...")
        print("    Verifying the arguments...")
    assert type(op) == str
    assert len(op) == 1
    assert type(expr) == str
    assert expr.find(op) != -1, f"{op=} must occur in {expr=}"
    assert type(expect) == str
    assert expect.find(op) == -1, f"{op=} must not occur in {expect=}"
    assert type(max_steps) == int
    assert max_steps > 0
    assert type(description) == str
    if verbose:
        print("    Parsing the expression...")
    tree = ParseTree(expr)
    if verbose:
        print("    Reducing the expression...")
        print("LHS: {expr}")
    test_set = rule_set | {method}
    result = str(Reducer.on(expr, rule_set=test_set, maxlen=maxline,
               max_steps=max_steps, trace=verbose))
    assert result == expect, f"{result=}, but {expect=}"
    if verbose:
        print("    Proposed rule has been verified.  Adding the rule...")
    combinators[op] = (expr, expect, description)
    Reducer.add_rule(method, name=op, rule_set=rule_set)
    if verbose:
        print("    The rule has been added...")

def new_recursive_rule(op:str, method:callable, expr:str, expect:str,
                      description:str="?", verbose=True, max_steps=1,
                      maxline=50, ref:str=None) -> set:
    """enter a recursive rule into a set by itself"""
    if verbose:
        print(f"  Creating a recursive rule for {op=}...")
        print("    Verifying the arguments...")
    assert type(op) == str
    assert len(op) == 1
    assert type(expr) == str
    assert expr.find(op) != -1, f"{op=} must occur in {expr=}"
    assert type(expect) == str
    assert type(max_steps) == int
    assert max_steps > 0
    assert type(description) == str
    if verbose:
        print("    Parsing the expression...")
    tree = ParseTree(expr)
    if verbose:
        print("    Reducing the expression...")
        print("LHS: {expr}")
    rule_set = {method}
    result = str(Reducer.on(expr, rule_set=rule_set, maxlen=maxline,
               max_steps=max_steps, trace=verbose))
    assert result == expect, f"{result=}, but {expect=}"
    if verbose:
        print("    Proposed rule has been verified. Logging the rule set.")
    if not ref:
        ref = op
    recursives[ref] = (rule_set, expr, expect, description)
    Reducer.rename(method, op)
    return rule_set

def lbracket_reduction(tree:ParseTree, parent, child=-1):
    """perform a left bracket reduction: |||[xyz = ||z|Kyz"""
    def Ex5ab(result, a, b, z):
        """shorten circuit using Rosenbloom page 131 ex 5 (a-b)"""
        if (not Settings.shortcuts()) and (not Settings.arithmetic()):
            return result
        if z == '0':                            # Ex 5a
            return a
        if z == 'I':                            # Ex 5b, I = |S0
            return b
        if type(z) != list or z[0] != '|':
            return result
        if z[1] == 'K' and z[2] == 'I':         # Ex 5a, |KI = 0
            return a
        if z[1] == 'S':                         # Ex 5b (universal!)
            return b
        return result

    node = tree.validate_parentage(parent, child)
    if type(node) == str or node[0] != '|':
        return False
    Exy, z = node[1], node[2]
    if type(Exy) == str or Exy[0] != '|':
        return False
    Ex, y = Exy[1], Exy[2]
    if type(Ex) == str or Ex[0] != '|' or Ex[1] != '[':
        return False
    x = Ex[2]
    result = ['|', ['|', z, ['|', 'K', y]], x]    # ||z|Kyx
    result = Ex5ab(result, x, y, z)
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def alpha_reduction(tree:ParseTree, parent, child=-1):
    """perform an alpha reduction: |αx = ||[|S|x0|x0"""
    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|' or node[1] != "α":
        return False
    x = node[2]
    x0 = ["|", x, "0"]                      # |x0
    Sx0 = ["|", "S", x0]                    # |S|x0
    result = ['|', ['|', "[", Sx0], x0]     # ||[|S|x0|x0
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def beta_reduction(tree:ParseTree, parent, child=-1):
    """perform a beta reduction: ||||βxyzw"""
    def Ex5gh(result, a, g, f, w):
        """shortcut"""
        if (not Settings.shortcuts()) and (not Settings.arithmetic()):
            return result
        if w == '0':
            return a                        # Ex 5g
        if w == 'I':
            gI = ['|', g, 'I']
            fI = ['|', f, 'I']
            return ['|', gI, fI]            # Ex 5h, |S0=I
        if type[w] == list:
            if w[0] == '|' and w[1] == 'K' and w[2] == 'I':
                return a                    # Ex 5g, 0=|KI
        if not Settings.arithmetic():
            return result
        if type(w) != list:
            return result
        n = in_N(w)
        if type(n) != int:
            return result
        n = to_N(n)
        gn = ['|', g, n]
        fn = ['|', f, n]
        return ['|', gn, fn]                # Ex 5h

    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|':
        return False
    Bxyz, w = node[1], node[2]
    if type(Bxyz) != list or Bxyz[0] != '|':
        return False
    Bxy, z = Bxyz[1], Bxyz[2]
    if type(Bxy) != list or Bxy[0] != '|':
        return False
    Bx, y = Bxy[1], Bxy[2]
    if type(Bx) != list or Bx[0] != '|' or Bx[1] != "β":
        return False
    x = Bx[2]
    Kx = ['|', 'K', x]
    lbrKx = ['|', '[', Kx]
    Pw = ['|', 'P', w]
    yPw = ['|', y, Pw]
    result = ['|', ['|', ['|', lbrKx, yPw], w], ['|', z, Pw]]
    result = Ex5gh(result, x, y, z, w)
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def predecessor_reduction(tree:ParseTree, parent, child=-1):
    """perform a predecessor reduction: |Px = |||xα|K0I"""
    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|' or node[1] != "P":
        return False
    x = node[2]
    K0 = ['|', 'K', '0']                    # |K0
    xa = ['|', x, "α"]                      # |xα
    xaK0 = ['|', xa, K0]                    # ||xα|K0
    result = ['|', xaK0, 'I']               # |||xα|K0I
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def R_reduction(tree:ParseTree, parent, child=-1):
    """perform an R reduction: ||Rxy = |ϑ||βxy

    NOTE: The theta reduction is recursive:
        ||Rxy = |ϑ|βxy = |||βxy|ϑ||βxy
    """
    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|':
        return False
    Rx, y = node[1], node[2]
    if type(Rx) != list or Rx[0] != '|' or Rx[1] != "R":
        return False
    x = Rx[2]
    betax = ['|', 'β' , x]              # |βx
    betaxy = ['|', betax , y]          # ||βxy
    result = ['|', 'ϑ', betaxy]         # |ϑ||βxy
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def theta_reduction(tree:ParseTree, parent, child=-1):
    """perform a theta reduction: |ϑa = |a|ϑa

    This reduction is recursive.  Use with caution!
    """
    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|' or node[1] != "ϑ":
        return False
    a = node[2]
    result = ['|', a, ['|', 'ϑ', a]]
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def Lambda_reduction(tree:ParseTree, parent, child=-1):
    """perform a Λ reduction: |||Λxy = |||Py||B|μxS||μx0"""
    node = tree.validate_parentage(parent, child)
    if type(node) == str or node[0] != '|':
        return False
    Lx, y = node[1], node[2]
    if type(Lx) == str or Lx[0] != '|' or Lx[1] != 'Λ':
        return False
    x = Lx[2]
    mux = ['|', 'μ', x]                 # |μx
    mux0 = ['|', mux, '0']              # ||μx0
    BmuxS = ['|', ['|', 'B', mux], 'S'] # ||B|μxS
    Py = ['|', 'P', y]                  # |Py
    PyBmuxS = ['|', Py, BmuxS]          # ||Py||B|μxS
    result = ['|', PyBmuxS, mux0]       # |||Py||B|μxS||μx0
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def in_N(node:"Tree", child=None) -> (int, None):
    """returns the integer value or None"""
    constants = {"0":0, "I":1, "2":2, "3":3, "4":4,
                 "5":5, "6":6, "7":7, "8":8, "9":9}
    if type(child) == int:
        node = node[child]
    if type(node) != list:
        return constants.get(node)
    n = 0
    while True:
        if type(node) != list:
            k = constants.get(node)
            return n + k if type(k) == int else None
        if node[0] != '|':
            return
        if node[1] != 'S':
            return
        node = node[2]
        n += 1

def to_N(n:int) -> "Tree":
    top = [0, 0, '0']
    node = top
    while n > 0:
        if n == 1:
            node[2] = 'I'
        else:
            node[2] = ['|', 'S', '0']
            node = node[2]
        n -= 1
    return top[2]

def new_plus_reduction(tree:ParseTree, parent, child=-1):
    """filtered addition"""
    def reduce_by_adding(node):
        """try this way"""
        Plusm, n = node[1], in_N(node, 2)
        if n == None:
            return
        if Plusm[0] != '|':
            return
        if Plusm[1] != '+':
            return
        m = in_N(Plusm, 2)
        if m == None:
            return
        return to_N(m+n)
        
    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|':
        return False
    if Settings.arithmetic():
        total = reduce_by_adding(node)
        if total != None:
            if parent == None:
                tree.tree = total           # surgery
            else:
                parent[child] = total       # surgery
            return total
    return CLA.plus_reduction(tree, parent, child)

def new_times_reduction(tree:ParseTree, parent, child=-1):
    """filtered multiplication"""
    def reduce_by_multiplying(node):
        """try this way"""
        Timesm, n = node[1], in_N(node, 2)
        if n == None:
            return
        if Timesm[0] != '|':
            return
        if Timesm[1] != '.':
            return
        m = in_N(Timesm, 2)
        if m == None:
            return
        return to_N(m*n)
        
    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|':
        return False
    if Settings.arithmetic():
        product = reduce_by_multiplying(node)
        if product != None:
            if parent == None:
                tree.tree = product           # surgery
            else:
                parent[child] = product       # surgery
            return product
    return CLA.times_reduction(tree, parent, child)

def new_power_reduction(tree:ParseTree, parent, child=-1):
    """filtered exponentiation"""
    def reduce_by_power(node):
        """try this way"""
        Powerm, n = node[1], in_N(node, 2)
        if n == None:
            return
        if Powerm[0] != '|':
            return
        if Powerm[1] != '^':
            return
        m = in_N(Powerm, 2)
        if m == None:
            return
        return to_N(m**n)
        
    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|':
        return False
    if Settings.arithmetic():
        product = reduce_by_power(node)
        if product != None:
            if parent == None:
                tree.tree = product           # surgery
            else:
                parent[child] = product       # surgery
            return product
    return CLA.power_reduction(tree, parent, child)

def mu_reduction(tree:ParseTree, parent, child=-1):
    """perform a mu reduction: ||||μfa

    This is a recursive rule! Use with caution!

        μ = |ϑλxλyλz|||[z||xy|Sz|yz
    ||μfa = ||(|ϑλxλyλz|||[z||xy|Sz|yz)fa
          = |||ϑMfa
          = |||M|ϑMfa
          = |||Mxyz where x=|ϑM=μ, y=f, z=a
    """
    node = tree.validate_parentage(parent, child)
    if type(node) != list or node[0] != '|':
        return False
    Mf, a = node[1], node[2]
    if type(Mf) != list or Mf[0] != '|' or Mf[1] != "μ":
        return False
    f = Mf[2]
    lbrz = ['|', '[', a]
    xy = ['|', 'μ', f]
    Sz = ['|', 'S', a]
    yz = ['|', f, a]
    result = ['|', ['|', lbrz, ['|', xy, Sz]], yz]
    if parent == None:
        tree.tree = result                  # surgery
    else:
        parent[child] = result              # surgery
    return result

def add_rules(verbose=False):
    """add reduction rules from exercises in Rosenbloom"""
    default = Settings.default()
    Settings.default(True)
    assert Settings.default() == True
    if verbose:
        print("ADDING STANDARD RULES...")
    new_standard_rule('[', lbracket_reduction, '|||[xyz', '||z|Kyx',
                      "left bracket", verbose=verbose, max_steps=1,
                      maxline=50)
    new_standard_rule('α', alpha_reduction, '|αx', '||[|S|x0|x0',
                      "alpha reduction", verbose=verbose, max_steps=1,
                      maxline=50)
    new_standard_rule('β', beta_reduction, '||||βxyxw',
                      '||||[|Kx|y|Pww|x|Pw',
                      "beta reduction", verbose=verbose, max_steps=1,
                      maxline=50)
    new_standard_rule('P', predecessor_reduction, '|Px', '|||xα|K0I',
                      "predecessor", verbose=verbose, max_steps=1,
                      maxline=50)
    new_standard_rule('R', R_reduction, '||Rxy', '|ϑ||βxy',
                      "recursion setter", verbose=verbose, max_steps=1,
                      maxline=50)
    new_standard_rule('Λ', Lambda_reduction, '||Λxy', '|||Py||B|μxS||μx0',
                      "big lambda reduction", verbose=verbose, max_steps=1,
                      maxline=50)

    if verbose:
        print("ADDING RECURSIVE RULES...")
    new_recursive_rule('ϑ', theta_reduction, '|ϑx', '|x|ϑx',
                      "theta reduction", verbose=verbose, max_steps=1,
                      maxline=50, ref='th')
    new_recursive_rule('μ', mu_reduction, '||μfa', '|||[a||μf|Sa|fa',
                      "mu reduction", verbose=verbose, max_steps=1,
                      maxline=50, ref='mu')
    Settings.default(default)
    
    if verbose:
        print("ADDING FILTER RULES...")
    if CLA.plus_reduction in _full_set:
        _full_set.remove(CLA.plus_reduction)
        del _names[CLA.plus_reduction]
        Reducer.add_rule(new_plus_reduction, name='+')
        if verbose:
            print("replacing plus_reduction...")
        filters[new_plus_reduction] = (("||+|S|S00", 2), \
                ("||+0|S|S0", 2), ("||||+mnab", "||ma||nab"))
    if CLA.times_reduction in _full_set:
        _full_set.remove(CLA.times_reduction)
        del _names[CLA.times_reduction]
        Reducer.add_rule(new_times_reduction, name='•')
        if verbose:
            print("replacing times_reduction...")
        filters[new_times_reduction] = (("||.|SI|S|SI", 6), \
                ("||||.mnab", "||m|nab"))
    if CLA.power_reduction in _full_set:
        _full_set.remove(CLA.power_reduction)
        del _names[CLA.power_reduction]
        Reducer.add_rule(new_power_reduction, name='mⁿ')
        if verbose:
            print("replacing power_reduction...")
        filters[new_power_reduction] = (("||^|SI|S|SI", 8), \
                ("||||^mnab", "|||nmab"))
    if verbose:
        print("registering |||[abn (left bracket)")
    filters[lbracket_reduction] = (("|||[ab0", "a"), ("|||[abI", "b"), \
        ("|||[ab|KI", "a"), ("|||[ab|Sx", "b"))

    if verbose:
        print("registering |||βagfw (beta)")
    filters[beta_reduction] = (("||||βagf0", "a"), \
        ("||||βagf|KI", "a"), ("||||βagfI", "||gI|fI"), \
        ("||||βagf|S|S|S0", "||g|S|SI|f|S|SI"))

    if verbose:
        print("RULES HAVE BEEN UPDATED...")

def alpha_replacement(tree:(ParseTree, str), n:(ParseTree, str),
                      max_steps=10, verbose=False) -> ParseTree:
    """replace expressions of the form |||nα|K00 with n

    This replacement is valid if n is in ℕ.
    """
    if type(tree) != ParseTree:
        tree = ParseTree(tree)
    if type(n) != ParseTree:
        n = ParseTree(n)

    def Ex5c(node, parent, child=-1):
        """check a location: |||nα|K00 = n"""
        if type(node) != list or node[0] != '|' or node[2] != '0':
            return
        nak0 = node[1]
        if type(nak0) != list or nak0[0] != '|' or nak0[2] != ['|', 'K', '0']:
            return
        na = nak0[1]
        if type(na) != list or na[0] != '|' or na[1] != n.tree or na[2] != 'α':
            return
        if parent == None:
            tree.tree = n.tree
        else:
            parent[child] = n.tree
        return n

    def Corr5c(node, parent, child=-1):
        """check a location: |||nα|K00 = |Pn"""
        if type(node) != list or node[0] != '|' or node[2] != 'I':
            return
        nak0 = node[1]
        if type(nak0) != list or nak0[0] != '|' or nak0[2] != ['|', 'K', '0']:
            return
        na = nak0[1]
        if type(na) != list or na[0] != '|' or na[1] != n.tree or na[2] != 'α':
            return
        result = ['|', 'P', n.tree]
        if parent == None:
            tree.tree = result
        else:
            parent[child] = result
        return result

    count = 0
    if verbose:
        print("Alpha replacement for", str(n))
        print("  0:", str(tree))
    while count < max_steps:
        stack = list()
        packet = tree.tree, None
        stack.append(packet)
        count += 1
        found = False
        while stack:
            packet = stack.pop()
            result = Ex5c(*packet)
            if result == None:
                result = Corr5c(*packet)
            if result == None:
                node = packet[0]
                if type(node) == list and node[0] == '|':
                    packet = node[1], node, 1
                    stack.append(packet)
                    packet = node[2], node, 2
                    stack.append(packet)
                continue
            if verbose:
                print(f"{count:3}:", str(tree))
            found = True
            break
        if not found:
            break
    return tree

def test_alpha_replacement(verbose=False, maxline=72):
    """test the alpha replacement tool"""
    _title("Alpha Replacement", maxline)

    result = alpha_replacement("n", "n", verbose=verbose)
    assert str(result) == "n", str(result)

    result = alpha_replacement("|nα", "n", verbose=verbose)
    assert str(result) == "|nα", str(result)

    result = alpha_replacement("||nαK", "n", verbose=verbose)
    assert str(result) == "||nαK", str(result)

    result = alpha_replacement("||nα|K0", "n", verbose=verbose)
    assert str(result) == "||nα|K0", str(result)
    print("simple failures: ok!")

    result = alpha_replacement("|||nα|K00", "n", verbose=verbose)
    assert str(result) == "n", str(result)

    result = alpha_replacement("|||mα|K00", "m", verbose=verbose)
    assert str(result) == "m", str(result)

    result = alpha_replacement("|||mα|K0I", "m", verbose=verbose)
    assert str(result) == "|Pm", str(result)

    result = alpha_replacement("||||mα|K00|||nα|K00", "m", verbose=verbose)
    assert str(result) == "|m|||nα|K00", str(result)

    result = alpha_replacement("||||mα|K00|||nα|K00", "n", verbose=verbose)
    assert str(result) == "||||mα|K00n", str(result)
    print("single instances: ok!")

    result = alpha_replacement("||||mα|K00|||mα|K00", "m", verbose=verbose)
    assert str(result) == "|mm", str(result)
    print("repetitions: ok!")

    result = alpha_replacement("||||mα|K00|||mα|K00", "m", \
            verbose=verbose, max_steps=1)
    assert str(result) == "||||mα|K00m", str(result)
    print("single application: ok!")

    print("all tests: ok!")

if __name__ == "__main__":
    def test_match(v1, v2):
        assert v1 == v2, f"{v1}, expect {v2}"
    test_match(Settings.default(), False)
    test_match(Settings.arithmetic(), False)
    test_match(Settings.shortcuts(), False)
    test_match(in_N('K'), None)
    test_match(in_N('0'), 0)
    test_match(in_N('I'), 1)
    test_match(in_N('2'), 2)
    test_match(in_N(['|', 'S' , '0']), 1)
    test_match(in_N(['|', 'S' , 'I']), 2)
    test_match(in_N(['|', 'S' , '2']), 3)
    test_match(in_N(['|', 'A' , '0']), None)
    test_match(in_N(['|', 'A' , ['|', 'S' , '0']]), None)
    test_match(in_N(['|', 'S' , ['|', 'S' , '0']]), 2)
    test_match(to_N(0), '0')
    test_match(to_N(1), 'I')
    test_match(to_N(2), ['|', 'S' , 'I'])
    test_match(to_N(3), ['|', 'S' , ['|', 'S' , 'I']])

    show_all()
    all_reductions()
    test_standard()
    add_rules(verbose=True)
    assert Settings.default() == False
    all_reductions()
    test_standard()
    test_recursive()
    all_filters()
    test_alpha_replacement()
