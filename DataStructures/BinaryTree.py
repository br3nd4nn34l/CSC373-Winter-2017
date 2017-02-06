class BinaryTree:

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        ret_str = "({val}, {lft}, {rt})".format(val=self.value,
                                                lft=self.left,
                                                rt=self.right)
        return ret_str

    def is_full(self):
        if [self.left, self.right] == [None, None]:
            return True
        else:
            return ((None not in [self.left, self.right]) and
                    (self.left.is_full()) and
                    (self.right.is_full()))

    def prefix_free_encodings(self):
        if not self.is_full():
            print("PREFIX-FREE NOTATION CANNOT OCCUR IN A NON-FULL TREE")
            return
        else:
            if [self.left, self.right] == [None, None]:
                return {"0":self.value}
            else:
                left_prefix_free