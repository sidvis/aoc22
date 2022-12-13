import os
from functools import cmp_to_key

from helpers.inputs import AocData

def compare_items(a,b):
    """
    compares to lists or int
    returns negative if a < b
    returns zero     if a == b
    returns positive if a > b
    """
    if isinstance(a, int) and isinstance(b, int):
        return a - b

    if isinstance(a, int):
        return compare_items([a], b)
    if isinstance(b, int):
        return compare_items(a, [b])

    # both lists
    for x,y in zip(a,b):
        c = compare_items(x,y)
        if c != 0:
            return c
    else: # zip ends at shortest, check which list is longer
        return len(a)-len(b)


class Day13():
    def __init__(self, data):
        self.data = data

    def solve1(self):
        pairs = [tuple(eval(s) for s in g.data) for g in self.data.split_groups()]
        return sum(i+1 for i,p in enumerate(pairs) if compare_items(*p) < 0)

    def solve2(self):
        packets = [eval(s) for s in self.data.data if s != '']
        packets += [ [[2]], [[6]] ] # additional packets
        packets.sort(key=cmp_to_key(compare_items))
        return (packets.index([[2]])+1)*(packets.index([[6]])+1)

sample = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

class Test13():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day13(data)
        assert p.solve1() == 13

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day13(data)
        assert p.solve2() == 140

if __name__ == "__main__":
    f = os.path.join('data/13')
    data = AocData.from_file(f)
    P = Day13(data)
    print(P.solve1())
    print(P.solve2())
