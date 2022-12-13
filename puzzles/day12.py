import os

import numpy as np

from helpers.inputs import AocData

class HeightMap():

    def __init__(self, data):
        self.map = None
        self.start = None
        self.end = None

        grid=[]
        for i,line in enumerate(data.data):
            row = []
            for j,c in enumerate(line):
                if c == 'S':
                    self.start = (i,j)
                    c = 'a'
                elif c == 'E':
                    self.end = (i,j)
                    c = 'z'
                row.append(ord(c)-ord('a'))
            grid.append(row)

        self.map = np.array(grid)

    def can_move_in_dir(self, orientation):
        return np.diff(np.rot90(self.map, k=orientation), append=99)<=1

    def move_in_dir(self, start, orientation):
        P = self.can_move_in_dir(orientation)
        return np.rot90(np.roll(P & np.rot90(start,k=orientation), 1), k=-orientation)

    def find_origins(self, start, orientation):
        P = self.can_move_in_dir(orientation)
        return np.rot90(P & np.roll(np.rot90(start,k=orientation), -1), k=-orientation)

    def find_moves(self, start, reverse=False):
        _next = start.copy()
        for orientation in range(4):
            if reverse:
                _next |= self.find_origins(start, orientation)
            else:
                _next |= self.move_in_dir(start, orientation)
        return start | _next

    def find_route_up(self, limit = 1000):
        self.reachable = np.zeros_like(self.map, dtype=bool)
        self.reachable[self.start] = True

        for i in range(limit):
            self.reachable = self.find_moves(self.reachable)
            if self.reachable[self.end]:
                return i + 1
        else:
            raise RuntimeError('Maximum iterations reached')

    def find_route_down(self, limit = 1000):
        self.reachable = np.zeros_like(self.map, dtype=bool)
        self.reachable[self.end] = True

        for i in range(limit):
            self.reachable = self.find_moves(self.reachable, reverse=True)
            if 0 in self.map[self.reachable]:
                return i + 1
        else:
            raise RuntimeError('Maximum iterations reached')

class Day12():
    def __init__(self, data):
        self.M = HeightMap(data)

    def solve1(self):
        return self.M.find_route_up()

    def solve2(self):
        return self.M.find_route_down()

sample = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

class Test12():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day12(data)
        assert p.solve1() == 31

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day12(data)
        assert p.solve2() == 29

if __name__ == "__main__":
    f = os.path.join('data/12')
    data = AocData.from_file(f)
    P = Day12(data)
    print(P.solve1())
    print(P.solve2())
