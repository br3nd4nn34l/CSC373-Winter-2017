import random

from Programming.Testing import Tester

"""
Problem: Counting the Number of Inversions in a List
    Input: A: [int] (ALL DISTINCT)
    Output: number of times where:
        (A[i] > A[j]) AND
        (i < j)

"""


# Trivial solution, runs in O(n^2) time
def naive_inversion_counter(A):
    inversions = 0
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            if A[i] > A[j]:
                inversions += 1
    return (sorted(A), inversions)


"""
Note that the number of inversions is equal to the number of movements needed to
transform an array into a sorted version of itself"""


# Enhance Merge from Mergesort so that every time a
# merge between inversions is done, it counts the inversion
def enhanced_merge(A, B):
    """([int], [int]) -> [int]"""

    # Ideally, every element in A should be less than every element in B
    # (for no inversions between the two), thus, for every element that isn't,
    # we need to add the number of elements left over in A to the number
    # of inversions - this is the number of elements the current element
    # "inverts" with

    inversions = 0
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
            inversions += (len(A) - cur_A_ind)
            ret_lst += [cur_B]
            cur_B_ind += 1

    # At least one of these is guaranteed to be empty, since the loop will only
    # stop once one of the indices is at the end of one of the arrays.
    A_leftovers = A[cur_A_ind:]
    B_leftovers = B[cur_B_ind:]

    return (ret_lst + A_leftovers + B_leftovers,
            inversions)  # To generate test cases

def div_conq_inversion_counter(A):
    if len(A) < 2:
        return (A, 0)
    else:
        mid = len(A) // 2
        left, right = A[:mid], A[mid:]
        left_sorted, left_invs = div_conq_inversion_counter(left)
        right_sorted, right_invs = div_conq_inversion_counter(right)

        final_sorted, last_invs = enhanced_merge(left_sorted, right_sorted)
        total_invs = left_invs + right_invs + last_invs
        return (final_sorted, total_invs)

def generate_randomly_sized_lst():
    temp_set = set()
    for i in range(30):
        to_put = random.randint(0, 20)
        if to_put not in temp_set:
            temp_set.add(to_put)
    return (list(temp_set),)


if __name__ == '__main__':
    tester = Tester("Inversion Counting Tester", naive_inversion_counter,
                    generate_randomly_sized_lst, 5000)
    tester.add_function("Divide and Conquer Inversion Counter", div_conq_inversion_counter)
    tester.test_all_functions()