# Cyclic groups and rings modulo *n*

## Contents

1.  Definitions
2.  The cyclic rings ℤₙ
3.  Examples

## 1. Definitions

### 1.1 Binary operations

A *binary operation* is a function on a set *X* which maps every ordered pair of elements in *X* to an element of *X*.  There are three parts to this definition:

1.  A binary operation is a type of relation $R$ -- *R* is a set of of ordered triples *u*=(*x*,*y*,*z*) of elements in $X$ -- our concern is whether a given triple *u* is a member of *R*;
2.  for each pair *x* and *y* of members of *X*, there is at *least* one member *z* of *X* such that the triple *u*=(*x*,*y*,*z*) is a member of $R$; and
3.  for each pair *x* and *y* of members of *X*, there is at *most* one member *z* of *X* such that the triple *u*=(*x*,*y*,*z*) is a member of $R$.

We normally write a triple using an infix operator: *x*★*y*=*z* is another way of saying that (*x*,*y*,*z*) is a member of $R$.  Condition 2 tells us that we can find a $z$, while condition 3 tells us that we cannot find more than one $z$.

### 1.2 Groups

A *group* is an algebraic structure consisting of a non-empty set and a binary operation defined on the set that obeys certain axioms.  More formally, a group is an ordered pair G=(*X*,★), consisting of a non-empty set X and a binary operation ★ on the set, such that:

1.  there exists *e* in *X* such that, for every *g* in *X* *e*★*g*=*g*;
2.  for each *g* in *X*, there exists *h* in *X* such that *h*★*g*=*e*; and
3.  for each *g*, *h*, and *j* in *X*, *g*★(*h*★*j*)=(*g*★*h*)★*j*.

The operation ★ is called the *group composition*.  Axiom 1 says that the group composition has a *left identity* element, which we will refer to as *e*.  (Axiom 1 does not, by itself, preclude the existence of additional left identities.) Axiom (2) says, for the left identity *e* mentioned in Axiom 1, each element *g* has a corresponding *left inverse*.  Axiom 3 says that the group composition is *associative*.

With this definition, we can prove (1) that *e* is a two-sided identity; (2) that the only left identity is *e* and the only right identity is *e*; (3) that the inverses are two-sided and uniquely determined, (4) that the inverse of the inverse of *g* in *X* is *g*; as well as a host of other familiar algebratic processes.  For example, we have two cancellation laws:

1.  (left cancellation) if *a*★*g* = *a*★*h*, then *g*=*h*; and
2.  (right cancellation)  if *g*★*a* = *h*★*a*, then *g*=*h*.

There are important groups, such as the symmetric group S₃ on three objects, in which the group composition is not commutative.  When the group composition is commutative, we call the group *abelian* (after nineteenth century mathematician Niels Abel) or *commutative*, and we sometimes refer to the group composition as addition.

When we write an abelian group *additively*, we call the identity element 0 and write the group composition as +.

When we write a group *multiplicatively*, we call the identity element 1 and write the group composition as a juxtaposition (*e.g.* *gh* for *g*★*h*) or, as needed, as a centered dot (*e.g.* *g*⋅*h* for *g*★*h*).  When we write a group multiplicatively does not presume that the group is commutative.

*Examples:* Addition of integers, of rational numbers, of real numbers, and of complex numbers are all groups.  Vector addition is another example.  The positive rational numbers, the non-zero rational numbers, the real numbers, and the nonzero complex numbers all give rise to groups under multiplication.  On the other hand, the integers under multiplication does not give rise to a group since 0 has no multiplicative inverse.

### 1.3 Monoids

A *monoid with identity* is an ordered pair G=(*X*,★), consisting of a non-empty set X and a binary operation ★ on the set, such that:

1.  there exists *e* in *X* such that, for every *g* in *X* *e*★*g*=*g*=*g*★*e*; and
2.  for each *g*, *h*, and *j* in *X*, *g*★(*h*★*j*)=(*g*★*h*)★*j*.

So a monoid is an algebraic structure with an associative composition and a two-sided identity.  (We can show that the identity is unique.)

We typically write monoids with identity multiplicatively.

### 1.4 Rings

A *ring with unity* is an algebraic structure with two binary operators, one forming a commutative group, the other a monoid with identity, and connected in a specific way using the distributive laws.

Formally a *ring with unity* is a triple R=(*X*,+,⋅) consisting of a set *X* and two binary operations + and ⋅ on *X* such that:

1.  (*X*,+) is a commutative group (with identity 0 and inverses -*x*);
2.  (*X*,⋅) is a commutative monoid with identity 1; and
3.  ⋅ distributes over +, *i.e.* *x*(*y*+*z*)=*xy*+*xz* and (*x*+*y*)*z*=*xz*+*yz* for each *x*, *y* and *z* in *X*.

