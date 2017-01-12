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
	lowest_score = distance(*closest_pair)

	for i in range(len(P)): # O(n)
		for j in range(i, len(P)): # O(n)
			cur_pair = (P[i], P[j])
			if distance(*cur_pair) < lowest_score:
				closest_pair = cur_pair
				lowest_score = distance(*cur_pair)

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
	return (generate_point_lst(random.randint(3, 50)),)

if __name__ == '__main__':
	tester = Tester(baseline=brute_closest_pair,
					input_generator=generate_randomly_sized_point_lst,
					num_tests=50)
	tester.add_function("Brute Force Closest Point", brute_closest_pair)
	tester.test_all_functions()