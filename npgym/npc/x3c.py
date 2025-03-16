import random


def generate_instance(num_elements: int, num_subsets: int):
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

    set_indices = [i for i in range(len(shuffled))]
    shuffle_sets = {}
    for idx, i in enumerate(shuffled):
        # print(idx, i)
        shuffle_sets[idx] = i
    # print(shuffle_sets)

    solution = []

    for i in indices:
        if indices[i] < cover_size:
            solution.append(i)
    # print(solution)

    instance = {"universe": list(range(all_elements)), "subsets": shuffle_sets}

    return instance, solution


def verify_solution(instance, solution):
    elements = instance["universe"]
    subsets = instance["subsets"]

    try:
        if not (max(solution) < len(subsets) and min(solution) >= 0):
            return False, "The solution is invalid."

        elements_covered = []

        for i in solution:
            elements_covered += subsets[i]
        if sorted(list(elements_covered)) == elements:
            return True, "Correct solution."
        else:
            return False, "The solution is not correct."

    except:
        return False, "verification error"


instance, solution = generate_instance(num_elements=3, num_subsets=10)

print(instance)
print(solution)

print(verify_solution(instance, solution))