If all nonzero elements of the ring have multiplicative inverses, then the ring is a *division ring* -- and if multiplication is commutative, the ring is a *field*.  (A division ring with non-commutative multiplication is called a *skew field*.)

It is not difficult to show that 0*x*=0=*x*⋅0 for all $x$ in a ring.

In addition, to avoid trivialities, we generally assume that *1≠0*.  If the additive identity and the multiplicative identity are equal, then the ring contains just one element.  Assuming that *1≠0* is equivalent to assuming that there are at least two elements in the ring.

## 2. The cyclic rings ℤₙ

The ordinary integers ℤ form a commutative ring under addition and multiplication.

Now let *n* be a positive integer and consider equivalence classes modulo *n*.

For example, with *n=2*, we have two equivalence classes, namely E=\[0\], the set of even integers and O=\[1\], the set of odd integers.  If we add two integers in the same class, the result is even, but if we add two integers with opposite parity, the result is odd.  The additive inverse of an even integer is even and that of an odd integer is odd.

Multiplication modulo 2 works in a similar fashion: multiplication by an even integer always yields an even integer; the product of two odd integers is always odd.

The resulting structure is a field with addition and multiplication defined as follows:
```
        E = {..., -6, -4, -2, 0, 2, 4, 6, ...}
        O = {..., -5, -3, -1, 1, 3, 5, 7, ...}
        X = {E, O}

                 y:                       y:
        x + y ┃  E   O              xy ┃  E   O
        ━━━━━━╋━━━━━━━           ━━━━━━╋━━━━━━━
        x:  E ┃  E   O           x:  E ┃  E   E
            O ┃  0   E               O ┃  E   0

              Additive inverses:  -E = E; -O = O
        Multiplicative inverses:         O⁻¹ = O
```

Generally we replace the equivalence classes with the smallest non-negative element in the class.  So a typical presentation of the field ℤ₂ is as follows:
```
            Tables for the ring ℤ₂

      x ┃ 0 1
    ━━━━╋━━━━
     -x ┃ 0 1   additive inverses
    1/x ┃ ┄ 1   multiplicative inverses  (┄ means "not applicable")

    Addition in ℤ₂              Subtraction in ℤ₂
     + ┃ 0 1                     - ┃ 0 1
    ━━━╋━━━━                    ━━━╋━━━━
     0 ┃ 0 1                     0 ┃ 0 1
     1 ┃ 1 0                     1 ┃ 1 0

    Multiplication in ℤ₂        Division in ℤ₂
     × ┃ 0 1                     ÷ ┃ 1
    ━━━╋━━━━                    ━━━╋━━
     0 ┃ 0 0                     1 ┃ 1
     1 ┃ 0 1
```
Subtraction is defined by adding one number to the additive inverse of another.  Since a number is its own additive inverse in ℤ₂, the addition and the subtraction tables are the same.  Division is the product of a number with the multiplicative inverse (or "reciprocal") of another.  Since 0 does not have a reciprocal, the division table is necessarily smaller than the addition, subtraction, and multiplication tables.  We omitted the trivial row where 0 is divided by something.

Now let's look at the ring of integers modulo 3, or ℤ₃. ℤ₃ is also a field:
```
            Tables for the ring ℤ₃

      x ┃ 0 1 2
    ━━━━╋━━━━━━
     -x ┃ 0 2 1   additive inverses
    1/x ┃ ┄ 1 2   multiplicative inverses  (┄ means "not applicable")

    Addition in ℤ₃                  Subtraction in ℤ₃
     + ┃ 0 1 2                       - ┃ 0 1 2
    ━━━╋━━━━━━                      ━━━╋━━━━━━
     0 ┃ 0 1 2                       0 ┃ 0 2 1
     1 ┃ 1 2 0                       1 ┃ 1 0 2
     2 ┃ 2 0 1                       2 ┃ 2 1 0

    Multiplication in ℤ₃            Division in ℤ₃
     × ┃ 0 1 2                       ÷ ┃ 1 2
    ━━━╋━━━━━━                      ━━━╋━━━━
     0 ┃ 0 0 0                       1 ┃ 1 2
     1 ┃ 0 1 2                       2 ┃ 2 1
     2 ┃ 0 2 1
```
Note first that -1=2.  This actually comes from the following special case of the division algorithm:
```
        -1 = 3(-1) + 2      (divisor 3; quotient -1; remainder 2)
```
In our implementation, the equivalence classes modulo *n* are represented by the smallest non-negative remainder after division by *n*.

