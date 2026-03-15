"""
tests.test_linear2o - second order linear module (tests)
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

from sequences.linear2o import Sequences

def ratios(a, b):
    print(f"                 ratio: {a}/{b} = {a/b}")

def testFibo():
    print()
    print("\tFIBONACCI SEQUENCES TEST")
    fibo = Sequences(1, 1)
    print("characteristic equation:", fibo.charpoly, "=", 0)
    lambda0, lambda1 = fibo.eigenvalues
    print("            eigenvalues:", f"{lambda0}, {lambda1}")
    f1, f2 = fibo.eigenfunctions

    print()
    fibonacci1 = fibo.iterates(1, 0, 13)
    print(f"          Fibonacci(1): {fibonacci1}")
    assert fibonacci1[12] == 89

    A, B = fibo.coeffs(1, 0)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    fibonacci2 = fibo.iterates(0, 1, 13)
    print(f"          Fibonacci(2): {fibonacci2}")
    assert fibonacci2[12] == 144

    A, B = fibo.coeffs(0, 1)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    lucas = fibo.iterates(2, 1, 13)
    print(f"                 Lucas: {lucas}")
    assert lucas[12] == 322

    A, B = fibo.coeffs(2, 1)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    ratios(fibonacci1[12], fibonacci1[11])
    ratios(fibonacci2[12], fibonacci2[11])
    ratios(lucas[12], lucas[11])
    ratios(fibonacci2[12], fibonacci1[12])
    print(f"              (1+√5)/2: (1+√5)/2 = {(1+sqrt(5))/2}")

def testDouble():
    print()
    print("\tDOUBLING SEQUENCES TEST")
    root2 = Sequences(0, 2)
    print("characteristic equation:", root2.charpoly, "=", 0)
    lambda0, lambda1 = root2.eigenvalues
    print("            eigenvalues:", f"{lambda0}, {lambda1}")
    f1, f2 = root2.eigenfunctions

    print()
    root2_10 = root2.iterates(1, 0, 13)
    print(f"           double(1,0): {root2_10}")
    assert root2_10[12] == 64

    A, B = root2.coeffs(1, 0)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    root2_01 = root2.iterates(0, 1, 13)
    print(f"           double(0,1): {root2_01}")
    assert root2_01[12] == 0

    A, B = root2.coeffs(0, 1)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    lucas = root2.iterates(2, 1, 13)
    print(f"          double(2,1): {lucas}")
    assert lucas[12] == 128

    A, B = root2.coeffs(2, 1)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

def testRoot2():
    print()
    print("\tSQRT(2) ESTIMATE SEQUENCES TEST")
    root2 = Sequences(2, 1)
    print("characteristic equation:", root2.charpoly, "=", 0)
    lambda0, lambda1 = root2.eigenvalues
    print("            eigenvalues:", f"{lambda0}, {lambda1}")
    f1, f2 = root2.eigenfunctions

    print()
    root2_10 = root2.iterates(1, 0, 13)
    print(f"            root2(1,0): {root2_10}")
    assert root2_10[12] == 5741

    A, B = root2.coeffs(1, 0)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    root2_01 = root2.iterates(0, 1, 13)
    print(f"            root2(0,1): {root2_01}")
    assert root2_01[12] == 13860

    A, B = root2.coeffs(0, 1)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    diff = root2.iterates(-1, 1, 13)
    print(f"           root2(-1,1): {diff}")
    assert diff[12] == 8119

    A, B = root2.coeffs(2, 1)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    ratios(root2_10[12], root2_10[11])
    ratios(root2_01[12], root2_01[11])
    ratios(diff[12], diff[11])
    ratios(root2_01[12], root2_10[12])
    print(f"                  1+√2: 1+√2 = {1+sqrt(2)}")

def testRoot3():
    print()
    print("\tSQRT(3) ESTIMATE SEQUENCES TEST")
    root3 = Sequences(2, 2)
    print("characteristic equation:", root3.charpoly, "=", 0)
    lambda0, lambda1 = root3.eigenvalues
    print("            eigenvalues:", f"{lambda0}, {lambda1}")
    f1, f2 = root3.eigenfunctions

    print()
    root3_10 = root3.iterates(1, 0, 11)
    print(f"            root3(1,0): {root3_10}")
    assert root3_10[10] == 4896

    A, B = root3.coeffs(1, 0)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    root3_01 = root3.iterates(0, 1, 11)
    print(f"            root3(0,1): {root3_01}")
    assert root3_01[10] == 6688

    A, B = root3.coeffs(0, 1)
    print(f"          coefficients: {A}, {B}")
    print(f"         Binet at n=12: {A*f1(12)+B*f2(12)}")
    print(f"        Binet at n=-12: {A*f1(-12)+B*f2(-12)}")
    print(f"        Binet at n=-11: {A*f1(-11)+B*f2(-11)}")

    print()
    ratios(root3_10[10], root3_10[9])
    ratios(root3_01[10], root3_01[9])
    print(f"                  1+√3: 1+√3 = {1+sqrt(3)}")

if __name__ == "__main__":
    print("Testing module sequences.linear2o")
    testFibo()
    print()
    testDouble()
    print()
    testRoot2()
    print()
    testRoot3()
    print()
    print("SUCCESS!")

# END tests.test_linear2o
