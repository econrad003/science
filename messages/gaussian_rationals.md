# Facts about ℚ(i) and ℤ[i]

Contents

1. The Gaussian rational numbers
2. The units
3. The Argand plane
4. Norms
5. Pythagorean triples
6. Gaussian integers
7. The division algorithm
8. Gaussian primes
9. The Euclidean (GCD) algorithm and continued fractions

## 1. The Gaussian rational numbers

The Gaussian rational numbers ℚ(i) consist of complex numbers whose real and imaginary parts are both rational.  For example:
```
        z = (-39-30i)/46
```
The real part is Re(z)=-39/46 and its imaginary part Im(z)=-15/23. We write these in a normal form (a+bi)/c where a, b and c are integers, c is positive, and the greatest common divisor of a, b, and c is 1:
```
       gcd(39,30,46) = 1
```
The components are the real part and the imaginary part:
```
       Re z = -39/46
       Im z = -30/46 = -15/23
```
The absolute value of a Gaussian rational is the same as the complex absolute value, *i.e.* the square root of the sum of the squares of the components.  To avoid square roots, we usually use the square norm which is the square of the complex absolute value:
```
       N(z) = 2421/2116
       |z| = 1.069644747838482 (approximately)
``` 

## 2. The units

There are four Gaussian rational numbers with absolute value 1, namely the ordinary integers 1 and -1, and the pure imaginary numbers i and -i.

The number i is one of two square roots of -1.  If we draw two perpendicular number lines, one horizontal with integers increasing from left to right and the other vertical with integers increasing from bottom to top, then 0 is (0,0), 1 is (1,0), and i is (0,1). The coordinate system is right-handed, so the first coordinate is horizontal, the second vertical.  The other square root of -1 is -i, located at (0,-1).

## 3. The Argand plane

We consider only the rational points in our coordinate system. If the first coordinate is x and the second y, then the point (x,y) is the location of z=x+iy.  This respresentation of complex numbers as points in a Cartesian plane is known as the Argand plane.

Our sample point z=(-39-30)/46 is located in the third quadrant, 39/46 units to the left and 30/46 (or 15/23) units down from the origin.

## 4. Norms

The complex norm or absolute value is somewhat inconvenient as square roots may be required, so we normally square the norm:
```
       z = (-39-30)/46
       N(z) = (Re z)² + (Im z)² = (-39/46)² + (-30/46)² = 2421/2116
       |z| = √N(z) ≈ 1.069644747838482
```
The square norm N(z) (python `z.sqnorm`) is an exact value, but the calculated absolute value (or norm) given here is an approximation (unless N(z) is a perfect square).

The both the complex norm and the square norm are multiplicative:
```
       N(wz) = N(w) · N(z)
       |wz| = |w| · |z|
```

The square norm is the componentwise dot product of a number with its complex conjugate:
```
       N(a+bi) = (a+bi)(a-bi) = aa - bibi = a² + b²
```
Note that it is always non-negative.  It is zero if and only if a=b=0.

## 5. Pythagorean triples

Rational Pythagorean triples occur when the square norm N(z) is a perfect square.  For example consider the following fact:
```
       5² + 12² = 169  and √169 = 13
```
Let z=5+12i.  Then |z|=13 (exactly).  So (5,12,13) is an example of a Pythagorean triple.  We can obtain more triples from this one in a number of ways.  Three trivial ways are as follows:
<ol type='a'>
   <li>change the sign of some of the entries; or</li>
   <li>interchange some of the entries; or</li>
   <li>multiply the numbers by the same rational number.</li>
</ol>

But (5,12,13) is special in ways that others obtained in either way are not:
<ol type='i'>
   <li>5, 12, and 13 are all integers;</li>
   <li>5 ≤ 12 ≤ 13;</li>
   <li>5, 12, and 13 are all positive; and</li>
   <li>gcd(5, 12, 13) = 1.</li>
</ol>

A Pythagorean triple which satisfies all four conditions ((i) integers, (ii) increasing, (iii) positive, (iv) relatively prime) is primitive. If the one or all of the entries are zero, then the triple is trivial.  So:
<ol type='a'>
   <li>(3,4,5), (5,12,13) and (8,15,17) are primitive;</li>
   <li>(0, 0, 0), (1,0,1) and (0, -17, 0) are trivial;</li>
   <li>(15, 8, 17) is not primitive (interchange);</li>
   <li>(-5, 8, 13) is not primitive (sign);</li>
   <li>(6, 8, 10) is not primitive (gcd); and</li>
   <li>(3, 4, 6) is not a Pythagorean triple (3²+4²=25≠6²)</li>
