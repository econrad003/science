"""
tests.test_polymod - test univariate polynomials modulo n
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
from random import randrange
from polynomials.polymod import make_poly

def print_doc():
    """display the help"""
    PolyMod = make_poly(11)
    help(PolyMod)

def test1(n, *coeffs):
    """a simple test

    DESCRIPTION

        Create a polynomial and subtract it from itself.  If the result
        is zero, the test passes.
    """
    print("TEST1:", n, *coeffs)
    PolyMod = make_poly(n)
    print(f"  PolyMod.__name__= {PolyMod.__name__}")
    f = PolyMod(coeffs)
    print(f"  f(x)={str(f)}")
    assert f==f
    assert f-f==0
    g = PolyMod(*coeffs)
    assert g==f
    assert g-f==0
    h = PolyMod(f)
    assert h==f
    assert h-f==0
    p = +f
    assert p==f
    assert p-f==0
    q = -f
    assert f+q==0
    assert f == -q
    r = 0-f
    assert f+r==0
    assert f == -r
    print("  ok!")

def test2():
    """verify that evaluation works correctly"""
    PolyMod = make_poly(5, indeterminate='y')   # an easy modulus
    f = PolyMod(4, 3, 2, 1, 5)
    R = f.coefficient_ring()
    print(f"TEST2: f(y)={f}")
    assert f.deg == 3, f"{f.deg}"
    assert f.apply(R(0)) == R(4), f"{f.apply(R(0))}"
    assert f.apply(R(1)) == R(0), f"{f.apply(R(1))}"  # 4+3+2+1 = 10 = 0
    assert f.apply(R(2)) == R(1), f"{f.apply(R(2))}"  # 4+6+8+8 = 26 = 1
    assert f.apply(R(3)) == R(3), f"{f.apply(R(3))}"  # 4-6+8-8 = -2 = 3
    assert f.apply(R(4)) == R(2), f"{f.apply(R(4))}"  # 4-3+2-1 = 2
    print("  ok!")

def test3():
    """test the coefficient manipulations"""
    PolyMod = make_poly(11)
    f = PolyMod(1, 2, 3, 4, 5)
    R = f.coefficient_ring()
    print(f"TEST3: coefficients in f(x)={f}")
    assert len(f) == 5
    assert f.deg == 4
    assert abs(f) == 4, f"abs(f)"   # same as degree
    assert f.coeffs == [R(1), R(2), R(3), R(4), R(5)]
    print("    coefficient list... ok!")
    foo = iter(f)
    assert next(foo) == R(1)
    assert next(foo) == R(2)
    assert next(foo) == R(3)
    assert next(foo) == R(4)
    assert next(foo) == R(5)
    try:
        next(foo)
        assert False, "iteration failure"
    except StopIteration:
        print("    iter... ok!")
    assert f[0] == R(1)
    assert f[1] == R(2)
    assert f[2] == R(3)
    assert f[3] == R(4)
    assert f[4] == R(5)
    assert f[5] == R(0)
    assert f[6] == R(0)
    print("    [n] when n >= 0... ok!")
    assert f[-1] == R(5)
    assert f[-2] == R(4)
    assert f[-3] == R(3)
    assert f[-4] == R(2)
    assert f[-5] == R(1)
    try:
        f[-6]
        assert False, "negative indexing failure"
    except IndexError:
        print("    [n] when n < 0... ok!")
    assert f>>0 == f
    assert f>>1 == PolyMod(0, 1, 2, 3, 4, 5)
    assert f>>2 == PolyMod(0, 0, 1, 2, 3, 4, 5)
    print("    right shift... ok!")
    assert f<<0 == f
    assert f<<1 == PolyMod(2, 3, 4, 5)
    assert f<<2 == PolyMod(3, 4, 5)
    assert f<<3 == PolyMod(4, 5)
    assert f<<4 == PolyMod(5)
    assert f<<5 == 0
    assert f<<6 == 0
    print("    left shift... ok!")
    print("  ok!")

def test4():
    """test multiplication"""
    def mpy(a, b, exp, verbose=False):
        """test a multiplication"""
        result = a*b
        if verbose:
            print(f"      ({a})({b})={exp}")
        assert result == exp, f"({a})({b})={exp};\n   got={result}"
    PolyMod = make_poly(11)
    f = PolyMod(1, 2, 3, 4, 5)
    R = f.coefficient_ring()
    print(f"TEST4: multiplication with f(x)={f}")
    assert 2*f == PolyMod(2, 4, 6, 8, 10)
    assert 3*f == PolyMod(3, 6, 9, 1, 4)
    assert R(3)*f == 3*f
    print("    scalar multiplication... ok!")
    assert 1*f == f
    mpy(PolyMod(1), f, f)
    mpy(PolyMod(0, 1), f, f>>1)
    mpy(PolyMod(0, 0, 1), f, f>>2)
    mpy(PolyMod(0, 0, 0, 1), f, f>>3)
    mpy(PolyMod(0, 2), f, 2*(f>>1))
    mpy(PolyMod(0, 0, 2), f, 2*(f>>2))
    mpy(PolyMod(0, 0, 0, 2), f, 2*(f>>3))
    print("    monomial multiplication... ok!")
    print("      Example 1:")
    print(f"           {2*(f>>1)}       -- f(x) times 2x")
    print(f"          +     {f}     -- f(x) times 1")
    print("          + ----------------------")
    print(f"           {2*(f>>1)+f}    -- sum (modulo 11)")
    print("      ---")
    mpy(PolyMod(1, 2), f, f + 2*(f>>1), verbose=True)
    mpy(PolyMod(1, 2, 3), f, f + 2*(f>>1) + 3*(f>>2), verbose=True)
    print("    multinomial multiplication (mod 11)... ok!")
    print("      *** If a lead coefficient is a zero divisor,")
    print("          the degree of the product may be less than")
    print("          the sum of the degrees ***")
    PolyMod10 = make_poly(10)
    g = PolyMod10(1, 2, 3, 4, 5)
    h = PolyMod10(1, 2, 3, 4)
    print(f"      modulus = 10  (Ring {PolyMod10.coefficient_ring().__name__})")
    print(f"        g(x) = {g}")
    print(f"        h(x) = {h}")
    print("        Product (g*h)(x):")
    print(f"             1 g(x) =         {g}")
    print(f"            2x g(x) =         {2*(g>>1)}    <-- note degree")
    print(f"           3x² g(x) = {3*(g>>2)}")
    print(f"           4x³ g(x) = {4*(g>>3)}           <-- note degree")
    print("           ------------------------------------")
    print(f"           (g*h)(x) = {g*h}")
    print("         Many terms drop out...")
    print("               x⁷: 4*5 = 20           <- multiple of 10")
    print("               x⁴: 5+8+9+8 = 30       <- multiple of 10")
    print("               x³: 4+6+6+4 = 20       <- multiple of 10")
    print("               x²: 3+4+3=10           <- multiple of 10")
    print("         Also note lead term of 2x g(x)...")
    mpy(g, h, g+2*(g>>1)+3*(g>>2)+4*(g>>3), verbose=True)
    print("    multinomial multiplication (mod 10)... ok!")
    print("  ok!")

def test5(quadratics=40, cubics=20):
    """division algorithm"""
    PolyMod = make_poly(11)         # modulus is prime, greater than 6
    f = PolyMod(1, 2, 3, 4, 5)
    R = f.coefficient_ring()
    print(f"TEST5: dividend f(x)={f} over {R.__name__}")
    g = PolyMod(0)
    print("    division by zero? need exception...")
    try:
        divmod(f, g)
        assert False, "no ZeroDivisionError exception"
    except ZeroDivisionError:
        print("        ZeroDivisionError successfully raised")
    print("    division by zero? ok!")
    g = PolyMod(1)
    q, r = divmod(f, g)
    assert f == g * q + r, f"{f}: ({g})({q})+({r})={g*q+r}"
    assert q==f and r==0, f"q={q}, r={r}"
    print(f"    ({g})({q})+({r})={f}...ok!")
    g = PolyMod(2, 3, 4, 5)
    q, r = divmod(f, g)
    assert f == g * q + r, f"{f}: ({g})({q})+({r})={g*q+r}"
    assert q==PolyMod(0,1) and r==1, f"q={q}, r={r}"
    print(f"    ({g})({q})+({r})={f}...ok!")
    g = PolyMod(3, 4, 5)
    q, r = divmod(f, g)
    assert f == g * q + r, f"{f}: ({g})({q})+({r})={g*q+r}"
    assert q==PolyMod(0,0,1) and r==PolyMod(1,2), f"q={q}, r={r}"
    print(f"    ({g})({q})+({r})={f}...ok!")

    g = PolyMod(1,2, 3, 4, 5, 6)
    q, r = divmod(f, g)
    assert f == g * q + r, f"{f}: ({g})({q})+({r})={g*q+r}"
    assert q==0 and r==f, f"q={q}, r={r}"
    print(f"    ({g})({q})+({r})={f}...ok!")

    count = 0
    for x in R.elements():
        g = PolyMod(-x, 1)
        fx = f.apply(x)
        q, r = divmod(f, g)
        assert f == g * q + r, f"{f}: ({g})({q})+({r})={g*q+r}"
        assert r == fx, f"r={r}, f({x})={fx}"
        for a in R.elements():
            if a.is_zero_divisor:
                continue
            count += 1
            g = PolyMod(-x, a)
            fx = f.apply(x / a)
            q, r = divmod(f, g)
            assert f == g * q + r, f"{f}: ({g})({q})+({r})={g*q+r}"
            assert r == fx, f"g(x)={g}, r={r}, f({x})={fx/a}"
    print(f"    all {count} linear divisors checked... ok!")
    for count in range(quadratics):
        a = randrange(1, 11)
        b = randrange(11)
        c = randrange(11)
        g = PolyMod(c, b, a)
        q, r = divmod(f, g)
#        print(f"  divmod({f}, {g}) q={q} r={r}")
        assert f == g * q + r, f"{f}: ({g})({q})+({r})={g*q+r}"
        assert r.deg < g.deg, f"{r.deg} < {g.deg}"
    print(f"    {quadratics} random quadratic divisors checked... ok!")
    for count in range(cubics):
        a = randrange(1, 11)
        b = randrange(11)
        c = randrange(11)
        d = randrange(11)
        g = PolyMod(d, c, b, a)
        q, r = divmod(f, g)
#        print(f"  divmod({f}, {g}) q={q} r={r}")
        assert f == g * q + r, f"{f}: ({g})({q})+({r})={g*q+r}"
        assert r.deg < g.deg, f"{r.deg} < {g.deg}"
        q2 = f // g
        assert q2 == q
        r2 = f % g
        assert r2 == r
    print(f"    {cubics} random cubic divisors checked... ok!")
    print("  ok!")

def test6():
    """quick GCD test"""
    from polynomials.polymod import polynomialGCD as GCD
    PolyMod = make_poly(11)         # modulus is prime
        # two quintics
    f = PolyMod(1, 3)**2 * PolyMod(3, 1)**2 * PolyMod(7, 1)
    g = PolyMod(1, 3)**2 * PolyMod(3, 1) * PolyMod(5, 1) * PolyMod(1, 7)
    p = PolyMod(1, 3)**2 * PolyMod(3, 1)
    print(f"TEST6: GCD({f}, {g})")
    h = GCD(f, g)
    print(f"    GCD = {h}  -- expected {p/p[-1]}")
    assert f % h == 0
    assert g % h == 0
    assert h[-1] == 1
    assert h.deg == 3
    assert h == p/p[-1]
    print("  ok!")

def test7():
    """quick power test"""
    PolyMod = make_poly(13)
    f = PolyMod(1, 1)
    g = f ** 11
    print(f"TEST7: ({f})^11 == {g}")
    h = f * f * f * f * f * f * f * f * f * f * f # <-- 11 factors
    print(f"    expected: {h}")
        # check the value of h using the binomial theorem
    assert h.deg == 11   # wrong number of terms
    assert h[0] == h[-1] == 1  #           BINOMIAL THEOREM
    assert h[1] == h[-2] == 11 # 11 mod 13, by binomial theorem
    assert h[2] == h[-3] == 3  # 11x10/2 = 55; 55 mod 13 = 3
    assert h[3] == h[-4] == 9  # 11x10x9/6 = 55x3; 55x3 mod 13 = 9
        # progressively check g
    assert g.deg == 11
    assert g[0] == g[-1] == 1  #           BINOMIAL THEOREM
    assert g[1] == g[-2] == 11 # 11 mod 13, by binomial theorem
    assert g[2] == g[-3] == 3  # 11x10/2 = 55; 55 mod 13 = 3
    assert g[3] == g[-4] == 9  # 11x10x9/6 = 55x3; 55x3 mod 13 = 9
    assert g == h
    print("  ok!")

def test8():
    """continued fractions of quotients"""
    from polynomials.polymod import cfrac
    PolyMod = make_poly(11)     # prime modulus
    R = PolyMod.coefficient_ring()
    print("TEST8: continued fractions f(x)/g(x)")
    print("  >>> The continued fraction gives meaning to the quotient.")
    f = PolyMod(1, 1) ** 11
    g = PolyMod(1, 2)                   # GCD(f,g)=1
        # if the GCD is not 1, the check at the end won't work
    print(f"  >>> EXAMPLE 1: f(x)={f}; g(x)={g}")
    cf = cfrac(f, g)
    print(f"    terms: {len(cf)}")
    print(f"    result = ({cf[0]}) + 1/({cf[1]})")
    assert len(cf) == 2
    a0, a1 = PolyMod(0), PolyMod(1)
    b0, b1 = PolyMod(1), PolyMod(0)
    for n in range(len(cf)):
        q = cf[n]
        a2 = q * a1 + a0
        b2 = q * b1 + b0
        print(f"      {n=}  a(x)={a2}; b(x)={b2}")
        a0, a1 = a1, a2
        b0, b1 = b1, b2
    m = f[-1] / a1[-1]
    assert m * a1 == f          # Using GCD=1
    assert m * b1 == g

    g = PolyMod(1, 2) * PolyMod(1, 3)   # GCD(f,g)=1
    print(f"  >>> EXAMPLE 2: f(x)={f}; g(x)={g}")
    cf = cfrac(f, g)
    print(f"    terms: {len(cf)}")
    print(f"    result = ({cf[0]}) + 1/({cf[1]} + 1/({cf[2]}))")
    assert len(cf) == 3
    a0, a1 = PolyMod(0), PolyMod(1)
    b0, b1 = PolyMod(1), PolyMod(0)
    for n in range(len(cf)):
        q = cf[n]
        a2 = q * a1 + a0
        b2 = q * b1 + b0
        print(f"      {n=}  a(x)={a2}; b(x)={b2}")
        a0, a1 = a1, a2
        b0, b1 = b1, b2
    m = f[-1] / a1[-1]
    assert m * a1 == f          # Using GCD=1
    assert m * b1 == g
    print("  >>> The numerator and denominator are recovered up to a scalar")
    print("      multiple of the GCD.")
    print("  ok!")

def test9():
    """(formal) derivatives and integrals"""
    print("TEST9:", test9.__doc__)
    PolyMod = make_poly(3)      # small prime modulus
    print("     -- FUN FACTS:")
    print("     --              prime modulus")
    print("     --   In (ℤ/3ℤ)[x], the third derivative is always zero!")
    print("     --   In (ℤ/pℤ)[x], the pth derivative is always zero!")
    print("     --   Some polynomials don't have antiderivatives!")
    print("     --")
    f = PolyMod(1,1,1,1,1,1,1)
    print(f"         f(x) = {f}            modulo 3")
    print(f"        f'(x) = {f.D}")
    assert f.D == PolyMod(1, 2, 0, 1, 2)
    print(f"       f''(x) = {f.D.D}")
    assert f.D.D == PolyMod(2, 0, 0, 2)
    print(f"      f'''(x) = {f.D.D.D}")
    assert f.D.D.D == 0
    g = PolyMod(1,1,0,1,1)
    print("  Some antiderivatives modulo 3")
    print(f"        g(x) = {g}")
    print(f"     (Ig)(x) = {g.int}")
    assert g.int == PolyMod(0,1,2,0,1,2)
    print(f"           Ig doesn't have an antiderivative...")
    try:
        g.int.int
        assert False, f"(IIg)(x) = {str(g.int.int)}"
    except ZeroDivisionError as msg:
        print("   ZeroDivisionError:", msg, "<----- OK!")
        print(f"   {g.int} does not have an antiderivative!")
    
    PolyMod = make_poly(10)      # composite modulus
    R = PolyMod.coefficient_ring()
    print("     -- FUN FACTS:")
    print("     --              composite modulus")
    print("     --   Numbers which are not relatively prime to the modulus")
    print("     --      are divisors of zero.  If both the exponent of a")
    print("     --      term and the coefficient of the term are divisors")
    print("     --      of zero, then the derivative of the term might be")
    print("     --      zero.  Or it might not.  It will whenever the")
    print("     --      product of the exponent and the coefficient is")
    print("     --      zero.")
    print("     --   For example, in (ℤ/10ℤ)[x]:")
    print("     --      (a) the derivative of 2x^2 is 4x (not zero);")
    print("     --      (b) the derivative of 5x^2 is zero.")
    print("     --   In (ℤ/nℤ)[x], the nth derivative is always zero!")
    print("     --")
    f = PolyMod(1,1,2,1,1,2,1,1,2,1,1,2,1,1,2)
    print(f"    f(x)={f}    modulus=10")
    i = 0
    while f != 0:
        i += 1
        name = f"f^({i})(x)"
        f = f.D
        print(f"        {name}(x)={f}")
    assert i == 5
    print("  ok!")
            #   0 1 2 3 4 5 6 7 8 9 0 1 2
    g = PolyMod(1,0,1,0,0,0,1,0,1,0,1,0,1)
    print(f"       g(x)={g}    modulus=10")
    print(f"    (Ig)(x)={g.int}")
    assert g.int == PolyMod(0,1,0,R(1)/3,0,0,0,R(1)/7,0,R(1)/9,0,1,0,R(1)/3)
    try:
        g.int.int
        assert False, f"(IIg)(x) = {str(g.int.int)}"
    except ZeroDivisionError as msg:
        print("   ZeroDivisionError:", msg, "<----- OK!")
        print(f"   {g.int} does not have an antiderivative!")
    

if __name__ == "__main__":
    print_doc()
    test1(10, 1, 2, 3, 4, 5)
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    print("SUCCESS!")

# END tests.test_polymod
