# Comparisons of several logic models

Run the script in a shell from the science folder in python or in idle, or perhaps in spyder...  For python, in the shell:
```
    science$ python -m logic.tests.pm1
```
For idle, in the shell:
```
    science$ idle

    In the GUI, select File->Open Module.
    In the text box that appears, enter "logic.tests.pm1" (without quotes).
```

## Contents

1. The classical propositional calculus (PM)
2. Verifying the controls
3. Ł₃ (3-valued Łukasiewicz algebra
4. Ł₄ (4-valued Łukasiewicz algebra)
5. G₃ (3-valued Gödel-Dummett algebra)
6. G₄ (4-valued Gödel-Dummett algebra)
7. ℒ(4) (the lattice of divisors of 4, i.e. {1, 2, 4})
8. ℒ(6) (the lattice of divisors of 6, i.e. {1, 2, 3, 6})
9. ℒ(30) (the lattice of divisors of 30)
10. ℒ(60) (the lattice of divisors of 60)

## 1. The classical propositional calculus

The experimental control is the standard model for the classical propositional calculus.  The standard model involves a set containing two values which we call F and T.  There is one unary operator and four binary operators.  These are as follows:

* logical negation: ~p is a transposition, mapping F↦T and T↦F;
* disjunction or join: p∨q maps (F,F)↦F, (F,T)↦T, (T,F)↦T, and (T,T)↦T;
* conjunction or meet: p∧q maps (F,F)↦F, (F,T)↦F, (T,F)↦F, and (T,T)↦T;
* material implication: p⊃q maps (F,F)↦T, (F,T)↦T, (T,F)↦F, and (T,T)↦T; and
* material equivalence: p≡q maps (F,F)↦T, (F,T)↦F, (T,F)↦F, and (T,T)↦T.

The usual interpretation is that the letters (or propositional variables) represent true/false statements. for example:

* p = "Yesterday I went to the store."
* q = "Today I have some bananas."

The statements ~p and ~q can be interpreted as follows:

* ~p = "Yesterday I did *not* go to the store."
* ~q = "Today I do *not* have any bananas."

The connective ~ transforms a true statement into a false statement, and, conversely, a false statement into one that is true.  We some read ~p as: "It is false that p."; or, shorter, as: "Not p." 

The binary connectives are translated into English as follows:

* p∨q = "*Either* yesterday I went to the store *or* today I have some bananas."
* p∧q = "*Both* yesterday I went to the store *and* today I have some bananas.".
* p⊃q = "*If* yesterday I went to the store *then* today I have some bananas."
* p≡q = "Yesterday I went to the store *if and only if* today I have some bananas."

A key point is that these compound statements depend *materially* only on on the truth or falsity of the components.  Other matters such as causality are *immaterial*.  For example, the following statements are all treated as true:

* If purple cows exist, then 2+2=3.  (A false proposition implies any proposition.)
* If purple cows exist, then 2+2=4.  (A false proposition implies any proposition.)
* If George Washington's head appears on the US 25¢ coin, then 2+2=4.  (A true proposition is implied by any proposition.)

Note that the value of a sum of two integers is independent of the existence of a certain variety of cows, or of the design of US coinage.  We don't assert any sort of causal connection.

In 1910, in a work entitled *Principia Mathematica*, Alfred North Whitehead and Bertrand Russell presented a set of definitions, axioms, and rules for determining which statements involving propositional variables and the connectives above are always true,  This system has been shown to be both complete and consistent.  Negation and disjunction are primitive.

Conjunction, implication and equivalence are defined as follows:
```
    D1: (p∧q) := ~(~p∨~q)
    D2: (p⊃q) := (~p∨q)
    D3: (p≡q) := ((p⊃q)∧(q⊃p))
```

The axioms of the system are the following five schemas:
```
    A1: (p∨p)⊃p                              tautology
    A2: q⊃(p∨q)                              addition
    A3: (p∨q)⊃(q∨p)                          permutation
    A4: (p∨(q∨r))⊃(q∨(p∨r))                  association
    A5: (q⊃r)⊃((p∨q)⊃(p∨r))                  summation
```
Axiom A3 is called "permutation" in *Principia Mathematica*, but is ordinarily referred to as "commutation" or "commutativity" or, more informally, a "commutative law".

As written, they only involve disjunction and implication.  But implication is defined in terms of negation and disjunction.  For purposes of proving statements, the first of these axioms is intended to be thought of as a shorthand for:
```
   A1': ~(p∨p)∨p
```
But A1  is a statement in its own right, and for purposes of this demonstration, we view the statements A1 and A1' as statements which are different in form.

To complete the axiomatization of propositional calculus, we need to define some rules of inference (or transformation).  In *Principia Mathematica*, three rules are given.

* An axiom is a valid statement.
* *modus ponens*: If X⊃Y and X are valid statements, then Y is a valid statement.
* *substitution*: We can produce a valid statement by uniformly replacing each propositional variable in a valid statement by a well-formed formula (or *wff*, plural: *wffs*).

We abbreviate "is a valid statement" by prefixing a statement with the turnstile symbol "⊢".

We call this axiom system *PM* (for *Principia Mathematica*).  To illustrate how *PM* actually works, we repeat a few proofs from the *Principia Mathematica*,

Filling in the details, the first proof, proposition 2.01 on page 100, is as follows:
```
   Proposition 2.01. ⊢(p⊃~p)⊃~p.
   Proof:
      1. ⊢(p∨p)⊃p                       Axiom A1 (tautology)
      2. ⊢(~p∨~p)⊃~p                    1 × Substitution(~p/p)
      3. ⊢(p⊃~p)⊃~p                     2 x D2
```
Skipping a bit on the same page, in order to use *modus ponens*, we reproduce propositions 2.04 through 2.06 and their proofs.  We abbreviate substitution as *S* and *modus ponens* as *MP*
```
   Proposition 2.04. ⊢(p⊃(q⊃r))⊃(q⊃(p⊃r)).
   Proof:
      1. ⊢(p∨(q∨r))⊃(q∨(p∨r))           Axiom A4 (association)
      2. ⊢(~p∨(~q∨r))⊃(~q∨(~p∨r))       1 × S(~p/p, ~q/q)
      2. ⊢(p⊃(q⊃r))⊃(q⊃(p⊃r))           2 × D2 (four times!)

   Proposition 2.05. ⊢(q⊃r)⊃((p⊃q)⊃(q⊃r)).
   Proof:
      1. ⊢(q⊃r)⊃((p∨q)⊃(p∨r))           Axiom A5 (summation)
      2. ⊢(q⊃r)⊃((~p∨q)⊃(~p∨r))         1 × S(~p/p)
      3. ⊢(q⊃r)⊃((p⊃q)⊃(p⊃r))           2 x D2 (twice!)

   Proposition 2.06. ⊢(p⊃q)⊃((q⊃r)⊃(p⊃r)).
   Proof:
      1. ⊢(p⊃(q⊃r))⊃(q⊃(p⊃r))           Proposition 2.04
      2. ⊢(2.05)⊃(2.06)                 1 × S((q⊃r)/p, (p⊃q)/q, (p⊃r)/r)
      3. ⊢(p⊃q)⊃((q⊃r)⊃(p⊃r))           2, 2.05 × MP
```
Line 2 in the proof of Proposition 2.06 is shorthand for:
```
      2. ⊢((q⊃r)⊃((p⊃q)⊃(q⊃r)))⊃((p⊃q)⊃((q⊃r)⊃(p⊃r)))
```

In our statement of the rules, the axiom rule is implicit.  To avoid a complicated statement of the substitution rule, we treat the proposition letters as schemas which can be replaced by wffs.  So our primitive rules are written more compactly in a single line:
```
    R1: If ⊢(p⊃q) and ⊢p, then ⊢q.       modus ponens
```

For help in comparing various system, we have included a number of theorem schemas (labelled T1 through T26) and three derived rules of inference in our survey.

## 2. Verifying the controls

We first ran our definitions, statements (axioms and theorems), and rules through an engine which implements a model of the propositional calculus as a 2-valued Łukasiewicz algebra -- we call this model Ł₂.

For the definitions:
```
    D1: (p∧q) := ~(~p∨~q)                    conjunction
    D2: (p⊃q) := (~p∨q)                      implication
    D3: (p≡q) := ((p⊃q)∧(q⊃p))               equivalence
	--> All the definitions are valid.
```

For the axiom schemas:
```
    A1: (p∨p)⊃p                              tautology
    A2: q⊃(p∨q)                              addition
    A3: (p∨q)⊃(q∨p)                          permutation
    A4: (p∨(q∨r))⊃(q∨(p∨r))                  association
    A5: (q⊃r)⊃((p∨q)⊃(p∨r))                  summation
	--> All the axiom schemas are valid.
```

For the primitive rule of inference, *modus ponens*:
```
    R1: If ⊢(p⊃q) and ⊢p, then ⊢q.           modus ponens
	--> All the transformations are valid.
```

For the 26 theorem schemas:
```
    T1: p≡p                                  reflexivity
    T2: (p≡q)⊃(q≡p)                          symmetry
    T3: (p≡q)⊃((q≡r)⊃(p≡r))                  transitivity
```
Using *modus ponens*, T1 through T3 show that material equivalence is an equivalence relation.
```
    T4.1: (p≡q)⊃(~p⊃~q)                        monotony
    T4.2: (p≡q)⊃((p∨r)⊃(q∨r))                  monotony
    T4.3: (q≡r)⊃((p∨q)⊃(p∨r))                  monotony
    T4.4: (p≡q)⊃((p∧r)⊃(q∧r))                  monotony
    T4.5: (q≡r)⊃((p∧q)⊃(p∧r))                  monotony
    T4.6: (p≡q)⊃((p⊃r)⊃(q⊃r))                  monotony
    T4.7: (q≡r)⊃((p⊃q)⊃(p⊃r))                  monotony
```
Using *modus ponens*, the monotony theorems (T4.1 through T4.7), and theorems T1 through T3 allow us to derive a rule (more precisely a meta-rule) for substitution of material equivalents.
``` 
    T5: (p⊃(q⊃r))⊃((p⊃q)⊃(p⊃r))              importation
```
Theorem T5 is a self-distributive law for material implication.  It is key to showing that the classical propositional calculus supports *natural deduction*:

* If, given that X1 through Xn and Y are valid, we can in turn prove that Z is valid, we can then prove that the validity of X1 through Xn is sufficient to prove the validity of X⊃Y.
* For example, take the rule *modus ponens*:
    - If ⊢(p⊃q) and ⊢p, then ⊢q.
* Swap the premises:
    - If ⊢p and ⊢(p⊃q), then ⊢q.
* Now rewrite the rule using some new notation and use natural deduction:
    - p, (p⊃q) ⊢q. Premises, separated by commas precede the turnstile.
    - p ⊢(p⊃q)⊃q.
    - ⊢p⊃((p⊃q)⊃q).

```
    T6: p⊃p                                  identity
    T7: (p⊃q)⊃((q⊃p)⊃(p≡q))                  antisymmetry
    T8: (p⊃q)⊃((q⊃r)⊃(p⊃r))                  transitivity
```
Using *modus ponens*, T6 through T8 show that material implication is a partial order.
```
    T9: ((p⊃q)⊃p)⊃p                          Pierce
   T10.1: (p⊃r)⊃((q⊃r)⊃((p∨q)⊃r))              dilemma
   T10.2: (p⊃r)⊃((q⊃s)⊃((p∨q)⊃(r∨s)))          dilemma
   T11: (p⊃(q⊃r))⊃((p∧q)⊃r)                  importation
   T12: ((p∧q)⊃r)⊃(p⊃(q⊃r))                  exportation
   T13.1: p∨~p                                 tertium non datur
   T13.2: (p⊃q)∨(q⊃p)                          tertium non datur
```
T13.1 is the usual form of the law of the excluded middle -- the Latin *tertium non datur* means "the third is not given".  T13.2 is somewhat weaker.
```
   T14: ~(p∧~p)                              contradiction
   T15.1: (p⊃~p)⊃~p                            reductio ad absurdum
   T15.2: (~p⊃p)⊃p                             reductio ad absurdum
```
Using natural deduction, T15, and *modus ponens*, we have the basic tools for a proof by contradiction:
*  1. ⊢(p⊃~p)⊃~p                             T15
*  2. p ⊢~p                                  Assumed: deduce ~p when given p
*  3. ⊢p⊃~p                                  2 × natural deduction
*  4. ⊢~p                                    1, 3 × *modus ponens*
```
   T16.1: (p⊃q)⊃(~q⊃~p)                        contraposition
   T16.2: (~p⊃~q)⊃(q⊃p)                        contraposition
   T17.1: p⊃~~p                                double negation
   T17.2: ~~p⊃p                                double negation
   T17.3: p≡~~p                                double negation
```
T16.1 through T17.3 are properties of negation.  They are important in the intuitionistic propositional calculus and in Gödel-Dummett algebras because some of these are not valid in those systems.
```
   T18.1: p≡(p∨p)                              tautology
   T18.2: p≡(p∧p)                              tautology
   T19.1: p⊃(p∨q)                              simplification
   T19.2: (p∧q)⊃p                              simplification
   T20.1: (p∨q)≡(q∨p)                          commutation
   T20.2: (p∧q)≡(q∧p)                          commutation
   T21.1: (p∨(q∨r))≡((p∨q)∨r)                  association
   T21.2: (p∧(q∧r))≡((p∧q)∧r)                  association
   T22.1: (p∧(q∨r))≡((p∧q)∨(p∧r))              distribution
   T22.2: (p∨(q∧r))≡((p∨q)∧(p∨r))              distribution
   T23.1: (p∨(p∧q))≡p                          absorption
   T23.1: (p∧(p∨q))≡p                          absorption
```
T18.1 through T23.2 are important in lattice theory.  Not all lattices obey the distributive laws.
```
   T24.1: (p⊃q)⊃(p≡(p∧q))                      subset
   T24.2: (p≡(p∧q))⊃(p⊃q)                      subset
   T24.3: (p⊃q)⊃(q≡(p∨q))                      subset
   T24.4: (q≡(p∨q))⊃(p⊃q)                      subset
```
Taken in pairs (T24.1 with T24.3, or T24.2 with T24.4) these four thorens are essentially definitions which induce a partial order on a lattice. In a system where A2 is not suitable for defining implication, we might use either pair.
```
   T25.1: (p∨F)≡p                              binding
   T25.2: (p∧T)≡p                              binding
   T25.3: (p⊃F)≡~p                             binding
```
These are basic lattice properties for the constants T and F.
```
   T26: (p∨q)≡((p⊃q)⊃q)                      alternate def: Apq
```
This is how disjunction is defined in the Łukasiewicz algebras.  Definition A1, though valid in Ł₂, is not valid those algebras when there are truth values other than T or F.

And we confirm that all these theorems are classically valid:
```
	--> All the theorem schemas are valid.
```

Finally we state three derived Rules:
```
   DR1: If ⊢p and ⊢q, then ⊢(p∧q).                                   adjunction
   DR2: If ⊢(p⊃q) and ⊢~q, then ⊢~p.                              modus tollens
   DR3: If ⊢(~p⊃p), then ⊢p.                                      contradiction
	--> All the transformations are valid.
```
Note that DR3 comes from T15.2, the second form of *reductio ad absurdum*.

## 3. Ł₃, the 3-valued Łukasiewicz algebra

Using our engine for Ł₃ on our database of definitions, wffs, and rules, we find:
```
    Total number of invalid items: 9
```
The possible truth values are reported here as F, I, and T.  The values are ordered F < I < T.  (In fact, F=0, I=1/2, and T=1.)  To be valid, a wff must take on the value T for all possible truth value assignments.

Ł₃ defines generalizes the basic operators in so that when the propositional variables take the values T or F, the result agrees with the corresponding classical operators.  The join and meet operators are defined as maximum and minimum, respectively, so that the lattice properties are preserved.  The implication operator agrees with the definition of a subset in a Boolean algebra -- see theorems T24.1 through T24.4.  Here are the matrix definitions:

```
                p∨q       p∧q       p⊃q       p≡q
    p  ~p    q: F  I  T   F  I  T   F  I  T   F  I  T
   ----------------------------------------------------
    F   T       F  I  T   F  F  F   T  T  T   T  I  F
    I   I       I  I  T   F  I  I   I  T  T   I  T  I
    T   F       T  T  T   F  I  T   F  I  T   F  I  T
```

The first issue that comes up is our definition of material implication:
```
    D2: (p⊃q) := (~p∨q)                      implication
    	   not valid: |p|=I, |q|=I, result=I           (#1)
```
The detected problem is that the operator ~p∨q returns a value of I (not T) when p and q are both I.  If we defined implication this way, then p⊃q would not be valid.

However, we find that T26 is valid, and as noted, this is how disjunction is defined in the Łukasiewicz algebras.

We also find that the implication operator satisfies the defining characteristics of the standard partial order on a lattice, namely T24.1 through T24.4.

The axioms and *modus ponens* are all valid (in stated form):
```
    Axiom Schemas:
       A1: (p∨p)⊃p                              tautology
       A2: q⊃(p∨q)                              addition
       A3: (p∨q)⊃(q∨p)                          permutation
       A4: (p∨(q∨r))⊃(q∨(p∨r))                  association
       A5: (q⊃r)⊃((p∨q)⊃(p∨r))                  summation
	   --> All the axiom schemas are valid.

    Rules of Transformation:
       R1: If ⊢(p⊃q) and ⊢p, then ⊢q.           modus ponens
	   --> All the transformations are valid.
```
The axiom system PM fails for Ł₃ because of a definition!  But this failure will show up in the theorems.

Material equivalence is an equivalence relation in Ł₃ and we can substitute equivalent expressions because the operators are all monotone.  But Ł₃ is not a natural deduction system because T5 fails:
```
    T5: (p⊃(q⊃r))⊃((p⊃q)⊃(p⊃r))              importation
	not valid: |r|=F, |q|=I, |p|=I, result=I           (#2)
```

Pierce's Law also fails.  If we replace q by F in Pierce's Law and then apply the binding rule T25.3 (⊢(p⊃F)≡~p), we get the second form of *reductio ad absurdum*.  Note that T25.3 is valid in Ł₃.
```
    T9: ((p⊃q)⊃p)⊃p                          Pierce
	not valid: |p|=I, |q|=F, result=I                  (#3)
```
We therefore expect *reductio ad absurdum* (RAA) to fail.  Both forms fail
```
   T15.1: (p⊃~p)⊃~p                            reductio ad absurdum
	not valid: |p|=I, result=I                         (#4)
   T15.2: (~p⊃p)⊃p                             reductio ad absurdum
	not valid: |p|=I, result=I                         (#5)
```
Since the double negation law T17.3 (⊢p≡~~p) is valid, if either fails, then both must fail. Pierce's Law and the two forms of RAA are interrelated when taken together with the binding law T25.3 and double negation T17.3.

In Ł₃, exporting a conjunction is valid, but importing it is not:
```
   T11: (p⊃(q⊃r))⊃((p∧q)⊃r)                  importation
	not valid: |r|=F, |p|=I, |q|=I, result=I           (#6)
   T12: ((p∧q)⊃r)⊃(p⊃(q⊃r))                  exportation
            (VALID)
```

The strong form of the law of the excluded and the contradiction law are both invalid.  But the weak form of the excluded middle law is valid.
```
   T13.1: p∨~p                                 tertium non datur
	not valid: |p|=I, result=I                         (#7)
   T13.2: (p⊃q)∨(q⊃p)                          tertium non datur
            (VALID)
   T14: ~(p∧~p)                              contradiction
	not valid: |p|=I, result=I                         (#8)
```

The remaining theorems in the database all hold.  Briefly stated, contrapositives behave well, and all the lattice properties including the distributive laws are valid.

The final failure is in the contradiction rule DR3:
```
   DR3: If ⊢(~p⊃p), then ⊢p.                 contradiction
	 Conclusion p = I when |p|=I and premises hold.    (#9)
```
When natural deduction is available, this rule is equivalent to T15.2.  But in Ł₃, natural deduction fails so the rule and the theorem are not necessarily equivalent.

## 4. Ł₄, the 4-valued Łukasiewicz algebra

As with Ł₃, we have nine items in our database which are not valid in Ł₄.  Note that Ł₃ and Ł₄ are structurally different.  But our database is not rich enough to actually demonstrate the difference.
```
    Total number of invalid items: 9
```

The truth values are F=0 (false), I=1/3, J=2/3, and T=1 (true).  Values I and J are to be thought of as intermediate, with I closer to F and J closer to T.  As in Ł₃, joins take the larger value and meets take the smaller value.  Here are the tables for the connectives:
```
                p∨q          p∧q          p⊃q          p≡q
    p  ~p    q: F  I  J  T   F  I  J  T   F  I  J  T   F  I  J  T
   ---------------------------------------------------------------
    F   T       F  I  J  T   F  F  F  F   T  T  T  T   T  J  I  F
    I   J       I  I  J  T   F  I  I  I   J  T  T  T   J  T  J  I
    J   I       J  J  J  T   F  I  J  J   I  J  T  T   I  J  T  J
    T   F       T  T  T  T   F  I  J  T   F  I  J  T   F  I  J  T
```
The matrix for p⊃q is essentially upper triangular -- true on the diagonal and in the upper triangle.  In the lower triangle, values F, I and J reflect the distance from the diagonal -- F in the lower corner, I in the the band running northwest from T⊃I, and J in the band rumming northwest from T⊃J.

The matrix for p≡q is the same as that for p⊃q in the lower triangle and on the diagonal.  In the upper triangle, banding mirrors the lower triangle. 

Here are the database entries which fail in Ł₄:
```
    Definitions:
        D2: (p⊃q) := (~p∨q)                      implication
	       not valid: |q|=I, |p|=I, result=J
    Theorem Schemas:
        T5: (p⊃(q⊃r))⊃((p⊃q)⊃(p⊃r))              importation
	       not valid: |p|=I, |r|=F, |q|=I, result=J
        T9: ((p⊃q)⊃p)⊃p                          Pierce
	       not valid: |p|=I, |q|=F, result=J
        T11: (p⊃(q⊃r))⊃((p∧q)⊃r)                 importation
	       not valid: |q|=I, |r|=F, |p|=I, result=J
        T13.1: p∨~p                                 tertium non datur
	       not valid: |p|=I, result=J
        T14: ~(p∧~p)                              contradiction
	       not valid: |p|=I, result=J
        T15.1: (p⊃~p)⊃~p                            reductio ad absurdum
	       not valid: |p|=I, result=J
        T15.2: (~p⊃p)⊃p                             reductio ad absurdum
	       not valid: |p|=I, result=J
    Derived Rules:
        DR3: If ⊢(~p⊃p), then ⊢p.                 contradiction
	       Conclusion p = J when |p|=J and premises hold.
```

These results differ in value from the results for Ł₃, but the same wffs and rules are invalid.  As noted in the outset, this small database is not rich enough to show differences in the set of theorems and rules.  But its clear that there are classical theorems and rules which are not valid in Ł₄.

In particular, given the faileure of T5, Ł₄ is not a natural deduction system.

## 5. G₃, 3-valued Gödel-Dummett algebra

The Gödel-Dummett algebras use the same matrix definitions for joins and meets, but differ in how negation, implication, and equivalence are defined.  Here are the matrices for G₃:
```
                p∨q       p∧q       p⊃q       p≡q
    p  ~p    q: F  I  T   F  I  T   F  I  T   F  I  T
   ----------------------------------------------------
    F   T       F  I  T   F  F  F   T  T  T   T  F* F
    I*  F       I  I  T   F  I  I   F* T  T   F* T  I
    T   F       T  T  T   F  I  T   F  I  T   F  I  T
```
The starred entries mark the differences with the matrices for Ł₃. Gödel-Dummett algebras set `|~p|=F` whenever `|p|<T`.  For implication, `|p⊃q|=|q|` whenever `|p|>|q|`. The matrix for negation breaks symmetry.  The matrix for material equivalence is symmetric, but it differs from the corresponding matrix for Ł₃.

The consequences for our database are:
* there are more discrepancies; and
* the discrepances are not all in the same places.

We detected one additional discrepancy:
```
    Total number of invalid items: 10
```

But we need to look at where the discrepancies occur...

```
Definitions:
    D1: (p∧q) := ~(~p∨~q)                    conjunction
	   not valid: |q|=I, |p|=I, result=I           (#1)
    D2: (p⊃q) := (~p∨q)                      implication
	   not valid: |q|=I, |p|=I, result=I           (#2)
```
DeMorgan's law fails (D1) because negation breaks symmetry.  The definition of implication from negation and disjunction (joins) also fails, but the alternate definition in T26 (used in the standard axioms for Ł₃)  is also not valid.  We can, however, use the set relations in T24,1 through T24.4 to define implication in terms of either joins and equivalence or meets and equivalence. 

The axiom schemas are all valid, but this is no suprise since these are based on lattice axioms.  *Modus ponens* is also valid.

Material equivalence is an equivalence relation (T1, T2, T3), and is also monotone (T4.1 through T4.7) with respect to the five basic connectives.  So substitution of equivalences holds as a meta-rule.  Material implication is a partial order (T6, T7, T8).

The system supports natural deduction since T5 is valid.  This is a significant difference between the Gödel-Dummett algebras and the Łukasiewicz algebras.

The distributive lattice properties (T18 through T24) all hold.  The binding properties (T25) also hold, so the lattice is complete.

The two dilemma arguments (T10), import (T11.1) and export (T11.2) all hold.  Note that import is not valid in Ł₃.

That leaves only a few theorems in the database that need some discussion: 
```
Theorem Schemas:
    T9: ((p⊃q)⊃p)⊃p                          Pierce
	   not valid: |q|=F, |p|=I, result=I           (#3)
   T13.1: p∨~p                                 tertium non datur
	   not valid: |p|=I, result=I                  (#4)
   T13.2: (p⊃q)∨(q⊃p)                          tertium non datur
   T14: ~(p∧~p)                              contradiction
   T15.1: (p⊃~p)⊃~p                            reductio ad absurdum
   T15.2: (~p⊃p)⊃p                             reductio ad absurdum
	   not valid: |p|=I, result=I                  (#5)
   T16.1: (p⊃q)⊃(~q⊃~p)                        contraposition
   T16.2: (~p⊃~q)⊃(q⊃p)                        contraposition
	   not valid: |q|=T, |p|=I, result=I           (#6)
   T17.1: p⊃~~p                                double negation
   T17.2: ~~p⊃p                                double negation
	   not valid: |p|=I, result=I                  (#7)
   T17.3: p≡~~p                                double negation
	   not valid: |p|=I, result=I                  (#8)
   T26: (p∨q)≡((p⊃q)⊃q)                      alternate def: Apq
	   not valid: |q|=F, |p|=I, result=I           (#9)
```
Pierce's Law (T9) fails, as it does in Ł₃.

The strong form of the law of the excluded middle (T13.1) fails, as it does in Ł₃.  The weak form (T13.2) is valid, and indeed, it is what must be added to the intuitionistic propositional calculus (or IPC) to produce the weakest of the Gödel-Dummett algebras.  Contradiction (T14) is valid -- it fails in Ł₃.

*Reductio ad absurdum* is valid when proving a negative (T15.1), but not when proving a positive (T15,2).  The same situation holds in the IPC, but in Ł₃ neither form is valid.

Contrapositives are valid in some cases (*e.g.* T16.1) but fail in some others  (*e.g.* T16.2).  Negation in G₃ once again breaks symmetry.  Both forms are valid in Ł₃.

Double negation is valid when proving a negative (as in T17.1) but not when proving a positive (T17.2) or when one side of an equivalence is positive (T17.3).

Finally, as mentioned before, T26 which is used as a definition in the Łukasiewicz algebras fails for the Gödel-Dummett algebras.

Our database fails in one more place:
```
Derived Rules:
   DR1: If ⊢p and ⊢q, then ⊢(p∧q).                 adjunction
   DR2: If ⊢(p⊃q) and ⊢~q, then ⊢~p.               modus tollens
   DR3: If ⊢(~p⊃p), then ⊢p.                       contradiction
	 Conclusion p = I when |p|=I and premises hold.    (#10)
```

Our result for DR3 agrees with T15.2.  But note that the following rule is *valid*:
```
   DR3': If ⊢(p⊃~p), then ⊢~p.
```

Note also that a the following variation of *modus tollens* is not valid:
```
   DR2': If ⊢(~p⊃q) and ⊢q, then ⊢p.               modus tollens
```

*N.B.*: Based on comments above, we have added a few theorems and rules to the database.  Try running the script to see what's new.

## 6. G₄, 4-valued Gödel-Dummett algebra

The truth values are F=0 (false), I=1/3, J=2/3, and T=1 (true).  Values I and J are to be thought of as intermediate, with I closer to F and J closer to T.  As in Ł₃, joins take the larger value and meets take the smaller value.  Here are the tables for the connectives:
```
                p∨q          p∧q          p⊃q          p≡q
    p  ~p    q: F  I  J  T   F  I  J  T   F  I  J  T   F  I  J  T
   ---------------------------------------------------------------
    F   T       F  I  J  T   F  F  F  F   T  T  T  T   T  F  F  F
    I   F       I  I  J  T   F  I  I  I   F  T  T  T   F  T  I  I
    J   F       J  J  J  T   F  I  J  J   F  I  T  T   F  I  T  J
    T   F       T  T  T  T   F  I  J  T   F  I  J  T   F  I  J  T
```

The database is not (yet!) sufficiently refined to distinguish between G₃ and G₄.  See the remarks above.

## 7. ℒ(4), the lattice of divisors of 4

### A note on divisor logic

The tests in these next few sections involve propositional calculus developed from lattices of divisors. We start with the positive integers which evenly divide of some integer larger than one. (We'll refer to this integer in general as n.) The AND operator (conjunction or meet) returns the GCD (greatest common divisor) of its arguments, and the OR operator (disjunction or join) returns the LCM (least common multiple). Together, these operations form an algebraic structure called a lattice.

We also define negation and implication operators on these lattices.  There are many ways of doing this, and the appeal of the results depend largely on the eye of the beholder.  (This is my first attempt.  I was inspired by a very cursory scan of an exercise in Paul Rosenbloom's *Elements of Mathematical Logic* (Dover, 1950).  I haven't actually read the exercise yet, but it did mention the divisors of 30 on connection with many-world models of Clarence Lewis's calculi of strict implication known as S1, S2, and so on through S9.)

If the number is a product of distinct primes, the result can be viewed as a two-valued propositional calculus with each prime associated with a separate possible world (or universe).  Depending on how negation and implication are implemented, there may be interactions between the worlds, or the worlds may be completely independent.  2, 6 and 30 are examples of products of distinct primes.   ℒ(2) is a two-valued one-world calculus, and  ℒ(6) is a two-valued two-world calculus, while ℒ(30) is a two-valued three-world calculus.

If a divisor is a prime power (*i.e.*, a prime raised to a power *greater* than one), then the lattice has a many-valued world.  For example 4, 36, and 900 are squares which are products of one, two, and three squared primes.  The number of truth values in a prime's world is one more than the power of the prime in the (unique!) factorization.  So ℒ(4), ℒ(36), and ℒ(900) are all three-valued calculi respectively with one world, two world, and three worlds.

Negation was implemented in a manner consistent with the Łukasiewicz algebras (which are also lattices).  The Łukasiewicz algebras work with min-max lattices.  The negation operator maps the element of a given rank to its coranked ("corank" = "complementary rank") partner.  For negation, we mapped each divisor to its codivisor (*i.e.*, its complementary divisor).  For  example, in ℒ(36), the negations of 1, 2 and 12 are respectively 36, 18, and 3.  For ℒ(n) the definition is:
```
        |~p| := n / |p|.
```
For a divisor logic which more closely resembles a Gödel-Dummett algebra, the definition would need to be:
```
        |~p| := n if |p|=1, and 1 in all other cases.
```

Material implication was more difficult.  Obviously we have:
```
        |p⊃q| := n whenever |p| evenly divides |q|; and         (1)
        |p⊃q| := 1 whenever |p|=n and |q|=1.                    (2)
        |p⊃q| is not n whenever |q| is not a multiple of |p|.   (3)
```
Point (2) is for agreement with the two-valued calculus as the value 1 corresponds to false in all worlds, while n indicates that a statement absolutely true in all worlds.  Point (1) does insures that the remaining two-valued cases holds, but, it is also the most natural divisor lattice generalization of |p|≤|q| for min-max lattices.

Point (3) is the sticky one.  We want p⊃q to be a partial order, and for many-world algebras, we'd like material implication to keep the worlds independent of one another.  But we'd also like to keep computations as simple as possible.  (Computing the GCD and the LCM is straightforward and fast using Euclid's algorithm -- one does not need to factor anything in order to compute them.  (Finding the divisors of, however, does require factoring!) 

In the tests below, for case (3) we used:
```
  (3.1) |p⊃q| := GCD(|p|, |q|) whenever |q| is not a multiple of |p|.
``` 
This choice led to some interesting but undesirable results.

Our second set of trials (logic.divisor2 and logic.tests.pm2) used the following definition for case (3):
```
  (3.2) |p⊃q| := n / LCM(|p|, |q|) whenever |q| is not a multiple of |p|.
```
The results were even worse.  (Again, beauty here is in the eye of the beholder.)

The third set of trials (logic.divisor3 and logic.tests.pm3) gave satisfactory results:
```
  (3.3) |p⊃q| := n|q| / LCM(|p|, |q|) whenever |q| is not a multiple of |p|.
```
For two-valued many-world calculi, this model completely satisfied the classical propositional calculus.

Here we focus on the results of our attempts using the GCD as the result, *i.e.* implication defined using points (1), (2) and (3.1).

### And, returning to ℒ(4)

The set of divisors of 4 (in the positive integers) is {1, 2, 4}).

If we had chosen any prime number p for our lattice (*e.g.* `p=17`), we would have just two divisors, 1 and p (*e.g.* `ℒ(17)={1,17}`). In this case our lattice of divisors is isomorphic to (*i.e.* structurally the same as) the classical propositional calculus.

There are twelve differences from the definitions, axioms, theorems, and rules that are recorded in the current database:
```
Total number of invalid items: 12
```

The PM definition of material implication doesn't work for the natural partial ordering in the lattice:
```
Definitions:
    D2: (p⊃q) := (~p∨q)                      implication
	   not valid: |p|=2, |q|=1, result=1           (#1)
```

The axioms in the *Principia Mathematica* and *modus ponens* are valid in ℒ(4).  Lattice properties hold, and material implication is defined as in T24.1 through T24.4.

Here are the remaining discrepancies:
```
Theorem Schemas:
    T4: (p≡q)⊃(~p⊃~q)                        monotony
        	not valid: |p|=2, |q|=4, result=1          (#2)
```
Negation is not monotone given our default method for computing implication.  Using the indicated failure:
```
        p   ~p  q   ~q  p⊃q q⊃p p≡q ~p⊃~q   (p≡q)⊃(~p⊃~q)
        2    2   4   1   4   2   2    1          1
            4/2     4/4 top gcd min  gcd        gcd
```
*N.B.*: there are other ways of defining material implication the antecedent does not divide the subsequent.  The third line states how we computed each value.  Note that we used the *GCD* to compute the value of failed implications.

```
    T9: ((p⊃q)⊃p)⊃p                          Pierce
        not valid: |p|=2, |q|=1, result=2          (#3)
   T13: p∨~p                                 tertium non datur
	   not valid: |p|=2, result=2                  (#4)
   T14: ~(p∧~p)                              contradiction
	   not valid: |p|=2, result=2                  (#5)
   T15.1: (p⊃~p)⊃~p                            reductio ad absurdum
	   not valid: |p|=2, result=2                  (#6)
   T15.2: (~p⊃p)⊃p                             reductio ad absurdum
	   not valid: |p|=2, result=2                  (#7)
```
These five are fail in Ł₃.  But T5 (used to prove natural deduction) and import (T11) both suuceed here and fail in Ł₃.

```
   T16.1: (p⊃q)⊃(~q⊃~p)                        contraposition
	   not valid: |p|=4, |q|=2, result=1           (#8)
   T16.2: (~p⊃~q)⊃(q⊃p)                        contraposition
	   not valid: |p|=1, |q|=2, result=1           (#9)
```
Contrapositives fail in ℒ(4), but double negation succeeds.  These two failures and the failure of T4 indicate that the gcd might not be the best choice for handling a failed implication.

```
   T25.3: (p⊃F)≡~p                              binding
	   not valid: |p|=2, result=1                  (#10)
```
The failure of T25 might help to determine a better approach to defining implication.

```
   T26: (p∨q)≡((p⊃q)⊃q)                       alternate def: Apq
	   not valid: |p|=2, |q|=1, result=2           (#11)
```
This is a definition in Ł₃.

```
Derived Rules:
   DR3: If ⊢(~p⊃p), then ⊢p.                  contradiction
	 Conclusion p = 2 when |p|=2 and premises hold.    (#12)
```
Not surprising as RAA also fails

If we look at the square of any prime number p, we get an isomorphic structure.  This particular lattice of divisors is a 3-valued propositional caclulus which is isomorphic to neither Ł₃ nor G₃.  More thought needs to be given to the failure vectors in the implication operator.


# 8. ℒ(6), lattice of divisors of 6

The set of divisors of 6 (in the positive integers) is {1, 2, 3, 6}.  Any lattice of divisors generated by the product of two primes will be isomorphic.

Whereas ℒ(4) is a three-valued calculus, ℒ(6) is a three-world calculus with just two values in each world:
```
                        6=TT                4=T
                        /  \                 |
                       /    \                |
                     2=TF   3=FT            2=I
                       \    /                |
                        \  /                 |
                        1=FF                1=F

                        ℒ(6)                ℒ(4)
```
The negation operator was defined as `|~p|=4/|p|` in ℒ(4), and as `|~p|=6/|p|` in ℒ(6).  This generalizes negation in the Łukasiewicz algebras to multiple worlds.  For ℒ(n), the rule is `|~p|=n/|p|`.  The real issue is how to *best* define implication when it fails, *i.e.* in the lower diagonal.  We have elected to use the *GCD* -- and we note that it leads to some undesirable features.  Be that as it may, we proceed with this working definition:
```
                    ┏
                    ┃  n, if |p| ≤ |q|, and
            |p⊃q| = ┫
                    ┃  gcd(|p|, |q|), if |p|>|q|.
                    ┗
```

The number of failures detected in our database was 17, so our database is rich enough to distinguish between a two-world binary model (like ℒ(6)) and a single-world ternary model (like ℒ(4)).

In the axiomatization, the only problem is the definition of implication:
```
Definitions:
    D2: (p⊃q) := (~p∨q)                      implication
	   not valid: |q|=1, |p|=2, result=1               (#1)
```
The axioms and modus ponens are fine.  But material equivalence goes haywire -- it is not transitive (T3) -- a bad sign!  We also lose the monotonic properties (T4).  We do have natural deduction (T5).
```
Theorem Schemas:
    T1: p≡p                                  reflexivity
    T2: (p≡q)⊃(q≡p)                          symmetry
    T3: (p≡q)⊃((q≡r)⊃(p≡r))                  transitivity
	   not valid: |p|=2, |r|=3, |q|=6, result=1        (#2)
    T4.1: (p≡q)⊃(~p⊃~q)                        monotony
	   not valid: |q|=6, |p|=2, result=1               (#3)
    T4.2: (p≡q)⊃((p∨r)⊃(q∨r))                  monotony
    T4.3: (q≡r)⊃((p∨q)⊃(p∨r))                  monotony
    T4.4: (p≡q)⊃((p∧r)⊃(q∧r))                  monotony
	   not valid: |q|=2, |r|=3, |p|=6, result=1        (#4)
    T4: (q≡r)⊃((p∧q)⊃(p∧r))                     monotony
	   not valid: |p|=2, |r|=3, |q|=6, result=1        (#5)
    T4: (p≡q)⊃((p⊃r)⊃(q⊃r))                     monotony
	   not valid: |q|=2, |r|=3, |p|=6, result=1        (#6)
    T4: (q≡r)⊃((p⊃q)⊃(p⊃r))                     monotony
	   not valid: |p|=2, |r|=3, |q|=6, result=1        (#7)
    T5: (p⊃(q⊃r))⊃((p⊃q)⊃(p⊃r))              importation
```

Implication is no longer transitive, and Pierce's law fails.  T8.2 is the same as T3.
```
    T8.1: (p⊃q)⊃((q⊃r)⊃(p⊃r))                  transitivity
	   not valid: |p|=2, |r|=3, |q|=6, result=1        (#8)
    T8.2: (p≡q)⊃((q≡r)⊃(p≡r))                  transitivity
	   not valid: |p|=2, |r|=3, |q|=6, result=1        (#9)
    T9: ((p⊃q)⊃p)⊃p                          Pierce
	   not valid: |p|=2, |q|=1, result=2               (#10)
```

Exporting fails, but this is also a feature of the Lewis modal systems S2 and S3.  That might actually be a good feature.
```
   T12: ((p∧q)⊃r)⊃(p⊃(q⊃r))                  exportation
	   not valid: |q|=2, |r|=1, |p|=3, result=1        (#11)
```

The law of the excluded middle passes in its strong form (as it does in even the weakest Lewis modal systems S1 and even S1⁰).  The weak form (T13.2) fails.
```
   T13.1: p∨~p                                 tertium non datur
   T13.2: (p⊃q)∨(q⊃p)                          tertium non datur
	   not valid: |p|=2, |q|=3, result=1               (#12)
```

Contradiction, double negation, and RAA all pass, but the contrapositive fails:
```
   T14: ~(p∧~p)                              contradiction
   T15: (p⊃~p)⊃~p                            reductio ad absurdum
   T15: (~p⊃p)⊃p                             reductio ad absurdum
   T16: (p⊃q)⊃(~q⊃~p)                        contraposition
	   not valid: |p|=6, |q|=2, result=1               (#13)
   T16: (~p⊃~q)⊃(q⊃p)                        contraposition
	   not valid: |p|=1, |q|=2, result=1               (#14)
   T17: p⊃~~p                                double negation
   T17: ~~p⊃p                                double negation
   T17: p≡~~p                                double negation
```

The distributive lattice properties all hold, but one of the partial order definitions fails -- an important clue:
```
   T24.4: (q≡(p∨q))⊃(p⊃q)                      subset
	   not valid: |q|=2, |p|=3, result=1               (#15)
```

And two more failures for implication:
```
   T25.3: (p⊃F)≡~p                             binding
	   not valid: |p|=2, result=1                      (#16)
   T26: (p∨q)≡((p⊃q)⊃q)                      alternate def: Apq
	   not valid: |q|=1, |p|=2, result=2               (#17)
```

The three derived rules are all valid.


## 9. ℒ(30),lattice of divisors of 30

Since we have three primes, 2, 3, and 5, whose product is 30, this is a three-word binary calculus.  For example, 10 indicate true in worlds 2 and 5 and false in world 3.

The 17 failures are as for ℒ(6)

Definitions:
```
    D2: (p⊃q) := (~p∨q)                      implication
        	not valid: |q|=1, |p|=2, result=1
```

Theorem Schemas:
```
    T3: (p≡q)⊃((q≡r)⊃(p≡r))                  transitivity
        	not valid: |r|=2, |q|=6, |p|=3, result=1
    T4.1: (p≡q)⊃(~p⊃~q)                        monotony
        	not valid: |q|=6, |p|=2, result=1
    T4.2: (p≡q)⊃((p∨r)⊃(q∨r))                  monotony
    T4.3: (q≡r)⊃((p∨q)⊃(p∨r))                  monotony
    T4.4: (p≡q)⊃((p∧r)⊃(q∧r))                  monotony
        	not valid: |r|=2, |q|=3, |p|=6, result=1
    T4.5: (q≡r)⊃((p∧q)⊃(p∧r))                  monotony
        	not valid: |r|=2, |q|=6, |p|=3, result=1
    T4.6: (p≡q)⊃((p⊃r)⊃(q⊃r))                  monotony
        	not valid: |r|=2, |q|=3, |p|=6, result=1
    T4.7: (q≡r)⊃((p⊃q)⊃(p⊃r))                  monotony
        	not valid: |r|=2, |q|=6, |p|=3, result=1
                    ...
    T8.1: (p⊃q)⊃((q⊃r)⊃(p⊃r))                  transitivity
        	not valid: |r|=2, |q|=6, |p|=3, result=1
    T8.2: (p≡q)⊃((q≡r)⊃(p≡r))                  transitivity
        	not valid: |r|=2, |q|=6, |p|=3, result=1
    T9: ((p⊃q)⊃p)⊃p                          Pierce
	    not valid: |p|=2, |q|=1, result=2
                    ...
   T12: ((p∧q)⊃r)⊃(p⊃(q⊃r))                  exportation
	   not valid: |r|=1, |q|=2, |p|=3, result=1
   T13.1: p∨~p                                 tertium non datur
   T13.2: (p⊃q)∨(q⊃p)                          tertium non datur
	   not valid: |p|=2, |q|=3, result=1
                    ...
   T16.1: (p⊃q)⊃(~q⊃~p)                        contraposition
       not valid: |p|=6, |q|=2, result=1
   T16.2: (~p⊃~q)⊃(q⊃p)                        contraposition
	   not valid: |p|=1, |q|=2, result=1
                    ...
   T24.4: (q≡(p∨q))⊃(p⊃q)                      subset
	   not valid: |q|=2, |p|=3, result=1
   T25.3: (p⊃F)≡~p                             binding
	   not valid: |p|=2, result=1
   T26: (p∨q)≡((p⊃q)⊃q)                      alternate def: Apq
	   not valid: |q|=1, |p|=2, result=2
                    ...
    Total number of invalid items: 17
```

## 10. ℒ(60) (lattice of divisors of 60)

Since 60=2²⋅3⋅5, we have a three world scenario where world 2 is ternary (T,I,F) and worlds 3 and 5 are binary (T,F).  The 22 failures seem to be the union of what goes wrong in ℒ(6) (two binary worlds and what goes wrong in ℒ(4) (one ternary world).

We save the problems here:
```
Definitions:
    D2: (p⊃q) := (~p∨q)                      implication
	   not valid: |q|=1, |p|=2, result=1
Theorem Schemas:
    T3: (p≡q)⊃((q≡r)⊃(p≡r))                  transitivity
	   not valid: |r|=2, |p|=3, |q|=6, result=1
    T4.1: (p≡q)⊃(~p⊃~q)                        monotony
	   not valid: |q|=4, |p|=2, result=1
    T4.3: (p≡q)⊃((p∨r)⊃(q∨r))                  monotony
    T4.3: (q≡r)⊃((p∨q)⊃(p∨r))                  monotony
    T4.4: (p≡q)⊃((p∧r)⊃(q∧r))                  monotony
	   not valid: |r|=2, |q|=3, |p|=6, result=1
    T4.5: (q≡r)⊃((p∧q)⊃(p∧r))                  monotony
	   not valid: |r|=2, |p|=3, |q|=6, result=1
    T4.6: (p≡q)⊃((p⊃r)⊃(q⊃r))                  monotony
	   not valid: |r|=2, |q|=3, |p|=6, result=1
    T4.7: (q≡r)⊃((p⊃q)⊃(p⊃r))                  monotony
	   not valid: |r|=2, |p|=3, |q|=6, result=1
                    ...
    T8.1: (p⊃q)⊃((q⊃r)⊃(p⊃r))                  transitivity
	   not valid: |r|=2, |p|=3, |q|=6, result=1
    T8.2: (p≡q)⊃((q≡r)⊃(p≡r))                  transitivity
	   not valid: |r|=2, |p|=3, |q|=6, result=1
    T9: ((p⊃q)⊃p)⊃p                          Pierce
	   not valid: |p|=2, |q|=1, result=2
                    ...
   T12: ((p∧q)⊃r)⊃(p⊃(q⊃r))                  exportation
	   not valid: |r|=1, |q|=2, |p|=3, result=1
   T13: p∨~p                                 tertium non datur
	   not valid: |p|=2, result=30
   T13: (p⊃q)∨(q⊃p)                          tertium non datur
	   not valid: |p|=2, |q|=3, result=1
   T14: ~(p∧~p)                              contradiction
	   not valid: |p|=2, result=30
   T15: (p⊃~p)⊃~p                            reductio ad absurdum
	   not valid: |p|=2, result=30
   T15: (~p⊃p)⊃p                             reductio ad absurdum
	   not valid: |p|=30, result=30
   T16: (p⊃q)⊃(~q⊃~p)                        contraposition
	   not valid: |p|=4, |q|=2, result=1
   T16: (~p⊃~q)⊃(q⊃p)                        contraposition
	   not valid: |p|=1, |q|=2, result=1
                    ...
   T24.4: (q≡(p∨q))⊃(p⊃q)                      subset
	   not valid: |q|=2, |p|=3, result=1
                    ...
   T25.3: (p⊃F)≡~p                             binding
	   not valid: |p|=2, result=1
   T26: (p∨q)≡((p⊃q)⊃q)                      alternate def: Apq
	   not valid: |q|=1, |p|=2, result=2
	--> 20 theorem schemas are not valid.
Derived Rules:
   DR3: If ⊢(~p⊃p), then ⊢p.                 contradiction
	 Conclusion p = 30 when |p|=30 and premises hold.
                    ...
        Total number of invalid items: 22
```