</ol>

If we divide by the third number, something interesting happens:
```
       (5, 12, 13) -> (5/13, 12/13, 1)
       z = (5+12i)/13
        N(z) = (5/13)² + (12/13)² = 1
```

The square norm and the norm are both equal to 1.  Basically we have projected the Pythagorean triple onto the unit circle about the origin.

### Historical note

Pythagorean triples have been known since ancient times.  Our first evidence for them comes from cuneiform tablets in Mesopotamia dating to about 1850 BCE, or about 1200 to 1300 years before Pythagoras.  We know that some Babylonian scribes knew some way of constructing them, but we don't know the actual procedure that they used, or how complete it was.  The first known complete algorithm for finding primitive Pythagorean triples is found in Euclid's Elements and is usually dated to about 300 BCE, or about 1500 years after they were encountered in Babylonian records, and about 200 years after Pythagoras.

## 6. Gaussian integers

If we restrict ourselves to Gaussian fractions with denominator 1, our domain is the set ℤ[i] of Gaussian integers.  Although the Gaussian integers are not ordered, they do share many properties with the ordinary integers.  Among others are the facts that they contain a subset of prime numbers and that there is a unique factorization theorem.

### 6.1 Division algorithm

In the "natural numbers", the positive integers and zero, there is a well-defined division operation (apart from dividing by zero) which satisfies the following theorem:

#### Division Algorithm for ℕ:

<blockquote>For every natural number a and every positive integer b, there are unique natural numbers q and r such that:
<ol type='i'>
    <li>a = qb + r; and</li>
    <li>0 ≤ r < b.</li>
</ol>
</blockquote>

The given numbers a and b are known as the *dividend* and the *divisor*. The derived numbers q and r are known as the *quotient* and the *remainder*. To generalize this to the integers, we need the notion of absolute value.  Once we have it, it is easy to generalize:

#### Division Algorithm for ℤ:

<blockquote>For every integer a and every nonzero integer b, there are unique integers q and r such that:
<ol type='i'>
    <li>a = qb + r; and</li>
    <li>0 ≤ r < |b|.</li>
</ol>
</blockquote>

Note that very little wording has changed.  The big change was enclosing the divisor in absolute value bars in point (ii).  Other that, we just changed the domain.  This is called floor division:

| quadrant |   a |  b | condition (i)     | condition (ii)   |  q | r |
| -------: | --: | -: | ----------------- | ---------------- | -: | - |
|        I |  24 |  5 | 24 = 4 × 5 + 4    | 0 ≤ 4 < \|5\|    |  4 | 4 |
|       II | -24 |  5 | -24 = -5 × 5 + 1  | 0 ≤ 1 < \|5\|    | -5 | 1 |
|      III | -24 | -5 | -24 = 5 × -5 + 1  | 0 ≤ 1 < \|-5\|   |  5 | 1 |
|       IV |  24 | -5 | 24 = -4 × -5 + 4  | 0 ≤ 4 < \|-5\|   | -4 | 4 |

Note that the quotient in this particular division is not symmetric with respect to arithmetic sign:
```
         24/5 = -24/-5 = 4.8
        -24/5 = 24/-5 = -4.8
```
The quotient in both cases is the *floor* of (or *greatest integer* in) the rational quotient.  We can make the quotient symmetric by changing the requirements for the remainder:

#### Symmetric Division Algorithm for ℤ:

<blockquote>For every integer a and every nonzero integer b, there are unique integers q and r such that:
<ol type='i'>
    <li>a = qb + r;</li>
    <li>0 ≤ |r| < |b|; and</li>
    <li>if r ≠ 0, then sgn(r) = sgn(a).</li>
</ol>
</blockquote>

Condition (ii) on the remainder make sure that, if there is a remainder, then its sign is the same as the sign of the dividend.

| quadrant |   a |  b | condition (i)     | condition (ii)      |  q |  r |
| -------: | --: | -: | ----------------- | ------------------- | -: | -: |
|        I |  24 |  5 | 24 = 4 × 5 + 4    | 0 ≤ \|4\| < \|5\|   |  4 |  4 |
|       II | -24 |  5 | -24 = -4 × 5 - 4  | 0 ≤ \|-4\| < \|5\|  | -4 | -4 |
|      III | -24 | -5 | -24 = 4 × -5 - 4  | 0 ≤ \|-4\| < \|-5\| |  4 | -4 |
|       IV |  24 | -5 | 24 = -4 × -5 + 4  | 0 ≤ \|4\| < \|-5\|  | -4 |  4 |

