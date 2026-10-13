"""
logic.D12 - find an implication function for the divisor lattice D12
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

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
from math import gcd, lcm
from functools import partial
from itertools import product

def f_generator(A, B):
    def f_template(d, x):
        return d[x]
    for b_values in product(B, repeat=len(A)):
        yield partial(f_template, dict(zip(A, b_values)))

    # The theoretical minimum
D12 = [1,2,3,4,6,12]
notTrue = [1,2,3,4,6]

IMP = dict()
for i in D12:
    for j in D12:
        if j % i == 0:
            IMP[i,j] = 12
            continue
        if i == 12:
            IMP[i,j] = j

def imp(i, j):
    """the candidate implication function"""
    index = i,j
    return IMP.get(index)

def codivisor(i):
    """the codivisor"""
    return 12 // i

def fix_contrapositive():
    """close IMP under contrapositive"""
    fixes = 0
    for i in D12:
        for j in D12:
            y = imp(i, j)
            if y == None:
                continue
            a = codivisor(i)
            b = codivisor(j)
            z = imp(b,a)
            if z:
                msg = f"contrapositive C{i},{j}={y}, C{b},{a}={z}"
                assert z==y, msg
            else:
                print(f"contrapositive C{i},{j}={y}=C{b},{a}")
                IMP[b,a] = y
                fixes += 1
    print(f"    {fixes} fixes...")
    return fixes

def get_possibilities():
    """determine what will work"""
    proper = D12[1:-1]
    unknown = list()
    for i in proper:
        for j in proper:
            args = i, j
            if imp(*args) == None:
                unknown.append(args)
    print()
    print(f"    {len(unknown)} unassigned values")
    flist = list(f_generator(unknown, notTrue))
    findex = set(range(len(flist)))
    print(f"    {len(flist)} functions")
    return unknown, flist, findex

def pass1(unknown, index, flist, findex):
    """try a given possibility (contrapositive)"""
    f = flist[index]
    def try_f(i, j):
        y = imp(i,j)
        if y:
            return y
        return f((i,j))
    for pair in unknown:
        i, j = pair
        a, b = codivisor(i), codivisor(j)
        y = f(pair)
        z = try_f(b, a)
        if y != z:
            # print("Reject", index)
            findex.remove(index)
            return
    # print("Accept", index)

def pass2(unknown, index, flist, findex):
    """try a given possibility (definition of disjunction)"""
    f = flist[index]
    def try_f(i, j):
        y = imp(i,j)
        if y:
            return y
        return f((i,j))
    for i in D12:
        for j in D12:
            y = try_f(try_f(i, j), j)
            z = lcm(i,j)
            if y != z:
                # print("Reject", index)
                findex.remove(index)
                return
    # print("Accept", index)

def pass3(unknown, index, flist, findex):
    """try a given possibility (positive paradox)"""
    f = flist[index]
    def try_f(i, j):
        y = imp(i,j)
        if y:
            return y
        return f((i,j))
    for pair in unknown:
        i, j = pair
        y = try_f(i, try_f(j, i))
        if y != 12:
            # print("Reject", index)
            findex.remove(index)
            return
    # print("Accept", index)

def pass4(unknown, index, flist, findex):
    """try a given possibility"""
    f = flist[index]
    def try_f(i, j):
        y = imp(i,j)
        if y:
            return y
        return f((i,j))
    print()
    print(f"        Cij  {index=}")
    for i in D12:
        s = ""
        for j in D12:
            y = try_f(i,j)
            s += f"{y:3}"
        print(s)
    # print("Accept", index)

def display():
    """display the current function"""
    print()
    print("        Cij                 Aij")
    for i in D12:
        s1 = ""
        s2 = ""
        for j in D12:
            y = imp(i,j)
            z = imp(y,j)
            s1 += f"{y:3}" if y else "  ?"
            s2 += f"{z:3}" if z else "  ?"
        print(s1, s2)

fix_contrapositive()
display()
unknown, flist, findex=get_possibilities()

to_do = list(findex)
for index in to_do:
    pass1(unknown, index, flist, findex)
print("Pass 1:", len(findex), "functions")

to_do = list(findex)
for index in to_do:
    pass2(unknown, index, flist, findex)
print("Pass 2:", len(findex), "functions")

to_do = list(findex)
for index in to_do:
    pass3(unknown, index, flist, findex)
print("Pass 3:", len(findex), "functions")

to_do = list(findex)
for index in to_do:
    pass4(unknown, index, flist, findex)
