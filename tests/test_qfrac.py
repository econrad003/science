"""
tests.test_qfrac - test the quadratic rationals base package
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module tests the following classes:

        _QFrac - a quadratic rational number class.

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
from fractions import Fraction
from utilities._quadratic import _QFrac

def info(number):
    """output info"""
    print(f"\trepr={repr(number)}, str={str(number)}", end="")
    if isinstance(number, _QFrac):
        print(f", TeXform={number.TeXform}", end="")
    print()

class GaussianFrac(_QFrac):
    """Gaussian rationals"""
    def __init__(self, a, b, c, d=-1):
        """constructor"""
        assert d == -1
        super().__init__(a, b, c, -1)
        # info(self)

class GoldenFrac(_QFrac):
    """Gaussian rationals"""
    def __init__(self, a, b, c, d=5):
        """constructor"""
        assert d == 5
        super().__init__(a, b, c, 5)
        info(self)

print("Testing module quadratic")

def test1():
    print("1) Gaussian rationals...")
    I = GaussianFrac(0, 1, 1)
    print(f"    (0,1) = {I}, Norm = {I.sqnorm}")
    assert str(I) == "i", str(I)
    assert I.TeXform == "\\imath", I.TeXform
    assert I == I
    assert I == 1 * I
    assert I.real == 0
    assert I.imag == 1
    assert I.sqnorm == 1

    MI = I.conjugate()
    print(f"    (0,-1) = {MI}, Norm = {MI.sqnorm}")
    assert str(MI) == "-i", str(MI)
    assert MI.TeXform == "-\\imath", MI.TeXform
    assert MI == -I
    assert MI.real == 0
    assert MI.imag == -1
    assert MI.sqnorm == 1

    MONE = I * I
    print(f"    (-1,0) = {MONE}, Norm = {MONE.sqnorm}")
    assert str(MONE) == "-1", str(MONE)
    assert MONE.TeXform == "-1", MONE.TeXform
    assert MONE == -1
    assert MONE.real == -1
    assert MONE.imag == 0
    assert MONE.sqnorm == 1

    ONE = I * MI
    print(f"    (1,0) = {ONE}, Norm = {ONE.sqnorm}")
    assert str(ONE) == "1", str(ONE)
    assert ONE.TeXform == "1", ONE.TeXform
    assert ONE == 1
    assert ONE.real == 1
    assert ONE.imag == 0

    ZERO = GaussianFrac(0, 0, 1)
    assert str(ZERO) == "0", str(ZERO)
    assert ZERO.TeXform == "0", ZERO.TeXform

    PRIME2a = 1 + I
    print(f"    (1,1) = {PRIME2a}, Norm = {PRIME2a.sqnorm}")
    assert str(PRIME2a) == "1+i", str(Prime2a)
    assert PRIME2a.TeXform == "1+\\imath", PRIME2a.TeXform
    assert PRIME2a == GaussianFrac(1, 1, 1)
    assert PRIME2a.real == 1
    assert PRIME2a.imag == 1
    assert PRIME2a.sqnorm == 2

    PRIME2b = ONE - I
    print(f"    (1,-1) = {PRIME2b}, Norm = {PRIME2b.sqnorm}")
    assert str(PRIME2b) == "1-i", str(Prime2b)
    assert PRIME2b.TeXform == "1-\\imath", PRIME2b.TeXform
    assert PRIME2b == PRIME2a.conjugate()
    assert PRIME2b.real == 1
    assert PRIME2b.imag == -1
    assert PRIME2b.sqnorm == 2

    TWO = PRIME2a * PRIME2b
    print(f"    (2,0) = {TWO}, Norm = {TWO.sqnorm}")
    assert TWO == 2
    assert TWO.real == 2
    assert TWO.imag == 0
    assert TWO.sqnorm == 4

    A = GaussianFrac(2, 3, 5)
    print(f"    (2,3)/5 = {A=}, Norm = {A.sqnorm}")
    assert str(A) == "(2+3i)/5", str(A)
    assert A.TeXform == "\\frac{2+3\\imath}{5}", A.TeXform
    assert A.real == Fraction(2, 5)
    assert A.imag == Fraction(3, 5)
    assert A.sqnorm == Fraction(13, 25)

    B = GaussianFrac(5, 12, 13)
    print(f"    (5,12)/13 = {B=}, Norm = {B.sqnorm}")
    assert str(B) == "(5+12i)/13", str(B)
    assert B.TeXform == "\\frac{5+12\\imath}{13}", B.TeXform
    assert B.real == Fraction(5, 13)
    assert B.imag == Fraction(12, 13)
    assert B.sqnorm == Fraction(25+144, 169) == 1

    ApB = A + B
    print(f"    A+B = {ApB}, Norm = {ApB.sqnorm}")
    re, im = ApB.real, ApB.imag
    assert re == A.real + B.real
    assert im == A.imag + B.imag
    assert ApB.sqnorm == re*re+im*im

    AB = A * B
    print(f"    {AB=}, Norm = {AB.sqnorm}")
    re, im = AB.real, AB.imag
    assert re == Fraction(2*5-3*12, 5*13)
    assert im == Fraction(2*12+3*5, 5*13)
    assert AB.sqnorm == re*re+im*im
    assert str(AB) == "(-2+3i)/5", str(B)
    assert AB.TeXform == "\\frac{-2+3\\imath}{5}", AB.TeXform

    Ar = A.reciprocal
    print(f"    A^(-1)={Ar}, Norm = {Ar.sqnorm}")
    assert Ar * A == 1
    assert Ar.sqnorm == Fraction(25, 13)
    assert str(Ar) == "(10-15i)/13", str(Ar)
    assert Ar.TeXform == "\\frac{10-15\\imath}{13}", Ar.TeXform

    Br = B.reciprocal
    print(f"    B^(-1)={Br}, Norm = {Br.sqnorm}")
    assert Br * B == 1
    assert Br.sqnorm == 1

    assert Ar == A ** -1
    assert Br == B ** -1

    A2 = A ** 2
    assert A2 == A * A

    A3 = A ** 3
    assert A3 == A2 * A

    A4 = A ** 4
    assert A4 == A2 * A2 == A3 * A

        # 11 in binary 1011  8+2+1
    A11 = A ** 11
    assert A11 == A4 * A4 * A2 * A

    Am11 = A ** -11
    assert Am11 == A11.reciprocal

test1()

def test2():
    print("2) Golden rationals...")
    PHI = GoldenFrac(1, 1, 2)
    PHIBAR = GoldenFrac(1, -1, 2)
    ROOT5 = GoldenFrac(0, 1, 1)

test2()


print("SUCCESS!")


