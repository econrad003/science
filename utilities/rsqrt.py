"""
utilities.rsqrt - best rational approximation of the square root
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module finds a best rational approximation of the square root
    of a rational number using Newton's method.  The Newton approximation
    of the square root is equivalent to the algorithm that was probably
    used by Babylonian mathematicians to estimate square roots.

NEWTON'S METHOD

    Suppose we want to find the square root of some positive rational
    number n.  In the modern formulation of Newton's method, we consider
    the equation:

        y = f(x) = x² - n

    The number we are trying to find is the positive root of this equation,
    i.e., the value of x which is to the right of the y-axis, and for which
    f(x)=0.

    We note that the slope of a tangent line at x is given by:

        f'(x) = 2x

    Now suppose we have an estimate xₙ.  The slope of the tangent to f(x)
    at xₙ is m=2xₙ.  So the equation of the tangent line is:

        y - yₙ = m(x - xₙ)

    The value of -yₙ is n - xₙ².  Putting in the values of m and -yₙ, we
    have:

        y + n - xₙ² = 2xₙ(x - xₙ) = 2xₙx - 2xₙ²

    The y-intercept (i.e. y=0) gives the value of our next extimate:

        2xₙxₙ₊₁ - 2x² = n - xₙ²

              2xₙxₙ₊₁ = n + xₙ²

                          n
                         ---- + xₙ
                          xₙ
                 xₙ₊₁ = -----------
                            2

    It can be shown that this process will converge.

THE BABYLONIAN METHOD

    Based on actual estimates and procedures used to solve quadratic
    equations, we can guess that the Babylonian estimates were obtained
    by completing the square.  Our anachronistic "translation" makes
    use of the language of equations which was developed in Europe in
    the seventeenth century CE.  (The underlying algorithm is at least
    3500 years earlier.)

            +-----------+-----+
            |           |     |
            |           |     |
          a |    a²     | ab  |     (a+b)² = a² + 2ab + b²
            |           |     |
            +-----------+-----+
            |           |     |
          b |    ab     | b²  |
            +-----------+-----+

    Suppose n = (a + b)² where a is our guess for √n and b is the real
    error in our guess.  If b is small compared to a, then b² is
    negligible.  So we will estimate the error b using the equation:

        n = a² + 2ab = a(a + 2b)

    Divide by a:

         n
        --- = a + 2b
         a

    Subtract a, then divide by two:

              n
             --- - a
              a
        b = ----------
                 2

    This is the estimated error.  So our new estimate of √n is obtained
    by adding a:

                  n
                 --- + a
                  a
        a + b = ----------
                     2

EXAMPLE

    Suppose we want to estimate the square root of five and suppose our
    initial guess is 4.  (Yes, it's awful!)

        x₀ = 4          a = 4

                        a + b = (5/4 + 4) / 2 = 21/8

        x₁ = 21/8       a = 21/8

                        a + b = (40/21 + 21/4) / 2 = 761/336

        x₂ = 761/336    a = 761/336

                        a + b = (1680/761 + 761/336) / 2 = 1143601/511392

        x₃ = 1143601/511392

    The underlying assumption is that the square of the error was
    "neglible".  The obvious question is whether that was a reasonable
    assumption.  The answer is that it depends on the guess.  So let's
    see how our guesses compare with Python's estimate of √5:

        √5 : 2.23606797749979

        n   guess                   approximate error       rating
       -------------------------------------------------------------
        0   4                           -1.8                awful!
        1   21/8                        -0.4                better, but bad
        2   761/336                     -0.03               better
        3   1143601/511392              -0.0002             much better

    Even though we were off to a bad start, with just three iterations,
    our estimate was accurate to roughly five significant decimal digits
    of precision.

    In fact, √5 is between 2 and 3, so what if we started with one of those
    values.  We will try 2...

        x₀ = 2          a = 2

                        a + b = (5/2 + 2) / 2 = 9/4

        x₁ = 9/4        a = 9/4

                        a + b = (20/9 + 9/4) / 2 = 161/72

        x₂ = 161/72     a = 161/72

                        a + b = (360/161 + 161/72) / 2 = 51841/23184

        x₃ = 51841/23184

    Now! How did we do?

        n   guess                   approximate error       rating
       -------------------------------------------------------------
        0   2                           0.23                bad
        1   9/4                         -0.014              better
        2   761/336                     -4.3e-05            great
        3   1143601/511392              -4.2e-10            smokin'!!

    Some observations:

        1) If we start with a bad estimate, we get a better one on the
           next round.

        2) If we start with a good estimate, we get a great one on the
           next round.

        3) If we undershoot on the first estimate, we will overshoot.
           (All subsequent estimates will be high.)

    If we do one more iteration, we get:

        x₄ = 5374978561/2403763488

    The error is too close to call:

        sqrt(5) - x₄ = 0.0 (floating point underflow)

    This last value is actually a better estimate of the square root of
    5 than the 14-significant digit floating point estimate returned
    by sqrt(5). It is accurate to roughly 20 significant digits.

NOTE

    To estimate the error in an estimate, get the next estimate, find
    the difference, and then double the result.  (Doubling the result
    compensates for the overshoot in both estimates.)

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
from numbers import Real
from fractions import Fraction
from math import floor, isqrt

PRECISION = Fraction(1, 100000)
assert PRECISION > 0

def next_estimate(n, x):
    """used to obtain the next estimate"""
    return (n/x + x) / 2

def rsqrt(n:Real, x0:Real=None, maxerr=PRECISION, debug:bool=False) -> Fraction:
    """obtain a rational estimate of the square root using Newton's method

    REQUIRED ARGUMENTS

        n - the number whose square root is to be estimated.  It must be
            non-negative.

    OPTIONAL ARGUMENT

        x0 - an initial estimate.  If none is given, then:

            a) if n>1, then isqrt(n) will be used as an estimate;

            b) otherwise, we consider the reciprocal and use isqrt.

        maxerr - the maximum error in the estimate.  The default is
            0.00001 (exact). The actual error will be less than
            this value.

        debug - if True, display the intermediate estimates
    """
            # SETUP AND VALIDATION
    if debug:
        k = 0
        print(f"estimating: sqrt({n})")
    n = Fraction(n)
    if n < 0:
        raise ValueError("'n' must be non-negative")
    if x0 == None:
        if n >= 1:
            x0 = isqrt(floor(n))
        elif n > 0:
            x0 = Fraction(1, isqrt(floor(1/n)))
        else:
            x0 = 0
    x0 = Fraction(x0)
    if x0 < 0:
        raise ValueError("'x0' must be non-negative")
    if maxerr <= 0:
        raise ValueError("'maxerr' must be positive")
            # LOOP
    while True:
        if debug:
            print(f"guess {k}: {x0}")
            k += 1
        x1 = next_estimate(n, x0)
        err = abs(2 * (x0 - x1))
        if err <= maxerr:
            break
        x0 = x1
    return x0

# END utilities.rsqrt
