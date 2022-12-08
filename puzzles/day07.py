import os
import re

from helpers.inputs import AocData, TerminalParser

class FsObject():
    all_objects = []

    def from_str(s):
        check_dir = re.findall(r"dir (\w+)", s)
        if check_dir:
            return FsObject(check_dir[0], is_dir=True)

        check_file = re.findall(r"(\d+) (.+)", s)
        if check_file:
            f = check_file[0]
            return FsObject(f[1], is_dir=False, size=int(f[0]))

    def __init__(self, name, is_dir, size=0):
        self.name = name
        self.is_dir = is_dir
        self.size = int(size)
        self.contains = []
        FsObject.all_objects.append(self)

    @property
    def treesize(self):
        return self.size + sum(x.treesize for x in self.contains)

    def get_by_name(self, name):
        for f in self.contains:
            if f.name == name:
                return f

class Day07():
    def __init__(self, data):
        cmds = TerminalParser.parse_data(data)

        assert cmds.pop(0)[0] == 'cd /'
        self.root = FsObject('_root', is_dir=True)

        cur_path = [self.root]
        for (cmd, stdout) in cmds:
            if cmd == 'ls':
                cur_path[-1].contains = [FsObject.from_str(s) for s in stdout]
            elif cmd == 'cd ..':
                cur_path.pop()
            elif cmd.startswith('cd'):
                new_dir = cmd[3:]
                assert new_dir != '..'
                cur_path.append(cur_path[-1].get_by_name(new_dir))
            else:
                raise AssertionError("cmd not known or expected")

        self.dir_sizes = [d.treesize for d in FsObject.all_objects if d.is_dir]

    def solve1(self):
        return sum(s for s in self.dir_sizes if s <= 100000)

    def solve2(self):
        total_space = 70000000
        used_space = self.root.treesize
        required_space = 30000000

        free_space_needed = required_space - (total_space - used_space)
        return min(s for s in self.dir_sizes if s >= free_space_needed)

sample = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

class Test07():
    def test_1(self):
        data = AocData.from_str(sample)
        p = Day07(data)
        assert p.solve1() == 95437

    def test_2(self):
        data = AocData.from_str(sample)
        p = Day07(data)
        assert p.solve2() == 24933642

if __name__ == "__main__":
    f = os.path.join('data/07')
    data = AocData.from_file(f)
    P = Day07(data)
    print(P.solve1())
    print(P.solve2())
