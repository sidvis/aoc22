import os

from helpers.inputs import AocData

operators = {
    '+': int.__add__,
    '-': int.__sub__,
    '*': int.__mul__,
    '/': int.__floordiv__,
}

class Monkey():

    _all = dict()
    _parent_of = dict()

    def from_str(s):
        return Monkey(*s.split(': '))

    def __init__(self, name, definition):
        self.name = name
        self.definition = definition

        if definition.isdigit():
            self._value = int(definition)
        else:
            self._value = None

            name1, op, name2 = self.definition.split(' ')
            self._parent_of[name1] = name
            self._parent_of[name2] = name

        self._all[name] = self

    @property
    def value(self):
        if self._value is None:
            name1, op, name2 = self.definition.split(' ')
            m1, m2 = self._all[name1], self._all[name2]
            self._value = operators[op](m1.value, m2.value)
        return self._value



def solve(expression, result, unknown):
    """
    solves a simple equation [expression = result] for named unknown
    variable within expression

    expression = 'a + b'
    result = 4
    unknown = 'a'

    returns 4 - b.value

    """
    m1, op, m2 = expression.split()
    x = Monkey._all[m1].value if m2 == unknown else Monkey._all[m2].value
    if op == '+':
        return result - x
    elif op == '-' and m1 == unknown:
        return result + x
    elif op == '-' and m2 == unknown:
        return x - result
    elif op == '*':
        return result // x
    elif op == '/' and m1 == unknown:
        return x * result
    elif op == '/' and m2 == unknown:
        return x // result



class Day21():
    def __init__(self, data):
        self.M = [Monkey.from_str(s) for s in data.data]

    def solve1(self):
        return Monkey._all['root'].value

    def solve2(self):
        # starting at humn, trace all monkeys to root and list their equations
        # equations are of the form ('humn', 'abcd + humn'), the first element
        # representing the unknown in the following expression.
        equations = []
        name = 'humn'
        while name != 'root':
            parent_name = Monkey._parent_of[name]
            definition = Monkey._all[parent_name].definition

            # replace the last expression of root to 'a - b == 0' to simulate a == b
            if parent_name == 'root':
                definition = definition[:5] + '-' + definition[6:]

            equations.append((name, definition))
            name = parent_name

        # starting at the last equation, work backwards:
        result = 0
        for var, eq in equations[::-1]:
            result = solve(eq, result, var)

        return result


sample = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

class Test21():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day21(data)
        assert p.solve1() == 152

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day21(data)
        assert p.solve2() == 301

if __name__ == "__main__":
    f = os.path.join('data/21')
    data = AocData.from_file(f)
    P = Day21(data)
    print(P.solve1())
    print(P.solve2())
