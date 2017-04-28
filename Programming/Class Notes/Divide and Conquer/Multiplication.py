import random

from Programming.Testing import Tester

"""
Multiplication - Divide and Conquer Example 2
"""
"""

Problem: Integer Multiplication
    Inputs:
        a \in N
        b \in N
    Output:
        a * b \in N
            OR
        a TIMES b

    Input Size Measurement:
        Number of digits

    Performance Measurement:
        Number of single-digit-multiplications

Notes:
    For the sake of simplicity, assume:
        A and B are decimal numbers (BASE 10)
        len(A) = len(B) is a power of 2

    The elementary-school multiplication algorithm uses O(n^2) single-digit multiplications.
    This is because every digit in the first number (of size O(n)) must be multiplied by
    every digit in the second number (O(n)), thus leading to runtime O(n) * O(n) -> O(n^2)

"""

#### Convenience functions for doing operations on numerical strings #####
def string_multiplication(A, B):
    """(str, str) -> str"""
    return str(int(A) * int(B))

def string_addition(arr):
    """(str, str) -> str"""
    total = 0
    for num in arr:
        total += int(num)
    return str(total)

def string_subtraction(arr):
    """(str, str) -> str"""
    total = 0
    for num in arr:
        total -= int(num)
    return str(total)

def split_in_half(arr):
    """[Object] -> ([Object], [Object])
    """
    mid = (len(arr) // 2)
    return (arr[:mid], arr[mid:])
####

"""Idea:

Let A obey the following properties:
    A is written in base b
    A has n digits
Then:
    The digits of A can be split up such that:
        A -> (a1, a2), A = (a1 with (n / 2) zeroes on the end) + a2 = (a1 * (base ** (n / 2)) + a2
    For base 10:
        A = (a1 * (10 ** (n / 2)) + a2

When we multiply the split equation of two numbers A, B, we get:
    A * B
        = ((a1 * (10 ** (n / 2)) + a2) * ((b1 * (10 ** (n / 2)) + b2)
    Let h = base ** (n // 2)
    We can foil this out to:
        =  ((a1 * b1) * (h ** 2)) + ((h) * (a2 * b1 + a1 * b2)) + (a2 * b2)

This expansion lends itself to a recursive form! (there are multiplications in it!)
"""
"""Cost-Analysis

In the algorithm, there are 4 recursive calls:
    A1_B1_product = div_conq_multiplication(A1, B1)
    A1_B2_product = div_conq_multiplication(A1, B2)
    A2_B1_product = div_conq_multiplication(A2, B1)
    A2_B2_product = div_conq_multiplication(A2, B2)
Note that (A1, A2, B1, B2) are all size (n / 2), which means there are
FOUR recursive calls on instances of size n over TWO

Note that after the recursive call we need to call some for-loops that
add zeroes to the end of the necessary numbers. These loops take O(n) time.

In the algorithm's base case there is ONE single-digit multiplication,
which leads to the following recurrence relation:


T(n) =
    if n == 1:
        O(1)
    else:
        4 * T(n / 2) + O(n)

In this case, (a, b, d) = (4, 2, 1)

Determining what case of master theorem to use:
    a ** b vs. d
    -> 4 ** 2 vs. 1
    -> 4 ** 2 > 1
    -> a ** b > d
This corresponds to the following case in master theorem:
    a ** b > d --> T(n) \in Theta(n ^ log_b a)
    Since (a, b) = (4, 2):
    T(n) \in Theta(n ^ log_b a) --> T(n) \in Theta(n ^ log_2 4) = Theta(n^2)
    Thus:
        T(n) \in Theta(n^2)

Since this algorithm is in Theta(n^2), it is NO BETTER than the
elementary-school algorithm! We need to go back to the drawing board!
"""
def div_conq_multiplication(A, B):
    if len(A) == 1:
        return string_multiplication(A, B)
    else:

        num_digits = len(A)

        A1, A2 = split_in_half(A)
        B1, B2 = split_in_half(B)

        # Figure out the four products that we need
        A1_B1_product = div_conq_multiplication(A1, B1)
        A1_B2_product = div_conq_multiplication(A1, B2)
        A2_B1_product = div_conq_multiplication(A2, B1)
        A2_B2_product = div_conq_multiplication(A2, B2)

        # Attach num_digits many zeroes onto the end of A1*B1
        for i in range(num_digits):
            A1_B1_product += "0"

        # Attach num_digits // 2 many zeroes onto the end of A1*B2, A2*B1
        for i in range(num_digits // 2):
            A1_B2_product += "0"
            A2_B1_product += "0"

        # Return the result
        return string_addition([A1_B1_product,
                                string_addition([A1_B2_product, A2_B1_product]),
                                A2_B2_product])


""" Idea
Note that:
    (x1 + x2)(y1 + y2)
        = (x1 * y1) + (x1 * y2) + (x2 * y1) + (x2 * y2)
    If we rearrange this:
    (x1 * y2) + (x2 * y1) = (x1 + x2)(y1 + y2) - ((x1 * y1) + (x2 * y2))

    Therefore, we can find (A1_B2_product + A2_B1_product) using:
        A1, A2, B1, B2, A1_B1_product, A2_B2_product (all of which we have)
        In other words:
            (A1_B2_product + A2_B1_product) = (A1 + A2)(B1 + B2) - (A1_B1_product + A2_B2_product)

    Note that (A1, A2, B1, B2) can be combined using two additions and only one multiplication -
        this fewer multiplications than finding (A1_B2_product, A2_B1_product),
        which would need two multiplications total (for A1 * B2 and A2 * B1)

    THIS DERIVATION MEANS:
        WE CAN DO ONE LESS MULTIPLICATION AND THEREFORE ONE LESS RECURSIVE CALL ON OUR NUMBERS!
"""
"""Cost-Analysis

In the algorithm, there are 3 recursive calls:
    A1_B1_product = div_conq_multiplication(A1, B1)
    product_sum_A1_A2_sum_B1_B2 = string_multiplication(sum_A1_A2, sum_B1_B2)
    A2_B2_product = div_conq_multiplication(A2, B2)

Note that (A1, A2, B1, B2) are all size (n / 2), which also means that their sums are size (n / 2):
In conclusion, there are THREE recursive calls on instances of size n over TWO

Note that after the recursive call we need to call some for-loops that
add zeroes to the end of the necessary numbers. These loops take O(n) time.

In the algorithm's base case there is ONE single-digit multiplication,
which leads to the following recurrence relation:


T(n) =
    if n == 1:
        O(1)
    else:
        3 * T(n / 2) + O(n)

In this case, (a, b, d) = (3, 2, 1)

Determining what case of master theorem to use:
    a ** b vs. d
    -> 3 ** 2 vs. 1
    -> 3 ** 2 > 1
    -> a ** b > d
This corresponds to the following case in master theorem:
    a ** b > d --> T(n) \in Theta(n ^ log_b a)
    Since (a, b) = (4, 2):
    T(n) \in Theta(n ^ log_b a) --> T(n) \in Theta(n ^ log_2 3)

Since this algorithm is in Theta(n^(log_2 3)), it is about Theta(n ^ 1.58),
which means that it is BETTER than the elementary-school algorithm!
"""
def karatsuba_div_conq(A, B):
    if len(A) == 1:
        return string_multiplication(A, B)
    else:

        num_digits = len(A)

        A1, A2 = split_in_half(A)
        B1, B2 = split_in_half(B)

        # Figure out the products
        A1_B1_product = div_conq_multiplication(A1, B1)
        A2_B2_product = div_conq_multiplication(A2, B2)

        # Use the trick
        sum_A1_A2 = string_addition([A1, A2])
        sum_B1_B2 = string_addition([B1, B2])
        product_sum_A1_A2_sum_B1_B2 = string_multiplication(sum_A1_A2,
                                                            sum_B1_B2)
        sum_A1B1_A2B2 = string_addition([A1_B1_product, A2_B2_product])
        middle = string_addition([product_sum_A1_A2_sum_B1_B2,
                                  "-" + sum_A1B1_A2B2])

        # Attach num_digits many zeroes onto the end of A1*B1
        for i in range(num_digits):
            A1_B1_product += "0"

        # Attach num_digits // 2 many zeroes onto the end of the middle
        for i in range(num_digits // 2):
            middle += "0"

        # Return the result
        return string_addition([A1_B1_product,
                                middle,
                                A2_B2_product])


def generate_valid_number_pair():

    desired_length = 2 ** random.randint(1, 3)
    num1, num2 = str(random.randint(1, 9)), str(random.randint(1, 9))

    for i in range(desired_length - 1):
        num1 += str(random.randint(0, 9))
        num2 += str(random.randint(0, 9))

    return (num1, num2)


if __name__ == '__main__':

    # Testing Multiplication
    mult_tester = Tester(name="Multiplication Tester",
                         num_tests=50,
                         baseline=string_multiplication,
                         input_generator=generate_valid_number_pair)
    mult_tester.add_function("Naive Div Conq Multiplication", div_conq_multiplication)
    mult_tester.add_function("Karatsuba's Div Conq Multiplication", karatsuba_div_conq)
    mult_tester.test_all_functions()