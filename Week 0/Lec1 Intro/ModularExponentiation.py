import random
from Testing.Tester import Tester
'''
Problem: Modular Exponentiation

	Inputs:
		a \in N
		b \in N
		m \in N

	Outputs:
		((a ** b) mod m) \in [0, 1, ... m - 1]
						OR
		(a to the b) remainder m

	Performance Measurement:
		Number of multiplications

Important Notes:
	For ease of notation:
		a mod b <--> mod(a, b)
	For any {a, b, m} \subset N:
		mod((a * b), m) = mod((mod(a, m) * mod(b, m)),
		                      m)
	Thus:
		mod(a ** i, m) -->

			Tautology:
				= mod(a * (a ** (i - 1)),
				      m)
				= mod((mod(a, m) * mod(a ** (i - 1), m),
				      m)
			If i is even:
				= mod((a ** (i/2)) * (a ** (i/2)),
				      m)
				= mod(mod(a ** (i/2), m) * mod(a ** (i/2), m),
				      m)
				= mod(mod(a ** (i/2), m) ** 2,
					  m)

			Note that if i is odd, i - 1 must be even - the top equation can
			therefore be used to "reduce" an odd number to an even one for
			fewer computations.
'''

def mod(a, b):
	'''(int, int) -> int
	Modulo function to emulate my notation given above.
	Returns (a mod b).
	'''
	return a % b


def correct_modular_exp(a, b, m):
	"""
	Dumb way, but this works for sure
	"""
	return mod(a ** b,
			   m)

'''
Naive Solution - Looping

General Idea - from the top equation in the notes above, we can expand the
recurrence into the following for various values:
	mod(a ** i, m) = mod((mod(a, m) * mod(a ** (i - 1), m),
	                      m)
	mod(a ** (i - 1), m) = mod((mod(a, m) * mod(a ** (i - 2), m),
							   m)
	mod(a ** (i - 2), m) = mod((mod(a, m) * mod(a ** (i - 3), m),
							   m)
	...
	mod(a ** 4, m) = mod(mod(a, m) * mod(a ** 3, m),
                         m)
	mod(a ** 3, m) = mod(mod(a, m) * mod(a ** 2, m),
                         m)
	mod(a ** 2, m) = mod(mod(a, m) * mod(a, m),
                         m)

Note that for every expansion, the first argument of the mod function is
equal to mod(a, m) * (the result of the previous calculation). This means we
can easily use a loop that accesses the result of the previous calculation.

Cost of running:
	Note that every iteration of the loop does O(1) modulo calculations.
	Since the loop runs in O(b) time (range(b - 1) is clearly O(b)), we can
	say that the cost of this solution is O(1) * O(b) = O(b).

'''
def looping_modular_exp(a, b, m):
	"""(int, int, int) -> int
	Implementation of the naive looping solution to modular exponentiation
	"""

	# Trivial case, just return ASAP
	if m == 1:
		return 0

	# Otherwise start the loop
	a_m_remainder = mod(a, m)
	result = a_m_remainder
	for i in range(b - 1):
		result = mod(a_m_remainder * result, m)
	return result