Next note the division table.  It seems to be saying "1/2 modulo *n* is equal to 2".  It is really saying that, if we multiply a number whose remainder is 1 (after division by 3) by the *additive inverse* of a number whose remainder is also 1, then the result is a number whose remainder is 2.  What we are doing here is giving meaning to the statement in quotes.

Now we don't always get a field this way.  In fact, the only way we get a field is when *n* is prime.  In other cases, we get a commutative ring with nonzero elements which are divisors of zero.  These elements, corresponding to numbers which are not relatively prime to *n* do not have multiplicative inverses.  The remaining elements are known as units and do have multiplicative inverses.  The smallest example is when *n*=4:
```
            Tables for the ring ℤ₄

      x ┃ 0 1 2 3
    ━━━━╋━━━━━━━━
     -x ┃ 0 3 2 1   additive inverses
    1/x ┃ ┄ 1 ┄ 3   multiplicative inverses  (┄ means "not applicable")

    Addition in ℤ₄                  Subtraction in ℤ₄
     + ┃ 0 1 2 3                     - ┃ 0 1 2 3
    ━━━╋━━━━━━━━                    ━━━╋━━━━━━━━
     0 ┃ 0 1 2 3                     0 ┃ 0 3 2 1
     1 ┃ 1 2 3 0                     1 ┃ 1 0 3 2
     2 ┃ 2 3 0 1                     2 ┃ 2 1 0 3
     3 ┃ 3 0 1 2                     3 ┃ 3 2 1 0

    Multiplication in ℤ₄            Division in ℤ₄
     × ┃ 0 1 2 3                     ÷ ┃ 1 3
    ━━━╋━━━━━━━━                    ━━━╋━━━━
     0 ┃ 0 0 0 0                     1 ┃ 1 3
     1 ┃ 0 1 2 3                     3 ┃ 3 1
     2 ┃ 0 2 0 2
     3 ┃ 0 3 2 1
```
Note here that 2 is a divisor of 0 -- if we multiply two integers whose remainder (after division by 4) is 2, their product is divisible by 4 and hence in the equivalence class \[0\] modulo 4.

In the division table, we omitted the rows associated with 0 and 2 -- the complete table is:
```
            Division in ℤ₄
             ÷ ┃ 1 3
            ━━━╋━━━━
             0 ┃ 0 0
             1 ┃ 1 3
             2 ┃ 2 2
             3 ┃ 3 1
```
The missing rows can be inferred from the multiplication table after taking the multiplicative inverse of the divisors in the column headings.  Notice however that we cannot widen the table since 0 and 2 don't have multiplicative inverses.  The square division table is intended to highlight the fact that the units (1 and 3) form a multiplicative group.

Note the rows in the addition table:
```
        0123 -- 1230 -- 2301 -- 3012
```
Each row is obtained from its predecessor by a cyclic shift one place to the left.  The same fact holds for the columns.  The subtraction table also exhibits cyclic shifts, but the column shifts are one place to the right.  Finally each element of the group can be obtained by add ones to any element:
```
        0:      0+1=1       0+1+1=2     0+1+1+1=3   0+1+1+1+1=4
        1:      1+1=2       1+1+1+1=3   1+1+1+1=4   1+1+1+1+1=5
                        etc.
```
The same sorts of cyclic shifts occur in the (infinite) addition and subtraction tables for ℤ.  While we cannot generate every integer by adding ones, we can generate every integer by a mix of adding and subtracting ones.
If we can generate an entire group *G* from a single element by adding or subtracting copies of that element the group is said to be cyclic.  Conversely, if we take one element of a group and consider all sums and differences of copies of that element, we get a cyclic group.

As it turns out, every cyclic group is isomorphic to either ℤ or to ℤₙ for some positive integer *n*.

## 3. Examples

The tables in Section 2 above were produced by a demonstration module (*demos.modn_addition*).  In this section, we both show how to produce tables of this sort and we make a few comments on our examples.

### 3.1 The demonstration module

Here is the usage information:
```
    $ python -m demos.modn_addition -h
    usage: modn_addition.py [-h] [-m] [-x] [n]

    Display tables for the additive group in ℤₙ.

    positional arguments:
      n           the order of the ring. (n>1; default=11)

    options:
      -h, --help  show this help message and exit
      -m, --mult  when set, multiplication and division tables will
              also be displayed.
      -x, --ext   when set, show extended multiplication group
              analysis.

    Extended analysis implies tables for multiplication and division.
```

Note that *n* is an optional positional parameter.  The default is *n*=11, interesting because 11 is prime and its difference with 10 is 1.

