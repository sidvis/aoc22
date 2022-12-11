import os
import math

from helpers.inputs import AocData

class Monkey():
    """
    Monkey class

    this class can be more efficient, but who doesn't
    to implement actual throw/catch methods in this
    context?! xD
    """

    def __init__(self, items, operation, test):
        self.items = items
        self.operation = operation
        self.test = test
        self.monkey_true = None
        self.monkey_false = None

        self.count = 0

    def inspect_all(self, worry):
        while self.items:
            self.count += 1
            old = self.items.pop(0)
            new = self.operation(old)
            worry_score = worry(new)
            self.throw(worry_score)

    def throw(self, item):
        if self.test(item):
            self.monkey_true.catch(item)
        else:
            self.monkey_false.catch(item)

    def catch(self, item):
        self.items.append(item)

    def set_recipients(self, monkey_true, monkey_false):
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false


class Crowd():
    """
    Group of Monkeys
    """

    def __init__(self, data):
        self.monkeys = []
        self.connections = []

        self.divisors = []

        for config in data.split_groups(''):
             self.add_monkey(config)

        self.connect_all()

    def add_monkey(self, data):
        split_data = lambda i: data.data[i].split(': ')[1]
        get_last_int = lambda i: int(data.data[i].split(' ')[-1])

        # starting items
        s_items = split_data(1)
        items = [int(s) for s in s_items.split(', ')]

        # operation
        s_op = split_data(2)
        f_op = s_op.split(' = ')[1]
        operation = lambda old: eval(f_op)

        # test
        div = get_last_int(3)
        self.divisors.append(div)
        test = lambda i: (i % div) == 0

        self.monkeys.append( Monkey(items, operation, test) )
        self.connections.append( (get_last_int(4), get_last_int(5)) )

    def connect_all(self):
        for monkey, (i_true, i_false) in zip(self.monkeys, self.connections):
            monkey.set_recipients( self.monkeys[i_true], self.monkeys[i_false])

    def play_rounds(self, n, worry):
        for i in range(n):
            for monkey in self.monkeys:
                monkey.inspect_all(worry)

    @property
    def monkey_business_level(self):
        passes = [m.count for m in self.monkeys]
        passes.sort(reverse=True)
        return passes[0]*passes[1]



class Day11():
    def __init__(self, data):
        self.data = data

    def solve1(self):
        C = Crowd(self.data)
        worry = lambda val: val // 3
        C.play_rounds(20, worry)
        return C.monkey_business_level

    def solve2(self):
        C = Crowd(self.data)
        lcm = math.lcm(*C.divisors)
        worry = lambda val: val % lcm
        C.play_rounds(10000, worry)
        return C.monkey_business_level

sample = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

class Test11():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day11(data)
        assert p.solve1() == 10605

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day11(data)
        assert p.solve2() == 2713310158

if __name__ == "__main__":
    f = os.path.join('data/11')
    data = AocData.from_file(f)
    P = Day11(data)
    print(P.solve1())
    print(P.solve2())
