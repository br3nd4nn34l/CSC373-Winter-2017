import random

from Testing.Tester import Tester
from DataStructures.Point import Point
"""
Closest Pair of Points - Divide and Conquer Example 3
"""
"""
Problem: Find the closest two points in an array of points
	Input - array of points P = [p1, p2, ... pn], len(P) > 2
	Output - (p_i, p_j) such that:
		1) i != j
		2) distance(p_i, p_j) = min{distance(p_a, p_b) \forall p_a, p_b \in P}
	Measure of Interest:
		Number of Real Number calculations (basically just number of
		distance calculations)
"""

"""
Important Notation
	distance(p_i, p_j) = root(((p_i.x - p_j.x) ** 2))
"""
def distance(P1, P2):
	"""(Point, Point) -> Num
	Distance function to emulate my notation above.
	"""
	return P1.distance(P2)


"""Naive Solution: compare every point to every other point

In order to do this, we need two nested for-loops. Since each of these
for-loops is O(n) and one distance calculation takes place within the
innermost body, the cost is O(n) * O(n) * O(1) = O(n ** 2)

This algorithm is inefficient, but we know it works for sure (no trickery)
"""
def brute_closest_pair(P):
	"""([Point]) -> (Point, Point)

	Brute force implementation of the solution to the closest-pair of points
	problem. Runs in O(n ** 2) time.

	:param P: the array of points
	:return: 2-tuple of points
	"""

	# Find an initial low score (since pseudocode infinity is bullshit)
	closest_pair = (P[0], P[1])
	lowest_score = place_holder_distance(P)

	for i in range(len(P)): # O(n)
		for j in range(i + 1, len(P)): # O(n)
			if i == j:
				print("Warning")
			cur_pair = (P[i], P[j])
			if distance(*cur_pair) < lowest_score:
				closest_pair = cur_pair
				lowest_score = distance(*cur_pair)

	return order_pair(closest_pair)


"""

Naive solution that uses the principle of divide and conquer:
	1) DIVIDE:
		Split the points using a vertical line that puts half the points on one
		side and half on the other side (approximately) (DIVIDE)
	2) RECURSE:
		Call the algorithm on both halves of the points
	3) MERGE:
		We know that we've already compared points within their respective
		sides, so WLOG trying to compare points from the left side with
		points from the left side is redundant

		Therefore, only compare points BETWEEN the left and right groups
"""

def order_pair(pair):
	"""
	Used to order a pair of points into a new pair that is consistently ordered.
	"""
	if pair[0].x < pair[1].x:
		return pair
	else:
		return (pair[1], pair[0])

def place_holder_distance(P):

	# Ideally should be infinity - could use float("inf")
	return distance(*place_holder_points(P))

def place_holder_points(P):
	return (P[0], P[1])

def determine_splitting_line(X):
	"""([Point]) -> int

	X is a list of Points sorted according to their X coordinates. Returns an
	integer that represents the line that will split n points into two groups
	of size ~n/2.

	"""
	mid = len(X) // 2
	mid_x = X[mid].x
	next_to_mid_x = X[mid - 1].x
	line = (mid_x + next_to_mid_x) / 2
	return line

def split_points(X, split):
	"""([Point]) -> ([Point], [Point])
	Split a list of points into two groups: left and right
	"""
	# Figure out which points lie on the left and right
	left, right = [], []
	for pt in X:
		if pt.x < split:
			left += [pt]
		else:
			right += [pt]
	return (left, right)

def naive_div_conq(P):
	"""([Point, sorted by x]) -> (Point, Point)

	Wrapper function for the actual implementation of this algorithm.
	Automatically sorts P into X for us before passing it to the actual
	implementation, which assumes the input is sorted for recursive purposes.

	"""
	X = sorted(P,
			   key=lambda point:point.x)
	return order_pair(naive_div_conq_actual(X))

def naive_div_conq_actual(X):
	"""([Point, sorted by x]) -> ((Point, Point))
	"""
	# Edge Cases - return None
	if len(X) < 2:
		return None

	# Base Case, shortest possible list is two points.
	elif len(X) == 2:
		return (X[0], X[1])

	else: # len(X) > 2
		# Figure out the splitting line
		split = determine_splitting_line(X)

		# Figure out which points lie on the left and right of the line
		(left, right) = split_points(X, split)

		# Figure out the closest pair for each group
		closest_pair_L = naive_div_conq_actual(left)
		closest_pair_R = naive_div_conq_actual(right)

		# Figure out shortest distance for L, R sides, set place holders in
		# the event of edge cases
		if closest_pair_L != None:
			distance_L = distance(*closest_pair_L)
		else:
			distance_L = place_holder_distance(X)
			closest_pair_L = place_holder_points(X)

		if closest_pair_R != None:
			distance_R = distance(*closest_pair_R)
		else:
			distance_R = place_holder_distance(X)
			closest_pair_R = place_holder_points(X)

		# Set the low score
		if distance(*closest_pair_L) < distance(*closest_pair_R):
			closest_pair = closest_pair_L
			lowest_dist = distance_L
		else:
			closest_pair = closest_pair_R
			lowest_dist = distance_R

		for l in left:
			for r in right:
				cur_dist = distance(l, r)
				if cur_dist < lowest_dist:
					closest_pair = (l, r)
					lowest_dist = cur_dist

		return closest_pair

def optimized_naive_div_conq(P):
	"""([Point, sorted by x]) -> (Point, Point)

	Wrapper function for the actual implementation of this algorithm.
	Automatically sorts P into X for us before passing it to the actual
	implementation, which assumes the input is sorted for recursive purposes.

	"""
	X = sorted(P,
			   key=lambda point: point.x)
	return order_pair(optimized_naive_div_conq_actual(X))

