class Point():

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "({x}, {y})".format(x=self.x,
								   y=self.y)

	def __repr__(self):
		return "Point" + str(self)

	def __eq__(self, other):
		return (self.x, self.y) == (other.x, other.y)

	def __ne__(self, other):
		return not(self == other)

	def distance(self, other):
		x_diff = self.x - other.x
		y_diff = self.y - other.y
		return ((x_diff ** 2) + (y_diff ** 2)) ** 0.5