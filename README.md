# Science Toolbox

This is a small toolbox for solving (or at least demonstrating) toy problems in the sciences.  These probably will not be useful for serious research work, but they might be adequate for use in homework problems in some undergraduate courses.

There isn't any particular rhyme or reason to what goes in this repository other than it's a mix of topics that has caught my fancy.  As a result, there may be some duplication here and there.

The programming here is mainly in Python.  But I reserve the right to program in any language (including COBOL and Fortran!) as I happen to see fit.

# 1 Mathematics

## 1.1 Utilities

See the README.md file in the *utilities* folder.

## 1.2 Demos

The *basel1* and *basel2* demonstration modules use Euler's solution the Basel Problem to estimate the value of π.  The result, though both beautiful and important, is not very practical for this particular purpose.  See the module's *docstring* for additional information and some historical background.  (Wikipedia and MathWorld both have fairly detailed articles on the Basel Problem.)

## 1.3 Symbolic Logic

### 1.3.1 Nonstandard propositional logics

The *logic* folder contains some programs which work with symbolic logic -- with propositional logic -- in particular, modal and many-valued logic.  Check the *messages* folder for some output (*.txt* extension) and some analysis (markdown files, *.md* extension).

### 1.3.2 Combinatory logic

The *logic.curry* module deals with combinatory logic. It can be run as a demonstration script and it can be incorporated into test programs.  See the *logic/tests* folder for examples like *curry1* and *curry2*.  The presentation is based on the discussion in *Elements of Mathematical Logic* by Paul Rosenbloom (*pp* 109-133).

As implemented here, combinatory logic deals with two kinds of objects, a single binary operator (called application) and a set of constants (functions).  The application operator maps a pair of functions to a function.  In the formulation by Rosenbloom, every function is obtained using the application operator from just two constants, A and K, which are defined by the following rules, written using Polish (prefix) notation:

* |||Afgh = ||fh|gh; and
* ||Kfg = f.

The stroke operator is the application operator.  In infix notation, we would write:

* ((A|f)|g)|h = (f|h)|(g|h);
* (K|f)|g = f.

Two functions are equal if the have the same effect.  For example, consider an identity function I.  Using typical functional notation, we would write I(f)=f.  In infix form using the stroke, we would write I|f=f.  In Polish notation, we instead write |If=f.  (The principal advantage of Polish notation is that we don't need parentheses.)  So is there an identity function in combinatory logic?  The answer is yes:

```
    |||AKKf = ||Kf|Kf = f, for all functions f.  So ||AKK=I.
```

Note that we can construct I in other ways, for example:
```
    |||AKAf = ||Kf|Af = f, for all f.  So ||AKA=I.
    |||||A|KAKI fg = |||||KAI|KIfg = |||A|KIfg
                    = |||KIg|fg = |I|fg = |fg = ||Ifg, for all f and g.
        Then ||||A|KAKIf = |If for all f.
        Then |||A|KAKI = I.
```

Combinatory logic is rich enough to form a model of computing, like Conway's Life and Turing machines.  In module *logic.tests.curry3*, I do most of exercises 3 and 5 (*pp* 130-131 in Rosenbloom) which develop a model of primitive recursive arithmetic inside combinatory logic.  Towards the end of that demonstration, I show how one can recursively define a one-sided subtraction operator, and I show with a few examples that it does actually work.

*(The computer language Lisp, developed in the late 1950s, was based on combinatoric logic.  The language Scheme is a descendant of Lisp.  Lambda operators in languages like Python are based on more compact ways of defining functions than to representing them as applications of the constant functions A and K.  The notion of a decorator in Python, a function with one argument, is built into combinatory logic -- every function that can be defined using applications of A and K is really nothing more than a decorator.)*

# 2 Biology

## 2.1 Genetics

*package:* **Genes**

A collection of modules dealing with what is generally called the *genetic code*.  The simplest of these problems is protein-encoding, determining the sequence of amino acids produced by a sequence of nucleotides in a strand of DNA or RNA.

* module: *amino_acid*: a database of amino acids.  The database includes the 20 amino acids involved in the standard encoding.  Others may be added.
* module: *RNA_codons*: a table of codons and a protein-encoder for the standard model of RNA encoding.  (This is the fundamental table.)
* module: *DNA_codons*: a table of codons and a protein-encoder for the standard model of DNA encoding.  (This table is derived from the table in module *RNA_codons*.)
* module: *mitochondrial*: for deriving the codon tables for vertibrate mitochondrial DNA or RNA.

## 2.2 Ecology

*package:* **ecology**

A collection of modules dealing with ecology.

### 2.2.1 Population density models

Numerical approximation of ordinary differential equations:

* module: *predator_prey*: the Lotka-Volterra two-species predator-prey model
* module: *competition*: a two-species competition model based on the logistic differential equation
