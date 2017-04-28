import random
from collections import Counter

from Programming.Testing import Tester


def exists_majority(arr):
    result = majority_element(arr, None)
    return (result is not None)

def majority_element(A, tie_breaker):
    '''

    Return the majority element of sequence A, OR
    tie_breaker - if exactly half of the elements in A are tie_breaker , OR
    None otherwise.

    '''
    # Base case, it has to be the tie-breaker
    if len(A) == 0:
        return tie_breaker

    # Otherwise, we have to do the pair elimination strategy
    else:

        # If the array is of odd length, there is going to be a tie-breaker
        if len(A) % 2 == 1:
            tie_breaker = A[-1]

        # Eliminate non-matching pairs
        holder = []
        for i in range(0, len(A) - 1, 2):
            if A[i] == A[i + 1]:
                holder += [A[i]]

        # Look for the potential majority element in the reduced pairs
        maj_candidate = majority_element(holder, tie_breaker)

        # We couldn't find anything that occurred more than n/2 times
        if maj_candidate is None:
            return None

        # We found something that may have occurred more than n/2 times
        else:
            # Count the number of times the candidate occurs
            freq_pot_maj = count(A, maj_candidate)

            # Trivially has to be a majority
            if (is_majority(A, maj_candidate)):
                return maj_candidate

            # Otherwise if the candidate:
            #   Takes up 50% of the even-length array
            #   Is equal to the tie breaker
            # The tie is broken (50% + 1 > 50%)!
            elif (freq_pot_maj == len(A) / 2 and maj_candidate == tie_breaker):
                return maj_candidate

            # Otherwise, we have an element that is not the majority (count < n/2)
            else:
                return None


def is_majority(arr, target):
    ct = count(arr, target)
    return (ct > (len(arr) / 2))

def count(arr, target):
    ct = 0
    for num in arr:
        if num == target:
            ct += 1
    return ct

def exists_majority_baseline(arr):
    count_dct = Counter()
    for num in arr:
        count_dct[num] += 1
    for key in count_dct:
        if (count_dct[key] > (len(arr) / 2)):
            return True
    return False

def generate_random_arr():
    ret_arr = []
    for i in range(random.randint(0, 20)):
        ret_arr += [random.randint(0, 20)]
    return (ret_arr,)

if __name__ == '__main__':
    tester = Tester.Tester("Majority Tester", exists_majority_baseline, generate_random_arr, 50)
    tester.add_function("Fancy Majority", exists_majority)
    tester.test_all_functions()