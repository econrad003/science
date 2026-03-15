# Mathematics - utilities

Some say that mathematics is the queen of the sciences, and some call it the handmaiden of the sciences.  What is your take on this?

Is mathematics discovered or is it invented?

## Contents

**1. Primes**  
**2. Primality**  
**3. Quadratic rational fields**  
**4. Inequalities and continued fractions**  


## 1. Primes

Class *Primes* (from module *moremath* in the *utilities* folder is a utility for managing integer primes using the sieve of Eratosthenes.  To use it, simply import the class.  It's contains a list of "small" positive primes and several class methods.  The small primes list is extended as needed or as requested by sieving.

**Methods:**

* *Primes.small_primes()* - returns a copy of the current small primes list.
* *Primes.largest()* - returns a pair consisting of the index of the largest prime in the table and the last sieved value.  For example, if the return value is (8, 21), that means there are 8 positive primes and the sieve has progressed to n=21.  Then the largest sieved prime would be *Primes.pi(8)* which returns 19.
* *Primes.pi(n)* returns the indexed prime.  The value of *n* must be a non-negative integer.  For *n* equal to 0, 1, 2, 3, 4, 5, 6, 7, and 8, *Primes.pi(n)* returns 0, 2, 3, 5, 7, 11, 13, 17, and 19, respectively, and so on.  If the index exceeds index of the largest sieved prime, then sieving will resume until the requested positive prime has been found and tabulated.
* *Primes.sieve_to(n)* sieves to the indicated value.  (If the value is even, the sieve will continue through *n+1*.)  For example, *Primes.sieve_to(99)* will extend the list to all primes less than 100.  The sieve always picks up from where it last left off.
* *Primes.is_small_prime(n)* returns *True* if the absolute value of n is in the small primes list.  For example, *Primes.is_small_prime(n)* returns *True* for *n* equal to 0, -11 and 11 and *False* for -1, 1, -10 and 10.  The sieve is not engaged so primes larger in absolute value than the largest tabulated prime will return *False*.  (This is not a test for primality.)
* *Primes.is_prime(n, sieve=False)*.  To sieve or not to sieve, that is the question.  If the default (*sieve=False*) is taken, then there are three possible return values: *True* (if the number is provably prime), *False* (if the number is either a unit or provably composite), or *Primes.MAYBE* (0.5, if primality cannot be proved or disproved by dividing by a small prime.)  If *sieve=True*, then the sieve will extend the list as far as needed to establish primality.

The initial small positive primes list is (2, 3, 5, 7, 11, 13, 17, 19).  This is adequate to determine primality for any positive integer less than or equal to the square of 19 (*i.e.* 361).  Larger values which have any of these 8 primes as a divisor are, of course *provably* composite without sieving.

## 2. Primality

The *primality* module in the *utilities* folder provides the following utilities which use the *Primes* class:

* Method *is_positive_prime(n)* returns *True* if the positive integer *n* is prime and *False* ptherwise.  (An exception is raised if *n* is not a positive integer.)  Results are cached so this method is useful when a given number is repeatedly checked.
* Method *is_prime(n)* returns *True* if the absolute value of the number *n* is a positive prime or is zero.  The method uses *is_positive_prime*, so it uses caching indirectly.
* Method *is_square_free(n)* returns True if the integer *n* is square-free.  It uses the *Primes* class to try finding a positive prime whose square divides *n*.  Results are cached, so this method is useful for a situation where some given number needs to be repeatedly checked.  Note that 0 is not square-free as 4 divides 0, but both 1 and -1 are square-free. Apart from 0, the smallest non-square-free integers are -4 and 4.  Note that a number does not need to be a perfect square to be non-square-free; for example 8 is not a perfect square, but, since 4 divides 8, -8 and 8 are the next smallest non-square-free integers.

## 3. Quadratic rational fields

These classes mentioned below are derived from class *_QFrac* in module *_quadratic* in the *utilities* package.  Class *_QFrac* uses the above-mentioned *is_square_free* method to check the discriminant.

## 3.1 Imaginary quadratic field (D<0)

There are five negative values which yield number fields which are Euclidean domains:

* -1, -2, -3, -7, and -11

The integral domains ℤ\[√-1\], ℤ\[(1+√-3)/2\], and ℤ\[(1+√-7)/2\] are known respectively as the Gaussian, the Eisensteinian, and the Kleinian integers.

* ℚ(√-1) -- the Gaussian rational numbers -- module *gauss_frac* in the *utilities* folder.  The Gaussian integers ℤ\[√-1\] are a Euclidean domain consisting of the Gaussian rationals with denominator 1.
* ℚ(√-2) -- the root -2 rational numbers -- module *rootm2_frac* in the *utilities* folder.  Its quadratic integer ring ℤ\[√-2\] is a Euclidean domain consisting of the field elements with denominator 1.
*  ℚ(√-3) -- the root -3 or Eisenstein rational numbers -- module *eisenstein_frac* in the *utilities* folder.  Its subring ℤ\[√-3\] is not a Euclidean domain.  If instead of √-3, we take ω=(1+√-3)/2 as a generator, we obtain a quadratic integer ring ℤ\[ω\] which is a Euclidean domain consisting of the field elements of the form a+bω where a and b are ordinary integers.

## 3.2 Real quadratic fields (D>0)

There are sixteen positive values which yield number fields which are Euclidean domains:

* 2, 3, 5, 6, 7, 11, 13, 17, 19, 21, 29, 33, 37, 41, 57, and 73

The integral domain ℤ\[(1+√5)/2\] is referred to as the set of golden integers.

* ℚ(√2) -- the root 2 rational numbers.  I am calling them the Brounckerian rationals after William Brouncker (1620-1684), but the name is not standard. They are found in module *brouncker_frac* in the *utilities* folder.  The quadratic integer ring ℤ\[√2\] is a Euclidean domain consisting of the field elements with denominator 1.
* ℚ(√5) -- the golden rational numbers, named after the "golden" ratio, *i.e.* (1+√5)/2, typically abbreviated as φ (a variant form of the Greek lower case letter phi).  (In Euclid's *Elements*, this ratio is referred to as the mean-extreme ratio.)  Module *golden_frac* in the *utilities* folder is my implementation.  Its subring ℤ\[√5\] is not a Euclidean domain.  If instead of √5, we take φ=(1+√5)/2 as a generator, we obtain a quadratic integer ring ℤ\[φ\] which is a Euclidean domain consisting of the field elements of the form a+bφ where a and b are ordinary integers.  If the units of the integral domain are written in the form a+bφ, the values of a and b are consecutive Fibonacci numbers.

# 4. Inequalities and comtinued fractions

The *inequalities* module is intended for working with *real* quadratic rational numbers, *i.e.* any number which can be found as the root of some quadratic equation with integer coefficients.  This includes integers like 0, 1 or -1728, rational fractions such as 1/2, -42/5 or 355/113, and quadratic surds such as √2, (1+√5)/2 (traditionally known the mean-extreme ratio, now commonly known as the golden ratio) or its complement (1-√5)/2.  It culminates in a class *ContinuedFraction* which expresses real quadratic surds as continued fractions and finds best rational estimates.

See the test module *tests.inequalities* for some applications.  The messages folder contains a test run (*test_inequalities.txt*) with some explanation and some clues for finding help or background material.
