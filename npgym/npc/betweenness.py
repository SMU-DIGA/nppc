import random


def generate_instance(num_element=20, num_triples=30):
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

    return triples, element_perm


def verify_solution(instance, solution):
    for triple in instance:
        if (solution[triple[0]] < solution[triple[1]] < solution[triple[2]]) or (
            solution[triple[0]] > solution[triple[1]] > solution[triple[2]]
        ):
            continue
        else:
            return False, "Some triple is not satisfying."
    return True, "Correct solution."


instance, solution = generate_instance()
random.shuffle(solution)
print(verify_solution(instance, solution))
