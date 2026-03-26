# The Messages Folder

## File types

Two types of files are here: markdown files (*filename.md*) and Unicode text files (*filename.txt*).

The markdown files can be read in a markdown reader or any web browser that supports markdown.  At present, most web browsers require an add-on in order to natively support markdown.  For example, Firefox displays markdown as text by default, but markdown add-ons do exist. (Although Firefox won't convert the file without an add-on, the file will still be readable, but features that depend on HTML won't display properly.) Sites like *github* convert markdown to HTML when a web surfer asks to read the file.

The text files have Unix-style line endings, so a text editor like *notepad* on Windows will produce a mess.  The basic requirements are a text editor that supports Unix line endings and Unicode.  Most text editors for Linux and Macintosh have the required support.  There are many text editors available for Windows that will suffice.

## Contents

Files with names that begin with "test-" are output from test runs, mainly from python script modules in the *tests* folder.  These have been edited.  You can run the script yourself, either in Python IDLE or on the command line from the working directory (*science*).

To run the file in a command shell, the syntax is:
```
    python -m tests.filename
```
The command "python" is the Python 3 interpreter.  The "-m" flag indicates that the file being run is to be treated as a module.  In this case, the file is a hypothetical python module:
```
    science/tests/filename.py
        (Working folder is "science")
```
Note that the slash after "tests" is replaced by a dot and the extension ".py" is not part of the module name.

To run the file in IDLE, bring up an IDLE interface using the command "idle".  Then load the file, and finally run it.  (If you access IDLE using a "Start Menu", you will need to change the working directory.)

## Files

*basel1.txt* - IDLE session (edited) - some exercises with the Basel Problem solved by Leonhard Euler in 1735.

*basel2.txt*, *basel3.txt* - IDLE sessions (minimally edited) - more exercises with the Basel Problem solved by Leonhard Euler in 1735.

*gaussian_rationals.md* - background information about Gaussian rationals

*tables_cfrac.txt* - IDLE session - continued fraction tables; a description of the contents and some suggestions for use are included in the preamble.  The remainder of the document has not been edited.

*test_brouncker.txt* - IDLE session (edited) - exercise with ℚ(√2)

*test_eisenstein.txt* - IDLE session (edited) - exercise with ℚ(√-3)

*test_gauss.txt* - IDLE session (edited) - exercise with ℚ(√-1)

*test_golden.txt* - IDLE session (edited) - exercise with ℚ(√5)

*test_inequalities.txt* - IDLE session (edited) - inequalities and continued fractions for quadratic rationals with positive discriminant.

*test_linear20.txt* - IDLE session (edited) - test of module *linear2o* in folder *sequences*; contains some information about Fibonacci-type sequences

*test_linear20_demo.txt* - IDLE session (edited) - extended test and demonstration of module *linear2o* in folder *sequences*; contains some information about Fibonacci-type sequences and some extended precision rational estimates of a small number of square roots.  (The estimates appear at the end of the session script.)

*test_rootM2.txt* - IDLE session (edited) - exercise with ℚ(√-2)

