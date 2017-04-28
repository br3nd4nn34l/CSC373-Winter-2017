"""Notes on Multivariate Induction"""
"""
Bivariate Induction

Source: http://math.stackexchange.com/questions/7660/induction-on-two-integer-variables

To prove that predicate P(x, y) holds for all possible (x, y):
	Base Case:
		Show that P(smallest x, smallest y) holds
	Inductive Hypothesis:
		Assume that P(x, y) holds for x, y
	Inductive Step 1:
		Show that since P(x, y) holds, P(x + 1, y) must also hold
	Inductive Step 2:
		Show that since P(x, y) holds, P(x, y + 1) must also hold
	Conclusion:
		P(x, y) must hold for all x, y

"""