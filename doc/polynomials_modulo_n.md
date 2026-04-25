# Polynomials Modulo *n*

## Contents

**1. Introduction**  
    1.1 Clock arithmetic (ℤ/12)  
    1.2 Prime moduli  
    1.3 Polynomials  
**2. The PolyMod module**  

## 1. Introduction

You may want to skip ahead to section 2.  Just scan this quickly and return to it later as needed.

### 1.1 Clock arithmetic

One of the everyday uses of modular arithmetic is the enumeration of hours on a 12-hour clock.  3 hours after 11 o'clock is 2 o'clock:
```
        >>> (11 + 3) % 12
        2
```

Mathematicians normally think of 12 o'clock as 0, but that's just a label.
```
        >>> (11 + 1) % 12
        0
```


Clock arithmetic has a type of structure which mathematicians call a "ring".  The clock arithmetic ring has a special name, "integers modulo 12", or "ℤ modulo 12" usually written either as "ℤ/12ℤ" or "ℤ₁₂" or "ℤ/12".  The double-struck capital Z ("ℤ") has become a standard symbol for the integers.  Double-strike fonts are called "blackboard bold" as they were first used on chalkboards to represent bold letters.  Here, the slash is read as "mod" (short for "modulo").


Let's use Python briefly investigate the ring ℤ/12...
```
    >>> from utilities.modn import make_Zn
    >>> R = make_Zn(12)
    R.__name__
    'ℤ/12'
```

ℤ/12 has twelve elements, labelled 0 through 11:
```
    >>> for i in range(2):
    ...     print(["  n ", "R(n)"][i], end="")
    ...     for j in range(24):
    ...         print(f"{[j,R(j)][i]:3}", end="")
    ...     print()
    ...
      n   0  1  2  3  4  5  6  7  8  9 10 11
    R(n)  0  1  2  3  4  5  6  7  8  9 10 11

      n  12 13 14 15 16 17 18 19 20 21 22 23
    R(n)  0  1  2  3  4  5  6  7  8  9 10 11
```
The label 0 in ℤ/12 is shorthand for an infinite set of integers, namely the set of multiples of 12:
```
        [0] = {..., -24, -12, 0, 12, 24, ...}
```
The other labels, 0 through 11, are the smalles positive remainders after division by 12.  For example the label 3 represents all integers which, when divided by 3 have a smallest positive remainder of 3:
```
        [3] = {..., -21, -9, 3, 15, 27, ...}
```
The word "division" is used here to indicate an inverse of multiplication.  It is tied to an important theorem about the integers which goes back to a section on number theory in Euclid's *Elements* (c. 300 BCE).  The theorem is usually called "The Division Algorithm", or rarely but more accurately as "The Division Lemma".  (The algorithm is implied in the proof of the lemma.)

**Division Algorithm for ℤ**
```
    For all integers a and b, if b is not equal to zero, then there are unique integers q and r such that:
        i)   a = qb+r; and
        ii)  0 ≤ r < |b|.
```
The numbers a, b, q, and r are the dividend, the divisor, the quotient, and the remainder.  Item (i) says simply that division, the operation of finding a quotient and a remainder is an inverse of multiplication -- we can recover the dividend from the divisor, the quotient, and the remainder.  Item (ii) is what makes this division unique -- a strong restriction on the remainder.  The preferred remainder is smaller in absolute value than the divisor, and never negative.  There are other ways to make the quotient and remainder unique, but this is the standard way, and it is also how integer division in implemented in Python.

Let's create an addition table:
```
    >>>for i in range(12):
    ...     print(list(R(i)+R(j) for j in range(12)))

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2]
    [4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3]
    [5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4]
    [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]
    [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]
    [8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7]
    [9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    [10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```
