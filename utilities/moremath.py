"""
utilities.moremath - extensions to Python's math package
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DEFINITIONS

    An integer x divides an integer y if there is an integer m such
    that y = mx.  So 1 and -1 divide every integer, and 0 divides 0, but
    0 does not divide any other integer.  (Note that 0/0 is still
    undefined.  The quotient b/a is defined if and only if the integer m
    is unique.  0 is just weird, okay?)  2 divides all of the even
    integers.  And every integer divides 0.

    The units are -1 and 1.  A unit is an integer which divides every
    integer.

    The definition of prime used here is related to prime ideals.  An
    integer q is prime if and only if (i) it is not a unit and (i) whenever
    q divides a product of several integers, it also divides at least one of
    the factors in that product.

    Note that 0 is a prime by this definition.  Note also that the remaining
    primes come in pairs, a positive prime and its negative.  For example,
    2 and -2 are prime, as are 3 and -3.  Think of this definition as telling
    us that primes are sort of like zero.  Take a prime, for example, 5.
    Now consider all the multiples of 5:
            ..., -15, -10, -5, 0, 5, 10, 15, ...
    Now take any product which is a multiple of 5, for example:
                14 x 20 = 280
    Now 280 happens to be in that list of multiples of 5 since 56x5=280.
    Since 5 divides 280 and 5 is prime, it must divide either 14 or 20.
                (4x5=20, check!)
    Now 8 is not prime and neither 14 nor 20 is a multiple of 8.  But
    8 does divide 280:
                (35x8=280.)
    Note that the property just works in one direction.  For example 4 is
    not prime, and it does divide 280 and also 20.

    An irreducible is an integer q which (i) is not a unit, and (ii) for
    every pair of integers a, b with product ab=q, ether a is a unit or
    b is a unit.  Note that zero is not irreducible, and for every nonzero
    integer q, q is prime if and only if it is irreducible.

    There are generalized integers which contain irreducibles which do not
    obey an analogue of the zero-product property.

    Composites are integers which are not units and primes or irreducibles. 

    A pair q, q' of integers are associates if they divide each other.  If
    q and q' are associates, either q'=q or q'=-q.  In generalized integer
    settings, there may be other units.  For example, the Gaussian integers,
    the units are 1, -1, i and -i. The Gaussian-associates of a Gaussian
    integer q are q, -q, iq and -iq.

DESCRIPTION

    This module provides the following classes:

        class Primes
            keeps track of positive primes

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

MAYBE = 0.5

class Primes(object):
    """keeps track of positive primes

    The table is maintained at the class level.
    """
    __slots__ = ()

    __pi = {1:2, 2:3, 3:5, 4:7, 5:11, 6:13, 7:17, 8:19}
    __primes = {2, 3, 5, 7, 11, 13, 17, 19}
    __largest_checked = 21

    @classmethod
    def small_primes(cls) -> list:
        """return the list of saved primes"""
        result = list()
        for k in range(1, len(cls.__primes)+1):
            result.append(cls.__pi[k])
        return result

    @classmethod
    def largest(cls) -> tuple:
        """returns the index of the largest saved prime and the largest
        checked value
        """
        k = len(cls.__primes)
        return k, cls.__largest_checked

    @classmethod
    def pi(cls, k:int):
        """returns the kth nonnegative prime (if k=0, returns 0)"""
        if type(k) != int:
            raise TypeError("Primes.pi: 'k' must be an integer")
        if k == 0:
            return 0
        if k < 0:
            raise ValueError("Primes.pi: 'k' must not be negative")
        if k > len(cls.__primes):
            m, q = cls.largest()
            while k > m:
                    ### SIEVE OF ERATOSTHENES
                q += 2                  # only check odd values
                for j in range(1, m+1):
                    p = cls.__pi[j]
                    if p * p > q:       # too large...
                        m += 1
                        cls.__pi[m] = q             # prime!
                        cls.__primes.add(q)         # prime!
                        # print(f"Added {m}:{q}")     # DEBUGGING
                        break
                    if q % p == 0:      # divisor found
                        break
            cls.__largest_checked = q
        return cls.__pi[k]

    @classmethod
    def sieve_to(cls, n:int):
        """extend the list of saved primes"""
        if type(n) != int:
            raise TypeError("Primes.sieve_to: 'n' must be an integer")
        if n <= 0:
            raise ValueError("Primes.sieve_to: 'n' must be positive")
        k, q = cls.largest()
        while q < n:
                # SIEVE OF ERATOSTHENES
            q += 2
            for j in range(1, k+1):
                p = cls.__pi[j]
                if p * p > q:       # smallest proper divisor is less than p
                    k += 1
                    cls.__pi[k] = q             # prime!
                    cls.__primes.add(q)         # prime!
                    # print(f"Added {k}:{q}")     # DEBUGGING
                    break
                if q % p == 0:      # divisor found
                    break                       # composite!
        cls.__largest_checked = q

    @classmethod
    def is_small_prime(cls, q:int) -> bool:
        """check whether q is a saved prime

        Will return True if q is zero or the absolute value of q has
        been saved in the table of small positive primes.
        """
        if type(q) != int:
            raise TypeError("Primes.sieve_to: 'q' must be an integer")
        if q == 0:
            return True             # trivial
        return abs(q) in cls.__primes

    @classmethod
    def is_prime(cls, q:int, sieve=False) -> (bool, int):
        """check whether q is prime

        Possible return values are:
            True (1)
                    definitely prime.  Note that True==1 in Python.
            False (0)
                    definitely not prime.  Note that False==0 in Python
            MAYBE (0.5)
                    Insufficient information.

        Note that 0 is prime, but the units 1 and -1 are not prime.
        """
        if type(q) != int:
            raise TypeError("Primes.is_prime: 'q' must be an integer")
        if q == 0:
            return True

        q = abs(q)                  # sign makes no difference
        if q == 1:
            return False            # q is a unit

        if q in cls.__primes:
            return True             # |q| is a saved prime
        if q <= cls.__largest_checked:
            return False            # small but not a saved prime

                # Does q have a small prime factor?
        for k in range(1, len(cls.__primes)+1):
            p = cls.__pi[k]
            if p*p > q:             # prime!
                return True
            if q % p == 0:          # composite
                return False

                # Now what?
        if not sieve:
            return MAYBE            # indeterminate (0.5)

                # SIEVE OF ERATOSTHENES
        k, n = cls.largest()
        while n*n <= q:
            n += 2
            for j in range(1, k+1):
                p = cls.__pi[j]
                if p * p > n:       # smallest proper divisor is less than p
                    k += 1
                    cls.__pi[k] = n             # prime!
                    cls.__primes.add(n)         # prime!
                    # print(f"Added {k}:{q}")     # DEBUGGING
                    cls.__largest_checked = n
                    if q % n == 0:      # divisor found
                        return False        # composite!
                    break
                if n % p == 0:
                    break
        return True

# DEBUGGING
if __name__ == "__main__":
    assert Primes.pi(0) == 0
    assert Primes.pi(1) == 2
    assert Primes.pi(2) == 3
    assert Primes.pi(7) == 17
    assert Primes.pi(8) == 19
    assert Primes.small_primes() == [2, 3, 5, 7, 11, 13, 17, 19]
    assert Primes.largest() == (8, 21)
        # The next prime is 23.
    assert Primes.is_prime(23*23) == MAYBE
    assert not Primes.is_prime(29*29, sieve=True)
    # print(Primes.largest())
    assert Primes.largest() == (10, 29)
    assert Primes.small_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        # Since 2 is already included, we only sieve odd integers
        # The sieve only stops at odd integers.  The stopping point
        # is not necessarily a prime.
    Primes.sieve_to(100)
    assert not Primes.is_small_prime(103)   # prime, but not yet found
    assert Primes.is_small_prime(101)       # prime, found by the sieve
    assert not Primes.is_small_prime(100)   # 100=2x50
    assert not Primes.is_small_prime(99)    # 99=3x33

    assert Primes.largest() == (26, 101)    # <- 101: 2nd number is always odd
    assert Primes.pi(25) == 97
    assert Primes.pi(26) == 101
    Primes.sieve_to(104)
    assert Primes.largest() == (27, 105)    # <- 103: 2nd number is always odd
    assert Primes.pi(27) == 103
    assert Primes.pi(28) == 107
    assert Primes.pi(100) == 541
    assert Primes.pi(500) == 3571
    assert Primes.pi(1000) == 7919
    k, q = Primes.largest()
    p = Primes.pi(k)
    print(f"largest: π({k})={p}; checked up to q={q}")
    print("SUCCESS!")

# end module utilities.moremath
