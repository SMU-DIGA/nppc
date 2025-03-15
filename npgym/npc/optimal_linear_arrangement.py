import random


def generate_instance(num_nodes: int, k: int):
    """
    Generate an instance of the decision version of Optimal Linear Arrangement problem
    that is guaranteed to have at least one solution.

    Args:
        n: Number of vertices
        k: Target cost for the decision version

    Returns:
        Tuple containing:
        - List of edges as tuples (u, v)
        - Target cost k
    """

    # Create a basic path graph to ensure connectedness
    node_perm = [i for i in range(num_nodes)]
    random.shuffle(node_perm)

    node_perm1 = [i for i in range(num_nodes)]
    random.shuffle(node_perm1)
    node_perm2 = [i for i in range(num_nodes)]
    random.shuffle(node_perm2)

    edges = set()

    current_cost = 0
    for u in node_perm1:
        for v in node_perm2:
            if u > v:
                continue
            if (u, v) not in edges:
                current_cost += abs(node_perm[u] - node_perm[v])

                if current_cost < k:
                    edges.add((min(u, v), max(u, v)))

    instance = {
        "k": k,
        "graph": {"nodes": [i for i in range(num_nodes)], "edges": edges},
    }

    return instance, node_perm


def verify_solution(instance, solution):
    """
    Verify if a given arrangement is a valid solution for the OLA instance.

    Args:
        n: Number of vertices
        edges: List of edges as tuples (u, v)
        k: Target cost
        arrangement: Proposed arrangement of vertices (permutation of 0 to n-1)

    Returns:
        bool: True if the arrangement is valid and meets the target cost, False otherwise
    """
    # Check if arrangement is a valid permutation
    num_nodes = len(instance["graph"]["nodes"])
    if sorted(solution) != list(range(num_nodes)):
        return False, "the solution is invalid."

    edges = instance["graph"]["edges"]
    # Calculate the cost of the arrangement
    total_cost = 0
    for u, v in edges:
        # Get positions of vertices in the arrangement
        pos_u = solution[u]
        pos_v = solution[v]
        # Add the cost of this edge
        total_cost += abs(pos_u - pos_v)

    # Check if cost meets the target
    if total_cost <= instance["k"]:
        return True, "Correct solution."
    else:
        return False, "The solution is with larger value."


instance, solution = generate_instance(num_nodes=20, k=300)

print(instance)
print(solution)

solution = list(range(20))
random.shuffle(solution)

print(verify_solution(instance, solution))
