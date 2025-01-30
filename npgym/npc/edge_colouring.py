import random


def generate_instance(num_nodes: int, edge_prob: float = 0.7):
    """
    Generate an edge coloring instance that is guaranteed to have at least one valid solution.

    Args:
        n: Number of vertices in the graph
        density: Edge density (0 to 1), controls how many edges to add

    Returns:
        tuple containing:
        - Adjacency matrix representing the graph
        - Minimum number of colors needed (upper bound)
        :param num_nodes:
    """

    instance = {"graph": {}}
    # Initialize empty adjacency matrix
    adj_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    # Add edges based on density
    max_degree = 0
    edges = set()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_prob:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
                edges.add((i, j))
                edges.add((j, i))

    instance["graph"]["nodes"] = [i for i in range(num_nodes)]
    # instance["graph"]["adj_matrix"] = adj_matrix
    instance["graph"]["edges"] = edges

    # Calculate maximum degree (which gives us an upper bound on chromatic index)
    for i in range(num_nodes):
        degree = sum(adj_matrix[i])
        max_degree = max(max_degree, degree)

    # By Vizing's theorem, chromatic index is either max_degree or max_degree + 1
    # We'll use max_degree + 1 as it's guaranteed to have a solution
    chromatic_index = max_degree + 1

    instance["k"] = chromatic_index
    return instance


def verify_solution(instance, edge_colors: dict[tuple[int, int], int]):
    """
    Verify if a given edge coloring solution is valid.

    Args:
        adj_matrix: Adjacency matrix representing the graph
        edge_colors: Dictionary mapping edge (vertex pairs) to colors (integers)

    Returns:
        bool: True if the coloring is valid, False otherwise
    """
    # n = len(instance["graph"]["nodes"])
    # adj_matrix = instance["graph"]["adj_matrix"]
    # Get all edges from adjacency matrix
    edges = instance["graph"]["edges"]

    # Check if all edges are colored
    if set(edge_colors.keys()) != edges:
        return False

    # Check if adjacent edges have different colors
    for (u1, v1), color1 in edge_colors.items():
        for (u2, v2), color2 in edge_colors.items():
            # Skip comparing edge to itself
            if (u1, v1) == (u2, v2):
                continue

            # Check if edges share a vertex
            if u1 in (u2, v2) or v1 in (u2, v2):
                # Adjacent edges must have different colors
                if color1 == color2:
                    return False

    return True
