"""
demos.modn_addition - prepare additions table modulo n (ℤₙ)
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Prepare tables for the additive group in ℤₙ.

LICENSE
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from utilities.modn import make_Zn
from utilities.modlog import ModLog

RingType = "(Group, Ring)"

def nontrivial_int(s:str) -> int:
    """integer larger than 1"""
    n = int(s)
    if n <= 0:
        raise ValueError(f"{s}: the value must be positive")
    if n == 1:
        raise ValueError(f"{s}: trivial rings are inadmissible")
    return n

def inverses(R:RingType, maxlen:int, mult:bool=False):
    """prepare the table of inverses"""
    lines = list()
        ### table header for inverses
    prefix = "  x "
    suffix = ""
    for x in R.range():
        suffix += f" {x:{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    lines.append("━" * len(prefix) + "╋" + "━" * len(suffix))
        ### table detail for additive inverses
    prefix = " -x "
    suffix = ""
    for x in R.range():
        suffix += f" {-x:{maxlen}}"
    lines.append(prefix + "┃" + suffix)
        ### table detail for additive inverses
    if mult:
        ZD = " " + "┄" * maxlen
        prefix = "1/x "
        suffix = ""
        for x in R.range():
            if x.is_zero_divisor:
                suffix += ZD
            else:
                suffix += f" {x.inverse:{maxlen}}"
        lines.append(prefix + "┃" + suffix)
        ### DONE!
    return lines

def binary(R:RingType, opcode:str, op:callable, maxlen:int):
    """binary operation table"""
    lines = list()
        ### table header for binary operator
    prefix = " " * (maxlen) + opcode + " "
    suffix = ""
    for y in R.range():
        suffix += f" {y:{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    lines.append("━" * len(prefix) + "╋" + "━" * len(suffix))
        ### rows for binary operator
    ZD = " " + "┄" * maxlen
    for x in R.range():
        prefix = " " * len(opcode) + f"{x:{maxlen}} "
        suffix = ""
            ### columns for binary operator
        for y in R.range():
            try:
                z = op(x, y)
                suffix += f" {z:{maxlen}}"
            except ZeroDivisionError:
                suffix += ZD
        lines.append(prefix + "┃" + suffix)
        ### DONE!
    return lines

def multiplication(R:RingType, maxlen:int):
    """multiplication tables"""
        ### table of multiplication
    print("Multiplication in", R.__name__)
    op = lambda x, y: x*y
    lines = binary(R, "×", op, maxlen)
    for line in lines:
        print(line)
    print()

def binaryM(R:RingType, opcode:str, op:callable, maxlen:int):
    """binary operation table for multiplicative group"""
    lines = list()
        ### table header for binary operator
    prefix = " " * (maxlen) + opcode + " "
    suffix = ""
    for y in R.range():
        if not y.is_zero_divisor:
            suffix += f" {y:{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    lines.append("━" * len(prefix) + "╋" + "━" * len(suffix))
        ### rows for binary operator
    ZD = " " + "┄" * maxlen
    for x in R.range():
        if x.is_zero_divisor:
            continue
        prefix = " " * len(opcode) + f"{x:{maxlen}} "
        suffix = ""
            ### columns for binary operator
        for y in R.range():
            if y.is_zero_divisor:
                continue
            try:
                z = op(x, y)
                suffix += f" {z:{maxlen}}"
            except ZeroDivisionError:
                suffix += ZD
        lines.append(prefix + "┃" + suffix)
        ### DONE!
    return lines

def division(R:RingType, maxlen:int):
    """division tables"""
        ### table of division
    print("Division in", R.__name__)
    op = lambda x, y: x*y
    lines = binaryM(R, "÷", op, maxlen)
    for line in lines:
        print(line)
    print()

def tables(R:RingType, maxlen:int, mult:bool=False):
    """display the requested tables"""
    if mult:
        print(f"Tables for the ring {R.__name__}")
    else:
        print(f"Tables for the group {R.__name__}")
    print()
        ### table of inverses
    lines = inverses(R, maxlen, mult)
    for line in lines:
        print(line)
    print()
        ### table of addition
    print("Addition in", R.__name__)
    op = lambda x, y: x+y
    lines = binary(R, "+", op, maxlen)
    for line in lines:
        print(line)
    print()
        ### table of subtraction
    print("Subtraction in", R.__name__)
    op = lambda x, y: x-y
    lines = binary(R, "-", op, maxlen)
    for line in lines:
        print(line)
    print()
        ### additional tables
    if mult:
        multiplication(R, maxlen)
        division(R, maxlen)

def nvp(name, value, length=30):
    """display a name-value pair"""
    print(f"{name:>{length}}", value)

def ords(R:RingType, maxlen:int):
    """table of orders for the units"""
    lines = list()
    prefix = "      x "
    suffix = ""
    for x in R.range():
        if not x.is_zero_divisor:
            suffix += f" {x:{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    lines.append("━" * len(prefix) + "╋" + "━" * len(suffix))
        ### table detail for additive inverses
    prefix = " ord(x) "
    suffix = ""
    for x in R.range():
        if not x.is_zero_divisor:
            suffix += f" {x.ord:{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    return lines

def expbasezeta(R:RingType, logzeta:ModLog, maxlen:int):
    """table of powers for the selected primitive"""
    lines = list()
    zeta = logzeta.base
    prefix = "        n "
    suffix = ""
    for n in range(zeta.ord):
        suffix += f" {n:{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    lines.append("━" * len(prefix) + "╋" + "━" * len(suffix))
        ### table detail for additive inverses
    prefix = " exp(n,ζ) "
    suffix = ""
    for n in range(zeta.ord):
        suffix += f" {logzeta.exp(n):{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    return lines

def logbasezeta(R:RingType, logzeta:ModLog, maxlen:int):
    """table of logarithms for the selected primitive"""
    lines = list()
    zeta = logzeta.base
    prefix = "        x "
    suffix = ""
    args = list()
    for n in range(zeta.ord):
        args.append(int(logzeta.exp(n)))
    args.sort()
    for n in args:
        suffix += f" {R(n):{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    lines.append("━" * len(prefix) + "╋" + "━" * len(suffix))
        ### table detail for additive inverses
    prefix = " log(x,ζ) "
    suffix = ""
    for n in args:
        x = R(n)
        suffix += f" {logzeta.log(x):{maxlen}}"
    lines.append(prefix + "┃" + suffix)
    return lines

def extended(R:RingType, maxlen:int):
    """extended information"""
    nvp("additive order:", R.additive_order())
    nvp("multiplicative order:", R.multiplicative_order())

        # get orders of the units
    units = list()
    orders = dict()
    zeta = R(1)
    for x in R.range():
        if not x.is_zero_divisor:
            units.append(x)
            orders[x] = x.ord
            if x.ord > zeta.ord:
                zeta = x
    nvp("ζ =", zeta)
    nvp("ord(ζ) =", zeta.ord)
    nvp("is ζ primitive?", \
        "Yes" if zeta.ord == R.multiplicative_order() \
        else "No")
    print()
    print("Orders of the units in", R.__name__)
    lines = ords(R, maxlen)
    for line in lines:
        print(line)
    print()
    logzeta = ModLog(R, zeta)
    if zeta.ord != R.multiplicative_order():
        print()             # blank line after warning
    print(f"Powers of the unit {zeta} in", R.__name__)
    lines = expbasezeta(R, logzeta, maxlen)
    for line in lines:
        print(line)
    print()
    print(f"Logarithms to base {zeta} in", R.__name__)
    lines = logbasezeta(R, logzeta, maxlen)
    for line in lines:
        print(line)
    print()

def main(argv:list):
    """parse arguments"""
    import argparse
    DESC = "Display tables for the additive group in ℤₙ."
    EPI = "Extended analysis implies tables for multiplication and division."
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)
    parser.add_argument("n", type=nontrivial_int, nargs="?", default=11, \
        help="the order of the ring. (n>1; default=11)")
    parser.add_argument("-m", "--mult", action="store_true", \
        help="when set, multiplication and division tables will also be displayed.")
    parser.add_argument("-x", "--ext", action = "store_true", \
        help="when set, show extended multiplication group analysis.")
    args = parser.parse_args(argv)
    if args.ext:
        args.mult = True
    Zn = make_Zn(args.n)
    maxlen = len(str(args.n-1))
    tables(Zn, maxlen, args.mult)
    if args.ext:
        extended(Zn, maxlen)
    

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

# END demos.mod_addition
