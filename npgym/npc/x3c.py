import random


def generate_instance(num_elements, num_subsets):
    assert num_elements < num_subsets
    all_elements = 3 * num_elements

    elements = list(range(all_elements))

    cover_size = num_elements

    random.shuffle(elements)

    subsets = []

    for i in range(cover_size):
        subsets.append([elements[3 * i], elements[3 * i + 1], elements[3 * i + 2]])

    for _ in range(num_subsets - cover_size):
        random.shuffle(elements)
        subsets.append([elements[0], elements[1], elements[2]])

    indexed = list(enumerate(subsets))
    random.shuffle(indexed)
    indices, shuffled = zip(*indexed)

    solution = []

    for i in indices:
        if indices[i] < cover_size:
            solution.append(i)
    # print(solution)

    instance = {"elements": list(range(all_elements)), "subsets": shuffled}

    return instance, solution


def verify_solution(instance, solution):
    elements = instance["elements"]
    subsets = instance["subsets"]

    if not (max(solution) < len(subsets) and min(solution) >= 0):
        return False, "The solution is invalid."

    elements_covered = []

    for i in solution:
        elements_covered += subsets[i]
    # print(elements_covered)
    # print(sorted(list(elements_covered)))
    if sorted(list(elements_covered)) == elements:
        return True, "Correct solution."
    else:
        return False, "The solution is not correct."


instance, solution = generate_instance(num_elements=20, num_subsets=30)

print(verify_solution(instance, solution))
