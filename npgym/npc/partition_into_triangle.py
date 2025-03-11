import random


def generate_instance(n, edge_prob=0.3):
    all_nodes = 3 * n

    nodes = list(range(all_nodes))

    random.shuffle(nodes)

    edges = []

    solution = []

    for i in range(n):
        tri_list = [nodes[3 * i], nodes[3 * i + 1], nodes[3 * i + 2]]
        solution.append(tri_list)

        for i in range(3):
            for j in range(i + 1, 3):
                edges.append(
                    (min(tri_list[i], tri_list[j]), max(tri_list[i], tri_list[j]))
                )

    for i in range(all_nodes):
        for j in range(i + 1, all_nodes):
            if (min(nodes[i], nodes[j]), max(nodes[i], nodes[j])) in edges:
                continue
            else:
                if random.random() < edge_prob:
                    edges.append((min(nodes[i], nodes[j]), max(nodes[i], nodes[j])))

    instance = {"nodes": list(range(all_nodes)), "edges": edges}

    return instance, solution


def verify_solution(instance, solution):
    nodes = instance["nodes"]
    edges = instance["edges"]
    n = len(instance["nodes"]) // 3

    if len(solution) != n:
        return False, "The solution is invalid"

    all_nodes = []

    for sol in solution:
        all_nodes += sol

    if not (sorted(all_nodes) == nodes):
        return False, "The solution is invalid"

    for sol in solution:
        for i in range(3):
            for j in range(i + 1, 3):
                if not (min(sol[i], sol[j]), max(sol[i], sol[j])) in edges:
                    return False, "The solution is not correct."
    else:
        return True, "Correct solution."


# instance, solution = generate_instance(n=10)
# print(solution)
# print(verify_solution(instance, solution))
