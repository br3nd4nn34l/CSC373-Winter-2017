class Point():

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		x_str = '%.2f' % self.x
		y_str = '%.2f' % self.y
		return "({x}, {y})".format(x=x_str,
								   y=y_str)

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