(If you're familiar with casting out nines for checking arithmetic, look up casting out elevens.  If you're not familiar with casting out nines, look it up as well.)

The remaining options are switches.

### 3.2 The additive group ℤ₁₁

With no arguments, we get the addition and subtraction tables for ℤ₁₁.
```
$ python -m demos.modn_addition
            Tables for the group ℤ/11

      x ┃  0  1  2  3  4  5  6  7  8  9 10
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     -x ┃  0 10  9  8  7  6  5  4  3  2  1

    Addition in ℤ/11
      + ┃  0  1  2  3  4  5  6  7  8  9 10
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      0 ┃  0  1  2  3  4  5  6  7  8  9 10
      1 ┃  1  2  3  4  5  6  7  8  9 10  0
      2 ┃  2  3  4  5  6  7  8  9 10  0  1
      3 ┃  3  4  5  6  7  8  9 10  0  1  2
      4 ┃  4  5  6  7  8  9 10  0  1  2  3
      5 ┃  5  6  7  8  9 10  0  1  2  3  4
      6 ┃  6  7  8  9 10  0  1  2  3  4  5
      7 ┃  7  8  9 10  0  1  2  3  4  5  6
      8 ┃  8  9 10  0  1  2  3  4  5  6  7
      9 ┃  9 10  0  1  2  3  4  5  6  7  8
     10 ┃ 10  0  1  2  3  4  5  6  7  8  9

    Subtraction in ℤ/11
      - ┃  0  1  2  3  4  5  6  7  8  9 10
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      0 ┃  0 10  9  8  7  6  5  4  3  2  1
      1 ┃  1  0 10  9  8  7  6  5  4  3  2
      2 ┃  2  1  0 10  9  8  7  6  5  4  3
      3 ┃  3  2  1  0 10  9  8  7  6  5  4
      4 ┃  4  3  2  1  0 10  9  8  7  6  5
      5 ┃  5  4  3  2  1  0 10  9  8  7  6
      6 ┃  6  5  4  3  2  1  0 10  9  8  7
      7 ┃  7  6  5  4  3  2  1  0 10  9  8
      8 ┃  8  7  6  5  4  3  2  1  0 10  9
      9 ┃  9  8  7  6  5  4  3  2  1  0 10
     10 ┃ 10  9  8  7  6  5  4  3  2  1  0
```
Since 11 is prime, ℤ₁₁ (or ℤ/11ℤ or Z/11) is a field.  Here we display just the additive group.  ℤ₁₁ is generated additively by any element of ℤ₁₁ except 0.

### 3.3 The field ℤ₁₁

All rings have multiplication tables, and all rings with unity have at least one unit and a division table for the group of units.  ℤ₁₁ has a group of units which is isomorphic to ℤ₁₀.  (If *n* is prime, then the its group of units is cyclic and isomorphic to ℤₙ₋₁.)
```
    $ python -m demos.modn_addition -m
    Tables for the ring ℤ/11

      x ┃  0  1  2  3  4  5  6  7  8  9 10
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     -x ┃  0 10  9  8  7  6  5  4  3  2  1
    1/x ┃ ┄┄  1  6  4  3  9  2  8  7  5 10

        ... [omitting two tables]
```
Note that we have ten multiplicative inverses, one less than the number of elements.  (0 cannot have a multiplicative inverse in a nontrivial ring.)

