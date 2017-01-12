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

def generate_sorted_arr_pair():
	return (sorted(generate_random_arr(random.randint(0, 25))),
			sorted(generate_random_arr(random.randint(0, 25))))

def correct_merge(A, B):
	return sorted(A + B)


if __name__ == '__main__':
	merge_tester = Tester(num_tests=50,
						  baseline=correct_merge,
						  input_generator=generate_sorted_arr_pair)
	merge_tester.add_function("Iterative Merge", iterative_merge)
	merge_tester.add_function("Recursive Merge", recursive_merge)
	merge_tester.test_all_functions()