import random


def generate_instance(low: int, high: int):
    values = [random.randint(low, high) for _ in range(4)]
    c = values[0] * values[1] * values[1] + values[2] * values[3]

    instance = {"a": values[0], "b": values[2], "c": c}

    return instance, list([values[1], values[3]])


def verify_solution(instance, solution):
    a = instance["a"]
    b = instance["b"]
    c = instance["c"]

    try:
        if len(solution) != 2:
            return False, "The solution is not valid."
        x = solution[0]
        y = solution[1]

        if not (x > 0 and y > 0):
            return False, "The solution is not valid."
        else:
            if (a * x * x) + (b * y) == c:
                return True, "Correct solution."
            else:
                return False, "The solution does not match."
    except:
        return False, "Verification error."


def test():
    instance, solution = generate_instance(1, 100)
    print(instance)
    print(solution)
    print(verify_solution(instance, solution))
