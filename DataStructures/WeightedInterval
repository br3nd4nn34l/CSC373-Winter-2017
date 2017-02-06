from DataStructures.Interval import Interval
class WeightedInverval(Interval):

    def __init__(self, start, end, weight):
        super.__init__(start, end)
        self.weight = weight

    def __eq__(self, other):
        return (super.__eq__(self, other) and
                (self.weight == other.weight))

    def __str__(self):
        ret_str = "{range}, Weight: {wt}".format(range=super.__str__(self),
                                                 wt=self.weight)
        return ret_str

    def __hash__(self):
        return hash((self.start,
                     self.end,
                     self.weight))