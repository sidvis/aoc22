import os

from helpers.inputs import AocData

def find_first_marker(s, size=4):
    I = []
    for i in range(size):
        I.append(s[i:])

    L = [len(set(t)) == size for t in zip(*I)]
    return L.index(True) + size

class Day06():
    def __init__(self, data):
        self.buffer = data.data[0]

    def solve1(self):
        return find_first_marker(self.buffer, 4)

    def solve2(self):
        return find_first_marker(self.buffer, 14)

samples = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]

class Test06():
    def test_1(self):
        results = [7, 5, 6, 10, 11]
        for s, r in zip(samples, results):
            data = AocData.from_str(s)
            p = Day06(data)
            assert p.solve1() == r

    def test_2(self):
        results = [19, 23, 23, 29, 26]
        for s, r in zip(samples, results):
            data = AocData.from_str(s)
            p = Day06(data)
            assert p.solve2() == r


if __name__ == "__main__":
    f = os.path.join('data/06')
    data = AocData.from_file(f)
    P1 = Day06(data)
    print(P1.solve1())
    P2 = Day06(data)
    print(P2.solve2())