## 7. Division algorithm for the Gaussian integers

The Gaussian integers also have a division algorithm.  We can make it unique, but it is easier to state the conditions if we don't worry about uniqueness.

#### Division Algorithm for ℤ[i]:

<blockquote>For every Gaussian integer a and every nonzero Gaussian integer b, there are Gaussian integers q and r such that:
<ol type='i'>
    <li>a = qb + r; and</li>
    <li>0 ≤ |r| < |b|.</li>
</ol>
</blockquote>

Since the square norm is never negative, the second condition is equivalent to:
```
     N(r) < N(b).
```

Note that the conditions are the same as the first two conditions given for symmetric quotients.  This gives us four candidates for the quotient-remainder ordered pair.  Additional conditions can be used to fix the choice.  Now an example.

```
     Let a = 231+2040i and b = -2+3i.  One possibility:
         q = 435-367i and r = i.
     Does this meet the requirements?
         bq + r = 231+2040i
         1 = N(r); N(b) = 13
```
Since a=bq+r and N(r) < N(b), the requirements have been met.

## 8. Gaussian primes

Positive prime integers are Gaussian primes if and only if they are congruent to 3 modulo 4.  So 3, 7 and 11 are Gaussian but 2, 5 and 13 are not.  Let's try dividing each of those ordinary primes by Gaussian integers to get the divisors of each.  We can stay in the first quadrant...  The integer-valued function d is the number of Gaussian integers which divide the given Gaussian integer.  Each Gaussian integer in the given set has an associate in another quadrant.

To get the remaining divisors, multiply by i, -1, and -i, as we did in the results below for the divisors of 2.  Since there are 4 units (1, -1, i, -i), any number with 8 divisors is irreducible, and irreducibles (other than the units) in the Gaussian integers are also prime.

#### Divisors of 2 in the first quadrant

{1, 2, 1+i}  
d(2)=12

Multiply by i to get divisors in quadrant II: {i, 2i, i-1}.  
Multiply by -1 to get divisors in quadrant III: {-1, -2, -1-i}.  
Multiply by -i to get divisors in quadrant IV: {-i, -2i, 1-i}.

#### Divisors of 3 in the first quadrant

{1, 3}  
d(3)=8  
3 is a Gaussian prime.

#### Divisors of 5 in the first quadrant

{1, 1+2i, 2+i, 5}  
d(5)=16

#### Divisors of 7 in the first quadrant

{1, 7}  
d(7)=8
7 is a Gaussian prime.

#### Divisors of 11 in the first quadrant

{1, 11}  
d(11)=8  
11 is a Gaussian prime.

#### Divisors of 13 in the first quadrant

{1, 13, 2+3i, 3+2i}  
d(13)=16

To see (for example) that 2+3i is a divisor of 13, multiply by the conjugate:
```
       (2+3i) × (2-3i) = 13
```

## 9. The Euclidean algorithm

The Gaussian integers have a greatest common denominator algorithm. In honor of Euclid, the basic algorithm is known as the Euclidean algorithm.  It does not involve any actual factoring -- it is just a sequence of repeated divisions.

### How it works...

Let's see how it works by finding the gcd of 4180 and 177905:

|      a |      b |      q |      r | to proceed       |
| -----: | -----: | -----: | -----: | :--------------- |
| 177905 |   4180 |     42 |   2345 | b ⊢ a; r ⊢ b     |
|   4180 |   2345 |      1 |   1835 |                  |
|   2345 |   1835 |      1 |    510 |                  |
|   1835 |    510 |      3 |    305 |                  |
|    510 |    305 |      1 |    205 |                  |
|    305 |    205 |      1 |    100 |                  |
|    205 |    100 |      2 |      5 |                  |
|    100 |      5 |     20 |      0 | r = 0 ⇒ b ⊢ gcd  |

Then gcd(177905, 4180) = 5.

The maximum number of steps is aproximately the logarithm to the base (1+√5)/2 of the larger number.  This particular logarithm of 177905 is about 25.122, so we expect no more than 25 or 26 steps.  The actual number of steps was 8.

