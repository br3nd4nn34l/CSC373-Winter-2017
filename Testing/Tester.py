import random

"""Class to automatically test my code for this course."""
class Tester():
	def __init__(self, name, baseline, input_generator, num_tests):
		"""(String, ((Unknown) -> Unknown), ((None) -> (Unknown)), int) ->
			Tester"""
		self.name = name
		self.baseline = baseline
		self.input_generator = input_generator
		self.num_tests = num_tests
		self.functions = {}

	def add_function(self, fxn_name, fxn):
		"""(String, ((Unknown) -> Unknown)) -> None"""
		self.functions[fxn_name] = fxn

	def test_function(self, function_name):
		"""(String) -> (Unknown, Unknown, Unknown, bool)"""

		inp = self.input_generator()
		expected = self.baseline(*inp)
		result = self.functions[function_name](*inp)

		return (inp,
				expected,
				result,
				expected == result)

	def test_battery(self, function_name):
		print("Testing {fxn_name}".format(fxn_name=function_name))
		for i in range(self.num_tests):
			test_result = self.test_function(function_name)
			passed = test_result[-1]
			if not passed:
				print("Test failed.\n\tInput:{inp}\n\tExpected:{"
					  "exp}\n\tOutput:{out}".format(inp=test_result[0],
													exp=test_result[1],
													out=test_result[2]))
				return False
		return True

	def test_all_functions(self):
		passes = []
		failures = []
		for fxn_name in self.functions.keys():
			if self.test_battery(fxn_name):
				passes += [fxn_name]
			else:
				failures += [fxn_name]
		print("{name} Test Results:\n\tPassing Functions:{passes}\n\tFailing "
			  "Functions:{fails}".format(name=self.name,
										 passes=passes,
										 fails=failures))