Now let's edit that to make it look nice and pretty:
```
     +    0  1  2  3  4  5  6  7  8  9 10 11
    ━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     0 ┃  0  1  2  3  4  5  6  7  8  9 10 11
     1 ┃  1  2  3  4  5  6  7  8  9 10 11  0
     2 ┃  2  3  4  5  6  7  8  9 10 11  0  1
     3 ┃  3  4  5  6  7  8  9 10 11  0  1  2
     4 ┃  4  5  6  7  8  9 10 11  0  1  2  3
     5 ┃  5  6  7  8  9 10 11  0  1  2  3  4
     6 ┃  6  7  8  9 10 11  0  1  2  3  4  5
     7 ┃  7  8  9 10 11  0  1  2  3  4  5  6
     8 ┃  8  9 10 11  0  1  2  3  4  5  6  7
     9 ┃  9 10 11  0  1  2  3  4  5  6  7  8
    10 ┃ 10 11  0  1  2  3  4  5  6  7  8  9
    11 ┃ 11  0  1  2  3  4  5  6  7  8  9 10
```
The top row and the leftmost column match the headings.  This property of the table tells us that the element that we named 0 is a two-sided identity for the structure ℤ/12.

Each row and each column contains exactly one copy of each element of ℤ/12.  This characteristic, along with two-sided identities, make this a mathematical structure called a "loop".  In addition, though it isn't obvious from the table, the + operation (addition) on ℤ/12 is associative.  (Associativity follows from associativity of addition in the integers.  A structures with an associative binary operations is called a "monoid".)

A lttle inspection shows that, for each element *x*, there is a unique element *y* such that *x+y*=0=*y+x*.  (Look for the diagonal band of zeros below the diagonal that runs from 11+0 to 0+11.  The band continues through the top left corner.  The element *y* is a two-sided inverse for the element *x*.)  If we have associativity, left identities, and left inverses, we have a structure known as a *group*.  It is not hard to show in any group that the left identity is a two-sided identity, that the left inverses are also right inverses, and that the loop property (that each element appears exactly once in any given row or column) alsp holds.

Finally, note that the entries are symmetric on each side of the main diagonal from 0+0 to 11+11.  This property is commutativity: *x+y*=*y+x* for all elements of the group.  Groups that are commutative are known as "abelian groups" after Niels Abel, a nineteenth century mathematician.

