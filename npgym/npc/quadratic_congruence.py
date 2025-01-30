import random


def generate_instance(min_value=10, max_value=100):
    x = random.randint(min_value, max_value)

    b = random.randint(min_value, max_value)

    a = (x * x) % b

    c = x + random.randint(1, max_value)

    instance = {"a": a, "b": b, "c": c}

    return instance, x


def verify_solution(instance, x):
    a = instance["a"]
    b = instance["b"]
    c = instance["c"]

    if x >= c:
        return False, "x is larger than c."

    if a == x * x % b:
        return True, "Correct solution."
    else:
        return False, "The x*x % b != a."


instance, solution = generate_instance(min_value=10, max_value=20)

print(verify_solution(instance, solution))
