import re

class AocData():
    def from_str(s):
        return AocData(s.split('\n'))

    def from_file(f_in):
        with open(f_in, 'r') as f:
            data = [l.strip('\n') for l in f.readlines()]
            return AocData(data)

    def __init__(self, data):
        self.data = data

    def split_groups(self, sep=''):
        """
        splits the data on sep and returns a list of AocData objects
        """
        L = []
        cur = []
        for x in self.data:
            if x == sep:
                L.append(AocData(cur))
                cur = []
            else:
                cur.append(x)
        L.append(AocData(cur))

        return L


class DataParser():
    def __init__(self, *constructor, sep=None, check_len=True):
        assert (len(constructor) > 1) ^ (sep is None), "Multiple constructors require a separator"
        self.sep = sep
        self.constructor = constructor
        self.len = len(constructor)
        self.check_len = check_len


    def parse_line(self, line):
        if self.sep is None:
            return self.constructor[0](line)
        else:
            d = line.split(self.sep)
            assert self.check_len and (len(d) == self.len), "data length not matching parser"
            return tuple(c(x) for c,x in zip(self.constructor, d))

    def parse_data(self, data):
        return [self.parse_line(line) for line in data.data]


class TerminalParser():
    def parse_data(data):
        all_cmd = []
        cmd = None
        stdout = []
        for line in data.data:
            check_cmd = re.findall(r"\$ (.+)", line)
            if check_cmd:
                cmd = check_cmd[0]
                stdout = []
                all_cmd.append( (cmd, stdout) )
            else:
                stdout.append(line)

        return all_cmd
