import random, time
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
Better Solution - Recursion

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
Better Solution (Alternate Version) - More Intelligent Looping

Note that for the even case, we can just square the result instead of having
to recompute it, as the value is the same.

'''

def smarter_loop_modular_exp(a, b, m):

	# Throw out the trivial case
	if m == 1:
		return 0

	# Actually worth the time to compute now
	loops_left = b
	result = mod(a, m)

	while loops_left > 0:
		print(str(loops_left))
		if (loops_left % 2 == 1):
			result = mod(mod(a, m) * result,
						 m)
			loops_left -= 1
		else:
			result = mod(result ** 2,
						 m)
			loops_left //= 2

	return result

def testing_function(fxn_to_test, num_tests, verbose):
	"""((int, int, int) -> int) -> None
	Tests the given function with some random parameters to check validity
	:param fxn_to_test: the function I want to test
	:return: None
	"""
	t0 = time.time()
	for i in range(50):

		# Randomly generate a, b, and m
		a = random.randint(1, 10)
		b = random.randint(1, 7)
		m = random.randint(1, 35)

		# Calculate the expected result
		expected = (a ** b) % m
		# Calculate what the algorithm gets
		result = fxn_to_test(a, b, m)

		# Print out stuff maybe
		if verbose:
			print("(a, b, m) = {tup} | Answer = {ans}".format(tup=(a,b,m),
															  ans=result))

		# Notify on failures
		if expected != result:
			print("Failed on (a, b, m) = {tup}. Expected {exp}, "
				  "got {res}".format(tup=(a, b, m),
									 exp=expected,
									 res=result))
			return
	t1 = time.time()
	print("Tests successful! Total test time: {tm}. Average: {avg}".format(
		tm=t1 - t0,
		avg=(t1 - t0) / num_tests))

if __name__ == '__main__':
	num_tests = 50
	verbose = False

	print("Testing looping implementation...")
	testing_function(looping_modular_exp, num_tests, verbose)

	print("Testing recursive implementation...")
	testing_function(recursive_modular_exp, num_tests, verbose)

	print("Testing smarter looping implementation...")
	testing_function(smarter_loop_modular_exp, num_tests, verbose)
