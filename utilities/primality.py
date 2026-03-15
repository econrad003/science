"""
utilities.primality - cached primality checking
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The following cached functions are provided:

        is_prime(q) - returns True if q is an integer prime

        is_square_free(q) - returns True if q is a square-free integer

    Both functions raise TypeError exceptions if the argument is not an
    integer.  0 is treated as prime, as are all positive primes and their
    additive inverses.  (For example, 0, 2, -2, 3, -3 are all treated as
    prime.)  An integer is square-free if and only if it is not divisible by
    the square of a positive prime.  (For example, 1, -1, -3 and -6 are all
    square-free, but, since 9 divides 0 and -18, 0 and -18 are not
    square-free.)

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
from functools import cache

from utilities.moremath import Primes

@cache
def is_positive_prime(q:int) -> bool:
    """returns True if the integer is a positive prime

    The answers are cached.  This is primarily intended for situations where
    a small number of primes are encountered.

    Exceptions are raised if the argument is not a positive integer.
    """
    if type(q) != int:
        raise TypeError("'q' must be an integer")
    if q <= 0:
        raise ValueError("'q' must be positive")
    return Primes.is_prime(q, sieve=True)

def is_prime(q:int) -> bool:
    """returns True if the integer is an integer prime (or zero)

    Answers for absolute values are cached.

    Type checking won't occur if q is equal to zero or abs(q) returns an
    integer.
    """
    if q == 0:
        return True
    return is_positive_prime(abs(q))

@cache
def is_square_free(q:int) -> bool:
    """returns True if the integer is square_free

    Returns True if and only if, for every positive prime p, p*p does
    not divide q.

    Results are cached, so this version is intended for cases where
    only a few numbers are checked.
    """
    if type(q) != int:
        raise TypeError("'q' must be an integer")
    k = 1
    n = abs(q)
    while True:
        p = Primes.pi(k)
        if n % (p*p) == 0:
            return False
        if n < p*p:
            return True
        if n % p == 0:
            n //= p             # reduce the size of the search
        k += 1

if __name__ == "__main__":
    print("Primes less than 100:")
    primes = list()
    for n in range(100):
        if is_prime(n):
            primes.append(n)
    print(primes)
    for n in range(100):
        assert is_prime(-n)==(n in primes), f"{n} {is_prime(n)}"
    print("Square-free integers less than 100")
    sqfree = list()
    for n in range(100):
        if is_square_free(n):
            sqfree.append(n)
    print(sqfree)
    for n in range(100):
        assert is_square_free(-n)==(n in sqfree), f"{n} {is_square_free(n)}"
    assert is_square_free(547*557)
    assert is_prime(547)
    assert is_prime(557)
    assert not is_square_free(2*3*5*7*1229*1229)
    assert is_prime(1229)
# END utilities.primality
