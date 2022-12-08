import os

import numpy as np

from helpers.inputs import AocData

def find_visible(A, rotation=0):
    _A = np.rot90(A, k=rotation)
    curmax = np.ones(_A.shape[1]) * -1
    visible = np.zeros_like(_A, dtype=bool)

    for i, x in enumerate(_A):
        visible[i] = x > curmax
        curmax = np.max([x,curmax], axis=0)

    return np.rot90(visible, k=-rotation).copy()


def find_view_score(A, rotation=0):
    _A = np.rot90(A, k=rotation).copy()
    _A[-1,:] = 99
    view_scores = np.zeros_like(_A, dtype=int)

    for i in range(len(_A)-1):
        diffs = _A[i+1:] - _A[i]
        view_scores[i] = np.argmax(diffs >= 0, axis=0)+1

    return np.rot90(view_scores, k=-rotation).copy()


class Day08():
    def __init__(self, data):
        self.A = np.array([list(map(int, s)) for s in data.data])

    def solve1(self):
        V = np.zeros_like(self.A, dtype=bool)
        for rotation in range(4):
            V |= find_visible(self.A, rotation)

        return V.sum()

    def solve2(self):
        scenic_scores = np.prod([find_view_score(self.A, rot) for rot in range(4)], axis=0)
        return scenic_scores.max()

sample = """30373
25512
65332
33549
35390"""

class Test08():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day08(data)
        assert p.solve1() == 21

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day08(data)
        assert p.solve2() == 8

if __name__ == "__main__":
    f = os.path.join('data/08')
    data = AocData.from_file(f)
    P = Day08(data)
    print(P.solve1())
    print(P.solve2())
