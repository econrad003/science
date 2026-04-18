"""
utilities.modlog - define a logarithm on the integers modulo n (ℤₙ)
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

BACKGROUND

    For a given integer n > 1, the commutative ring ℤₙ is defined on
    the set ℤₙ={0, 1, 2, ..., n-1} for the operations of addition and
    multiplication by the remainder after division by n.  The elements
    of the set which are relatively prime to n form a multiplicative
    group.  The remaining elements are divisors of zero.

    The multiplicative group MZ(n)=M(ℤₙ) is cyclic if and only if either:

        i) n is prime; in this case, ℤₙ is a field;
        ii) n = 4;
        iii) n = 2q where q is a power of an odd prime.

    For example, for n from 2 through 20, MZ(n) is cyclic for the following
    values of n:

        2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 17, 18, and 19.

    For n=8, 12, 16, and 20, not that 4 is a proper divisor of n.  The
    remaining exception, n=15, is divisible by two distinct odd primes.

    Wheneven the multiplicative group is cyclic, there are primitive
    elements which whose powers encompass the entire group.

DESCRIPTION

    To create a (finite) logarithm function, we first need an
    exponential.  To show how this is done we will use n=18 as an
    example.  We start with an analysis of ℤ/18 with an emphasis
    on its multiplicative group.

    First, we note the prime divisors of 18 are 2 and 3, so we
    have the following zero divisors:

        0   2   4   6   8  10  12  14  16     (multiples of 2)
        0     3     6     9    12    15       (multiples of 3)

    The remaining elements form the multiplicative group:

        1   5   7  11  13  17

    Since 18 has just one odd prime divisor and 4 does not divide 18,
    the multiplicative group is cyclic.  The primitive elements are
    5 and 11.  We will define base 5 exponentials and base 5 logarithms
    on ℤ/18.

    First the exponential function:

            n   0   1   2   3   4   5
        exp n   1   5   7  17  13  11

    This values in the second row can be created with the following
    Python expression:

        list(5**k % 18 for k in range(6))

    The base 5 logarithm function is the functional inverse of exp:

            n   1   5   7  11  13  17
        log n   0   1   2   5   4   3

    Note that the domain of the exponential and the range of the
    logarithm is ℤ/6 while the range of the exponential and the
    domain of the logarithm are the multiplicative group M(ℤ/18).

    We can also create base 11 exponentials and logarithms:

            n   0   1   2   3   4   5
        exp n   1  11  13  17   7   5

            n   1   5   7  11  13  17
        log n   0   5   4   1   2   3

LAWS OF LOGARITHMS

                        log m + log n = log mn

        log mn |  1  5  7 11 13 17     mn |  1  5  7 11 13 17
        -------+-------------------   ----+-------------------
             1 |  0  1  2  5  4  3      1 |  1  5  7 11 13 17
             5 |  1  2  3  0  5  4      5 |  5  7 17  1 11 13
             7 |  2  3  4  1  0  5      7 |  7 17 13  5  1 11
            11 |  5  0  1  4  3  2     11 | 11  1  5 13 17  7
            13 |  4  5  0  3  2  1     13 | 13 11  1 17  7  5
            17 |  3  4  5  2  1  0     17 | 17 13 11  7  5  1

    The table on the left was created by adding the logarithms by hand.
    The table on the right was obtained from the table on the left by
    looking up the corresponding exponential (or "antilogarithm").

    You can verify that the multiplication table on the right is
    correct by running the following code:

            items = [1, 5, 7, 11, 13, 17]
            for i in items:
                for j in items:
                    print(f"{(i*j)%18:3}", end="")
                print()

    Checking that division works is trickier, but we can verify
    that logarithms also behave properly with respect to division:

            log m - log n = log (m/n)

    We created the logarithms using the "power rule":

            a log m = log m^a

    The units ℤ/6 are 1 and 5 (or -1), so the roots rule isn't very
    useful.

    Finally, let's look at the base change rule:

            log(a,b) = log a / log b
            log(b) log(a,b) = log(a)

    We did logarithms base 5, so set b = 5 and do our calculations
    in by default in base 11
             a        log(5) log(a,5) = log(a)
             1           5  ×    0    =   0
             5           5  ×    1    =   5
             7           5  ×    2    =   4
            11           5  ×    5    =   1
            13           5  ×    4    =   2
            17           5  ×    3    =   3
    Notice that we recovered the entire base 11 logarithm table from the
    base 11 logarithm of 5 and the base 5 logarithm table.

    Notice also that:
        log(a,b) = log(a,a) / log(b,a) = 1 / log(b,a)
    So log(a,b) is the multiplicative inverse of log(b,a).

                log(5,11) = 1 / log(11,5) = 1/5

    But 1/5 modulo 6 is 1/(-1) or -1 or 5.  Note that we need to be
    to do our arithmetic in the correct base.   

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
from utilities.modn import make_Zn

class ModLog(object):
    """logarithms modulo n"""

    __slots__ = ("__Domain", "__Range", "__exp", "__log")

    def __init__(self, Ring:"class(Zn)", zeta:int):
        """constructor"""
        self.__Domain = Ring
        self.__Range = make_Zn(Ring.multiplicative_order())
        try:
            self.base = zeta
        except Warning:
            print("WARNING:", Ring(zeta),
                  "is not a primitive element in", Ring.__name__)

    @property
    def base(self):
        """returns the default base"""
        return self.__exp[1]

    @base.setter
    def base(self, new_base:int):
        """changes the base

        EXCEPTIONS

            ZeroDivisionError - new_base is a divisor of zero (base
                is unchanged)

            ValueError - new base is 1 (base is unchanged)

            Warning - new base is not a primitive element (base has
                been changed)

            RuntimeError - something bad happened (the class is corrupt)

        If you want to experiment with partial logarithms, you can
        trap the Warning exception.
        """
        new_base = self.__Domain(int(new_base))
        m = self.__Domain.multiplicative_order()
        if new_base.is_zero_divisor:
            raise ZeroDivisionError("base.setter: divisor of zero")
        if new_base == 1:
            raise ValuError("base.setter: 1")
        self.__exp = [1, new_base]
        self.__log = {1:0, new_base:1}
        x = new_base * new_base
        while x != 1:
            i = len(self.__exp)
            self.__log[x] = i
            self.__exp.append(x)
            x *= new_base
        if len(self.__exp) == m:
            pass            # SUCCESS!
        elif len(self.__exp) < m:
            raise Warning("base.setter: not primitive")
        else:
            raise RuntimeError("base.setter: something bad happened")

    @property
    def Domain(self) -> "Image(exp)":
        """returns the domain class"""
        return self.__Domain

    @property
    def Range(self) -> "Image(log)":
        """returns the range class"""
        return self.__Range

    @property
    def order(self) -> tuple:
        """returns the additive and the multiplicative orders"""
        n = self.__Domain.additive_order()
        m = self.__Domain.multiplicative_order()
        return (n, m)

    def exp(self, k:int, b:"Image(exp)"=None) -> "Image(exp)":
        """powers by table lookup

        DESCRIPTION

            If b is None (default), then the indicated table
            value is returned.

            Suppose the default base is B.  Then, if base b is given,
            we use:

                exp(k, b) = b^k = B^(k log b)

        EXCEPTIONS

            KeyError - the base is not valid
        """
        k = int(k)
        if b != None:
            b = self.__Domain(b)
            k *= self.__log[b]
        k %= len(self.__exp)
        return self.__exp[k]

    def log(self, a:"Image(exp)", b:"Image(exp)"=None) -> "Image(log)":
        """logarithm by table lookup

        DESCRIPTION

            If b is None (default), then the indicated table
            value is returned.

            Suppose the default base is B.  If base b is given,
            we use:

                log_b(a) = log(a) / log(B)

            Note that division happens in the range ring.

        EXCEPTIONS

            ZeroDivisionError - the base is a divisor of zero

            KeyError - the argument or the base is not valid
        """
        a = self.__Domain(a)
        loga = self.__Range(self.__log[a])
        if b == None:
            return loga
        b = self.__Domain(b)
        logb = self.__Range(self.__log[b])
        return loga / logb

# END utilities.modlog
