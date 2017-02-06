import random # for testing
from Testing.Tester import Tester

"""
Merge Sort - Divide and Conquer Example 1
"""
"""
Problem: Sorting
	Input - array of integers A = [a1, a2, ... an]
	Output - sorted array B = [b1, b2, ... bn] such that:
				\forall i \in {1, ... n}:
					1) b_i in A
					2) b_i <= b_(i + 1) OR (b1 <= b2 <= ... <= bn)
"""
"""
Idea: Merging

Note that we can take two sorted arrays A, B and merge them together into a
sorted list as follows:
	1) Set the current index of A and B to 0, and the return list to []
	2) Compare A[A_cur_ind] with B[B_cur_ind]
	3) Append the smallest of the two elements to the return list
	4) Increment the current index of the list that was just used
	5) Repeat steps 3, 4 until one of the lists is depleted
	6) Append the leftover elements to the end of the return list
	7) Return the return list
"""

def correct_merge(A, B):
	return sorted(A + B)


""" Cost Analysis / Termination:

This algorithm uses a while-loop that loops until one of cur_A_ind or cur_B_ind
exceeds the bounds of their respective array. For every iteration of the loop,
either cur_A_ind or cur_B_ind will be incremented. The most incrementations possible
is 2*min(n, m) (the case where cur_A_ind is incremented every odd/even iteration and
cur_B_ind is incremented on every other iteration).

Since the while loop does 2*min(n, m) iterations, the cost/runtime of this solution is
O(min(n, m))

Once the while loop ends the algorithm attaches the leftovers from the larger array
to the end of the list and then terminates.
"""
"""Correctness:

Loop Invariant - P(i) -> true when after the i-th iteration of the while-loop,
the algorithm has built a list of length i that is sorted in increasing order

Induction on Loop Number:
	Base Case: i = 0
		After the 0-th iteration of the loop, the algorithm has constructed an
			empty array.
		By vacuous truth, this array is sorted in increasing order and is of length i = 0.
		Thus P(0) holds.
	Inductive Hypothesis:
		Assume that for some k \in N, P(k - 1) holds.
	Inductive Step:
		Consider what would happen before the loop enters iteration k
		We know from the inductive hypothesis that the loop has built an
			array sorted in increasing order that is of length k - 1

		Since this array has been created using the frontal elements of A and B,
			we know that the last element we added to the array was from the front
			of A or B. Since A and B are sorted in increasing order, we know that
			the currently observed elements of A and B are the smallest elements in
			A and B respectively that are not in ret_lst

		During this iteration, the loop will do the following:
			Case X: Currently observed element of A < Currently observed element of B
			Case Y: Currently observed element of B < Currently observed element of A
			Case Z: Currently observed element of B = Currently observed element of A

		All of these choices pick the smallest element(s) possible to append to ret_lst,
		but we also know that the element that is currently being observed
"""
def iterative_merge(A, B):
	"""([int], [int]) -> [int]"""

	ret_lst = []
	cur_A_ind = 0
	cur_B_ind = 0

	while (cur_A_ind < len(A)) and (cur_B_ind < len(B)):
		cur_A = A[cur_A_ind]
		cur_B = B[cur_B_ind]

		# They are the same:
		if cur_A == cur_B:
			ret_lst += [cur_A, cur_B]
			cur_A_ind += 1
			cur_B_ind += 1

		# A has the smaller element
		elif cur_A < cur_B:
			ret_lst += [cur_A]
			cur_A_ind += 1

		# B has the smaller element
		elif cur_B < cur_A:
			ret_lst += [cur_B]
			cur_B_ind += 1

	# At least one of these is guaranteed to be empty, since the loop will only
	# stop once one of the indices is at the end of one of the arrays.
	A_leftovers = A[cur_A_ind:]
	B_leftovers = B[cur_B_ind:]

	return ret_lst + A_leftovers + B_leftovers

def recursive_merge(A, B):
	"""([int], [int]) -> [int]

	Recursive implementation of the merge procedure. Easier to prove than
	coming up with a loop invariant for the iterative method, but recursion
	depth limitation in Python limits any sort of practical usage.

	:param A: a sorted integer list
	:param B: a sorted integer list
	:return: sorted(A + B)
	"""
	if A == []:
		return B
	elif B == []:
		return A
	else:
		if A[0] == B[0]:
			return [A[0], B[0]] + recursive_merge(A[1:], B[1:])
		elif A[0] < B[0]:
			return [A[0]] + recursive_merge(A[1:], B)
		elif A[0] > B[0]:
			return [B[0]] + recursive_merge(A, B[1:])

def merge_sort_using_iter(A):
	if len(A) < 2:
		return A
	else:
		mid = len(A) // 2
		left = A[:mid]
		right = A[mid:]

		sorted_L = merge_sort_using_iter(left)
		sorted_R = merge_sort_using_iter(right)

		return iterative_merge(sorted_L, sorted_R)

def merge_sort_using_rec(A):
	if len(A) < 2:
		return A
	else:
		mid = len(A) // 2
		left = A[:mid]
		right = A[mid:]

		sorted_L = merge_sort_using_rec(left)
		sorted_R = merge_sort_using_rec(right)

		return recursive_merge(sorted_L, sorted_R)

def generate_random_arr(size):
	"""
	Generates an array of length size, with each element randomly ranging
	between 0 and 20.
	:param size: the length of the desired array
	:return:
	"""
	ret_lst = []
	for i in range(size):
		ret_lst += [random.randint(0, 20)]
	return ret_lst

def generate_random_tupified_arr():
	return (generate_random_arr(random.randint(0, 40)),)

def generate_sorted_arr_pair():
	return (sorted(generate_random_arr(random.randint(0, 25))),
			sorted(generate_random_arr(random.randint(0, 25))))

if __name__ == '__main__':

	# Testing Merge
	merge_tester = Tester(name="Merge Tester",
						  num_tests=50,
						  baseline=correct_merge,
						  input_generator=generate_sorted_arr_pair)
	merge_tester.add_function("Iterative Merge", iterative_merge)
	merge_tester.add_function("Recursive Merge", recursive_merge)
	merge_tester.test_all_functions()

	# Testing MergeSort
	mergesort_tester = Tester(name="MergeSort Tester",
							  num_tests=50,
							  baseline=sorted,
							  input_generator=generate_random_tupified_arr)
	mergesort_tester.add_function("MergeSort Using Iterative Merge",
								  merge_sort_using_iter)
	mergesort_tester.add_function("MergeSort Using Recursive Merge",
								  merge_sort_using_rec)
	mergesort_tester.test_all_functions()