'''
Better Solution - Repeated Square Recursion

General Idea - from the top equation in the notes above, we can clearly
derive a recursive relationship. The following is the recurrence:

mod(a ** b, m) = if b == 1:
					mod(a, m)
				 elif (b is odd):
				 	mod((mod(a, m) * mod(a ** (b - 1), m),
				 	    m)
				 elif (b is even):
				 	mod(mod(a ** (b/2), m) ** 2,
				 	    m)

Note that the expansion for the odd case will lead directly into the quicker
even case!

'''
'''
Cost Analysis

If we cache mod(a ** (x / 2), m), where x is the largest even number no bigger
than b, (i.e. b if b is even or (b - 1) if b is odd), we get the following
recurrence relationship for the algorithm (T(n) is the number of mod
operations the algorithm executes when given b = n):
	T(b) =
		1 if b == 1
		T(b/2) + O(1) otherwise

	T(b/2) <-(recursive call) +
	O(1) <-(outer mod plus an extra mod for the odd case)

If we recall the master theorem, we see that this recurrence relation falls
into the same "format" as those allowed to be analyzed by the master theorem.

Master Theorem:
	If:
	 	T(n) = a * T(n/b) + O(n ** d)
		T(1) = c
	Then:
		If a < (b ** d) -> T(n) \in Theta(n ** d)
		If a = (b ** d) -> T(n) \in Theta((n ** d)(log n))
		If a > (b ** d) -> T(n) \in Theta(n ** (log_b a))

In our case, a = 1, b = 2, d = 0,
	--> a vs. (b ** d)
	--> 1 vs. (2 ** 0)
	--> 1 = 1
	--> a = (b ** d)
	--> T(n) \in Theta((n ** d)(log n))
	--> T(n) \in Theta((n ** 0)(log n))
	--> T(n) \in Theta(log n)
	--> T(b) \in Theta(log b)

Thus, the "cost" of this solution is Theta(log b) --> the solution is O(log b)
'''
'''
Proof of Termination (strong induction over b):

Note that b is the variable being recursed over. Since we are always feeding
(b // 2) = floor(b/2) into the recursive calls, the algorithm is being called on
smaller and smaller instances of b.

	Predicates and Variables:
		P(n) - true iff the algorithm terminates when b = n.

	Base Case
		Let b = 1
		Then the algorithm terminates directly after the first if-check.
		Then P(1) holds.

	Inductive Hypothesis
		Assume for all k \in (1, n) (exclusive range), P(k) holds.

	Inductive Step:
		Consider b = n.
		Then the algorithm will call itself with b = n // 2 = floor(n/2).
		Since floor(n/2) \in (1, n), we know that the call to the algorithm
		with b = floor(n / 2) will terminate.
		Since this call to the algorithm terminates, the outer call will also
		terminate as it only calls other methods that we know terminate

	Thus, the algorithm will terminate because P(n) has been proven to be
	true for all n.
'''
'''
Proof of Correctness (strong induction over b):

	Predicates and Variables:
		P(n) - true iff the algorithm returns mod(a ** n, m) when given b = n.

	Base Case
		Let b = 1.
		Then the algorithm hits the base case and returns:
			mod(a, m) = mod(a ** 1, m)
		Thus, P(1) holds.

	Inductive Hypothesis:
		Assume for all k \in (1, n), P(k) holds.

	Inductive Step:
		Consider the case where (b = n).
		Then the algorithm will call itself to calculate mod(a ** (n // 2), m)
		Since (n // 2) \in (1, n), P(n // 2) holds, which means that this
			calculation is correct.
		We already know from previous derivations that the algorithm
			correctly uses this result to calculate mod(a ** n, m)
		Thus, P(n) holds.

	Thus, the algorithm is correct for all b as P(n) was proven to hold for
	all n \in N,


'''
def recursive_modular_exp(a, b, m):
	"""(int, int, int) -> int
	Implementation of the recursive solution to modular exponentiation
	"""
	# Toss out the trivial case
	if m == 1:
		return 0
	# Otherwise continue
	return actual_recursive_modular_exp(a, b, m)

def actual_recursive_modular_exp(a, b, m):
	"""(int, int, int) -> int

	The "real" implementation of the recursive solution to modular
	exponentiation. This is separate from the above function so we don't have
	to do the triviality check with every recursive call (if we know m == 1
	once, there is no reason to continue checking it).

	"""

	if (b == 1):
		return mod(a, m)
	else:
		result_from_nearest_even = actual_recursive_modular_exp(a,
																b // 2,
																m) ** 2
		if (b % 2 == 1):
			return mod(mod(a, m) * result_from_nearest_even,
					   m)
		else:
			return mod(result_from_nearest_even,
					   m)

