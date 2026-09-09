# Models of propositional logic

The classed defined in this folder are intended as a toolbox for testing models of propositional logic with an emphasis on many-valued logics and possible world logics.

## Logic engines

Module *logic.boolean* defines class *BooleanLogic* which can be used in a single world scenario to test conjectures in the classical propositional calculus, and in multiple worlds scenarios, the class can be used to test conjectures in Lewis-style strict implication algebras.  (The multiple worlds scenarios involve only a finite number of worlds, so the Lewis algebras can only be approximated.)

Module *logic.lukasiewicz* defines class *LukasiewiczLogic* which can be used in a single world scenario to test conjectures in finitely many-valued Łukasiewicz propositional calculi.  In multiple worlds scenarios, the class can be used to test conjectures in Lewis-style extensions of these Łukasiewicz algebras.

Module *logic.godel* defines class *GodelLogic* which can be used in a single world scenario to test conjectures in finitely many-valued Gödel-Dummett (aka Gödel aka Dummett) propositional calculi. In multiple worlds scenarios, the class can be used to test conjectures in Lewis-style extensions of these Gödel-Dummett algebras.

Module *logic.post* defines class *PostLogic* which implements finite Post algebras in single-world and multiple-world scenarios.  Post algebras, developed by Emil Post in 1921, are briefly discussed in Section 4 of Paul Rosenbloom's book *Elements of Mathematical Logic*, originally published by the Dover Press (New York) in 1950.

## Formulas and rules

Module *logic.wff* defines various propositional operators (class *Constant*, class *Variable*, class *UnaryOperator*, and class *BinaryOperator*) and uses these operators to build well-formed formula (class *WFF*) which can be used in conjunction with the logic engines to evaluate them as needed.  One application is to test whether a given formula is logically valid in a given scenario.

Module *logic.deductions* defines simple rules of transformation (class *Rule*), for example, *modus ponens*. The logic engines can be used to test whether a given rule is logically valid in a given scenario.

## A note on parentheses

Setting up a well-formed formula (or *wff*) happens in two steps.  The first step is to create an instance which assigns a logic engine.  The second step is to use Polish notation to build the wff.  The wffs are displayed in fully-parenthesized infix notation.  Binary operations are enclosed in parentheses -- unary operators, constants, and variables are not parenthesized, and if the entire wff is parenthesized, then the outermost parentheses are discarded.

For example, consider a wff representing a hypothetical syllogism for strict implication:
```
                infix               Polish
          ((p⇒q)∧(q⇒r))⇒(p⇒r)    IKIpqIqrIpr
```
The outermost parentheses, which enclose the hypothesis `((p⇒q)∧(q⇒r))`, the strict implication operator `⇒` and the conclusion `(p⇒r)`, have been discarded.  The binary expressions in the hypothesis and the conclusion are fully enclosed.

Consider the following expression:
```
                infix               Polish
          ◇p⇒▫◇p                 IPpMPp
```
The scope of the possibility operators is immediate, covering `p`, and the scope of the necessity operator `▫` spans `◇p`.  If we wanted the first possibility operator to span the implication, we would need parentheses:
```
                infix               Polish
          ◇(p⇒▫◇p)               PIpMPp
```
Polish notation shows the functional form of the expression:
```
          PIpMPp          ->     P(I(p, M(P(p)))
          IPpMPp          ->     I(P(p), M(P(p)))
          IKIpqIqrIpr     ->     I(K(I(p,q), I(q,r)), I(p,r))
```

## Caveat emptor

Note that setting up a test using the logic toolbox is not a trivial programming task.  The modules above can be executed as main modules, and the testing code in the main portion can be used as a how-to guide.

Folder *logic.tests* includes tests of specific scenarios.  These test programs can also be used as guides.

There are undoubtedly better ways of organizing these modules.  In particular, I don't like the two-step approach to defining a well-formed formula.