Now, using the sequence of quotients, we write the following continued fraction:
```
            1
       42 + --------------------------
                1
            1 + ----------------------
                    1
                1 + ------------------
                        1
                    3 + --------------
                            1
                        1 + ----------
                                1
                            1 + ------
                                    1
                                2 + --
                                    20
```

The numerators are all 1.  The term before each plus sign is a quotient.  For a shorthand, we write this as an augmented row vector:
```
       [42; 1 1 3 1 1 2 20]
```
Now let's recover the input:

|       q |        A |     B | ratio (approx)     |
| ------: | -------: | ----: | :----------------- |
|         |        0 |     1 |                    |
|         |        1 |     0 |                    |
|      42 |       42 |     1 |  42                |
|       1 |       43 |     1 |  43                |
|       1 |       85 |     2 |  42.5              |
|       3 |      298 |     7 |  42.57142857142857 |
|       1 |      383 |     9 |  42.55555555555556 |
|       1 |      681 |    16 |  42.5625           |
|       2 |     1745 |    41 |  42.5609756097561  |
|      20 |    35581 |   836 |  42.561004784689   |

If we multiply 35581 and 836 by the 5, we get 177905 and 4180. Those were our starting numbers and 5 was their GCD. The last column is a series of successive decimal estimates of 35581/836, or equivalently of 177905/4180.  We can read off the actual rational estimates from the middle two columns:
```
       42, 43, 85/2, 298/7, 383/9, 681/16, 174/41, 35581/836
```
A modification of this algorithm allows up to estimate irrational numbers using a continued fraction, or equivalently, an infinite sequence of rational numbers.  ("Allows" is not literally true. There are a additional considerations related to computability.  These considerations are well beyond the scope of this introduction.)

### It also works with the Gaussian integers!

Now let us try it with Gaussian integers.  We will start by building two Gaussian integers.  The units are 1, -1, i, and -i. The unit are 1, -1, i, and -i.  Multiplying by a unit does not change the GCD.
```
       a = (1+i)(2+3i)(7+5i)(-13+11i)(-23+19i) = 12120+18700i
       N(a) = 496584400
       b = (i)(1+i)(-3+5i)(7+11i)(-7+13i) = 496+1508i
       N(b) = 2520080
       gcd(N(a), N(b)) = 80
```

|       a       |     b      |    q     |     r      |    N(b) |   N(r) |
| :-----------: | :--------: | :------: | :--------: | ------: | -----: |
| 12120+18700i  | 496+1508i  |  14-4i   | -856-428i  | 2520080 | 915920 |
| 496+1508i     | -856-428i  |   -1-i   |  68+224i   |  915920 |  54800 |
|   -856-428i   |  68+224i   |  -3+3i   |   20+40i   |   54800 |   2000 |
|     68+224i   |  20+40i    |  5+i     |  8+4i      |    2000 |     80 |
|      20+40i   |   8+4i     |  4+3i    |     0      |      80 |      0 |

In each row, a=qb+r and N(b)>N(r), so minimum requirements for Gaussian integer division have been met.

From the last row of the table, the GCD of 12120+18700i and 496+1508i is 8+4i. (This is valid up to multiplication by a unit.  Using other restrictions on the remainders, we might end up with 8-4i, -8-4i or -8+4i.) Dividing by the GCD:
```
       (12120+18700i) / (8+4i) = 2147+1264i
       (496+1508i) / (8+4i) = 125+126i
```
Also note that:
```
       (12120+18700i) / (496+1508i)
                 = (2147+1264i) / (125+126i)
                 = (427639-112522i)/31501
                 ≈ 13.5754-3.5720i
```
Let's work out the continued fraction convergents from the quotient column.

|         q |     A       |    B      | error    |
| :-------: | :---------: | :-------: | :------- |
|           |      0      |    1      |          |
|           |      1      |    0      |          |
|   14-4i   |   14-4i     |    1      | 0.602867 |
|    -1-i   | -17-10i     |  -1-i     | 0.104272 |
|   -3+3i   |  95-25i     |     7     | 0.004024 |
|     5+i   | 483-40i     | 34+6i     | 0.000163 |
|    4+3i   | 2147+1264i  | 125+126i  | 0        |

The values in the columns A and B are obtained as follows:
```
        A[n] = q[n] A[n-1] + A[n-2]
        B[n] = q[n] B[n-1] + B[n-2]
```
The bracketed number indicates the row.

The values in the error columns are the complex absolute value of the difference between the result and the estimate A[n]/B[n].  Note that these errors decrease to zero (exact).

