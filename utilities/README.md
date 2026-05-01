# Mathematics - utilities

Some say that mathematics is the queen of the sciences, and some call it the handmaiden of the sciences.  What is your take on this?

Is mathematics discovered or is it invented?

## Contents

**1. Primes**  
**2. Primality**  
**3. Quadratic rational fields**  
**4. Inequalities and continued fractions**  
**5. The cyclic rings ℤₙ**  
**6. Symmetric Groups**  

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

# 5. The cyclic rings ℤₙ

The module *utilities.modn* provides basic tools for playing with finite cyclic groups and rings.  The companion module *utilities.modlog* defines discrete logarithms on the groups of units on these rings.

The test file *tests.test1_modn* was used to help verify that the implementation is sound.  It can also serve as a programming guide or *how-to*.

A demonstration module *demos.modn_addition* produces operation tables.  Several demonstrations are included in the documentation file *doc/cyclic_rings.md*.

# 6. Symmetric Groups

Let *X* be a set, which we'll refer to an *alphabet*.  The elements are its *letters*.  A permutation of *X* is the set of bijections (1-1 and onto functions) from *X* into *X*.  If we consider a total ordering *O* of *X*, a permutation f acts on the ordering by creating another ordering *O'* in which each entry *x* in *O* is replaced by f(*x*) in *P*.  For example, Let $X$ be the set of digits {1,2,3}, *O* the ordering (1,2,3), and the permutation f which maps {(1,3), (2,2), (3,1)}.  Then *P*=f(*O*)=(3,2,1).

For a finite set *X*, given an ordering *O* we can count the number of "errors" in a permutation f by counting the total number of successors of each entry of f(*O*) which are predecessors in *O*.  For example, for f as above:
```
        O = 123                f(O) = 321

            3       3>2, 3>1            (2)
            2       2>1                 (1)
            1        ---                (0)
        Total       3 "errors"
```
The number of "errors" will depend on the choice of ordering *O*, but the parity (whether $n$ is even or odd) is independent of the ordering.

The number of permutations of a set grows rapidly with the number of elements in a set.  One can easily store all the permutations of a 4-set or 5-set in computer memory -- for a 10-set, there are 3,628,800 distinct permutations, for a 20-set, the number exceeds 2×10¹⁸...  A symmetric group on a set with *n* elements has *n*! permutations:

<table align="center">
<thead>
  <tr>
    <th style="border-bottom: 2px solid black; padding: 8px;" align="center">
      <i>X</i>
    </th>
    <th style="border-bottom: 2px solid black; padding: 8px;" align="center">
      |<i>X</i>|=<i>n
    </th>
    <th style="border-bottom: 2px solid black; padding: 8px;" align="center">
      |S(<i>X</i>)|=<i>n</i>!
    </th>
  </tr>
</thead>
<tdata>
  <tr>
    <td align="center">∅</th>
    <td align="center">0</td>
    <td align="center">1</td>
  </tr>
  <tr>
    <td align="center">{0}</th>
    <td align="center">1</td>
    <td align="center">1</td>
  </tr>
  <tr>
    <td align="center">{0,1}</th>
    <td align="center">2</td>
    <td align="center">2</td>
  </tr>
  <tr>
    <td align="center">{0,1,2}</th>
    <td align="center">3</td>
    <td align="center">6</td>
  </tr>
  <tr>
    <td align="center">{0,1,2,3}</th>
    <td align="center">4</td>
    <td align="center">24</td>
  </tr>
  <tr>
    <td align="center">{0,1,2,3,4}</th>
    <td align="center">5</td>
    <td align="center">120</td>
  </tr>
  <tr>
    <td align="center">{0,1,2,3,4,5}</th>
    <td align="center">6</td>
    <td align="center">720</td>
  </tr>
</tdata>
</table>
<center>
  <b>Table 6.1.</b> Sizes of symmetric groups
</center>

