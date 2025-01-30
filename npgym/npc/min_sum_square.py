import random


def generate_instance(num_elements, k, min_value=10, max_value=30):
    elements = []
    groups = []
    for i in range(num_elements):
        elements.append(random.randint(min_value, max_value))
        groups.append(random.randint(1, k))

    group_value = [0] * k
    for ele_idx, element in enumerate(elements):
        group_value[groups[ele_idx] - 1] += element

    J = sum([v * v for v in group_value]) + random.randint(0, max_value)

    instance = {"elements": elements, "k": k, "J": J}

    return instance, groups


def verify_solution(instance, solution):
    elements = instance["elements"]
    k = instance["k"]
    J = instance["J"]

    if len(elements) != len(solution):
        return False, "The solution is not with the same elements"

    if len(set(solution)) != k:
        return False, "The subset number is not correct"

    group_value = {}

    for ele_idx, element in enumerate(elements):
        if solution[ele_idx] in group_value:
            group_value[solution[ele_idx]] += element
        else:
            group_value[solution[ele_idx]] = element

    quad_sum = 0
    for group_key in group_value:
        quad_sum += (group_value[group_key]) ** 2

    if quad_sum <= J:
        return True, "Correct solution."
    else:
        return False, "The sum exceeds J."


instance, solution = generate_instance(num_elements=50, k=10)

num_elements = 50
k = 10
groups = []
for i in range(num_elements):
    groups.append(random.randint(1, k))
print(verify_solution(instance, groups))
