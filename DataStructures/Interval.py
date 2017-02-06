class Interval:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        ret_str = "[{start}, {end}]".format(start=self.start,
                                            end=self.end)
        return ret_str

    def __repr__(self):
        ret_str = "Interval({s}, {e})".format(s=self.start,
                                              e=self.end)
        return ret_str

    def __eq__(self, other):
        return (self.start, self.end) == (other.start, other.end)

    def conflicts(self, other):
        return (self._conflicts_helper(other) and
                other._conflicts_helper(self))

    def _conflicts_helper(self, other):
        return (other.start < self.start < other.end)

    def draw(self):
        ret_str_lst = [" "] * (self.end + 1)
        ret_str_lst[self.start - 1 : self.end - 1] = "-" * (self.end - self.start)

        return "".join(ret_str_lst)


    def __hash__(self):
        return hash((self.start, self.end))
