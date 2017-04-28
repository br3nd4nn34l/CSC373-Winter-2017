import random
import math

class Recurrence():

	def __init__(self, a, b, d):
		"""(int, int, int) -> Recurrence"""
		self.branching_factor = a
		self.subproblem_size = b
		self.poly_degree = d

	def __str__(self):
		"""(Recurrence) -> str"""

		# Be a dick and randomly trip me up when it comes to O(1)
		if self.poly_degree == 0:

			if random.randint(0, 2):
				poly_str = "1"
			else:
				poly_str = "n ^ 0"

		else:
			poly_str = "n ^ {pd}".format(pd=self.poly_degree)

		ret_str = "T(n) = {branch_factor} * T(n/{subproblem_size}) + O({fxn})".format(
			branch_factor=self.branching_factor,
			subproblem_size=self.subproblem_size,
			fxn=poly_str)
		return ret_str

	def correct_answer(self):
		"""(Recurrence) -> str"""

		# Figure out a, b^d
		a = self.branching_factor
		b_to_d = self.subproblem_size ** self.poly_degree

		wrapper = "Theta({eqn})"

		# Compare a with b^d
		if a < b_to_d:
			ret_str = wrapper.format(eqn="n ^ {poly_degree}")
		elif a == b_to_d:
			ret_str = wrapper.format(eqn="(n ^ {poly_degree}) * (log n)")
		elif a > b_to_d:
			ret_str = wrapper.format(eqn="n ^ (log_{subprob_size} {" \
									   "branching_factor})")

		return ret_str.format(poly_degree=self.poly_degree,
							  subprob_size=self.subproblem_size,
							  branching_factor=self.branching_factor)

def generate_abd():

	# Generate a random number in [0, 1, 2]
	type_num = random.randint(0, 2)

	# Generate a, b, and d's sufficiency value
	branching_factor = random.randint(1, 10)
	subproblem_size = random.randint(2, 10)
	sufficient = math.log(branching_factor,
						  subproblem_size)

	# This should be the less than case
	# d should be greater than sufficient
	if type_num == 0:

		# Generate whatever we want for the polynomial degree in this case
		if subproblem_size > branching_factor:
			polynomial_degree = random.randint(0, 10)

		# Otherwise we need a sufficiently large d (lol)
		else:
			polynomial_degree = random.randint(int(sufficient), 10)

	# This should be the (approximately) equals case
	# d should be equal to sufficient
	if type_num == 1:
		# b ^ d should equal a
		polynomial_degree = sufficient


	# This should be the greater than case
	# d should be less than sufficient
	else:
		# a > b ^ d
		polynomial_degree = random.randint(0, int(sufficient))

	return (branching_factor,
			subproblem_size,
			polynomial_degree)

def administer_question(question_num, rec, compact, tell_answer):

	# Format the question and print it
	pnt_str = "{rec}"
	if not compact:
		pnt_str = "What is the cost/runtime of " + pnt_str
	print(("Q{num}) " + pnt_str).format(num=question_num,
									   rec = rec))

	# Accept the user's answer
	answer = input()
	correct = rec.correct_answer()

	# Strip user answer and solution of all whitespace, compare
	answer = answer.lower().replace(" ", "")
	correct = correct.lower().replace(" ", "")

	if answer == correct:
		print("Right")
		return True
	else:
		print("Wrong")
		if tell_answer:
			print("Correct = {correct}".format(correct=rec.correct_answer()))
		return False

if __name__ == '__main__':
	num_questions = 12
	score = 0
	for i in range(num_questions):
		rec = Recurrence(*generate_abd())
		if (administer_question(i + 1, rec, True, True)):
			score += 1
	print("Your score was {num_correct}/{total}".format(num_correct=score,
														total=num_questions))


