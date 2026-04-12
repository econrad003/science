"""
tests.test_polynomials - test the univariate rational polynomials module
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
from fractions import Fraction

from polynomials.superscript import to_superscript
from polynomials.polynomial import Polynomial, deg
from polynomials.polynomial import polynomialMod as mod
from polynomials.polynomial import polynomialGCD as GCD
from polynomials.polynomial import polynomialCfrac as cfrac
from polynomials.polynomial import cfrac2polynomials as c2p

from polynomials.factor import factor

def prod(*args):
    """product of a list"""
    result = 1                  # empty product
    for arg in args:
        result *= arg
    return result

assert to_superscript(123) == "¹²³"
assert to_superscript(4567890) == "⁴⁵⁶⁷⁸⁹⁰"
assert to_superscript(5) != to_superscript(8), "Oops!"
assert to_superscript(-123) == "⁻¹²³"

zero = Polynomial()
print("P0:", zero)
assert len(zero) == 0
assert zero.deg == -1
assert deg(zero) == -1
assert zero == 0

one = Polynomial(1)
print("P1:", one)
assert len(one) == 1
assert one.deg == 0
assert deg(one) == 0
assert one == 1
assert one != zero

binomial1 = Polynomial(2, 1)
print("P2:", binomial1)
assert str(binomial1) == "x+2"

binomial2 = Polynomial(3, 1)
print("P3:", binomial2)
assert str(binomial2) == "x+3"

binomial3 = binomial1 + binomial2
print("P4:", binomial3)
assert str(binomial3) == "2x+5"

trinomial1 = binomial2 * binomial1
print("P5:", trinomial1)
assert str(trinomial1) == "x²+5x+6"

print("P6:", trinomial1.conjugate())
assert trinomial1.conjugate() == Polynomial(1,5,6)

print("P7:", binomial2 ** 0)
assert binomial2 ** 0 == 1

print("P8:", binomial2 ** 1)
assert binomial2 ** 1 == binomial2

print("P9:", binomial2 ** 2)
assert binomial2 ** 2 == Polynomial(9, 6, 1)

print("P10:", binomial2 ** 3)
assert binomial2 ** 3 == Polynomial(27, 27, 9, 1)

print("P11:", binomial2 ** 4)
assert binomial2 ** 4 == Polynomial(81, 108, 54, 12, 1)

print("P12:", Polynomial(binomial2 ** 4, indeterminate="y"))

monomialx = Polynomial(0, 1)
print("P13:", monomialx ** 4)
assert monomialx ** 4 == Polynomial(0, 0, 0, 0, 1)

print("P14:", binomial2 ** 4 - monomialx ** 4)
assert binomial2 ** 4 - monomialx ** 4 == Polynomial(81, 108, 54, 12)

print("P15:", (binomial2 ** 4 - monomialx ** 4) / 3)
assert (binomial2 ** 4 - monomialx ** 4) / 3 == Polynomial(27, 36, 18, 4)

print("P16:", (binomial2 ** 3).deriv)
assert (binomial2 ** 3).deriv == Polynomial(27, 18, 3)

print("P17:", (binomial2 ** 3).int0)
coeffs = [0, 27, Fraction(27, 2), 3, Fraction(1/4)]
# print((binomial2 ** 3).int0.coeffs)
assert (binomial2 ** 3).int0 == Polynomial(coeffs)

print("P18:", (binomial2 ** 3).int(17))
coeffs = [17, 27, Fraction(27, 2), 3, Fraction(1/4)]
# print((binomial2 ** 3).int0.coeffs)
assert (binomial2 ** 3).int(17) == Polynomial(coeffs)

print("\t === Division algorithm ===")
p19a = Polynomial(1,2,3,4,5)
p19b = Polynomial(1,2)
print("P19a:", p19a, "÷", p19b)
q, r = divmod(p19a, p19b)
print("P19b:", f"q={q}, r={r}")
print("P19c:", f"q({p19b})+r = {q*p19b+r}")
assert p19a == q*p19b + r
print("P19d:", f"{p19a} // {p19b} = {p19a//p19b}")
assert p19a // p19b == q 
print("P19e:", f"{p19a} % {p19b} = {p19a%p19b}")
assert p19a % p19b == r

print("\t === Evaluation ===")
print("P20a:", f"({binomial2})(10) = {binomial2.apply(10)}")
assert binomial2.apply(10) == 13
print("P20b:", f"({binomial2**2})(10) = {(binomial2**2).apply(10)}")
assert (binomial2**2).apply(10) == 13*13
print("P20c:", f"mod({binomial2**2}),5) = {mod((binomial2**2),5)}")
assert mod((binomial2**2),5) == Polynomial(4, 1, 1)

print("\t === Normalization ===")
f = Polynomial(6, Fraction(1,2))
g = f.normal
d, h = f.normal2
print("P21a:", f"f(x)={f}, normalized: {g}")
assert g == Polynomial(12, 1)
assert h == g
assert d*h == f
f = Polynomial(6, 0, 0, Fraction(1,2))
g = f.normal
d, h = f.normal2
print("P21b:", f"f(x)={f}, normalized: {g}")
assert g == Polynomial(12, 0, 0, 1)
assert h == g
assert d*h == f
f = Polynomial(6, 0, 0, Fraction(-1,2))
g = f.normal
d, h = f.normal2
print("P21c:", f"f(x)={f}, normalized: {g}")
assert g == Polynomial(-12, 0, 0, 1)
assert h == g
assert d*h == f
f = Polynomial(6, 0, 0, 2)
g = f.normal
d, h = f.normal2
print("P21d:", f"f(x)={f}, normalized: {g}")
assert g == Polynomial(3, 0, 0, 1)
assert h == g
print(d, g, "=", f)
assert d*h == f
f = Polynomial(6, 0, 0, -2)
g = f.normal
d, h = f.normal2
print("P21e:", f"f(x)={f}, normalized: {g}")
assert g == Polynomial(-3, 0, 0, 1)
assert h == g
assert d*h == f

print("\t === GCD ===")
f = Polynomial(-1, 0, 1)
g = Polynomial(1, 1)
h = GCD(f, g)
print(f"P22a: GCD({f}, {g}) = {h}")
assert h == g
h = GCD(f, g**2)
print(f"P22b: GCD({f}, {g**2}) = {h}")
assert h == g

print("\t === Continued Fractions ===")
f = Polynomial(-1, 0, 1)
g = Polynomial(6, 5, 1)
result = cfrac(f, g)
print(f"P23a: ({f}) / ({g}) = {result}")
assert GCD(f,g) == 1        # precondition for work below
assert len(result) == 3     # needed for work below
p, q, r = result
    # p + 1 / (q + 1 / r)
    # p + r / (qr + 1)
    # (p(qr+1) + r) / (qr + 1)
s = p*(q*r+1) + r
t = q*r+1
print(s.normal, "/", t.normal)
assert s.normal == f
assert t.normal == g
p, q = c2p(result, debug=True)
print(p, "/", q)

result = cfrac(g, f)
print(f"P23b: ({g}) / ({f}) = {result}")
assert GCD(g,f) == 1        # precondition for work below
assert len(result) == 3     # needed for work below
p, q, r = result
    # p + 1 / (q + 1 / r)
    # p + r / (qr + 1)
    # (p(qr+1) + r) / (qr + 1)
s = p*(q*r+1) + r
t = q*r+1
print(s.normal, "/", t.normal)
assert s.normal == g
assert t.normal == f
p, q = c2p(result, debug=True)
print(p, "/", q)

    # Now we just let it loose
f = Polynomial(1, 1) * Polynomial(4, 1) * Polynomial(1, 4)
g = Polynomial(1, 1) * Polynomial(2, 1) * Polynomial(1, 2)
print("P23c:", f, "/", g)
print("\tGCD =", GCD(f, g))
assert GCD(f,g) == Polynomial(1,1)
result = cfrac(f, g)
print("\tCFRAC =", result)
p, q = c2p(result, debug=True)
print("\t", p, "/", q)
assert p == Polynomial(4, 1) * Polynomial(1, 4)
assert q == Polynomial(2, 1) * Polynomial(1, 2)

print("\t === Linear Factoring ===")
f = Polynomial(1, 1) * Polynomial(4, 1) * Polynomial(1, 4)
factors = factor(f)
print("P24a:", f, "=", f"{factors[0]}{factors[1:]}")
assert len(factors) == 4
assert prod(*factors) == f
f = Polynomial(1, 1) * Polynomial(4, 1) * Polynomial(1, 0, 1)
factors = factor(f)
# print(divmod(Polynomial(4, 1, 4, 1), Polynomial(4, 1)))
print("P24b:", f, "=", f"{factors[0]}{factors[1:]}")
assert len(factors) == 4
assert prod(*factors) == f
f = Polynomial(-1, 0, 0, 1)
factors = factor(f)
print("P24c:", f, "=", f"{factors[0]}{factors[1:]}")
assert len(factors) == 3
assert prod(*factors) == f
f = Polynomial(-1, 0, 0, 0, 1)
factors = factor(f)
print("P24d:", f, "=", f"{factors[0]}{factors[1:]}")
assert len(factors) == 4
assert prod(*factors) == f
f = Polynomial(1, Fraction(2,3))*Polynomial(Fraction(5,7),1)
f *= Polynomial(Fraction(11,13), Fraction(17,19))
factors = factor(f)
print("P24e:", f)
d, g = f.normal2
print("\t", "=", f"({d})({g})")
print("\t", "=", f"({factors[0]}){factors[1:]}")
assert len(factors) == 4
assert prod(*factors) == f
f = Polynomial(-1, Fraction(2,3))*Polynomial(Fraction(5,7),-1)
f *= Polynomial(-Fraction(11,13), Fraction(17,19))
factors = factor(f)
print("P24f:", f)
d, g = f.normal2
print("\t", "=", f"({d})({g})")
print("\t", "=", f"({factors[0]}){factors[1:]}")
assert len(factors) == 4
assert prod(*factors) == f

