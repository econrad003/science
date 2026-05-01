"""
utilities.permutation - permutation groups
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Given an alphabet A of characters, S(A) is the set of bijections
    which map all elements of A into elements of A.  An element of S(A)
    is called a permutation of A.

    For example, if the alphabet is the ordered triple (1 2 3).  The
    permutations are:

          I = (1 2 3)               the identity
         R₊ = (3 1 2)               rotate right
         R₋ = (2 3 1)               rotate left
         T₃ = (2 1 3)               interchange 1 and 2 (3 is fixed)
         T₂ = (3 2 1)               interchange 1 and 3 (2 is fixed)
         T₁ = (1 3 2)               interchange 2 and 3 (1 is fixed)

    A permutation of (1 2 3) acts on a string in A by replacng 1 with
    the first letter in the permutation, 2 with the second, and 3 with
    with the third.  For example:
        T₁('123123') = '132132'

    The composition (or multiplication) of two permutation acts by
    applying first the multiplier and then the multiplicand.  The set
    of permutations of a set forms a group.  Cayley's Theorem tells
    us that every group is a subgroup of a group which is isomorphic
    to a permutation group.  The permutations groups S₁ and S₂ (on,
    respectively {1} and {1,2}) are abelian.  Permutation groups on
    of 3 or more elements are non-abelian.  The permutation group
    S₀ (on the empty set) is isomorohic to S₁ and consists of a single
    permutation, namely the group identity.

PARITY

    If we take order the alphabet in some fashion, then we can apply
    a permutation and count the number of times that an earlier letter
    appears after an later letter.  For the identity permutation, the
    number will be zero.  Regardless of how we order the alphabet, the
    number of a given permutation will always have the same parity, either
    even or odd.  Consider our 3-letter alphabet {1,2,3}.

                        Order 1             Order 2
        Permutation     1 2 3    n  p       1 3 2    n  p
        ----------------------------------------------------
            I           1 2 3    0  Even    1 3 2    0  Even
            R₊          3 1 2    2  Even    3 2 1    2  Even
            R₋          2 3 1    2  Even    2 1 3    2  Even
            T₃          2 1 3    1  Odd     2 3 1    3  Odd
            T₂          3 2 1    3  Odd     3 1 2    1  Odd
            T₁          1 3 2    1  Odd     1 2 3    1  Odd

    The number n is the total number of elements that are smaller in order
    but later after a permutation has been applied.  The column p identifies
    whether n is even or odd.  Before we count, we must establish the canonical
    order.

    For example, consider the permutation R₊ which maps 1 to 3, 2 to 1, and 3
    to 2.  If the standard order is "123", we consider R₊("123")="312".  After
    the 3, there are two earlier letters, and after the 1, there are no
    earlier letters, for a total of 2 which is even.  If we draw a line from
    each element placed in a canonically ordered row to the same element
    in the permuted row, the number of crossings is our number n.  This
    number depends on our canonical order.  (For the identity permutation,
    this number is always zero, but it is not necessarily fixed for other
    permutations.  But, regardless of how we order the alpabet, any given
    permutation is either always even or always odd.)  In the illustration,
    the number of crossings happens to be 2, so the permutation R₊ is an even
    permutation.

                1     2     3       Canonical Order
                 \     \   /
                  \     \ /
                   \     x          R₊
                    \   / \
                     \ /   \
                      x     \
                     / \     \
                    /   \     \
                   3     1     2    Permuted Order

    The set of even permutations forms a subgroup of the group of
    permutations.  This group is known as the alternating group.  For
    a set of zero letters or one letter, this is the full group.  For
    permutations of two or more letters, the alternating group is a
    proper subgroup.  For S₃, we have (as sets):

        S₃ = {I, R₊, R₋, T₃, T₂, T₁}
        A₃ = {I, R₊, R₋} 

    For finite permutation groups, the number of permutations is m! where
    m is the number of letters.  The alternating group has exactly half this
    number:

                            |Sₘ| = m! = 2|Aₘ|

                        Note: for infinite groups
                        -------------------------
        Permutation groups on infinite sets also have alternating
        proper subgroups, but we would need to modify the
        definition above of even and odd permutations.

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
from random import shuffle

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Permutation(object):
    """an object in a permutation group"""

    __slots__ = ("__G", "__map", "__domain")

    def __init__(self, G:"SymmeticGroup", mapping:dict, copy=True):
        """create a permutation

        The identity permutation is just an empty directory.
        """
        if not isinstance(G, SymmetricGroup):
            raise TypeError("invalid group")
        if not isinstance(mapping, dict):
            raise TypeError("invalid mapping")
        self.__G = G
        self.__domain = frozenset(mapping.keys())
        self.__map = mapping.copy() if copy else mapping

    def validate(self):
        """check to see if this is a valid permutation

        EXCEPTIONS
        """
        G = self.__G
        codomain = set(self.__map.values())
        if self.domain != codomain: raise ValueError("domain != range")
        for x in self.domain:
            if type(x) != int: raise TypeError("indices must be int")
            if x not in range(G.n): raise IndexError("index range error")
            if x == self.__map[x]: raise ValueError("mapped fixed element")

    @property
    def domain(self) -> frozenset:
        """returns the domain of the permutation

        The domain (as defined here) does not include items that are
        fixed.
        """
        return self.__domain

    @property
    def group(self) -> "Group":
        """returns the group"""
        return self.__G

    def __getitem__(self, x:int) -> int:
        """returns the mapped index"""
        if x in self.__domain:
            return self.__map[x]
        if type(x) != int: raise TypeError
        if x < 0 or x > self.__G.n: raise ValueError
        return x

    @property
    def is_identity(self) -> bool:
        """is this permutation an identity permutation?"""
        return len(self.__map) == 0

    def __eq__(self, other:"Permutation"):
        """determine whether two permutations are equal"""
        if self.__domain == set() and other == 1:
            return True
        if not isinstance(other, Permutation):
            return NotImplemented
        if self.__G != other.__G:
            return False
        return self.__map == other.__map

    def __mul__(self, other:"Permutation"):
        """compose two permutations"""
        if other == 1:
                # compose with the identity on the right
            return self

                # validate the permutations
        if not isinstance(other, Permutation):
            return NotImplemented
        if other.__G != self.__G:
            raise ValueError("__mul__: Permutations from different groups")

                # compose with an identity
        if other.__map == dict():
            return self
        if self.__map == dict():
            return other

                # create a new permutation (f*g)(x) = f(g(x))
        mapping = dict()
        for x in range(self.__G.n):
            y = other.__map.get(x, x)
            z = self.__map.get(y, y)
            if x != z:
                mapping[x] = z
        return Permutation(self.__G, mapping)

    def __rmul__(self, other:"Permutation"):
        """compose two permutations in reverse order"""
        if other == 1:
                # compose with the identity on the left
            return self

                # validate the permutations
        if not isinstance(other, Permutation):
            return NotImplemented

                # probably won't get here, but just in case...

        if other.__G != self.__G:
            raise ValueError("__rmul__: Permutations from different groups")

                # compose with an identity
        if other.__map == dict():
            return self
        if self.__map == dict():
            return other

                # create a new permutation (g*f)(x) = g(f(x))
        mapping = dict()
        for x in range(self.__G.n):
            y = self.__map.get(x, x)
            z = other.__map.get(y, y)
            if x != z:
                mapping[x] = z
        return Permutation(self.__G, mapping)

    @property
    def inverse(self) -> "Permutation":
        """returns the inverse"""
        mapping = dict()
        for x in self.__domain:
            mapping[self.__map[x]] = x
        # print(self.__map, mapping)
        return Permutation(self.__G, mapping)

    def __pow__(self, power:int):
        """integer powers"""
        if type(power) != int:
            return NotImplemented
        if power < 0:
            place = self.inverse
            power = - power
        else:
            place = self
        result = self.__G.identity
            # binary representation
            #   Example foo ** 13
            #   13 is 1101 in binary    (8+4+1=13)
            #   iteration   power   result      place   power%2 power//2
            #   1           1101    I           foo     1       110
            #   2           110     foo         foo**2  0       11
            #   3           11      foo         foo**4  1       1
            #   4           1       foo**5      foo**8  1       0
            #   END         0       foo**13     foo**16
        while power > 0:
            if power % 2 == 1:
                result *= place
            power //= 2
            place *= place
        return result

    def apply(self, s:str):
        """apply the permutation to a string (transfer to group)"""
        return self.__G.apply(self, s)

class SymmetricGroup(object):
    """define a permutation group"""

    __slots__ = ("__n", "__Sn", "__order", "__back", "__alphabet", "__name")

    def __init__(self, alphabet:str=ALPHABET, name:str=None):
        """constructor"""
        if not isinstance(alphabet, str):
            raise TypeError("Permutations: The alphabet must be a string")
        self.__n = len(alphabet)
        self.__Sn = dict()      # for storing permutations
        self.__alphabet = frozenset(alphabet)
        if self.__n != len(self.__alphabet):
            raise ValueError("Permutations: The alphabet may not contain duplicates")
        self.__order = dict()
        self.__back = dict()
        for i in range(self.__n):
            self.__order[i] = alphabet[i]
            self.__back[alphabet[i]] = i
        self.__name = name if name else f"S({self.n})"

    @property
    def n(self) -> int:
        """the length of the alphabet"""
        return self.__n

    def __getitem__(self, index) -> dict:
        """returns letter #i in the alphabet"""
        return self.__order[index]

    def to_index(self, letter:str) -> (int, type(None)):
        """returns the index of a letter, or None if the letter isn't there'"""
        return self.__back.get(letter)

    @property
    def alphabet(self) -> frozenset:
        """returns the alphabet as a (frozen) set"""
        return self.__alphabet

    @property
    def name(self) -> str:
        """returns the name of the group"""
        return str(self.__name)

    def fetch(self, key, delete=False) -> (Permutation, type(None)):
        """returns a stored permutation

        If delete is true, the key is removed.
        """
        s = self.__Sn.get(key)
        if delete and s:
            del self.__Sn[key]
        return s

    def store(self, key:"hashable", s:Permutation):
        """stores a permutation"""
        if isinstance(s, Permutation):
            if s.group == self:
                self.__Sn[key] = s
            else:
                raise ValueError("not in this group")
        else:
            raise TypeError("not a permutation")

    def apply(self, f:Permutation, s:str):
        """apply a permutation to a string"""
        if f.group != self:
            raise ValueError("permutation f not owned by this group")
        foo = list()
        for a in s:
            if a in self.__alphabet:
                x = self.to_index(a)
                y = f[x]
                b = self[y]
                foo.append(b)
            else:
                foo.append(a)
        return "".join(foo)

    @property
    def identity(self) -> Permutation:
        """return the identity permutation"""
        return Permutation(self, dict())

    def swap(self, a:str, b:str) -> Permutation:
        """return the permutation which interchanges a and b"""
        if a not in self.alphabet:
            raise ValueError("a is not a valid letter")
        if b not in self.alphabet:
            raise ValueError("b is not a valid letter")
        if a == b:
            raise ValueError("a and b must be different")
        mapping = dict()
        a = self.to_index(a)
        b = self.to_index(b)
        assert a!=None and b!=None
        mapping[a] = b
        mapping[b] = a
        return Permutation(self, mapping)

    def shift(self, h:int=1) -> Permutation:
        """return a rotation"""
        h = h % self.n
        if h == 0:
            return self.identity
        mapping = dict()
        for i in range(self.n):
            mapping[i] = (i + h) % self.n
        return Permutation(self, mapping)

    def cycle(self, *args) -> Permutation:
        """create a cyclic permutation"""
        if len(args) != len(set(args)):
            raise ValueError("no repeats in the arguments")
        n = len(args)
        mapping = dict()
        for i in range(n):
            a = args[i]
            b = args[(i+1)%n]
            if a not in self.alphabet:
                raise ValueError(f"{a=} is not a valid letter")
            if b not in self.alphabet:
                raise ValueError(f"{b=} is not a valid letter")
            a = self.to_index(a)
            b = self.to_index(b)
            assert a!=None and b!=None
            mapping[a] = b
        return Permutation(self, mapping)


