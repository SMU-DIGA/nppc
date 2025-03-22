import random
from typing import List


def generate_instance(num_nodes: int, directed: bool, edge_probability: float = 0.3):
    """Generate a graph instance containing a Hamiltonian cycle

    Args:
        n: Number of vertices
        directed: If True, generate directed graph; if False, undirected
        edge_probability: Probability of adding extra edges

    Returns:
        Adjacency matrix of the graph
    """

    instance = {"graph": {}}
    nodes = list(range(num_nodes))
    random.shuffle(nodes)

    edges = set()

    # Add edges forming a Hamiltonian cycle
    for i in range(num_nodes):
        v1, v2 = nodes[i], nodes[(i + 1) % num_nodes]
        edges.add((v1, v2))
        if not directed:
            edges.add((v2, v1))

    # Add random edges
    for i in range(num_nodes):
        for j in range(num_nodes if directed else i + 1):
            if i != j and (not (i, j) in edges) and random.random() < edge_probability:
                edges.add((i, j))
                if not directed:
                    edges.add((j, i))
    instance["graph"]["nodes"] = list(range(num_nodes))
    instance["graph"]["edges"] = edges
    return instance, nodes + nodes[:1]


def verify_solution(instance, cycle: List[int]):
    """Verify if the given cycle is a valid Hamiltonian cycle

    Args:
        graph: Adjacency matrix
        cycle: List of vertices representing the cycle
        directed: If True, treat graph as directed

    Returns:
        Tuple of (is_valid, error_message)
    """
    n = len(instance["graph"]["nodes"])
    edges = instance["graph"]["edges"]

    try:

        # Basic checks
        if len(cycle) != n + 1:
            return False, f"Path length should be {n + 1}."
        if cycle[0] != cycle[-1]:
            return False, "Path does not return to start."
        if len(set(cycle[:-1])) != n:
            return False, "Not all vertices visited exactly once."
        if not all(0 <= node < n for node in cycle):
            return False, "Invalid vertex in path."

        # Check if edges exist
        for i in range(len(cycle) - 1):
            v1, v2 = cycle[i], cycle[i + 1]
            if (v1, v2) not in edges:
                return False, f"No edge between vertices {v1} and {v2}."

        return True, "Correct solution."

    except:
        return False, "Verification error."


def test():
    # Test undirected graph
    n = 5
    undirected, solution = generate_instance(n, directed=False)
    # print("Undirected graph:")
    # # solution = [0, 2, 1, 4, 3, 0]
    print(undirected)
    print(solution)
    valid, msg = verify_solution(undirected, solution)
    print(f"Undirected graph validation result: {msg}\n")
    #
    # # Test directed graph
    directed, solution = generate_instance(n, directed=True)
    print(directed)
    print(solution)
    valid, msg = verify_solution(directed, solution)
    print(f"Directed graph validation result: {msg}")
