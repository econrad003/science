"""
logic.curry_lambda - combinatory logic lambda expression helper Rosenbloom
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    To help with making sense of lambda expressions in combinatory logic.

REFERENCES

    [1] Paul Rosenbloom. Elements of Mathematical Logic. New York (Dover,
        1950).

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
from logic.curry import *

def free_in(x:str, node:"TreeForm") -> bool:
    """return True if x appears nowhere in the tree"""
    stack = list()
    stack.append(node)
    while stack:
        curr = stack.pop()
        if type(curr) == str:
            if curr == x:
                return False
            continue
        assert type(curr) == list
        assert curr[0] == '|'
        stack.append(curr[1])
        stack.append(curr[2])
    return True

def AKI_eliminate(x:str, expr:str) -> ParseTree:
    """eliminate x from λx(expr)"""
    assert len(x) == 1
    assert x not in {"A", "K", "I"}
    tree = ParseTree(expr)
    top = ["TOP"]
    stack = list()
    packet = (top, 0, tree.tree)
    stack.append(packet)
    while stack:
        parent, child, node = stack.pop()
        # print(node)
        if free_in(x, node):
            parent[child] = ['|', 'K', node]
            continue
        if node == x:
            parent[child] = 'I'
            continue
        # print("more")
        assert type(node) == list
        assert len(node) == 3
        assert node[0] == '|'
        curr1 = ['|', 'A', 1]
        curr2 = ['|', curr1, 2] 
        parent[child] = curr2
        packet = (curr1, 2, node[1])
        stack.append(packet)
        packet = (curr2, 2, node[2])
        stack.append(packet)
    # print(top)
    tree.tree = top[0]
    return tree

def prune_AK(tree:ParseTree) -> int:
    """replaces subexpressions |A|Kx with |Ba

    returns the number of subexpressions that were replaced.
    """
    def test_AK(subtree:"TreeForm") -> bool:
        """can this subtree be simplified?

        Pattern:
            |A|Kx
            ['|', 'A', ['|', 'K', x]]
        """
        assert type(node) == list
        assert len(node) == 3
        assert node[0] == '|'
        if node[1] != 'A':
            return False
        if type(node[2]) == list:
            assert type(node[2]) == list
            assert len(node[2]) == 3
            assert node[2][0] == '|'
            if node[2][1] == 'K':
                return True
        return False

    n = 0
    stack = list()
    top = ["TOP"]
    packet = (top, 0, tree.tree)
    stack.append(packet)
    while stack:
        parent, child, node = stack.pop()
        if type(node) == str:
            parent[child] = node
            continue
        if test_AK(node):
            curr = [node[0], 'B', 1]
            parent[child] = curr
            packet = (curr, 2, node[2][2])
            stack.append(packet)
            n += 1
            continue
        curr = [node[0], 1, 2]
        parent[child] = curr
        packet = (curr, 1, node[1])
        stack.append(packet)
        packet = (curr, 2, node[2])
        stack.append(packet)
    if n > 0:
        tree.tree = top[0]
    return n

if __name__ == "__main__":
    print("Testing 'free_in'...")
    assert free_in('x', 'x') == False
    assert free_in('x', 'y') == True
    assert free_in('x', ['|', ['|', 'A', 'K'], ['|', 'x', 'y']]) == False
    assert free_in('x', ['|', ['|', 'A', 'K'], ['|', 'B', 'C']]) == True
    def AKI_test(n, x, expr, expected):
        """test AKI elimination"""
        print(f"{n:2}) expression = λ{x}{expr}")
        result = AKI_eliminate(x, expr)
        print("        result =", result)
        print("      expected =", expected)
        assert(str(result) == expected)
        expr2 = '|' + str(result) + x
        reduced = str(Reducer.on(expr2, trace=False))
        print("       applied =", reduced)
        assert reduced == expr
        n = prune_AK(result)
        print(f"           {n:5} A|K nodes pruned")
        print("       pruned =", result)
        reduced = str(Reducer.on(expr2, trace=False))
        print("       applied =", reduced)
        assert reduced == expr

    print("Testing 'AKI_eliminate'...")
    AKI_test(1, 'x', 'x', 'I')
    AKI_test(2, 'x', 'y', '|Ky')
    AKI_test(3, 'x', '|Ky', '|K|Ky')
    AKI_test(4, 'x', '|xx', '||AII')
    AKI_test(5, 'x', '|x|xy', '||AI||AI|Ky')
    AKI_test(6, 'x', '||xx|xx', '||A||AII||AII')
    AKI_test(7, 'x', '||y|Tx|zx', '||A||A|Ky||A|KTI||A|KzI')
    print("SUCCESS!")
    
