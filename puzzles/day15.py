import os
import re
from itertools import combinations

from helpers.inputs import AocData
from helpers.types import MyRange


def distance(a,b):
    return sum(abs(i-j) for i,j in zip(a,b))

beacons = set()

class BoundaryLine():

    def __init__(self, direction, offset):
        """ creates a line of type x + dir * y = offset"""
        assert abs(direction) == 1
        self.dir = direction
        self.offset = offset

    def intersect(self, other):
        """ returns intersection of two lines
            returns None if directions are the same
        """
        if self.dir == other.dir:
            return None

        x = (self.offset+other.offset)/2
        y = (self.dir*self.offset+other.dir*other.offset)/2

        return (x,y)


class Sensor():

    p = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

    def from_str(s):
        m = Sensor.p.findall(s)[0]
        xs, ys, xb, yb = (int(i) for i in m)
        return Sensor((xs,ys), (xb, yb))

    def __init__(self, pos, beacon):
        self.pos = pos
        self.beacon = beacon
        self.range = distance(self.pos, self.beacon)

        beacons.add(beacon) # append to global var

    def get_range_at_pos(self, x, axis=0):
        """ Returns a MyRange object of the sensor's coverage
            at a particular level x along given axis
        """
        d = abs(x-self.pos[axis])
        r = self.range-d

        start = self.pos[1-axis] - r
        end = self.pos[1-axis] + r

        return MyRange(start, end, check_valid=False)

    def in_range(self, pos):
        """ Checks if given position is in range of sensor """
        return distance(self.pos,pos) <= self.range

    def get_boundaries(self):
        """ Returns an iterator for the sensors 4 BoundaryLines """
        for p in [-1,1]:
            x = self.pos[0]
            y = self.pos[1] + p*(self.range+1)
            for d in [-1,1]:
                yield BoundaryLine(d, x+d*y)



def merge_ranges(ranges):
    """ Takes a list of MyRange objects and computes the union
        of all ranges.
        The union may consist of multiple ranges and is henceforth
        returned as a list of MyRange objects
    """
    out = []
    cur_range = ranges[0]
    for next_range in ranges[1:]:
        try:
            cur_range = cur_range.union(next_range, check_valid=True)
        except AssertionError:
            out.append(cur_range)
            cur_range=next_range
    else:
        out.append(cur_range)

    return out


class Day15():
    def __init__(self, data):
        self.sensors = [Sensor.from_str(l) for l in data.data]

    def find_covered(self, x, axis):
        ranges = [s.get_range_at_pos(x, axis=axis) for s in self.sensors] # get ranges
        ranges = [r for r in ranges if r.is_valid] # keep only the valid ones
        ranges.sort(key=lambda r: r.start) # sort by starting point

        covered = sum(r.size for r in merge_ranges(ranges)) # compute union
        occupied = len([b for b in beacons if b[axis]==x]) # number of cells with a beacon in it

        return covered-occupied


    def search_area_v1(self, search_area):
        """ searches for empty spot in the given area:
            (1..search_area) x (1..search_area)

            walk along the (outside) boundaries of all sensor ranges and
            identify cells which are also in the outside boundary of
            another sensor

            note: first attempt with mediocre performance
        """
        for s in self.sensors:
            for i in range(search_area+1):
                r = s.get_range_at_pos(i, axis=0)
                candidates = [(i, r.start-1), (i,r.end+1)]
                for (x,y) in candidates:
                    if y < 0 or y > search_area:
                        break
                    for other in self.sensors:
                        if other.in_range( (x,y) ):
                            break
                    else:
                        return (x,y)


    def search_area_v2(self, search_area):
        """ Same input/output as search_area_v1.

            Uses an approach where 4 line equations are computed
            for each (outside) sensor boundary. Intersections of
            all lines are computed to obtain a set of candidate
            coordinates. Finally, these coordinates are tested
            against the sensors.

            note: much faster due to exploiting of problem structure
        """
        # compute all borders and all their intersections
        borders = [b for s in self.sensors for b in s.get_boundaries() ]
        intersections = [a.intersect(b) for a,b in combinations(borders,2)]
        I = set(ix for ix in intersections if ix is not None)

        covered = lambda ix: any(sn.in_range(ix) for sn in self.sensors)
        in_search_range = lambda ix: 0 <= ix[0] <= search_area and 0 <= ix[1] <= search_area
        C = [ix for ix in I if not covered(ix) and in_search_range(ix)]

        assert len(C) == 1
        return C[0]


    def solve1(self, x=2_000_000):
        return self.find_covered(x, 1)

    def solve2_1(self, search_area=4_000_000):
        x,y = self.search_area_v1(search_area)
        return 4_000_000*x + y

    def solve2_2(self, search_area=4_000_000):
        x,y = self.search_area_v2(search_area)
        return int(4_000_000*x + y)

sample = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

class Test15():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day15(data)
        assert p.solve1(x=10) == 26

    def test_2_1(self):
        data = AocData.from_str(sample)
        p = Day15(data)
        assert p.solve2_1(search_area=20) == 56000011

    def test_2_2(self):
        data = AocData.from_str(sample)
        p = Day15(data)
        assert p.solve2_2(search_area=20) == 56000011


if __name__ == "__main__":
    f = os.path.join('data/15')
    data = AocData.from_file(f)
    P = Day15(data)
    print(P.solve1())
    print(P.solve2_2())
