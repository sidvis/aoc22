import os

import numpy as np

from helpers.inputs import AocData, DataParser

class Rope():

    dirs = {
        'U': np.array([1,0]),
        'D': np.array([-1,0]),
        'R': np.array([0, 1]),
        'L': np.array([0, -1]),
    }

    def __init__(self, child=None):
        self.head = np.array([0,0])
        self.tail = self.head.copy()
        self.trail = [tuple(self.tail)]
        self.child = child

    def move_head(self, _dir, count):
        self.head += self.dirs[_dir] * int(count)
        self.track_tail()

    def set_head(self, head):
        self.head = head
        self.track_tail()

    @property
    def distance(self):
        return int(np.abs(self.head - self.tail).max())

    @property
    def direction(self):
        diff = self.head - self.tail
        return (diff / self.distance).astype(int)

    @property
    def covered(self):
        return len(set(self.trail))

    def track_tail(self):
        dist = self.distance
        if dist == 0:
            return

        direction = self.direction
        for i in range(dist-1):
            self.tail = self.head -(dist-i-1)*direction
            self.trail.append(tuple(self.tail))
            if self.child is not None:
                self.child.set_head(self.tail)

    def move_multiple(self, cmds):
        for cmd in cmds:
            self.move_head(*cmd)

class MultiRope():
    def __init__(self, n):
        self.ropes = [Rope()]
        for i in range(n-1):
            self.ropes.append(Rope(child=self.ropes[-1]))
        self.ropes = self.ropes[::-1]

    @property
    def head_rope(self):
        return self.ropes[0]

    @property
    def tail_rope(self):
        return self.ropes[-1]

    def move_multiple(self, cmds):
        self.head_rope.move_multiple(cmds)


class Day09():
    def __init__(self, data):
        p = DataParser(str, int, sep=' ')
        self.cmds = p.parse_data(data)

    def solve1(self):
        R = Rope()
        R.move_multiple(self.cmds)
        return R.covered

    def solve2(self):
        M = MultiRope(9)
        M.move_multiple(self.cmds)
        return M.tail_rope.covered

sample1 = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

sample2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

class Test09():
    def test_1(self):
        data = AocData.from_str(sample1)
        p = Day09(data)
        assert p.solve1() == 13

    def test_2(self):
        data = AocData.from_str(sample1)
        p = Day09(data)
        assert p.solve2() == 1

    def test_3(self):
        data = AocData.from_str(sample2)
        p = Day09(data)
        assert p.solve2() == 36

if __name__ == "__main__":
    f = os.path.join('data/09')
    data = AocData.from_file(f)
    P = Day09(data)
    print(P.solve1())
    print(P.solve2())