The addition and subtraction tables were displayed in Section 3.2, so we omit them here.
```
    Multiplication in ℤ/11
      × ┃  0  1  2  3  4  5  6  7  8  9 10
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      0 ┃  0  0  0  0  0  0  0  0  0  0  0
      1 ┃  0  1  2  3  4  5  6  7  8  9 10
      2 ┃  0  2  4  6  8 10  1  3  5  7  9
      3 ┃  0  3  6  9  1  4  7 10  2  5  8
      4 ┃  0  4  8  1  5  9  2  6 10  3  7
      5 ┃  0  5 10  4  9  3  8  2  7  1  6
      6 ┃  0  6  1  7  2  8  3  9  4 10  5
      7 ┃  0  7  3 10  6  2  9  5  1  8  4
      8 ┃  0  8  5  2 10  7  4  1  9  6  3
      9 ┃  0  9  7  5  3  1 10  8  6  4  2
     10 ┃  0 10  9  8  7  6  5  4  3  2  1

    Division in ℤ/11
      ÷ ┃  1  2  3  4  5  6  7  8  9 10
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      1 ┃  1  2  3  4  5  6  7  8  9 10
      2 ┃  2  4  6  8 10  1  3  5  7  9
      3 ┃  3  6  9  1  4  7 10  2  5  8
      4 ┃  4  8  1  5  9  2  6 10  3  7
      5 ┃  5 10  4  9  3  8  2  7  1  6
      6 ┃  6  1  7  2  8  3  9  4 10  5
      7 ┃  7  3 10  6  2  9  5  1  8  4
      8 ┃  8  5  2 10  7  4  1  9  6  3
      9 ┃  9  7  5  3  1 10  8  6  4  2
     10 ┃ 10  9  8  7  6  5  4  3  2  1
```
Unlike ℤ₁₁, the nonzero elements of ℤ₁₀ don't all generate the full group.  For example, the group generated by 5 in ℤ₁₀ is isomorphic to ℤ₂.  (Exercise: Why?)  Now it might not be obvious from the multiplication table above, but the element of the group of units that corresponds to 5 in ℤ₁₀ is 10 (which is the same as -1 modulo 11).  Here is the correspondence:
```
        ℤ₁₀                         U(ℤ₁₁)
          + ┃  0  5                   × ┃  1 10
        ━━━━╋━━━━━━                 ━━━━╋━━━━━━
          0 ┃  0  5                   1 ┃  1 10
          5 ┃  5  0                  10 ┃ 10  1

                Note:   5 + 5 = 10;      10 = 1×10 + 0
                       10 × 10 = 100;   100 = 9×11 + 1
```
Note that if we replace + with ×, 0 with 1 and 5 with 10, the table on the left transforms into the table on the right.  If we just replace 5 with 1, we get the addition table for ℤ₂.

Also hidden in the multiplication table are 4 elements of order 5 and 4 elements of order 10.  The remaining element 1 is not hiding and has order 1.

### 3.4 The group of units for ℤ₁₁

Let's use the remaining switch so that we don't have all those elements playing hide and seek in the multiplication table:
```
    $ python -m demos.modn_addition -x
            Tables for the ring ℤ/11

        ... [omitting five tables]

               additive order: 11
         multiplicative order: 10
                           ζ = 2
                      ord(ζ) = 10
               is ζ primitive? Yes
```
After snipping the repeated information, we get some useful facts.  The additive order was given (*n*=11) and the multiplicative order is 10 because 11 is prime.  That number ζ is the smallest element of maximum order.  Since *n* is prime, its order must be 10 (as the group of units is cyclic of order 10).  An element of maximum order in a cyclic group is called a *primitive* element because it generates the whole group.
```
    Orders of the units in ℤ/11
          x ┃  1  2  3  4  5  6  7  8  9 10
    ━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ord(x) ┃  1 10  5  5  5 10 10 10  5  2
```
The next table displays the order of each unit.

