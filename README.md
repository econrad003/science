# Science Toolbox

This is a small toolbox for solving (or at least demonstrating) toy problems in the sciences.  These probably will not be useful for serious research work, but they might be adequate for use in homework problems in some undergraduate courses.

# 1 Mathematics

## 1.1 Utilities

See the README.md file in the *utilities* folder.

## 1.2 Demos

The *basel1* demonstration module uses Euler's solution the Basel Problem to estimate the value of π.  The result, though both beautiful and important, is not very practical for this particular purpose.  See the module's *docstring* for additional information and some historical background.  (Wikipedia and MathWorld both have fairly detailed articles on the Basel Problem.)

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
