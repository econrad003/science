"""
demos.linear2o - second order linear module (demonstrations)
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
from math import sqrt
from fractions import Fraction

from sequences.linear2o import Sequences

summary = dict()

def seq(a, b, n):
    """demonstration for s[n+2] = a s[n+1] + b s[n]"""
    if b >= 0:
        print(f"demo: s[n+2] = {a}s[n+1] + {b}s[n]")
    else:
        print(f"demo: s[n+2] = {a}s[n+1] + {b}s[n]")
    fibo = Sequences(a, b)
    lambda0, lambda1 = fibo.eigenvalues
    print(f"  eigenvalues: {lambda0} = {float(lambda0)}")
    print(f"               {lambda1} = {float(lambda1)}")
    f1, f2 = fibo.eigenfunctions
    print("     iterates:")
    fibo1 = fibo.iterates(1, 0, n+5)
    fibo2 = fibo.iterates(0, 1, n+5)
    print(f"        (1, 0) = {fibo1[:-5]}")
    print(f"        (0, 1) = {fibo2[:-5]}")
    print("  convergents:")
    c1 = Fraction(fibo1[-1], fibo1[-2])
    delta1 = float(c1 - lambda0)
    c2 = Fraction(fibo2[-1], fibo2[-2])
    delta2 = float(c2 - lambda0)
    c3 = abs(Fraction(fibo2[-1], fibo1[-1]))
    delta3 = float(c3 - lambda0)
    print(f"            c1 = {c1} = {float(c1)}  err={delta1:.2e}")
    print(f"            c2 = {c2} = {float(c2)}  err={delta2:.2e}")
    print(f"          * c3 = {c3} = {float(c3)}  err={delta3:.2e}")
    return lambda0, c1, c2, c3

def sqerror(root, estimate):
    """find the square-error"""
    return float(root.discriminant - estimate * estimate)

def unpack(args):
    """look for estimate of square root"""
    lambda1, c1, c2, c3 = args
    a1, a2 = lambda1.real, lambda1.imag
    root = (lambda1 - a1) / a2
    print(f"        root: {root} = {float(root)}")
    froot = float(root)
    u1 = (c1 - a1) / a2
    delta1 = sqerror(root, u1)
    if root in summary:
        u, delta = summary[root]
        if abs(delta1) < abs(delta):
            u, delta = u1, delta1
    else:
        u, delta = u1, delta1
    u2 = (c2 - a1) / a2
    delta2 = sqerror(root, u2)
    if abs(delta2) < abs(delta):
        u, delta = u2, delta2
    u3 = (c3 - a1) / a2
    delta3 = sqerror(root, u3)
    if abs(delta3) < abs(delta):
        u, delta = u3, delta3
    summary[root] = (u, delta)
    print(f"            u1 = {u1} = {float(u1)}  sqerr={delta1:.2e}")
    print(f"            u2 = {u2} = {float(u2)}  sqerr={delta2:.2e}")
    print(f"            u3 = {u3} = {float(u3)}  sqerr={delta3:.2e}")
    print()

if __name__ == "__main__":
    print("At the end is a summary which gives the closest rational estimate")
    print("for each root, based on how close it is to Python's estimate.")
    print()
    unpack(seq(1, 1, 15))
    unpack(seq(2, 1, 13))
    unpack(seq(3, 1, 12))
    unpack(seq(4, 1, 11))
    unpack(seq(5, 1, 11))
    unpack(seq(6, 1, 10))
    unpack(seq(7, 1, 10))
    unpack(seq(8, 1, 10))
    unpack(seq(9, 1, 10))
    unpack(seq(10, 1, 9))
    unpack(seq(11, 1, 9))
    unpack(seq(12, 1, 9))

    unpack(seq(3, -1, 12))
    unpack(seq(4, -1, 11))
    unpack(seq(5, -1, 11))
    unpack(seq(6, -1, 10))
    unpack(seq(7, -1, 10))
    unpack(seq(8, -1, 10))
    unpack(seq(9, -1, 10))
    unpack(seq(10, -1, 9))
    unpack(seq(11, -1, 9))
    unpack(seq(12, -1, 9))

    print("-" * 72)
    print()
    print("\t\tSQUARE ROOT SUMMARY")
    print()
    for root in summary:
        u, delta = summary[root]
        print(f"{root}\t{u} = {float(u):.8f}\t(sqerr={delta:.2e})")

    print()
    print("NOTES:")
    print("  1. Python floats have about 15 significant digits of precision.")
    print("     Except for √3, all the rational estimates exceed this precision.")
    print("  2. The square error is the signed difference between the")
    print("     discriminant and the square of the estimate.")
    print("  3. Five additional terms (beyond those displayed) were used.")

# END demos.linear2o
