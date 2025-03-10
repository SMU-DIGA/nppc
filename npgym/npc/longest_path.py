import random


def generate_instance(num_nodes, num_length, edge_prob=0.3):
    """
    Generate a Longest Path decision problem instance that guarantees at least one solution exists.

    Args:
        min_nodes: Minimum number of nodes in the graph
        max_nodes: Maximum number of nodes in the graph

    Returns:
        Tuple containing:
        - graph: Dictionary representing adjacency list of the undirected graph
        - s: Source node
        - t: Target node
        - k: Required minimum path length
    """
    # Generate random number of nodes
    # n = random.randint(min_nodes, max_nodes)

    if num_length > num_nodes - 1:
        raise "we only focus on simple path, so let num_length < num_nodes"
    # Create a base path to ensure at least one solution exists
    base_path = list(range(num_nodes))
    random.shuffle(base_path)

    edges = set()

    # Initialize graph as adjacency list
    # graph = defaultdict(list)

    # Add edges of the base path
    for i in range(num_length):
        u, v = base_path[i], base_path[i + 1]
        edges.add((min(u, v), max(u, v)))

    # Add some random edges to make the graph more complex

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if (i, j) in edges:
                continue
            else:
                if random.random() < edge_prob:
                    edges.add((i, j))

    # Set k to be less than or equal to the length of the base path

    instance = {
        "k": num_length,
        "s": base_path[0],
        "t": base_path[num_length],
        "graph": {"nodes": list(range(num_nodes)), "edges": edges},
    }

    return instance, base_path[: num_length + 1]


def verify_solution(instance, path):
    """
    Verify if the given path is a valid solution for the Longest Path decision problem.

    Args:
        graph: Dictionary representing adjacency list of the undirected graph
        s: Source node
        t: Target node
        k: Required minimum path length
        path: List of nodes representing the proposed solution path

    Returns:
        bool: True if the path is valid and meets all requirements, False otherwise
    """

    s = instance["s"]
    t = instance["t"]
    k = instance["k"]
    edges = instance["graph"]["edges"]
    # Check if path starts at s and ends at t
    if not path or path[0] != s or path[-1] != t:
        return False, "The path is invalid of the start or end nodes."

    # Check if path length is at least k edges
    if len(path) - 1 < k:
        return False, "The path is too short"

    # Check if path is simple (no repeated nodes)
    if len(path) != len(set(path)):
        return False, "The path is not simple"

    # Check if all edges in the path exist in the graph
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]

        if (current, next_node) not in edges and (next_node, current) not in edges:
            return False, "The path is not connected"

    return True, "Correct solution."


# Example usage:

instance, solution = generate_instance(num_nodes=20, num_length=18)

print(verify_solution(instance, solution))