Arranging this table in another way, we have:
```
        Order   Elements
          1       1
          2       10
          5       3, 4, 5, 10
         10       2, 6, 7, 8    <-- primitive elements
```
The orders are all divisors of 10.  (Lagrange's Theorem: The order of an element -- or more generally, the order of a subgroup -- divides the order of the group.)

(ord(3)=5) If we look at the powers of 3, we have:
```
        powers of 3
                0       1       2       3       4       5
        ℤ:      1       3       9      27      81     243
        ℤ₁₁:    1       3       9       5       4       1
                ----------- one period ----------
```
Above we happened to mention casting out elevens.  Let's do it now... Three cubed is 27, so 27 modulo 11 is 7-2 or 5.  Three to the fourth is 81; 1-8=-7, but 11-7 is 4. Three to the fifth is 243; 3-4+2=1.

Note that the powers of 3 are cyclic with a period of 5.  If we try the same experiment with one of the four primitive elements, we will find the order to be equal to 10.  (Exercise: Without a calculator, show that ord(2)=10.)

Since group of units for ℤ₁₁ is cyclic, we can use any primitive element to produce discrete logarithms.  (We can produce discrete logarithms based on powers of any unit, but only primitive elements map the whole group of units.

The first step is to compute the cycle of powers.  (Spoiler: If you did the exercise, you can check your answer below.)
```
    Powers of the unit 2 in ℤ/11
            n ┃  0  1  2  3  4  5  6  7  8  9
    ━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     exp(n,ζ) ┃  1  2  4  8  5 10  9  7  3  6
```
Here we map integers modulo 10 to units modulo 11.  To get the table of logarithms, simply interchange the two rows.  (You will probably also want to sort the columns so that the top row is in order.)
```
    Logarithms to base 2 in ℤ/11
            x ┃  1  2  3  4  5  6  7  8  9 10
    ━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     log(x,ζ) ┃  0  1  8  2  4  9  7  3  6  5
```
The usual logarithm laws apply to these discrete logarithms.

### 3.5 The commutative ring ℤ₁₈

18 is not prime, so ℤ₁₈ is not a field.  But it does have some nice features.  Let's take a look.  We will comment briefly after the display:
```
$ python -m demos.modn_addition 18 -x
    Tables for the ring ℤ/18

      x ┃  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     -x ┃  0 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1
    1/x ┃ ┄┄  1 ┄┄ ┄┄ ┄┄ 11 ┄┄ 13 ┄┄ ┄┄ ┄┄  5 ┄┄  7 ┄┄ ┄┄ ┄┄ 17

    Addition in ℤ/18
      + ┃  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      0 ┃  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
      1 ┃  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17  0
      2 ┃  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17  0  1
      3 ┃  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17  0  1  2
      4 ┃  4  5  6  7  8  9 10 11 12 13 14 15 16 17  0  1  2  3
      5 ┃  5  6  7  8  9 10 11 12 13 14 15 16 17  0  1  2  3  4
      6 ┃  6  7  8  9 10 11 12 13 14 15 16 17  0  1  2  3  4  5
      7 ┃  7  8  9 10 11 12 13 14 15 16 17  0  1  2  3  4  5  6
      8 ┃  8  9 10 11 12 13 14 15 16 17  0  1  2  3  4  5  6  7
      9 ┃  9 10 11 12 13 14 15 16 17  0  1  2  3  4  5  6  7  8
     10 ┃ 10 11 12 13 14 15 16 17  0  1  2  3  4  5  6  7  8  9
     11 ┃ 11 12 13 14 15 16 17  0  1  2  3  4  5  6  7  8  9 10
     12 ┃ 12 13 14 15 16 17  0  1  2  3  4  5  6  7  8  9 10 11
     13 ┃ 13 14 15 16 17  0  1  2  3  4  5  6  7  8  9 10 11 12
     14 ┃ 14 15 16 17  0  1  2  3  4  5  6  7  8  9 10 11 12 13
     15 ┃ 15 16 17  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
     16 ┃ 16 17  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
     17 ┃ 17  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16

    Subtraction in ℤ/18
      - ┃  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      0 ┃  0 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1
      1 ┃  1  0 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2
      2 ┃  2  1  0 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3
      3 ┃  3  2  1  0 17 16 15 14 13 12 11 10  9  8  7  6  5  4
      4 ┃  4  3  2  1  0 17 16 15 14 13 12 11 10  9  8  7  6  5
      5 ┃  5  4  3  2  1  0 17 16 15 14 13 12 11 10  9  8  7  6
      6 ┃  6  5  4  3  2  1  0 17 16 15 14 13 12 11 10  9  8  7
      7 ┃  7  6  5  4  3  2  1  0 17 16 15 14 13 12 11 10  9  8
      8 ┃  8  7  6  5  4  3  2  1  0 17 16 15 14 13 12 11 10  9
      9 ┃  9  8  7  6  5  4  3  2  1  0 17 16 15 14 13 12 11 10
     10 ┃ 10  9  8  7  6  5  4  3  2  1  0 17 16 15 14 13 12 11
     11 ┃ 11 10  9  8  7  6  5  4  3  2  1  0 17 16 15 14 13 12
     12 ┃ 12 11 10  9  8  7  6  5  4  3  2  1  0 17 16 15 14 13
     13 ┃ 13 12 11 10  9  8  7  6  5  4  3  2  1  0 17 16 15 14
     14 ┃ 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0 17 16 15
     15 ┃ 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0 17 16
     16 ┃ 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0 17
     17 ┃ 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0

    Multiplication in ℤ/18
      × ┃  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      0 ┃  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      1 ┃  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17
      2 ┃  0  2  4  6  8 10 12 14 16  0  2  4  6  8 10 12 14 16
      3 ┃  0  3  6  9 12 15  0  3  6  9 12 15  0  3  6  9 12 15
      4 ┃  0  4  8 12 16  2  6 10 14  0  4  8 12 16  2  6 10 14
      5 ┃  0  5 10 15  2  7 12 17  4  9 14  1  6 11 16  3  8 13
      6 ┃  0  6 12  0  6 12  0  6 12  0  6 12  0  6 12  0  6 12
      7 ┃  0  7 14  3 10 17  6 13  2  9 16  5 12  1  8 15  4 11
      8 ┃  0  8 16  6 14  4 12  2 10  0  8 16  6 14  4 12  2 10
      9 ┃  0  9  0  9  0  9  0  9  0  9  0  9  0  9  0  9  0  9
     10 ┃  0 10  2 12  4 14  6 16  8  0 10  2 12  4 14  6 16  8
     11 ┃  0 11  4 15  8  1 12  5 16  9  2 13  6 17 10  3 14  7
     12 ┃  0 12  6  0 12  6  0 12  6  0 12  6  0 12  6  0 12  6
     13 ┃  0 13  8  3 16 11  6  1 14  9  4 17 12  7  2 15 10  5
     14 ┃  0 14 10  6  2 16 12  8  4  0 14 10  6  2 16 12  8  4
     15 ┃  0 15 12  9  6  3  0 15 12  9  6  3  0 15 12  9  6  3
     16 ┃  0 16 14 12 10  8  6  4  2  0 16 14 12 10  8  6  4  2
     17 ┃  0 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1

    Division in ℤ/18
      ÷ ┃  1  5  7 11 13 17
    ━━━━╋━━━━━━━━━━━━━━━━━━
      1 ┃  1  5  7 11 13 17
      5 ┃  5  7 17  1 11 13
      7 ┃  7 17 13  5  1 11
     11 ┃ 11  1  5 13 17  7
     13 ┃ 13 11  1 17  7  5
     17 ┃ 17 13 11  7  5  1

               additive order: 18
         multiplicative order: 6
                           ζ = 5
                      ord(ζ) = 6
               is ζ primitive? Yes

    Orders of the units in ℤ/18
          x ┃  1  5  7 11 13 17
    ━━━━━━━━╋━━━━━━━━━━━━━━━━━━
     ord(x) ┃  1  6  3  6  3  2

    Powers of the unit 5 in ℤ/18
            n ┃  0  1  2  3  4  5
    ━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━
     exp(n,ζ) ┃  1  5  7 17 13 11

    Logarithms to base 5 in ℤ/18
            x ┃  1  5  7 11 13 17
    ━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━
     log(x,ζ) ┃  0  1  2  5  4  3
```
In the addition and subtraction tables, note the cyclic bands: ℤ₁₈ is a cyclic group.

The prime divisors of 18 are 2 and 3, so we have a lot of divisors of zero.  There are only 6 units, but the group of units is cyclic.  There are two primitive units, 5 and 11, so we can produce a full set of discrete logarithms.

In general, the group of units in ℤₙ will have a primitive element unless 4 is a proper divisor of *n* or *n* has more than one odd prime divisor.  For example 18 has just one odd prime divisor (3) and 4 does not divide 18, so group of units for ℤ₁₈ has a primitive elements.

4 is a curious special case: 4 divides 4, but 4 is not a proper divisor of 4.  In addition, 4 has no odd prime divisors, so 4 has a primitive element.  (3 is the only primitive element.  The group of units consists of 1 and 3.)

The smallest cyclic rings with no primitive element are tabulated below:
```
     n  units   not cyclic - why?       Notes
    --- -----   ----------------------- ---------------------
     8      4   4 properly divides 8    power of two
    12      4   4 properly divides 12   one odd prime divisor
    15      8   two odd prime divisors
```

### 3.6 The commutative ring ℤ₈

Let's see what goes wrong in ℤ₈.  We will remove some of the noise...
```
    $ python -m demos.modn_addition 8 -x
    Tables for the ring ℤ/8

      x ┃ 0 1 2 3 4 5 6 7
    ━━━━╋━━━━━━━━━━━━━━━━
     -x ┃ 0 7 6 5 4 3 2 1
    1/x ┃ ┄ 1 ┄ 3 ┄ 5 ┄ 7

        [2 tables omitted]

    Multiplication in ℤ/8
     × ┃ 1 3 5 7
    ━━━╋━━━━━━━━        [divisors of zero removed]
     1 ┃ 1 3 5 7
     3 ┃ 3 1 7 5
     5 ┃ 5 7 1 3
     7 ┃ 7 5 3 1

        [1 table removed]

               additive order: 8
         multiplicative order: 4
                           ζ = 3
                      ord(ζ) = 2
               is ζ primitive? No

    Orders of the units in ℤ/8
          x ┃ 1 3 5 7
    ━━━━━━━━╋━━━━━━━━
     ord(x) ┃ 1 2 2 2

    WARNING: 3 is not a primitive element in ℤ/8
```
The units are 1, 3, 5, and 7.  Except for 1, these have order 2.  The product of any two distinct order 2 elements is the third order 2 element. The square of any unit is 1.  We need two order 2 elements to generate the group.  We express this in notation as:
```
            U(ℤ₈) ≅ ℤ₂ ⨯ ℤ₂
```
The group of units of ℤ₈ is structurally the same as the product of two copies of ℤ₂.  Here is the addition table for ℤ₂ ⨯ ℤ₂:
```
            +  ┃ 00 01 10 11
            ━━━╋━━━━━━━━━━━━
            00 ┃ 00 01 10 11     (a,b) + (c,d) = ((a+c), (b+d))
            01 ┃ 01 00 11 10
            10 ┃ 10 11 00 01
            11 ┃ 11 10 01 00
```

If we try to use a unit to create exponentials and logarithms, we will fail to cover the group of units.  For example:
```
    Powers of the unit 3 in ℤ/8
            n ┃ 0 1
    ━━━━━━━━━━╋━━━━
     exp(n,ζ) ┃ 1 3

    Logarithms to base 3 in ℤ/8
            x ┃ 1 3
    ━━━━━━━━━━╋━━━━
     log(x,ζ) ┃ 0 1
```

The group of units of ℤ₁₂ has the same structure.

### 3.6 The commutative ring ℤ₁₅

Let's look at the multiplicative structure of ℤ₁₅:
```
    $ python -m demos.modn_addition 15 -x
    Tables for the ring ℤ/15

      x ┃  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     -x ┃  0 14 13 12 11 10  9  8  7  6  5  4  3  2  1
    1/x ┃ ┄┄  1  8 ┄┄  4 ┄┄ ┄┄ 13  2 ┄┄ ┄┄ 11 ┄┄  7 14

            [removed 2 tables]

    Multiplication in ℤ/15
      × ┃  1  2  4  7  8 11 13 14
    ━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━
      1 ┃  1  2  4  7  8 11 13 14
      2 ┃  2  4  8 14  1  7 11 13
      4 ┃  4  8  1 13  2 14  7 11   [removed divisors of zero]
      7 ┃  7 14 13  4 11  2  1  8
      8 ┃  8  1  2 11  4 13 14  7
     11 ┃ 11  7 14  2 13  1  8  4
     13 ┃ 13 11  7  1 14  8  4  2
     14 ┃ 14 13 11  8  7  4  2  1

            [removed 1 table]

               additive order: 15
         multiplicative order: 8
                           ζ = 2
                      ord(ζ) = 4
               is ζ primitive? No

    Orders of the units in ℤ/15
          x ┃  1  2  4  7  8 11 13 14
    ━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━
     ord(x) ┃  1  4  2  4  4  2  4  2

    WARNING: 2 is not a primitive element in ℤ/15

            [removed 2 tables]
```
Here we have eight elements in the group of units.  The largest order is 4, so we can generate half the elements using an order 4 element, for example 2.  Then we find an order 2 element which is not in the span of 2.
```
        span of 2         1  2  4  8
        span of 7         1  7

        from the multiplication table:  Addition in ℤ₄ ⨯ ℤ₂
                  × ┃  1  2  4  8         + ┃ 00 10 20 30
                ━━━━╋━━━━━━━━━━━━━━     ━━━━╋━━━━━━━━━━━━━━
                  1 ┃  1  2  4  8        00 ┃ 00 10 20 30
                  7 ┃  7 14 13 11        01 ┃ 01 11 21 31

        Addition in ℤ₄ ⨯ ℤ₂              Multiplication in ℤ₁₅
          + ┃ 00 01 10 11 20 21 30 31    × ┃  1  7  2 14  4 13  8 11
         ━━━╋━━━━━━━━━━━━━━━━━━━━━━━━   ━━━╋━━━━━━━━━━━━━━━━━━━━━━━━
         00 ┃ 00 01 10 11 20 21 30 31    1 ┃  1  7  2 14  4 13  8 11
         01 ┃ 01 00 11 10 21 20 31 30    7 ┃  7  1 14  2 13  4 11  8
         10 ┃ 10 11 20 21 20 31 00 01    2 ┃  2 14  4 13  8 11  1  7
         11 ┃ 11 10 21 20 31 30 01 00   14 ┃ 14  2 14  4 11  8  7  1
         20 ┃ 20 21 30 31 00 01 10 11    4 ┃  4 13  8 11  1  7  2 14
         21 ┃ 21 20 31 30 01 00 11 10   13 ┃ 13  4 11  8  7  1 14  2
         30 ┃ 30 31 00 01 10 11 20 21    8 ┃  8 11  1  7  2 14  4 13
         31 ┃ 31 30 01 00 11 10 21 20   11 ┃ 11  8  7  1 14  2 13  4
```
We rearranged the multiplication table to make it easier to see the isomorphism.  Break up the tables into 2×2 blocks.  For example, notice how the block in the upper left shows up on the right at the end of the third row.  In the fifth row it has moved two places left, and in the seventh row, two more places.  We have the same banding structure as in ℤ₄ addition, but instead of one entry, it is 4 entries in a 2×2 square.

If instead, we look at 4×4 square blocks, we see the familiar ℤ₂ addition structure.