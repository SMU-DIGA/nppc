import random
from typing import List, Tuple, Set


def generate_instance(num_nodes: int, k: int, edge_prob: float = 0.3):
    instance = {"k": k, "graph": {}}
    # Initialize empty adjacency matrix
    adj_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    # Generate a guaranteed circuit
    circuit_length = random.randint(k, num_nodes)
    circuit_vertices = random.sample(range(num_nodes), circuit_length)

    # Connect vertices in the circuit
    for i in range(circuit_length):
        v1 = circuit_vertices[i]
        v2 = circuit_vertices[(i + 1) % circuit_length]
        adj_matrix[v1][v2] = 1
        adj_matrix[v2][v1] = 1

    # Add random edges based on density
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if adj_matrix[i][j] == 0 and random.random() < edge_prob:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1

    instance["graph"]["nodes"] = [i for i in range(num_nodes)]
    # instance["graph"]["adj_matrix"] = adj_matrix
    edges = set()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            edges.add((i, j))
    instance["graph"]["edges"] = edges

    return instance, circuit_vertices


def verify_solution(instance, solution: List[int]):
    n = len(instance["graph"]["nodes"])
    # adj_matrix = instance["graph"]["adj_matrix"]
    edges = instance["graph"]["edges"]
    if not solution:
        return False, "The solution is empty."

    # Check if vertices are unique (simple circuit)
    if len(set(solution)) != len(solution):
        return False, "Duplicated nodes in the solution."
    if not (max(solution) < n and min(solution) >= 0):
        return False, "Invalid node index in the solution."

    if len(solution) >= instance["k"]:
        # Check if solution forms a valid circuit
        for i in range(len(solution)):
            v1 = solution[i]
            v2 = solution[(i + 1) % len(solution)]

            # Check if edge exists
            if not ((v1, v2) in edges or (v2, v1) in edges):
                return False, f"No edge between {v1} and {v2}."
        return True, "Correct solution."
    else:
        return False, f"The solution is with nodes less than {instance['k']}."


instance, solution = generate_instance(num_nodes=10, k=3)

print(solution)
solution.append(2)
print(solution)

result = verify_solution(instance, solution)
print(result)
