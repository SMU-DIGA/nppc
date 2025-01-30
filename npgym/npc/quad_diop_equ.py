import random


def generate_instance(low=1, high=100):
    values = [random.randint(low, high) for _ in range(4)]
    c = values[0] * values[1] * values[1] + values[2] * values[3]

    return (values[0], values[2], c), (values[1], values[3])


def verify_solution(instance, solution):
    a = instance[0]
    b = instance[1]
    c = instance[2]

    x = solution[0]
    y = solution[1]

    if not (x > 0 and y > 0):
        return False, "The solution is not valid."
    else:
        if (a * x * x) + (b * y) == c:
            return True, "Correct solution."
        else:
            return False, "The solution does not match."


# instance, solution = generate_instance()
# print(verify_solution(instance, solution))