'''
Better Solution (Alternate Version) - More Intelligent Looping (Repeated
Squaring)

We can use a while-loop to "jump" the value of the exponent by a factor of 2
every time we encounter an even number, shortening the runtime of the algorithm.

Idea:

Note for any i, mod(a ** i, m) = mod(mod(a, m) ** i, m)
mod(a ** 7, m)
	= mod(mod(a, m) ** 7, m)
	= mod((mod(a, m) ** 4) * (mod(a, m) ** 2) * (mod(a, m) ** 1), m)
	= mod((mod(a, m) ** (2 ** 2)) * (mod(a, m) ** (2 ** 1)) * (mod(a, m) ** (2 ** 0)), m)

We can clearly see that we can repeatedly square mod(a, m) while
right-bit-shifting b, only multiplying the first argument of the mod by the
new square of mod(a, m) when the least significant bit of b is 1.
'''
'''
Cost Analysis:

We can clearly see that the while loop's continuation condition depends on
exponent. At the end of every loop, exponent is reassigned to
	(exponent // 2) = floor(exponent / 2).

This is equivalent to bit-shifting the binary representation of exponent to
the right by one space.

Since the binary representation of exponent is O(log exponent) in length,
this operation can only be performed O(log exponent) times before exponent = 0,
at which point the loop will stop.

Therefore, the algorithm will only do O(log exponent) loop iterations before
stopping, and since exponent \in O(b), the algorithm must do O(log b)
iterations.

Since we are only doing 2 \in O(1) modular multiplications at the most for
each iteration, the algorithm must do O(1) * O(log b) modular multiplications.

Since O(1) * O(log b) \in O(log b), this algorithm can be said to have cost
O(log b).
'''
'''
Proof of Termination

As mentioned in the previous section on cost analysis, the operation
	exponent //= 2 is equivalent to bit shifting the binary
	representation of exponent to the right once.
Since the binary representation of exponent is finite in length, repeated
right bit shifts will eventually reduce exponent to 0, which means that the
algorithm will terminate.

OR

We know that exponent halves and floows with every iteration,
and that exponent will eventually reach zero after repeated iterations.
Thus, the algorithm will terminate.
'''
'''
Proof of Correctness

To prove the correctness of an iterative algorithm, we need a loop invariant
- a predicate that has the following property:
	Let P(i) be true when iteration i fulfills some property.
	(P(i) loop invariant) <=> (P(i) -> P(i + 1) holds)
'''
'''
Lemma A:
	After iteration i occurs, base = mod(a ** (2 ** i), m)
	Proof:

		Let P(n) be true when after iteration n,
			base = mod(a ** (2 ** n), m)

		Consider after the first iteration
			base
				= mod(mod(a, m) ** 2, m)
				= mod(a ** 2, m)
			By code inspection, P(1) holds.

		Assume for some n \in N, P(n) holds.

		Consider after iteration n + 1.
			base_(n + 1)
				= mod(base_n ** 2, m)
				= mod((mod(a, m) ** (2 ** n)) ** 2, m)
				= mod((mod(a, m) ** (2 ** n)) * (mod(a, m) ** (2 ** n)), m)
				= mod((mod(a, m) ** (2 ** (n + 1)), m)
				= mod(a ** (2 ** (n + 1)), m)
		Then P(n + 1) holds, and P must hold for all n.
'''
''' Correctness cont.
Proof by Weak Induction over Iteration Number:

	Predicates and Variables:

		Define A ++ B to be the concatenation of (in the order specified below):
			A's digits from left to right
			B's digits from left to right

		Define B(n) to be the binary representation of n

		Define len(n) to be the number of digits in n.

		Define A[n] to be the n-th digit of A
			(indexed starting from 0 in the right)

		Define A[n:m], (m < n) to be a slice of the digits from A
			Example:
				Anything[0:0] = 0
				(1001)[2:0] = 1 (001 -> 1)
				(321345)[3:1] = 134 (32[134]5 -> 134)

		Define f as follows:
			f(i)
				= mod(mod(a, m) ** B(b)[(i - 1):0], m)
				= mod(a ** B(b)[(i - 1):0], m)
			OR: the i-rightmost digits of B(b)

		Define loop invariant P(i) as follows:
			At the end of iteration i (before exponent is bit shifted),
				result = f(i)

'''
''' Correctness cont.
	Base Case:
		Consider the value of result before any iterations.
		Then by observation, result = 1.
		Also, f(1)
			= mod(mod(a, m) ** B(b)[0:0], m)
			= mod(mod(a, m) ** 0, m)
			= mod(1, m)
			= 1
		Thus, P(0) holds.
'''
''' Correctness cont.
	Inductive Hypothesis:
		Assume that for some (n - 1) \in N, P(n - 1) holds.

	Inductive Step:
		Consider i = n.
		Let L = len(B(b))
		After the (n-1)-th iteration, we know the following:
			exponent = B(b)[(L - 1):(n - 1)]
			result = mod(a ** B(b)[(n - 2):0], m)

		Case A: exponent is even (i.e. exponent[0] = 0)
			In this case, result does not change.
			The last digit of exponent is B(b)[n - 1] = 0, which means that
				B(b)[(n - 1):0] = 0 ++ B(b)[(n - 2):0]
			Since prepending a zero to a binary number doesn't change it's value
				B(b)[(n - 1):0] = B(b)[(n - 2):0]
			Since f(n) = B(b)[(n - 1):0] = B(b)[(n - 2):0],
				and the algorithm doesn't change the value of result,
				P(n) holds when exponent is even.

		Case B: exponent is odd (i.e. exponent[0] = 1)
			In this case, the if-statement is entered, causing:
				result = mod(result * base, m)
			By the induction hypothesis, after the (n - 1)-th iteration:
				result
					= mod(f(n - 1) * base, m)
					= mod(mod(a ** B(b)[(n - 2):0], m) * base, m)
			By Lemma A, we know that:
				base = mod(a ** (2 ** (n - 1)), m)
			Thus:
				result
					= mod(mod(a ** B(b)[(n - 2):0], m) * mod(a ** (2 ** (n - 1)), m), m)
				Since (mod(a ** i, m) = mod(mod(a, m) ** i, m):
					= mod(mod(a, m) ** (B(b)[(n - 2):0], m) + (2 ** (n - 1))), m)

				Looking at the exponent addition EA:
					exponent_addition
						= B(b)[(n - 2):0], m) + (2 ** (n - 1))
						= (2 ** (n - 1)) + B(b)[(n - 2):0], m)
						= 1(0...0)_2 <- this is a (n - 1)-long chain of zeros +
							B(b)[(n - 2):0] <- this is a (n - 1)-digit binary number
						= 1 ++ B(b)[(n - 2):0]

				Since exponent is odd, we know that it's last digit is 1, i.e.
					(exponent[0] = 1) -> B(b)[n - 1] =  1

				Thus, we know that:
					1 ++ B(b)[(n - 2):0]
						= B(b)[n - 1] ++ B(b)[(n - 2):0]
						= B(b)[(n - 1):0]

			Therefore, result = mod(mod(a, m) ** B(b)[(n - 1):0], m)
			Since f(n) = mod(mod(a, m) ** B(b)[(n - 1):0], m), result = f(n)
			In conclusion, P(n) holds when n is odd.

		Since we have shown that P(n) holds when n is both even and odd,
		P(n) must hold for all n.

	Conclusion:
		Since we have proven that P(n) holds for all n, if b has n
		binary digits, the final value of result will be equal to:
			f(n)
				= mod(mod(a, m) ** B(b)[(n - 1):0], m)
			Since B(b)[(n-1):0] is just B(b) = b (straight change of base has no effect on value),
				= mod(mod(a, m) ** b, m)
				= mod(a ** b, m)
		Thus the algorithm returns what it was designed to return.

'''
def smarter_loop_modular_exp(a, b, m):

	# Throw out the trivial case
	if m == 1:
		return 0

	# Actually worth the time to compute now
	# Code from Wikipedia, easier to understand
	result = 1
	base = mod(a, m)
	exponent = b
	while exponent > 0:
		if (exponent % 2 == 1):
			result = mod(result * base,
						 m)
		base = mod(base ** 2,
				   m)
		exponent //= 2
	return result

def abm_generator():
	return (random.randint(2, 10),
			random.randint(1, 7),
			random.randint(1, 35))

if __name__ == '__main__':
	mod_exp_tester = Tester(baseline=correct_modular_exp,
							input_generator=abm_generator,
							num_tests=50)

	fxns = [("Looping Modular Exponentiation", looping_modular_exp),
			("Recursive Modular Exponentiation", recursive_modular_exp),
			("Smarter Looping Modular Exponentiation", smarter_loop_modular_exp)]

	for fxn_tup in fxns:
		mod_exp_tester.add_function(*fxn_tup)

	mod_exp_tester.test_all_functions()