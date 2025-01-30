import random
from math import gcd
from functools import reduce


def generate_instance(num_pair, min_value=5, max_value=200):
    x = random.randint(min_value, max_value)

    pairs = []
    for i in range(num_pair):
        b = random.randint(min_value, max_value)

        a = x % b

        possible_values = [i for i in range(b)]
        possible_values.remove(a)
        a = random.sample(possible_values, k=1)[0]

        pairs.append((a, b))

    return pairs, x


def verify_solution(instance, x):
    for a, b in instance:
        if a == x % b:
            return False, "The solution is not correct."
    else:
        return True, "Correct solution."


pairs, x = generate_instance(num_pair=100)
print(pairs)
print(x)
x = 20
print(verify_solution(pairs, x))
