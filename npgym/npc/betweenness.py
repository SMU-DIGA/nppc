import random


def generate_instance(num_element: int, num_triples: int):
    element_perm = list(range(num_element))
    random.shuffle(element_perm)

    triples = []

    element_perm1 = list(range(num_element))
    for i in range(num_triples):
        random.shuffle(element_perm1)

        def get_middle_index(a, b, c):
            if (b >= a >= c) or (c >= a >= b):
                return 0
            elif (a >= b >= c) or (c >= b >= a):
                return 1
            else:
                return 2

        ele_indices = element_perm1[:3]
        values = [
            element_perm[ele_indices[0]],
            element_perm[ele_indices[1]],
            element_perm[ele_indices[2]],
        ]
        mid_idx = get_middle_index(*values)

        mid_element = ele_indices[mid_idx]
        ele_indices.remove(ele_indices[mid_idx])

        triples.append((ele_indices[0], mid_element, ele_indices[1]))
    instance = {"elements": list(range(num_element)), "triples": triples}

    return instance, element_perm


def verify_solution(instance, solution):
    n = len(instance["elements"])
    triples = instance["triples"]
    solution_set = set(solution)
    try:
        if len(solution_set) < n or max(solution) >= n or min(solution) < 0:
            return False, "Not one-to-one function."
        if len(solution) != n:
            return False, "Wrong size."
        for triple in triples:
            if (solution[triple[0]] < solution[triple[1]] < solution[triple[2]]) or (
                solution[triple[0]] > solution[triple[1]] > solution[triple[2]]
            ):
                continue
            else:
                return False, "Some triple is not satisfying."
        return True, "Correct solution."
    except:
        return False, "Value error"


num_element = 4
num_triples = 3

for i in range(1):
    print("=" * 20)
    instance, solution = generate_instance(num_element, num_triples)
    print(instance)
    print(solution)
    print(verify_solution(instance, solution))
    random.shuffle(solution)
    solution = [0, 0, 1, 2]
    print(verify_solution(instance, solution))
    solution = [0, 0, 1, 2]
    print(verify_solution(instance, solution))
    solution = [0, 1, 2, 4]
    print(verify_solution(instance, solution))
    solution = [0, 1, 2]
    print(verify_solution(instance, solution))