def optimized_naive_div_conq_actual(X):
	# Edge Cases - return None
	if len(X) < 2:
		return None

	# Base Case, shortest possible list is two points.
	elif len(X) == 2:
		return (X[0], X[1])

	else:  # len(X) > 2
		# Figure out the splitting line
		split = determine_splitting_line(X)

		# Figure out which points lie on the left and right of the line
		(left, right) = split_points(X, split)

		# Figure out the closest pair for each group
		closest_pair_L = optimized_naive_div_conq_actual(left)
		closest_pair_R = optimized_naive_div_conq_actual(right)

		# Figure out shortest distance for L, R sides, set place holders in
		# the event of edge cases
		if closest_pair_L != None:
			distance_L = distance(*closest_pair_L)
		else:
			distance_L = place_holder_distance(X)
			closest_pair_L = place_holder_points(X)

		if closest_pair_R != None:
			distance_R = distance(*closest_pair_R)
		else:
			distance_R = place_holder_distance(X)
			closest_pair_R = place_holder_points(X)

		# Set the low score
		if distance(*closest_pair_L) < distance(*closest_pair_R):
			closest_pair = closest_pair_L
			lowest_dist = distance_L
		else:
			closest_pair = closest_pair_R
			lowest_dist = distance_R

		# Throw away the points in left and right whose x-coordinate is more
		# than lowest_dist units of distance away from the splitting line (
		# since they won't be any closer to the other side)

		new_left, new_right = [], []

		for l in left:
			if abs(l.x - split) < lowest_dist:
				new_left += [l]

		for r in right:
			if abs(r.x - split) < lowest_dist:
				new_right += [r]


		for l in new_left:
			for r in new_right:
				cur_dist = distance(l, r)
				if cur_dist < lowest_dist:
					closest_pair = (l, r)
					lowest_dist = cur_dist

		return closest_pair

def fully_optimized_div_conq(P):
	"""([Point, sorted by x]) -> (Point, Point)

	Wrapper function for the actual implementation of this algorithm.
	Automatically sorts P into X for us before passing it to the actual
	implementation, which assumes the input is sorted for recursive purposes.

	"""
	X = sorted(P,
			   key=lambda point: point.x)
	Y = sorted(P,
			   key=lambda point: point.y)
	return order_pair(fully_optimized_div_conq_actual(X, Y))

def fully_optimized_div_conq_actual(X, Y):
	# Edge Cases - return None
	if len(X) < 2:
		return None

	# Base Case, shortest possible list is two points.
	elif len(X) == 2:
		return (X[0], X[1])

	else:  # len(X) > 2
		# Figure out the splitting line
		split = determine_splitting_line(X)

		# Figure out which points lie on the left and right of the line
		(left, right) = split_points(X, split)

		# Make the same list as above, but sorted in terms of Y instead (if Y
		# is already sorted in terms of Y, doing a simple filter will
		# maintain its sorted-ness)
		(left_y, right_y) = split_points(Y, split)

		# Figure out the closest pair for each group
		closest_pair_L = fully_optimized_div_conq_actual(left, left_y)
		closest_pair_R = fully_optimized_div_conq_actual(right, right_y)

		# Figure out shortest distance for L, R sides, set place holders in
		# the event of edge cases
		if closest_pair_L != None:
			distance_L = distance(*closest_pair_L)
		else:
			distance_L = place_holder_distance(X)
			closest_pair_L = place_holder_points(X)

		if closest_pair_R != None:
			distance_R = distance(*closest_pair_R)
		else:
			distance_R = place_holder_distance(X)
			closest_pair_R = place_holder_points(X)

		# Set the low score
		if distance(*closest_pair_L) < distance(*closest_pair_R):
			closest_pair = closest_pair_L
			lowest_dist = distance_L
		else:
			closest_pair = closest_pair_R
			lowest_dist = distance_R

		# Throw away the points in Y whose x-coordinate is more
		# than lowest_dist units of distance away from the splitting line (
		# since they won't be any closer to the other side)

		new_Y = []
		for pt in Y:
			if abs(pt.x - split) < lowest_dist:
				new_Y += [pt]

		# Use the fact that there can be no more than 6 points in the
		# rectangle (need more explanation) to create a linear-cost loop
		# We need to consider them in terms of increasing (or decreasing)
		# y-coordinates

		return closest_pair

"""Testing Code"""
def generate_rand_point():
	"""(None) -> Point
	Generate a random point in the rectangle (0, 0) : (20, 20)
	:return:
	"""
	return Point(random.random() * 20,
				 random.random() * 20)

def generate_point_lst(size):
	"""(int) -> [Point]

	Generate a list of size randomly generated points in the rectangle
	(0, 0) : (20, 20).

	:param size: length of the desired list
	:return: a list lst such that:
		len(lst) = size
		Every point in lst is random
	"""
	ret_lst = []
	for i in range(size):
		ret_lst += [generate_rand_point()]
	return ret_lst

def generate_randomly_sized_point_lst():
	return (generate_point_lst(random.randint(2, 50)),)

if __name__ == '__main__':

	p1 = Point(0, 0)
	p2 = Point(1, 1)
	pair = (p1, p2)

	tester = Tester(name="Closest Pair Tester",
					baseline=brute_closest_pair,
					input_generator=generate_randomly_sized_point_lst,
					num_tests=50)
	tester.add_function("Brute Force", brute_closest_pair)
	tester.add_function("Naive Divide and Conquer", naive_div_conq)
	tester.add_function("Optimized Naive Divide and Conquer",
						optimized_naive_div_conq)
	tester.test_all_functions()