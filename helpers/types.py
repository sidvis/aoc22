class MyRange():
    def from_str(s):
        a,b = s.split('-')
        return MyRange(int(a),int(b))

    def __init__(self, start, end, check_valid=True):
        """
        check_valid = True ensures start is before end (or equals)
        """
        self.start = start
        self.end = end
        if check_valid:
            assert self.is_valid

    @property
    def is_valid(self):
        """
        validates if a range is valid
        """
        return self.start <= self.end

    @property
    def size(self):
        """
        return the length of the range (ends inclusive)
        """
        if self.is_valid:
            return self.end-self.start+1
        else:
            return 0

    def overlap(self, other, check_valid=False):
        """
        finds overlap with other ranges and return a new range

        check_valid = True will raise an AssertionError whenever the
                            resulting range is invalid (i.e. empty)
                    = False might also return an invalid range
        """
        s = max(self.start, other.start)
        e = min(self.end, other.end)
        return MyRange(s,e,check_valid)

    def fully_contains(self, other):
        """
        returns true if self fully contains other
        """
        o = self.overlap(other, check_valid=False)
        return other.size == o.size

    def is_fully_contained_in(self, other):
        """
        returns true if self is fully contained in other
        """
        o = self.overlap(other, check_valid=False)
        return self.size == o.size