For programming information and examples, see the test script and the documentation.  Here are tables for the permutation group S₃:
```
                        S₃ = S({0,1,2})

    Six permutations:
        I(012)=012      R₁(012)=120     R₂(012)=201
        T₀(012)=021     T₁(012)=210     T₂(012)=102

    Legend: I=identity; R-rotation; T-interchange.
        The subscript n in Tₙ indicates the fixed element.

   Inverses
	 I  R₁ R₂ T₀ T₁ T₂
	═══════════════════
	 I  R₂ R₁ T₀ T₁ T₂

   Composition:
	 *  ║ I  R₁ R₂ T₀ T₁ T₂
	════╬═══════════════════
	 I  ║ I  R₁ R₂ T₀ T₁ T₂        (f*g)(x) = f(g(x))
	 R₁ ║ R₁ R₂ I  T₂ T₀ T₁
	 R₂ ║ R₂ I  R₁ T₁ T₂ T₀
	 T₀ ║ T₀ T₁ T₂ I  R₁ R₂
	 T₁ ║ T₁ T₂ T₀ R₂ I  R₁
	 T₂ ║ T₂ T₀ T₁ R₁ R₂ I 
```

And here are tables for S₄, the permutation group on four "letters":
```
                    S₄ = S({0,1,2,3})

    Twenty-four permutations (the names are not standard):
        I(0123)=0123    H₃(0123)=0132   G₂(0123)=0213
        C₁(0123)=0231   C₂(0123)=0312   G₃(0123)=0321

        F₁(0123)=1023   P₁(0123)=1032   C₃(0123)=1203
        R₁(0123)=1230   D₁(0123)=1302   C₄(0123)=1320

        C₅(0123)=2013   D₂(0123)=2031   F₂(0123)=2103
        C₆(0123)=2130   R₂(0123)=2301   D₃(0123)=2310

        R₃(0123)=3012   C₇(0123)=3021   C₈(0123)=3102
        F₃(0123)=3120   D₄(0123)=3201   P₃(0123)=3210

    Legend: I - identity; FGH - simple swaps, C - 3-cycles;
            R-rotations; D - 4-cycles (except rotations);
            P - disjoint products of interchanges (except R₂).

           1 identity element (I)
           6 2-cycles (F, G, H)
           3 products of disjoint 2-cycles (P and R₂)
           8 3-cycles (C)
           6 4-cycles (D and R₁, R₃)
         ━━━━
          24 permutations

                Inverses:
I  H₃ G₂ C₁ C₂ G₃ F₁ P₁ C₃ R₁ D₁ C₄ C₅ D₂ F₂ C₆ R₂ D₃ R₃ C₇ C₈ F₃ D₄ P₃
═══════════════════════════════════════════════════════════════════════
I  H₃ G₂ C₂ C₁ G₃ F₁ P₁ C₅ R₃ D₂ C₇ C₃ D₁ F₂ C₈ R₂ D₄ R₁ C₄ C₆ F₃ D₃ P₃

                Composition:
* ║ I  H₃ G₂ C₁ C₂ G₃ F₁ P₁ C₃ R₁ D₁ C₄ C₅ D₂ F₂ C₆ R₂ D₃ R₃ C₇ C₈ F₃ D₄ P₃
══╬════════════════════════════════════════════════════════════════════════
I ║ I  H₃ G₂ C₁ C₂ G₃ F₁ P₁ C₃ R₁ D₁ C₄ C₅ D₂ F₂ C₆ R₂ D₃ R₃ C₇ C₈ F₃ D₄ P₃
H₃║ H₃ I  C₂ G₃ G₂ C₁ P₁ F₁ D₁ C₄ C₃ R₁ R₃ C₇ C₈ F₃ D₄ P₃ C₅ D₂ F₂ C₆ R₂ D₃
G₂║ G₂ C₁ I  H₃ G₃ C₂ C₅ D₂ F₂ C₆ R₂ D₃ F₁ P₁ C₃ R₁ D₁ C₄ C₇ R₃ D₄ P₃ C₈ F₃
C₁║ C₁ G₂ G₃ C₂ I  H₃ D₂ C₅ R₂ D₃ F₂ C₆ C₇ R₃ D₄ P₃ C₈ F₃ F₁ P₁ C₃ R₁ D₁ C₄
C₂║ C₂ G₃ H₃ I  C₁ G₂ R₃ C₇ C₈ F₃ D₄ P₃ P₁ F₁ D₁ C₄ C₃ R₁ D₂ C₅ R₂ D₃ F₂ C₆
G₃║ G₃ C₂ C₁ G₂ H₃ I  C₇ R₃ D₄ P₃ C₈ F₃ D₂ C₅ R₂ D₃ F₂ C₆ P₁ F₁ D₁ C₄ C₃ R₁
F₁║ F₁ P₁ C₃ R₁ D₁ C₄ I  H₃ G₂ C₁ C₂ G₃ F₂ C₆ C₅ D₂ D₃ R₂ C₈ F₃ R₃ C₇ P₃ D₄
P₁║ P₁ F₁ D₁ C₄ C₃ R₁ H₃ I  C₂ G₃ G₂ C₁ C₈ F₃ R₃ C₇ P₃ D₄ F₂ C₆ C₅ D₂ D₃ R₂
C₃║ C₃ R₁ F₁ P₁ C₄ D₁ F₂ C₆ C₅ D₂ D₃ R₂ I  H₃ G₂ C₁ C₂ G₃ F₃ C₈ P₃ D₄ R₃ C₇
R₁║ R₁ C₃ C₄ D₁ F₁ P₁ C₆ F₂ D₃ R₂ C₅ D₂ F₃ C₈ P₃ D₄ R₃ C₇ I  H₃ G₂ C₁ C₂ G₃
D₁║ D₁ C₄ P₁ F₁ R₁ C₃ C₈ F₃ R₃ C₇ P₃ D₄ H₃ I  C₂ G₃ G₂ C₁ C₆ F₂ D₃ R₂ C₅ D₂
C₄║ C₄ D₁ R₁ C₃ P₁ F₁ F₃ C₈ P₃ D₄ R₃ C₇ C₆ F₂ D₃ R₂ C₅ D₂ H₃ I  C₂ G₃ G₂ C₁
C₅║ C₅ D₂ F₂ C₆ R₂ D₃ G₂ C₁ I  H₃ G₃ C₂ C₃ R₁ F₁ P₁ C₄ D₁ D₄ P₃ C₇ R₃ F₃ C₈
D₂║ D₂ C₅ R₂ D₃ F₂ C₆ C₁ G₂ G₃ C₂ I  H₃ D₄ P₃ C₇ R₃ F₃ C₈ C₃ R₁ F₁ P₁ C₄ D₁
F₂║ F₂ C₆ C₅ D₂ D₃ R₂ C₃ R₁ F₁ P₁ C₄ D₁ G₂ C₁ I  H₃ G₃ C₂ P₃ D₄ F₃ C₈ C₇ R₃
C₆║ C₆ F₂ D₃ R₂ C₅ D₂ R₁ C₃ C₄ D₁ F₁ P₁ P₃ D₄ F₃ C₈ C₇ R₃ G₂ C₁ I  H₃ G₃ C₂
R₂║ R₂ D₃ D₂ C₅ C₆ F₂ D₄ P₃ C₇ R₃ F₃ C₈ C₁ G₂ G₃ C₂ I  H₃ R₁ C₃ C₄ D₁ F₁ P₁
D₃║ D₃ R₂ C₆ F₂ D₂ C₅ P₃ D₄ F₃ C₈ C₇ R₃ R₁ C₃ C₄ D₁ F₁ P₁ C₁ G₂ G₃ C₂ I  H₃
R₃║ R₃ C₇ C₈ F₃ D₄ P₃ C₂ G₃ H₃ I  C₁ G₂ D₁ C₄ P₁ F₁ R₁ C₃ R₂ D₃ D₂ C₅ C₆ F₂
C₇║ C₇ R₃ D₄ P₃ C₈ F₃ G₃ C₂ C₁ G₂ H₃ I  R₂ D₃ D₂ C₅ C₆ F₂ D₁ C₄ P₁ F₁ R₁ C₃
C₈║ C₈ F₃ R₃ C₇ P₃ D₄ D₁ C₄ P₁ F₁ R₁ C₃ C₂ G₃ H₃ I  C₁ G₂ D₃ R₂ C₆ F₂ D₂ C₅
F₃║ F₃ C₈ P₃ D₄ R₃ C₇ C₄ D₁ R₁ C₃ P₁ F₁ D₃ R₂ C₆ F₂ D₂ C₅ C₂ G₃ H₃ I  C₁ G₂
D₄║ D₄ P₃ C₇ R₃ F₃ C₈ R₂ D₃ D₂ C₅ C₆ F₂ G₃ C₂ C₁ G₂ H₃ I  C₄ D₁ R₁ C₃ P₁ F₁
P₃║ P₃ D₄ F₃ C₈ C₇ R₃ D₃ R₂ C₆ F₂ D₂ C₅ C₄ D₁ R₁ C₃ P₁ F₁ G₃ C₂ C₁ G₂ H₃ I
```

(The tables were extracted from the testing results.)
