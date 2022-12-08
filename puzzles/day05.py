import os
import re

from helpers.inputs import AocData


class MultiStack():

    def from_data(data):

        def parse_line(s):
            return list(s[1::4])

        names = parse_line(data.data[-1])

        grid = [parse_line(l) for l in data.data[-2::-1]]
        transpose = map(''.join, zip(*grid))
        stacks = [list(s.strip()) for s in transpose]

        return MultiStack(names, stacks)

    def __init__(self, names, stacks):
        self.names = names
        self.stack_dict = {n:s for n,s in zip(names, stacks)}

    def move_one_by_one(self, count, from_stack, to_stack):
        for i in range(count):
            self.stack_dict[to_stack].append(self.stack_dict[from_stack].pop())

    def move_stack(self, count, from_stack, to_stack):
        self.stack_dict[to_stack] += self.stack_dict[from_stack][-count:]
        self.stack_dict[from_stack] = self.stack_dict[from_stack][:-count]

    @property
    def tops(self):
        """returns the top (final) element of all stacks as one string"""
        return ''.join(self.stack_dict[n][-1] for n in self.names)

def parse_actions(data):

    r = re.compile(r"move (\d*) from (\d*) to (\d*)")
    parse_line = lambda s: r.findall(s)[0]

    return [parse_line(s) for s in data.data]


class Day05():
    def __init__(self, data):
        init, actions = data.split_groups()
        self.state = MultiStack.from_data(init)
        self.actionlist = parse_actions(actions)

    def solve1(self):
        for (_cnt, _from, _to) in self.actionlist:
            self.state.move_one_by_one(int(_cnt), _from, _to)
        return self.state.tops

    def solve2(self):
        for (_cnt, _from, _to) in self.actionlist:
            self.state.move_stack(int(_cnt), _from, _to)
        return self.state.tops

sample = (
"    [D]    \n"
"[N] [C]    \n"
"[Z] [M] [P]\n"
" 1   2   3 \n"
"\n"
"move 1 from 2 to 1\n"
"move 3 from 1 to 3\n"
"move 2 from 2 to 1\n"
"move 1 from 1 to 2"
)

class Test05():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day05(data)
        assert p.solve1() == 'CMZ'

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day05(data)
        assert p.solve2() == 'MCD'


if __name__ == "__main__":
    f = os.path.join('data/05')
    data = AocData.from_file(f)
    P1 = Day05(data)
    print(P1.solve1())
    P2 = Day05(data)
    print(P2.solve2())
