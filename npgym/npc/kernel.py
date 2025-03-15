import random


def generate_instance(n, edge_prob=0.3):
    nodes = list(range(n))
    edges = set()

    node_perm = list(range(n))
    random.shuffle(node_perm)
    kernel = node_perm[: n // 2]

    for k in kernel:
        for j in node_perm[n // 2:]:
            edges.add((k, j))

    for i in nodes:
        for j in nodes:
            if i in kernel and j in kernel:
                continue
            if random.random() < edge_prob and (not ((i, j) in edges)):
                edges.add((i, j))

    instance = {"graph": {"nodes": nodes, "edges": edges}}

    return instance, kernel


def verify_solution(instance, solution):
    nodes = instance["graph"]["nodes"]
    edges = instance["graph"]["edges"]
    if not (max(solution) < len(nodes) and min(solution) >= 0):
        return False, "The solution is not valid."

    nodes_dominated = []

    for s in solution:
        for j in nodes:
            if s == j:
                continue
            if j in solution:
                if (s, j) in edges:
                    return False, "The solution is not correct."
            else:
                if (s, j) in edges:
                    nodes_dominated.append(j)
    if set(sorted(nodes_dominated)) == set(sorted(set(nodes) - set(solution))):
        return True, "Correct solution."
    else:
        return False, "The solution is not correct."


instance, solution = generate_instance(n=10)

print(verify_solution(instance, solution))
