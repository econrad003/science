"""
logic.divisors3 - logic based on divisor lattices (experimental)
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

EXAMPLE

    Pick an integer larger than 1 and consider its divisors, the
    positive integers that evenly divide the given number.  For example,
    consider the number 36.  Written as a product of primes, we have:
            36 = 2² ⋅ 3².
    We can arrange the divisors in a graph called the Hasse diagram for
    the lattice of divisors of 36:

                             36=T     (top value)
                            ╱ ╲
                           ╱   ╲
                          ╱     ╲
                         12     18
                        ╱ ╲     ╱ ╲
                       ╱   ╲   ╱   ╲
                      ╱     ╲ ╱     ╲
                     4       6       9
                      ╲     ╱ ╲     ╱
                       ╲   ╱   ╲   ╱
                        ╲ ╱     ╲ ╱
                         2       3
                          ╲     ╱
                           ╲   ╱
                            ╲ ╱
                             1=F    (bottom value)

    In the lattice, the join of two elements is the smallest element
    that we can reach from both elements by zero or more upward
    moves in the diagram.  In other words:
        p∨q := lcm(p,q)     (join = least common multiple)

    Similarly, the meet of two elements is the largest element
    that we can reach from both elements by zero or more downward
    moves in the diagram.  In other words:
        p∧q := gcd(a,b)     (meet = greatest common divisor)

    We can define the logical negative as a quotient:
        ~p := 36÷p

    In the latice of divisors, we can define partial order relations
    in terms of joins and equality:
        (p ≥ q) := (p = p∨q)
        (p ≤ q) := (q = p∨q)
    or equivalently using meets:
        (p ≥ q) := (q = p∧q)
        (p ≤ q) := (p = p∧q)
    or directly in terms of divisibility:
        (p ≥ q) := (q | p)
        (p ≤ q) := (p | q)
    In the diagram, p ≤ q means that we can reach q from p by a
    strictly ascending path.  (We allow the length of path to be
    zero so that p≤p.)

    p > q means that p ≥ q but p ≠ q.  Similary, p < q means that
    p ≤ q but p ≠ q.  Note that two numbers are not necesarily
    comparable.  For example, using these definitions, 4 and 18
    are not comparable.

    For material implication, we have some flexibility.  The main
    requirements are that:
        if p ≤ q, then p⊃q := T;
        if p > q, then p⊃q < T; and
        T⊃F=F.

    For the lattice of divisors of 36 (above), this gives the following
    incomplete matrix:

        p⊃q             p
         p     1   2   3   4   6   9  12  18  36
         1    36  36  36  36  36  36  36  36  36
         2     *  35   *  36  36   *  36  36  36
         3     *   *  36   *  36  36  36  36  36
         4     *   *   *  36   *   *  36   *  36
         6     *   *   *   *  36   *  36  36  36
         9     *   *   *   *   *  36   *  36  36
        12     *   *   *   *   *   *  36   *  36
        18     *   *   *   *   *   *   *  36  36
        36     1   *   *   *   *   *   *   *  36

    The asterisks represent entries that are not 36.

    Some choices for defining the starred values include:
        (a) the value of q; or
        (b) the value of p∧q (i.e. their greatest common divisor); or
        (c) top / (p∨q), i.e. n / lcm(p, q)
        (d) q * top / (p∨q)
        (e) 1

    (b) and (c) are not transitive -- using them yields material
    equivalence which fails as an equivalence relation for some
    values of n.  Here we experiment with (d) which _seems_ to produce
    a transitive implication function under very general condition.
    (Ideally we should prove this claim.  At minimum, we should test
    it.)


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
from math import gcd, lcm

class DivisorLogic(object):
    """propositional logic based on lattices of divisors"""

    __slots__ = ("__top", "__bottom", "__lattice", "__implication")

    @classmethod
    def _message(cls, method, message) -> str:
        """prefix the message"""
        return cls.__name__ + "::" + method + ": " + message

            # PART 1 - INSTANTIATION

    def __init__(self, *args, implication:"Function"=None,
                 verify=False):
        """initializer

        POSITIONAL ARGUMENTS

            n - the top element

                The positional arguments are passed to helper method
                make_lattice to obtain the values of __top, __bottom,
                amd __lattice.

        KEYWORD ARGUMENTS

            implication - a function implication(p,q) which defines
                the value of p⊃q when either p does not divide q or
                (p,q) is not equal to (n,1).

                If this function is not provided, it is set to the
                value returned by helper method implication_fails_default.

            verify - if True, verifies that the implication operation
                is well-defined
        """
        lattice = self.make_lattice(*args)
        self.__top, self.__bottom, self.__lattice = lattice
        if implication == None:
            implication = self.implication_fails_default(self.__top)
        self.__implication = self.make_implication(implication, verify)

    @classmethod
    def make_lattice(cls, n:int) -> "(TOP, BOTTOM, LATTICE)":
        """returns the top element, the bottom element, and the full set

        Note that these are set in __init__ based on the values returned
        by this method.  Subclasses may redefine this method but should
        return top (an int), bottom (an int), and lattice (a set with a
        divisibility lattice structure which includes both top and bottom
        as members.

        This particular make_lattice method takes an integer n greater than
        1 as its only input.  The top is n, the bottom is 1, and the lattice
        is the set of positive integers which evenly divide n.

        To determine the lattice, the program runs through all the integers
        from 2 through roughly sqrt(n) to find the proper divisors.  This
        is not suitable for large values of n.
        """
        method = "_set_lattice"
        if type(n) != int:
            raise TypeError(cls._message(method, "n must be an integer"))
        if n <= 1:
            raise ValueError(cls._message(method, "n must be larger than 1"))
        top = n
        bottom = 1
        lattice = {1, n}
        divisor = 2                         # a possible divisor
        t = 1                               # time cost
        while divisor*divisor <= n:
            codivisor, modulus = divmod(n, divisor)
            if modulus == 0:
                lattice.update({divisor, codivisor})
            t += 1
            divisor += 1
        message = f"L: {top=}, {bottom=}, |L|={len(lattice)}, {t=}"
        print(cls._message(method, message))
        return top, bottom, lattice

    @classmethod
    def implication_fails_default(cls, top):
        """returns failure values for the default implication function"""
        f = lambda p, q: q * (top // lcm(p, q))
        return f

    def make_implication(self, f, verify) -> "Function":
        """creates the actual material implication function

        The function is set by the initializer.  This method only returns
        the function.
        """
        method = "make_implication"
        if callable(f):
            def implication(p:int, q:int) -> int:
                """the implication lookup"""
                y, m = divmod(q, p)
                if m == 0:                      # q divides p
                    return self.__top               # successful
                if (p, q) == (self.__top, self.__bottom):             
                    return self.__bottom            # classic failure
                return f(p, q)                      # multi-valued failure
        elif type(f) == int:
            def implication(p:int, q:int) -> int:
                """the implication lookup"""
                y, m = divmod(q, p)
                if m == 0:                      # q divides p
                    return self.__top               # successful
                if (p, q) == (self.__top, self.__bottom):             
                    return self.__bottom            # classic failure
                return f                        # multi-valued failure
        else:
            raise TypeError(self._message(method, "type of f is unknown"))
        if verify:
            for p in self.__lattice:
                for q in self.__lattice:
                    y = implication(p, q)
                    if q % p != 0:
                        message = self._message(method, "failure {p},{q}->{y}")
                        if y == self.__top:
                            raise ValueError(message)
                    message = self._message(method, "domain {p},{q}->{y}")
                    if y not in self.__lattice:
                        raise ValueError(message)
            print(self._message(method, "verified"))
        return implication

    @property
    def lattice(self) -> tuple:
        """return the lattice as a sorted tuple"""
        return tuple(sorted(self.__lattice))

    @property
    def top(self) -> int:
        """return the maximum element"""
        return self.__top

    @property
    def bottom(self) -> int:
        """return the minimum element"""
        return self.__bottom

            # PART 2 - EVALUATION

    def defined(self, p:int, var:str='p'):
        """check whether a truth value is defined"""
        method = "defined"
        error = f"{str(var)}={p} is not defined"
        if p not in self.__lattice:
            raise ValueError(self._message(method, error))

    def AND(self, p:int, q:int) -> int:
        """conjunction"""
        return gcd(p, q)

    def OR(self, p:int, q:int) -> int:
        """inclusive disjunction"""
        return lcm(p, q)

    def IMP(self, p:int, q:int) -> int:
        """material implication"""
        return self.__implication(p, q)

    def EQU(self, p:int, q:int) -> int:
        """material equivalence"""
        return self.AND(self.IMP(p,q), self.IMP(q,p))

    def NOT(self, p:int) -> int:
        """logical negation"""
        return self.__top // p

    def XOR(self, p:int, q:int) -> int:
        """exclusive disjunction"""
        return self.AND(self.OR(p,q), self.NOT(self.AND(p,q)))

    @property
    def T(self):
        """absolute truth"""
        return self.__top

            #    For a multiworld scenario, redefine what follows....

            # PART 3 - THE ACTUAL WORD

    @property
    def actual_truth(self):
        return self.__top

    @property
    def actual_falsity_top(self):
        return self.__top // self.actual_truth

    def is_actually_true(self, p):
        """p is (actually) true in the actual world"""
        return self.AND(p ,self.actual_truth)

            # PART 4 - Tarski modalities

    def STRUE(self, p:int) -> int:
        """Tarski strongly true"""
        return self.__top if p==self.__top else self.__bottom

    def WTRUE(self, p:int) -> int:
        """Tarski weakly true"""
        return self.NOT(self.STRUE(self.NOT(p)))

            # PART 5 - Lewis modalities (S4-type)

    def NECESSARILY(self, p:int) -> int:
        """necessarily true"""
        return self.__top if p==self.__top else self.__bottom

    def POSSIBLY(self, p:int) -> int:
        """possibly true"""
        return self.NOT(self.NECESSARILY(self.NOT(p)))

            # PART 6 - Strict implication (Lewis type)

    def SIMP(self, p:int, q:int) -> int:
        """strict implication"""
        return self.NECESSARILY(self.IMP(p, q))

    def SEQU(self, p:int, q:int) -> int:
        """strict implication"""
        return self.AND(self.SIMP(p, q), self.SIMP(q, p))

if __name__ == "__main__":
        # TESTING
    def print_unary(L, lattice):
        """display table for the unary operators"""
        print()
        print("           UNARY OPERATORS")
        print("        p   ~p  □p  ◇p  Sp  Wp")
        print("       ━━━ ━━━ ━━━ ━━━ ━━━ ━━━")
        for p in lattice:
            Np = L.NOT(p)
            Mp = L.NECESSARILY(p)
            Pp = L.POSSIBLY(p)
            Sp = L.STRUE(p)
            Wp = L.WTRUE(p)
            print(f"       {p:3} {Np:3} {Mp:3} {Pp:3} {Sp:3} {Wp:3}")
        print()

    def print_matrix(name, lattice, f):
        """display a 2x2 matrix for a binary operator"""
        print()
        s = f"{name:>4} ┃     q="
        for q in lattice:
            s += f"{q:3}"
        print(s)
        print("━" * (len(s)+1))
        for p in lattice:
            s = f"       p={p:2} ┃"
            for q in lattice:
                y = f(p, q)
                s += f"{y:3}"
            print(s)

    print("testing DivisorLogic class")
    print("PART 1: CHECK SIMPLE ERROR TRAPS")
    try:
        print("  try: DivisorLogic.make_lattice('foo')")
        DivisorLogic.make_lattice('foo')
        raise RuntimeError("exception not raised")
    except TypeError as msg:
        print("  raised TypeError as", msg)
    try:
        print("  try: DivisorLogic.make_lattice(1)")
        DivisorLogic.make_lattice(1)
        raise RuntimeError("exception not raised")
    except ValueError as msg:
        print("  raised ValueError as", msg)

    print("PART 2: TEST LATTICE SETUP")
    print("  try: DivisorLogic.make_lattice(2)")
    top, bottom, lattice = DivisorLogic.make_lattice(2)
    assert top == 2
    assert bottom == 1
    assert lattice == {1, 2}
    print("  try: DivisorLogic.make_lattice(12)")
    top, bottom, lattice = DivisorLogic.make_lattice(12)
    assert top == 12
    assert bottom == 1
    assert lattice == {1, 2, 3, 4, 6, 12}
    print("  try: DivisorLogic.make_lattice(36)")
    top, bottom, lattice = DivisorLogic.make_lattice(36)
    assert top == 36
    assert bottom == 1
    assert lattice == {1, 2, 3, 4, 6, 9, 12, 18, 36}
    print("  try: DivisorLogic.make_lattice(60)")
    top, bottom, lattice = DivisorLogic.make_lattice(60)
    assert top == 60
    assert bottom == 1
    assert lattice == {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}
    print("  material implication default for 𝓛(60)...")
    lattice = sorted(lattice)
    f = lambda p, q: 60 // lcm(p, q)

    def one_shot(p, q):
        """set up the proposed material implication operator"""
        y, m = divmod(q, p)
        if m == 0:
            y = top
        else:
            if (p, q) == (top, bottom):
                y = bottom
            else:
                y = f(p, q)
                assert y < 60, f"{p=}, {q=}, p⊃q={y}"
        return y

    print_matrix("p⊃q", lattice, one_shot)

    print("PART 3: CASE STUDY FOR 𝓛(60):")
    print("  create instance of 𝓛(60)...")
    print("  do: L60 = DivisorLogic(60, verify=True)")
    L60 = DivisorLogic(60, verify=True)
    print_unary(L60, lattice)
    lattice = L60.lattice
    assert lattice == (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60)
    assert L60.top == 60
    assert L60.bottom == 1
    print("           BINARY OPERATORS")
    print_matrix("p∨q", lattice, L60.OR)
    print_matrix("p⊃q", lattice, L60.IMP)
    print_matrix("p≡q", lattice, L60.EQU)
    print_matrix("p⊻q", lattice, L60.XOR)

    print("PART 4: DETERMINE WHERE TRANSITIVITY FAILS")
    f1 = lambda x, y, z: L60.IMP(L60.IMP(y,z), L60.IMP(x,z))
    f2 = lambda x, y, z: L60.IMP(L60.IMP(x,y), f1(x,y,z))
    print("(p⊃q) ⊃ ((q⊃r) ⊃ (p⊃r))")
    errors = 0
    for p in lattice:
        for q in lattice:
            for r in lattice:
                Cpq = L60.IMP(p,q)
                Cqr = L60.IMP(q,r)
                Cpr = L60.IMP(p,r)
                result = f2(p,q,r)
                if result != 60:
                    print(f"   {(p,q,r)=}, {(Cpq,Cqr,Cpr)=}, {result=}")
                    errors += 1
    print(f"{errors} errors in transitivity")
    if errors == 0:
        import sys
        print("SUCCESS!")
        sys.exit()

    print("PART 5: TRY SOMETHING NEW...")
    def try_imp(p, q):
        """trial implication"""
        t2 = 60 // lcm(p, q)            # ~(p∨q)
        # result = min(60, q * t2)
        result = q * t2
        if (q % p == 0) and (result != 60):
            print(f"   {p=}, {q=}, {result=}    but p|q, expected 60")
        if (p == 60) and (result != q):
            print(f"   {p=}, {q=}, {result=}    but p=60, expected {q}")
        if (q == 1) and (result != 60 // p):
            print(f"   {p=}, {q=}, {result=}    but q=1, expected p={60//p}")
        if result % (60//p) != 0:
            print(f"   {p=}, {q=}, {result=}, {result%(60//p)=} != 0")
        return result

    print_matrix("C1", lattice, try_imp)

    # is this transitive?

    C1 = lambda p, q: q * (60 // lcm(p, q))
    f1 = lambda x, y, z: C1(C1(y,z), C1(x,z))
    f2 = lambda x, y, z: C1(C1(x,y), f1(x,y,z))
    print("(p⊃q) ⊃ ((q⊃r) ⊃ (p⊃r))")
    errors = 0
    for p in lattice:
        for q in lattice:
            for r in lattice:
                Cpq = C1(p,q)
                Cqr = C1(q,r)
                Cpr = C1(p,r)
                result = f2(p,q,r)
                if result != 60:
                    print(f"   {(p,q,r)=}, {(Cpq,Cqr,Cpr)=}, {result=}")
                    errors += 1
    print(f"{errors} errors in transitivity")
    assert errors == 0
    print("C1 is successful")

