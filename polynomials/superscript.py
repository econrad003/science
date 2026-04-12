"""
polynomials.superscript - integer superscripts polynomials module
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Provides a function 'to_superscript' which maps an integer to a superscript.

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
SUPERSCRIPTS = {0:'⁰', 1:'¹', 2:'²', 3:'³', 4:'⁴', 5:'⁵', 6:'⁶',
                7:'⁷', 8:'⁸', 9:'⁹', -1:'⁻'}

def to_superscript(i:int) -> str:
    """convert an integer to a superscipt"""
    i = int(i)
    if i == 0:
        return SUPERSCRIPTS[0]
    s = ""
    if i < 0:
        s += SUPERSCRIPTS[-1]
        i = abs(i)
    stack = list()
    while i:
        stack.append(SUPERSCRIPTS[i%10])
        i = i // 10
    while stack:
        s += stack.pop()
    return s

if __name__ == "__main__":
        # TEST CASES
    print("Testing:", __file__)
    assert to_superscript(1234567890) == "¹²³⁴⁵⁶⁷⁸⁹⁰", to_superscript(1234567890)
    assert to_superscript(-1234567890) == "⁻¹²³⁴⁵⁶⁷⁸⁹⁰", to_superscript(1234567890)
    assert to_superscript(0) == "⁰", to_superscript(0)
    print("SUCCESS!")

# END polynomials.superscript