Note here that the main diagonal contains two copies of each of the elements 0, 2, 4, 6, 8, and 10.  The northeast diagonal contains only the element 11.  (In fact, each of the bands parallel to the northeast diagonal is constant.  Uniqueness applies to rows and to columns, not to diagonal bands.

Now let's look at subtraction in ℤ/12, *i.e.* subtraction modulo 12:
```
>>> for i in range(12):
...     print(list(R(i)-R(j) for j in range(12)))
...
     -    0  1  2  3  4  5  6  7  8  9 10 11
    ━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     0 ┃  0 11 10  9  8  7  6  5  4  3  2  1
     1 ┃  1  0 11 10  9  8  7  6  5  4  3  2
     2 ┃  2  1  0 11 10  9  8  7  6  5  4  3
     3 ┃  3  2  1  0 11 10  9  8  7  6  5  4
     4 ┃  4  3  2  1  0 11 10  9  8  7  6  5
     5 ┃  5  4  3  2  1  0 11 10  9  8  7  6
     6 ┃  6  5  4  3  2  1  0 11 10  9  8  7
     7 ┃  7  6  5  4  3  2  1  0 11 10  9  8
     8 ┃  8  7  6  5  4  3  2  1  0 11 10  9
     9 ┃  9  8  7  6  5  4  3  2  1  0 11 10
    10 ┃ 10  9  8  7  6  5  4  3  2  1  0 11
    11 ┃ 11 10  9  8  7  6  5  4  3  2  1  0
```
Subtraction in ℤ/12 is neither commutative nor associative nor commutative.  It does have a right identity (0), but no left identity.  Each element does have a right identity corresponding to the right inverse.  Since we don't have a two-sided identity, subtraction does not give rise to a loop, but do note that rows and columns contain each element exactly once.  The main diagonal is constantly zero.  Bands parallel to the main diagonal are constant.

Next up multiplication modulo 12:
```
    >>> for i in range(12):
    ...     print(list(R(i)*R(j) for j in range(12)))
    ...
     ×    0  1  2  3  4  5  6  7  8  9 10 11
    ━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     0 ┃  0  0  0  0  0  0  0  0  0  0  0  0
     1 ┃  0  1  2  3  4  5  6  7  8  9 10 11   <--
     2 ┃  0  2  4  6  8 10  0  2  4  6  8 10
     3 ┃  0  3  6  9  0  3  6  9  0  3  6  9
     4 ┃  0  4  8  0  4  8  0  4  8  0  4  8
     5 ┃  0  5 10  3  8  1  6 11  4  9  2  7   <--
     6 ┃  0  6  0  6  0  6  0  6  0  6  0  6
     7 ┃  0  7  2  9  4 11  6  1  8  3 10  5   <--
     8 ┃  0  8  4  0  8  4  0  8  4  0  8  4
     9 ┃  0  9  6  3  0  9  6  3  0  9  6  3
    10 ┃  0 10  8  6  4  2  0 10  8  6  4  2
    11 ┃  0 11 10  9  8  7  6  5  4  3  2  1   <--
```
Multiplication by a multiple of 12 always returns a multiple of 12. -- the top row and leftmost column are all zero.  Note that 1 is a two-sided identitity, and multiplication is both associative and commutative.  Note the indicated rows, 1, 5, 7, and 11.  These four labels are the *units* of ℤ/12 -- note that each element of the ring appears exactly once in these four rows.  The same holds for the columns labelled 1, 5, 7, and 11.  That property does not hold in any of the other rows or columns.  Multiplication does not itself define a group on ℤ/12, but, it we restrict multiplication to the units, we do get a group:
```
     ×    1  5  7 11
    ━━━╋━━━━━━━━━━━━
     1 ┃  1  5  7 11
     5 ┃  5  1 11  7
     7 ┃  7 11  1  5
    11 ┃ 11  7  5  1
```
This isn't quite like ordinary multiplication.  Note that the square of each of the units is 1:
```
                a    q  b  + r
    ━━━━━━━━━━━━━━━━━━━━━━━━━━
     1 ×  1 =   1 =  0(12) + 1
     5 ×  5 =  25 =  2(12) + 1
     7 ×  7 =  49 -  4(12) + 1
    11 × 11 = 121 = 10(12) + 1
```
Note also that the multiplication table divides nicely into 2×2 blocks:
```
     ×    1  5    7 11     ×   1  5     ×   1  7     ×    1 11
    ━━━╋━━━━━━━╋━━━━━━    ━━━╋━━━━━    ━━━╋━━━━━    ━━━╋━━━━━━
     1 ┃  1  5 ┃  7 11     1 ┃ 1  5     1 ┃ 1  7     1 ┃  1 11
     5 ┃  5  1 ┃ 11  7     5 ┃ 5  1     7 ┃ 7  1    11 ┃ 11  1
      ━╋━━━━━━━╋━━━━━━
     7 ┃  7 11 ┃  1  5
    11 ┃ 11  7 ┃  5  1
```
Each of the units in ℤ/12 is its own multiplicative inverse.
```
>>> for i in [1, 5, 7, 11]:
    ...     print(f"x={R(i)}, multiplicative inverse: {R(i).inverse}")
    ...
    x=1, multiplicative inverse: 1
    x=5, multiplicative inverse: 5
    x=7, multiplicative inverse: 7
    x=11, multiplicative inverse: 11
```
If we are careful to distinguish between the integer 5 and the mod 12 integer 5, we can think of these inverses as defining fractions:
```
    >>> R(1)/R(5)
    5
```
Putting brackets around integers modulo 12, we could transcribe this as:
```
        [1]/[5] = [5].
```
We can divide any element by any unit, for example:
```
    R(2)/R(5)
    10
```
This is saying that
```
        [2] ÷ [5] = [10],    or as a fraction:
          [2]/[5] = [10].
```
Multiplication by a unit is the same as division by a unit in clock arithmetic.  (It is not necessarily the case in other rings.)  And in the ring of integers, we cannot, in general, divide by 5.  But let's consider two integers whose remainders are two after dividing by 12, and which are also divisible by 5... the smallest positive example is 50, the second smallest is 110:
```
        50 = 4(12) + 2              110 = 9(12) + 2
        50 ÷ 5 = 10                 110 ÷ 5 = 22
                                     22 = 1(12) + 10
```
Strange?  Yes.  But it works.

Now what about the eight elements which are not units.  One of them is zer0.  The others are divisors of zero.  None of these elements has a multiplicative inverse, so there is no good way to define a division operation.  In our implementation:
```
R(5)/R(2)
Traceback (most recent call last):
  File "/home/eric/repositories/science/utilities/modn.py", line 418, in __truediv__
    return self * other.inverse
  File "/home/eric/repositories/science/utilities/modn.py", line 407, in inverse
    self.ord            # calculate the order
  File "/home/eric/repositories/science/utilities/modn.py", line 281, in ord
    return self.__order_of(int(self))
  File "/home/eric/repositories/science/utilities/modn.py", line 265, in __order_of
    raise ZeroDivisionError(f"order_of: {k} is a zero divisor")
ZeroDivisionError: order_of: 2 is a zero divisor
```
As can be seen from the stack trace, \[2\] was *eventually* recognized as a zero divisor and a *ZeroDivisionError* exception was raised.

### 1.2 Prime moduli

When we define rings using addition and multiplication modulo *n*, we generally get several divisors of zero.  These correspond to integers which are not relatively prime to *n*.  If *n* happens to be prime, then the list of nonzero positive integers which are smaller than *n* but *not* relatively prime to *n* is an empty list.  The set of integers which are *not* relatively prime to a prime positive integer *p* is precisely the set of integer multiples of *p*.

As it turns out, if *p* is a positive prime:

1.  the ring ℤ/*p*ℤ is a field, *i.e.*, all nonzero elements have multiplicative inverses.
2.  the nonzero elements form a group under multiplication (the group of units) which is *isomorohic to* (*i.e.* structurally the same as) the additive group of ℤ/(*p-1*)ℤ.

As an example, consider ℤ/5ℤ, the integers modulo 5.
```
    >>> from utilities.modn import make_Zn
    >>> F = make_Zn(5)
    >>> for i in range(1,5):
    ...     print(f"x={F(i)}\tmultiplicative inverse: {F(i).inverse}")
    ...
    x=1	    multiplicative inverse: 1
    x=2	    multiplicative inverse: 3
    x=3	    multiplicative inverse: 2
    x=4	    multiplicative inverse: 4
```
Multiplication in ℤ/5 corresponds to addition in ℤ/4 in two ways:
```
        identity
    ℤ/5     1       2       3       4
            1       3       2       4       multiplicative inverse
    ℤ/4     0       1       3       2
            0       3       1       2       additive inverse
    ℤ/4     0       3       1       2
            0       1       3       2       additive inverse
```
The multiplicative order of an element is the smallest positive power which is 1.  The additive order is the smallest multiple which is 0.  Order must be preserved, so an identity maps to an identity, an order 1 element maps to an order 1 element, order 2 to order 2, *etc.*

The identity is the only order 1 element in either group, and there is only one order 2 element.  So 1 in ℤ/5 maps to 0 in ℤ/4 and 4 in ℤ/5 maps to 2 in ℤ/4.  We have two order 2 elements, and two ways to map them.  Both maps happen to work.  Let's look at the second map:
```
    f(1)=0   f(2)=3   f(3)=1   f(4)=2   <-- isomorphism

     ×    1  2  3  4                     +    0  3  1  2
    ━━━╋━━━━━━━━━━━━                    ━━━╋━━━━━━━━━━━━
     1 ┃  1  2  3  4                     0 ┃  0  3  1  2
     2 ┃  2  4  1  3     --> f -->       3 ┃  3  2  0  1
     3 ┃  3  1  4  2                     1 ┃  1  0  2  3
     4 ┃  4  3  2  1                     2 ┃  2  1  3  0
```
The addition table is shuffled by the isomorphism, but we can rearrange it:
```
                                         +    0  1  2  3
                                        ━━━╋━━━━━━━━━━━━
                                         0 ┃  0  1  2  3
                                         1 ┃  1  2  3  0
                                         2 ┃  2  3  0  1
                                         3 ┃  3  0  1  2
```

### 1.3 Polynomials

Polynomials, or more precisely *univariate polynomials* are a device for turning a finite list of scalars from a structure like a ring or a field and creating a vector.  For example, if our scalars are rational numbers, and we have the triple (1, 4, 3), we can map this triple into the quadratic polynomial:
```
        3x²+4x+1
```
Our convention is to write the triple from lowest order (*i.e.* constant term) to highest order (in this case the degree 2 or quadratic coefficient).  But polynomials are usually displayed leading term (highest order) first, and in displaying them, we follow that convention.

Adding polynomials is a matter of adding coefficients of terms of the same order -- if a term is missing, its coefficient is zero:
```
            f(x) = 3x²+4x+1
            g(x) = 7x³+3x²+1
        (f+g)(x) = 7x³+6x²+4x+2
```
Using our lists or vectors:
```
            f = (1, 4, 3)
            g = (1, 0, 3, 7)
          f+g = (2, 4, 6, 7)
```

Multiplication of polynomials involves an operation known as convolution.  First, let's multiply the same two polynomials:
```
      (fg)(x) = 21x⁵+37x⁴+19x³+6x²+4x+1
```
Now, using the vectors, let's see how this works.  We will write the shorter vector f as a column and the longer g as a row.  (Convolution is commutative when the scalar operations are commutative.)  The products:
```
                         g
                         1    0    3    7
                ━━━━━╋━━━━━━━━━━━━━━━━━━━
                f  1 ┃   1    0    3    7
                   4 ┃   4    0   12   28
                   3 ┃   3    0    9   21
```
To obtain the convolutions, we add along the northeast diagonals:
```
        0       1 = 1               = (1) * (1)
        1       4 = 4 + 0           = (1,4) * (1,0)
        2       6 = 3 + 0 + 3       = (1,4,3) * (1,0,3)
        3      19 = 0 + 12 + 7      = (1,4,3) * (0,3,7)
        4      37 = 9 + 28          = (4,3) * (3,7)
        5       7 = 7               = (3) * (7)
```
The convolution in a given row is the sum of products of terms whose net degree is the row number.  For example, for row 3 we have:
```
        19x³ = (3x²)(0x) + (4x)(3x²) + (1)(7x³).
```
The multiplication operation turns out to be associative as long as the scalars are reasonably well-behaved.  If R is a commutative ring, then the polynomials in *x* over R (R`[`*x*`]`) also form a commutative ring.

## 2. The PolyMod module

The PolyMod module (*polynomials.polymod*) implements polynomials over the modular integers.  To create the polynomial ring, use the *make_poly* method.:
```
    >>> from polynomials.polymod import make_poly
    >>> help(make_poly)
    Help on function make_poly in module polynomials.polymod:

    make_poly(n: int, indeterminate: str = 'x') -> 'Class:(ℤ/nℤ)[x]'
        create a mod-n polynomial class

        Returns a class.

        In addition, this creates the base ring class.  The ring class
        may be found using the class method "coefficient_ring".

        If the ring class has already been created, you can use the
        entry point "_make_poly".  Duck-type compatibility is the
        only requirement.
```
To create the class, we need an integer larger than 1 to define the coefficient ring, and, optionally, a string to use as an indeterminate.  The default indeterminate is 'x'.
```
    >>> P = make_poly(12)
    >>> R = P.coefficient_ring()
    >>> R.__name__
    ''
    >>> P.__name__
    'ℤ/12[x]'
```
Our coefficient ring (*R*) consists of the integers modulo 12 (clock arithmetic).  *P*=`R[`*x*`]` is our polynomial ring.  Addition and multiplication in *R* is modulo 12.  In *P*, for addition, we add like terms and reduce modulo 12.  Muliplication involves convolution -- multiply all pairs of terms and collect and add the terms of the same degree.

To define a polynomial, we specify its coefficients, starting with the constant term:
```
    >>> f = P(1,2,3,4,5)
    >>> print(f"f(x)={f}     deg(f)={f.deg}")
    f(x)=5x⁴+4x³+3x²+2x+1     deg(f)=4
```
The degree of a polynomial is the exponent of the leading coefficient.  The degree of a nonzero constant polynomial is 0.  The degree of the zero polynomial is undefined -- some take it to be negative infinity but any value less than zero is fine as a working definition.  For our purposes, it is convenient to set deg(0) to -1:
```
    >>> zero = P()
    >>> print(zero)
    0
    >>> zero.deg
    -1
```
The zero polynomial is the additive identity:
```
    >>> f + zero == f == zero + f
    True
```
The additive inverse is obtained by changing the sign of each term:
```
    >>> g = -f
    >>> print(g)
    7x⁴+8x³+9x²+10x+11          <-- say what???
    >>> g + f == zero == f + g
    True
```
The value of -f(*x*) may require explanation.  The coefficients lie in the ring ℤ/12 (which we named *R* in the Python code).  These are reduced modulo 12.  For example, we see that -5=7 in ℤ/12.  What this means is:
```
             a =  q  b  + r         0 ≤ r < b     (b=12)
            -5 = -1(12) + 7   and   0 ≤ 7 < 12.
```
In Python:
```
    -5 // 12
    -1                  <--- quotient (ignored)
    -5 % 12
    7                   <--- remainder (the additive inverse)
```
The easy way to compute the label for the additive inverse of a label other than 0 is to subtract from the modulus (12):
```
    >>> 12-5
    7
```
The only problem with that approach is that we prefer the label 0 for multiples of 12.

Now let's something other than 0 or -f(*x*) to f(*x*) -- the output has been edited for emphasis:
```
    >>> g = P(3, 6, 9, 12, 15)
    >>> print(f"f(x)={f}")
            f(x)=5x⁴+4x³+3x²+2x+1
    >>> print(f"g(x)={g}")
            g(x)=3x⁴    +9x²+6x+3
    >>> print(f"(f+g)(x)={f+g}")
        (f+g)(x)=8x⁴+4x³    +8x+4
```
A few things might need explaining here.  First, 12%12=0 and 15%12=3 -- that accounts for the missing coeffifient and the leading coefficient 3 in g(*x*).  Since 9+3=12 and 12%12=0, we have a missing quadratic term in the sum (f+g)(x).  Here is the unedited output:
```
    >>> g = P(3, 6, 9, 12, 15)
    >>> print(f"f(x)={f}")
    f(x)=5x⁴+4x³+3x²+2x+1
    >>> print(f"g(x)={g}")
    g(x)=3x⁴+9x²+6x+3
    >>> print(f"(f+g)(x)={f+g}")
    (f+g)(x)=8x⁴+4x³+8x+4
```

We can, of course, take the difference in either direction:
```
    >>> print(f"(f-g)(x)={f-g}")
    (f-g)(x)=2x⁴+4x³+6x²+8x+10
    >>> print(f"(g-f)(x)={g-f}")
    (g-f)(x)=10x⁴+8x³+6x²+4x+2
```
These differences are additive inverses of one another (as in the "real" arithmetic of real numbers):
```
    >>> (f-g) + (g-f) == 0
    True
```

We can multiply any two polynomials, including these two:
```
    >>> print(f"(fg)(x)={f*g}")
    (fg)(x)=3x⁸+6x⁶+9x⁴+6x²+3
```
Multiplication of polynomials involves a vector operation called convolution.  Basically we take all possible products of the terms, and then add terms with the same exponents.
```
    >>> from collections import defaultdict
    >>> coeffs = defaultdict(list)
            # HERE WE TAKE ALL POSSIBLE PRODUCTS
    >>> for i in range(len(f)):
    ...     for j in range(len(g)):
    ...         coeffs[i+j].append(f[i]*g[j])
    ...
            # HERE WE DISPLAY ALL POSSIBLE PRODUCTS,
            # COLLECTED BY EXPONENT
    >>> coeffs
    defaultdict(<class 'list'>, {0: [3], 1: [6, 6],
        2: [9, 0, 9], 3: [0, 6, 6, 0], 4: [3, 0, 3, 0, 3],
        5: [6, 0, 0, 6], 6: [9, 0, 9], 7: [0, 0], 8: [3]})
    >>> poly = list()
            # FOR EACH EXPONENT, WE ADD UP THE RELEVANT
            # PRODUCTS
    >>> for n in range(9):
    ...     poly.append(sum(coeffs[n]))
    ...
    >>> print(poly)
    [3, 0, 6, 0, 9, 0, 6, 0, 3]
```
We feed the coefficients into our polynomial constructor.  A list or a tuple will be expanded:
```
        # P([3, 0, 6, 0, 9, 0, 6, 0, 3]) and
        # P((3, 0, 6, 0, 9, 0, 6, 0, 3)) and
        # P(3, 0, 6, 0, 9, 0, 6, 0, 3) are handled as equivalent.
        # The constructor expands the list or tuple.
    >>> h = P(poly)
    >>> h == f*g
    True
```
We don't, in general, have true division for polynomials, but we can, with some restrictions do division with a remainder.  (If the remainder is zero, we do have true division, but the interface does not implement true division.)
```
    >>> f // g
    ZeroDivisionError: divmod: lead coefficient divides zero
```
The leading coefficient 3 is not relatively prime to 12 -- so we can't divide f by g.

But the leading coefficient of f is the unit 1, so we can divide by f:
```
    print(g // f)
    3
    print(g % f)
    0
```

Any leading coefficient is fine as long as it is a unit.  The units in ℤ/12 are 1, 5, 7 and 11.  The remaining elements (0, 2, 3, 4, 6, 8, 9, and 10) are divisors of zero.

In the following example, f is a degree 6 polynomial and g is a degree 3 polynomial.  Since the leading coefficient of g is a unit (*i.e.* 5), we can divide by g, but we may have a remainder.  In the worst case, the remainder will be quadratic -- the degree of the remainder is less than the degree of the divisor.
```
    >>> f = P(2, 1)*P(3, 1)*P(5, 2, 1)*P(5, 3, 1)
    >>> print(f"f(x)={f}")
    f(x)=x⁶+10x⁵+11x⁴+3x³+6x²+11x+6
    >>> g = P(1, 0, 0, 5)
    >>> print(f"g(x)={g}")
    g(x)=5x³+1
    >>> q, r = divmod(f, g)
    >>> print(f"(f//g)(x)={q}")
    (f//g)(x)=5x³+2x²+7x+2
    >>> print(f"(f%g)(x)={r}")
    (f%g)(x)=4x²+4x+4
```
Our remainder is quadratic.  Let's check:
```
    >>> a = q*g + r
    >>> print(f-a)
    0
```
We've recovered f(x)... excellent!

Now let's divide g(x) by f(x).  The leading coefficient of f is 1 which is a unit, so division is permissible.  Since deg(g)=3 and deg(f)=6, our quotient is 0 and our remainder is g(x):
```
    >>> q, r = divmod(g, f)
    >>> print(q)
    0
    >>> r == g
    True
```
If the lead coefficient of f had been a zero divisor, division would not be permitted even though deg(f)>deg(g):
```
    >>> q, r = divmod(g, f*2)
    ZeroDivisionError: divmod: lead coefficient divides zero
```