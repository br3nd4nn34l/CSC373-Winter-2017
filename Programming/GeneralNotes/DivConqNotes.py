"""Divide and Conquer - Algorithm Design Strategy"""
"""
Applicability:
    Suppose we have a problem with a given input and a desired output.

    This problem can be approached using DIVIDE AND CONQUER if:

        1) The input can be "split up" or partitioned into smaller
        sub-inputs

        2) The desired sub-outputs for the sub-inputs can be combined
        into the desired output for the given input

        3) The desired output for the smallest possible input is defined
        (i.e. there is a base case)
"""
"""
General Form of Divide and Conquer:

    def divConq_procedure(input):

        if base case:
            return correct_answer

        else:
            # Partition the input into sub-inputs
            inp1 = 1st partition of input
            inp2 = 2nd partition of input
            ...
            inpB = Bth partition of input

            # Find solutions to sub-inputs
            sol1 = divConq_procedure(inp1)
            sol2 = divConq_procedure(inp2)
            ...
            solB = divConq_procedure(inpB)

            # Combine solutions into answer and return it
            return combine(sol1, sol2, ..., solB)
"""
"""
Proving Termination of Divide and Conquer

    1) Prove that the combination method and any other helper functions
    used in the code terminate

    2) Do strong induction over the size of the input:

        Predicates and Variables:
            P(n) - the algorithm terminates on an input of size n

        Base Case:
            Show that algorithm terminates when given smallest possible
            input
            Then P(smallest input size) holds.

        Inductive Hypothesis:
            Assume that for some:
                (smallest input size) < k < n
                OR
                (k \in ((smallest input size), n)),
            P(k) holds.

        Inductive Step:
            Consider an input of size n.
            Show that the algorithm calls only:
                Itself on smaller instances of some size < n
                Other algorithms that are proved to terminate

            Since the algorithm calls itself on smaller instances and P(k)
            was assumed to hold for all (k \in ((smallest input size), n)),
            the algorithm must terminate in this case.

            Since the algorithm only calls code that we know terminates in
            this case, we know that it will terminate eventually for inputs
            of size n.

            Then P(n) holds.

        Conclusion:
            Since P(i) holds for all i \in [smallest input size, n],
            we can say that P holds for all possible inputs, which means
            that the algorithm must terminate for all possible inputs.
"""
"""
Proving Correctness of Divide and Conquer:

    0) Prove that the algorithm terminates! (see above)

    1) Prove the correctness of the combination method (combine()), and
    any other helper functions used in the code

    2) Do strong induction over the size of the input:

        Predicates and Variables:
            P(n) - the algorithm returns the correct output for an input of
            size n

        Base Case:
            Consider i = (smallest input size)
            Show that the algorithm returns the correct answer when given the
            smallest possible input
            Then P(smallest input size) holds.

        Inductive Hypothesis
            Assume that for some:
                (smallest input size) < k < n
                OR
                (k \in ((smallest input size), n)),
            P(k) holds.

        Inductive Step:

            Consider an input of size n.

            Show that the algorithm only calls the following to formulate its
            solution:
                Helper functions that we know are correct
                Itself on smaller inputs

            Since the algorithm was assumed to be correct for all k, and it
            is calling itself on inputs of size m < n, we know that P(m)
            must hold, and therefore these calls return the correct thing.

            Since we know all the helper functions are correct and the
            inputs we are feeding them from recursive calls are correct,
            we can conclude that the algorithm is producing a correct output.

            Thus P(n) holds.

        Conclusion:
            Since P(i) holds for all i \in [smallest input size, n],
            we can say that P holds for all possible inputs, which means
            that the algorithm must return the correct answer for all possible
            inputs.
"""
"""
Cost Analysis of Divide and Conquer (Master Theorem)

1) Figure out the "measure of interest" that will be used to gauge the
performance of the algorithm (e.g. number of comparisons, number of
executions for a certain operation)

2) Construct a recurrence relation T(n) that shows how the measure interest
varies according to n. Note: a recurrence relation refers to itself,
hence the name.

    General Form: T(n) = aT(m) + f, where:
        a - the number of times the algorithm is called again
        m < n - the size of the sub-problems
        f() is some arbitrary function

3) If the recurrence relation has form:
    T(n) = a * T(n / b) + O(n^d)

    Where:
        a = branching factor
        b = subproblem scaling factor
        d = the degree of some polynomial that bounds the other parts of the function

    Figure out
        a vs. (b ^ d) (i.e. figure out if vs. is <, >, or =)

    Master Theorem states:
        a < (b ^ d) -> T(n) \in Theta(n ^ d)
        a = (b ^ d) -> T(n) \in Theta((n ^ d)*(log n))
        a > (b ^ d) -> T(n) \in Theta(n ^ (log_b a))

    High-Level / Hand Wavy Reasoning:
        a < (b ^ d)
            Auxiliary cost of each subproblem is growing really fast, so n^d
            dominates -> Theta(n ^ d)

        a = (b ^ d)
            Auxiliary cost of each subproblem is the same (O(n^d)), and since n
            can only be divided by b O(log n) times, these terms are combined
            into: Theta((n ^ d) * (log n))

        a > (b ^ d)
            Auxiliary cost of each subproblem is decreasing, so this creates
            the slowest growth of them all
"""
"""
Cost Analysis of Non-Master Theorem Recurrences

1) Otherwise write out a table in the form:

depth | Expansion of T(n)
0		Expansion of T(n) at depth 0 (just T(n))
1		Expansion of T(n) at depth 1
2		Expansion of T(n) at depth 2
...
(Once the pattern has been figured out)
i		Expansion of T(n) at depth i

2) Figure out how many times T(n) can be expanded until it hits the base case;
for example (where base case is n ~= 1):
	T(n) = T(n / b) + ... can be expanded roughly (log_b n) times (n can only be
		divided by b (log_b n) times in a row)
	T(n) = T(n - 1) + ... can be expanded roughly n times
	T(n) = T(n - 4) + ... can be expanded roughly n/4 times

3) Set i to the number of possible expansions and solve for the closed form
of T(n)

"""