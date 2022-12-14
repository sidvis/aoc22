import os

from helpers.inputs import AocData, DataParser

def draw_line(start, end):
    """ Return a list of tuples in the straight line between start and end"""
    diff = (end[0]-start[0], end[1]-start[1])
    distance = max(abs(diff[0]), abs(diff[1]))
    direction = (diff[0]//distance, diff[1]//distance)
    for i in range(distance+1):
        yield (start[0]+i*direction[0], start[1]+i*direction[1])

class Cave():

    def from_data(data):
        rocks = set()
        p = DataParser(int,int,sep=',')
        for line in data.data:
            points = p.parse_list(line.split(' -> '))
            for s,e in zip(points, points[1:]):
                rocks |= set(draw_line(s,e))

        return Cave(rocks)

    def __init__(self, rocks):
        self.rocks = rocks
        self.max_y = max(y for x,y in self.rocks)
        self.init_fill = len(self.rocks)

        self.fill_from = (500,0)
        self.fill_order = [0, -1, 1] # down, left, right

    @property
    def sand_level(self):
        return len(self.rocks) - self.init_fill

    @property
    def is_full(self):
        return self.fill_from in self.rocks

    def trace_grain(self):
        assert not self.is_full, "Cave is already full"
        cur = self.fill_from
        while True:
            yield cur
            # explore candidates in prescribed order
            for dx in self.fill_order:
                cand = (cur[0]+dx, cur[1]+1)
                if cand not in self.rocks:
                    cur = cand
                    break
            else: # all candidates depleted, end move here
                return

    def fill_no_floor(self):
        while True:
            for grain in self.trace_grain():
                if grain[1] > self.max_y: # first grain to fall off the grid
                    return self.sand_level
            else: # iterator ended, add grain to cave
                self.rocks.add(grain)

    def fill_with_floor(self, offset):
        while not self.is_full:
            for grain in self.trace_grain():
                if grain[1] == self.max_y+offset-1:
                    break
            self.rocks.add(grain)

        return self.sand_level


class Day14():
    def __init__(self, data):
        self.cave = Cave.from_data(data)

    def solve1(self):
        return self.cave.fill_no_floor()

    def solve2(self):
        return self.cave.fill_with_floor(offset=2)

sample = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

class Test14():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day14(data)
        assert p.solve1() == 24

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day14(data)
        assert p.solve2() == 93

if __name__ == "__main__":
    f = os.path.join('data/14')
    data = AocData.from_file(f)
    P = Day14(data)
    print(P.solve1())
    print(P.solve2())
