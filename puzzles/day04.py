import os

from helpers.inputs import AocData, DataParser
from helpers.types import MyRange

class Day04():

    def __init__(self, data):
        p = DataParser(MyRange.from_str, MyRange.from_str, sep=',')
        self.pairs = p.parse_data(data)

    def solve1(self):
        fully_contained = lambda r1, r2: r1.fully_contains(r2) or r2.fully_contains(r1)
        return sum(fully_contained(*r) for r in self.pairs)

    def solve2(self):
        return sum(r1.overlap(r2).size > 0 for r1,r2 in self.pairs)



sample = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

class Test04():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day04(data)
        assert p.solve1() == 2


if __name__ == "__main__":
    f = os.path.join('data/04')
    data = AocData.from_file(f)
    P = Day04(data)
    print(P.solve1())
    print(P.solve2())
