import random


def generate_instance(num_elements: int, k: int, min_value=1, max_value=100):
    elements = []
    groups = []
    for i in range(num_elements):
        elements.append(random.randint(min_value, max_value))
        groups.append(random.randint(1, k))

    group_value = [0] * k
    for ele_idx, element in enumerate(elements):
        group_value[groups[ele_idx] - 1] += element
    # print(group_value)

    J = sum([v * v for v in group_value]) + random.randint(0, max_value)
    group_indices = [i + 1 for i in range(k)]
    # print(group_indices)

    instance = {"elements": elements, "set_indices": group_indices, "J": J}

    return instance, groups


def verify_solution(instance, solution):
    elements = instance["elements"]
    k = len(instance["set_indices"])
    J = instance["J"]

    if len(elements) != len(solution):
        return False, "The solution is not with the same elements"

    if len(set(solution)) > k:
        return False, "The subset number is not valid"

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


num_elements = 30
k = 5
instance, solution = generate_instance(num_elements=num_elements, k=k)
print(instance)
print(solution)
print(verify_solution(instance, solution))


groups = []
for i in range(num_elements):
    groups.append(random.randint(1, k))
print(groups)
print(verify_solution(instance, groups))
