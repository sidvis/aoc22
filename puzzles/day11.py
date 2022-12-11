import os

from helpers.inputs import AocData

class Item():
    """
    Class to keep track of remainders of mulitple divisors.

    Supports basic +, * and % for arithmetic with int and
    other Item instances.
    """

    # list of factors to keep track of in modulo-math
    factors = [2,3,5,7,11,13,17,19,23]

    def from_int(i):
        mods = [int(i) % f for f in Item.factors]
        return Item(mods)

    def __init__(self, mods):
        self.mods = mods

    def __repr__(self):
        return str(self.mods)

    # addition, either with int or Item
    def __add__(self, other):
        if isinstance(other, int):
            return self._add_int(other)
        elif isinstance(other, Item):
            return self._add_other(other)
        else:
            raise NotImplementedError

    def _add_other(self, other):
        gen = zip(Item.factors, zip(self.mods, other.mods))
        mods = [(i + j) % f for f, (i, j) in gen]
        return Item(mods)

    def _add_int(self, j):
        gen = zip(Item.factors, self.mods)
        mods = [(i + j) % f for f, i in gen]
        return Item(mods)

    # multiplication, either with int or Item
    def __mul__(self, other):
        if isinstance(other, int):
            return self._mul_int(other)
        elif isinstance(other, Item):
            return self._mul_other(other)
        else:
            raise NotImplementedError

    def _mul_other(self, other):
        gen = zip(Item.factors, zip(self.mods, other.mods))
        mods = [(i * j) % f for f, (i, j) in gen]
        return Item(mods)


    def _mul_int(self, j):
        gen = zip(Item.factors, self.mods)
        mods = [(i * j) % f for f, i in gen]
        return Item(mods)

    # modulo, for int only. Can only be one of the given factors
    def __mod__(self, div):
        for i, f in zip(self.mods, Item.factors):
            if f == div:
                return i
        else:
            raise ValueError('divisor not known')

    # only for divisor = 1 (return self), otherwise not implemented
    def __floordiv__(self, other):
        if other != 1:
            raise NotImplementedError()
        else:
            return self


class Monkey():
    """
    Monkey class

    this class can be more efficient, but who doesn't
    to implement actual throw/catch methods in this
    context?! xD
    """

    def __init__(self, items, operation, worry, test):
        self.items = items
        self.operation = operation
        self.worry = worry
        self.test = test
        self.monkey_true = None
        self.monkey_false = None

        self.count = 0

    def inspect_all(self):
        while self.items:
            self.count += 1
            old = self.items.pop(0)
            new = self.operation(old)
            worry_score = self.worry(new)
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

    worry_func = {
        1: (lambda x: x // 3), # part A
        2: (lambda x: x),      # part B
    }

    def __init__(self, data, worry_level):
        # worry_level = 1,2 depending on subproblem a,b
        self.monkeys = []
        self.connections = []

        assert worry_level in self.worry_func
        self.worry_level = worry_level

        for config in data.split_groups(''):
             self.add_monkey(config)

        self.connect_all()

    def add_monkey(self, data):
        split_data = lambda i: data.data[i].split(': ')[1]
        get_last_int = lambda i: int(data.data[i].split(' ')[-1])

        # starting items
        s_items = split_data(1)
        items = [int(s) for s in s_items.split(', ')]
        if self.worry_level == 2:
            items = [Item.from_int(i) for i in items]

        # operation
        s_op = split_data(2)
        f_op = s_op.split(' = ')[1]
        operation = lambda old: eval(f_op)

        # worry
        worry = self.worry_func[self.worry_level]

        # test
        div = get_last_int(3)
        if self.worry_level == 2:
            assert div in Item.factors, "encountered an unknown divisor"
        test = lambda i: (i % div) == 0

        self.monkeys.append( Monkey(items, operation, worry, test) )
        self.connections.append( (get_last_int(4), get_last_int(5)) )

    def connect_all(self):
        for monkey, (i_true, i_false) in zip(self.monkeys, self.connections):
            monkey.set_recipients( self.monkeys[i_true], self.monkeys[i_false])

    def play_rounds(self, n):
        for i in range(n):
            for monkey in self.monkeys:
                monkey.inspect_all()

    @property
    def monkey_business_level(self):
        passes = [m.count for m in self.monkeys]
        passes.sort(reverse=True)
        return passes[0]*passes[1]



class Day11():
    def __init__(self, data):
        self.data = data

    def solve1(self):
        C = Crowd(self.data, worry_level=1)
        C.play_rounds(20)
        return C.monkey_business_level

    def solve2(self):
        C = Crowd(self.data, worry_level=2)
        C.play_rounds(10000)
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
