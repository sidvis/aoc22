import os

from helpers.inputs import AocData

class CPU():
    def __init__(self, init_state = 1):
        self.state = init_state
        self.cycle = 0
        self.history = []

    def step(self, n=1):
        self.cycle += n
        self.history += [self.state]*n

    def noop(self):
        self.step()

    def addx(self, x):
        self.step(2)
        self.state += int(x)

    def parse_cmd(self, cmd):
        match cmd.split():
            case ['noop']:
                self.noop()
            case ['addx', x]:
                self.addx(int(x))
            case _:
                raise ValueError

    def signal_strength(self, i):
        return i * self.history[i-1]

    def render_output(self):
        output = ""
        for i,s in enumerate(self.history):
            px = i % 40
            if len(output) and (px % 40 == 0):
                output += '\n'

            if abs(s - px) <= 1:
                output += '#'
            else:
                output += '.'

        return output



class Day10():
    def __init__(self, data):
        self.c = CPU()
        for cmd in data.data:
            self.c.parse_cmd(cmd)

    def solve1(self):
        return sum(self.c.signal_strength(i) for i in range(20,240,40))

    def solve2(self):
        return self.c.render_output()

sample = """noop
addx 3
addx -5"""

class Test10():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day10(data)
        assert p.c.history == [1,1,1,4,4]
        assert p.c.state == -1

    def test_2(self):
        data = AocData.from_file('./data/10.sample')
        p = Day10(data)
        assert p.solve1() == 13140

    def test_3(self):
        data = AocData.from_file('./data/10.sample')
        p = Day10(data)
        result = (
            "##..##..##..##..##..##..##..##..##..##..\n"
            "###...###...###...###...###...###...###.\n"
            "####....####....####....####....####....\n"
            "#####.....#####.....#####.....#####.....\n"
            "######......######......######......####\n"
            "#######.......#######.......#######....."
        )
        assert p.solve2() == result

if __name__ == "__main__":
    f = os.path.join('data/10')
    data = AocData.from_file(f)
    P = Day10(data)
    print(P.solve1())
    print(P.solve2())
