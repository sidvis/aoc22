import os

from helpers.inputs import AocData


# Failed to turn these into proper Enums...
class Left():
    MOVE = (lambda i: i << 1)
    BORDER = 1 << 6

class Right():
    MOVE = (lambda i: i >> 1)
    BORDER = 1

# define blocks as binary. Yay!
blocks = [
    (0b1111 << 1, ),

    (0b010 << 2,
     0b111 << 2,
     0b010 << 2),

    (0b001 << 2,
     0b001 << 2,
     0b111 << 2),

    (0b1 << 4,
     0b1 << 4,
     0b1 << 4,
     0b1 << 4),

    (0b11 << 3,
     0b11 << 3)
]


class Block():

    def line_helper_can_shift(line, stack, direction):
        if line & direction.BORDER:
            return False
        elif direction.MOVE(line) & stack:
            return False
        else:
            return True

    def line_helper_can_fall(line, stack):
        return stack & line == 0

    def __init__(self, shape, stack):
        self.shape = shape[::-1]
        self.stack = stack
        self.vsize = len(self.shape)
        self.vpos = len(stack)+3

    def can_shift_block(self, direction):
        stack = self.stack_slice()
        return all(Block.line_helper_can_shift(*pair,direction) for pair in zip(self.shape, stack))

    def shift(self, direction):
        if self.can_shift_block(direction):
            self.shape = tuple(direction.MOVE(b) for b in self.shape)

    @property
    def can_fall(self):
        stack = self.stack_slice(offset=-1)
        if self.vpos == 0:
            return False
        else:
            return all(Block.line_helper_can_fall(*pair) for pair in zip(self.shape, stack))

    def fall(self):
        self.vpos -= 1

    def merge(self):
        for i, line in enumerate(self.shape):
            if self.vpos + i < len(self.stack):
                self.stack[self.vpos+i] |= line
            else:
                self.stack.append(line)

    def stack_slice(self, offset=0):
        vpos = self.vpos + offset
        if vpos > len(self.stack):
            return (0,) * self.vsize
        else:
            return tuple(self.stack[vpos: vpos + self.vsize]) + (0,) * max(0, vpos + self.vsize - len(self.stack))


class Stack():

    def __init__(self, jets):
        self.jets = jets
        self.stack = []

        self.block_counts = [] # (block_id, stack_height)

        self.i_shift = 0 # index within self.jets

    @property
    def height(self):
        return len(self.stack)

    def pile_blocks(self, n_block):

        for i_block in range(n_block):

            b = Block(blocks[i_block % len(blocks)], self.stack)

            while True:
                direction = Left if self.jets[self.i_shift % len(self.jets)] == '<' else Right
                self.i_shift += 1

                b.shift(direction)
                if b.can_fall:
                    b.fall()
                else:
                    b.merge()
                    self.block_counts.append( (i_block+1, len(self.stack)) )
                    break

    def _find_period_stack(self,window=100, offset=100, max_range=10000):
        for p_stack in range(1,max_range):
            if self.stack[-window-offset:-offset] == self.stack[-window-offset-p_stack:-offset-p_stack]:
                break
        else:
            raise AssertionError('could not find a pattern')

        return p_stack


    def _find_period_block(self, p_stack, offset=5, max_offset=100):

        for offset in range(offset, max_offset):
            ref_block, ref_height = self.block_counts[-1-offset]
            candidates = [b for b,line in self.block_counts if line+p_stack == ref_height]
            if len(candidates) == 1:
                break
        return ref_block - candidates[0]


    def extrapolate_height(self, n_block, kwargs_stack={}, kwargs_block={}):
        p_stack = self._find_period_stack(**kwargs_stack)
        p_block = self._find_period_block(p_stack, **kwargs_block)

        remainder = n_block % p_block

        for i_block, line in self.block_counts[::-1]:
            if i_block % p_block == remainder:
                break

        return line + p_stack * (n_block-i_block) // p_block



class Day17():
    def __init__(self, data):
        self.S = Stack(data.data[0])
        self.S.pile_blocks(10000)

    def solve1(self):
        return self.S.block_counts[2021][1]

    def solve2(self):
        return self.S.extrapolate_height(1_000_000_000_000)

sample = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

class Test17():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day17(data)
        assert p.solve1() == 3068

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day17(data)
        assert p.solve2() == 1514285714288

if __name__ == "__main__":
    f = os.path.join('data/17')
    data = AocData.from_file(f)
    P = Day17(data)
    print(P.solve1())
    print(P.solve2())
