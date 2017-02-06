from Testing.Tester import Tester
import random
import IntervalScheduling
from IntervalScheduling import conflicts
from DataStructures.Interval import Interval


"""
Problem: Interval Coloring
    Input: [Interval]
    Output: the minimum number of colors N needed to form N non-intersecting schedules
    Applications:
        If we assign a machine to a color, we have the minimum number of
        machines needed to process the intervals in parallel
"""


# Repeatedly call the optimal scheduling algorithm on the intervals
# - each optimal schedule will be their own color
def baseline_solution(intervals):
    if intervals == []:
        return 0
    else:
        no_conflict_schedule = IntervalScheduling.make_optimal_schedule_greedy(intervals)
        no_conf_interval_set = set(no_conflict_schedule)
        leftover_interval_set = set(intervals) - (no_conf_interval_set)
        return 1 + baseline_solution(list(leftover_interval_set))


# This is the greedy solution
def greedy_interval_coloring(intervals):

    if len(intervals) > 1:
        # Sort the intervals by start, ascending
        sorted_by_start = sorted(intervals,
                                 key=lambda interval: interval.start)

        # Map of form {int:[Interval]}
        highest_color = 1
        color_map = {highest_color:[sorted_by_start[0]]}


        # Go through the intervals
        for interval in sorted_by_start[1:]:

            # Filter the colors by which one can take the new interval without conflicts
            valid_colors = list(filter(lambda col: not conflicts(color_map[col][-1], interval),
                                       color_map.keys()))
            # Add the interval to the smallest color if it exists
            if len(valid_colors) > 0:
                color_map[min(valid_colors)] += [interval]

            # Otherwise add it to a new highest color
            else:
                highest_color += 1
                color_map[highest_color] = [interval]

        return highest_color
    else:
        return 0

if __name__ == '__main__':
    tester = Tester("Interval Coloring Tester",
                    baseline_solution,
                    IntervalScheduling.generate_random_interval_list,
                    50)
    tester.add_function("Greedy Interval Coloring",
                        greedy_interval_coloring)
    tester.test_all_functions()