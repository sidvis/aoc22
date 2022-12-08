from helpers.inputs import AocData
import puzzles.day04 as day04

def test_day04():
    data = AocData.from_str(day04.sample)
    p = day04.Day04(data)
    assert p.solve1() == 2
