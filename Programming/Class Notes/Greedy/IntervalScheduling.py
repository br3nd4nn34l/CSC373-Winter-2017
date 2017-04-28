import random
from Testing.Tester import Tester

from Programming.DataStructures import Interval

"""
Problem: Interval Scheduling
    Input: list of intervals
    Output: a schedule such that the number of intervals completed is maximized
"""

"""
The brute force solution: try all possible combinations, select the longest valid one.
This WILL find the optimal solution, but it will be very slow (O(2^n))
"""

# For notation ease
def conflicts(interval1, interval2):
    return interval1.conflicts(interval2)

# For finding all possible combinations of something
def all_subsets(lst):
    if len(lst) == 0:
        return [[]]
    else:
        rec_result = all_subsets(lst[1:])
        this_result = []
        for res in rec_result:
            this_result += [[lst[0]] + res]
        return this_result + rec_result

# For checking if a schedule contains no conflicts
def check_schedule_validity(schedule):
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if conflicts(schedule[i], schedule[j]):
                return False
    return True


# Implementation of the Brute Force solution
def make_optimal_schedule_brute(intervals):
    all_possible_schedules = all_subsets(intervals)
    valid_schedules = filter(check_schedule_validity,
                             all_possible_schedules)
    most_interval_schedule = max(valid_schedules,
                                 key = lambda schedule: len(schedule))
    return sorted(most_interval_schedule,
                  key = lambda interval: interval.start)


# Implementation of the Greedy Solution - sort by finish time
def make_optimal_schedule_greedy(intervals):
    sorted_intervals = sorted(intervals, key=lambda interval: interval.end)
    ret_schedule = []
    for interval in sorted_intervals:
        if check_schedule_validity(ret_schedule + [interval]):
            ret_schedule += [interval]
    return sorted(ret_schedule,
                  key = lambda interval: interval.start)

# To generate test cases
def generate_random_interval_list():
    ret_lst = []
    for i in range(random.randint(3, 7)):
        start = random.randint(0, 20)
        length = random.randint(1, 7)
        ret_lst += [Interval(start, start + length)]
    return (ret_lst,)

if __name__ == '__main__':
    lst = [1, 2, 3]
    tester = Tester("Interval Scheduling Tester",
                    make_optimal_schedule_brute,
                    generate_random_interval_list,
                    50,
                    equivalence_fxn=(lambda x, y: len(x) == len(y)))
    tester.add_function("Greedy - Sorting By Finish Time", make_optimal_schedule_greedy)
    tester.test_all_functions()

