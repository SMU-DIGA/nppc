import random


def generate_instance(num_nodes: int, bandwidth: int, edge_density=0.3):
    """
    Generate a graph instance for the Bandwidth decision problem with guaranteed solution.

    Args:
        num_vertices (int): Number of vertices in the graph
        target_bandwidth (int): Target bandwidth threshold
        edge_density (float): Desired density of edges (0.0 to 1.0)
        seed (int): Random seed for reproducibility

    Returns:
        list: Adjacency list representation of the graph where graph[i] contains
             vertices adjacent to vertex i
    """

    if bandwidth >= num_nodes:
        raise ValueError("Target bandwidth must be less than number of vertices")
    if edge_density < 0 or edge_density > 1:
        raise ValueError("Edge density must be between 0 and 1")

    # Create empty adjacency list
    instance = {"bandwidth": bandwidth, "graph": {}}

    # First, create a layout that achieves the target bandwidth
    # This will be our guaranteed solution
    vertex_positions = list(range(num_nodes))
    random.shuffle(vertex_positions)

    # Add edges ensuring bandwidth constraint is met
    possible_edges = []
    # First add some mandatory edges to ensure connectivity
    selected_edges = []
    for i in range(num_nodes):
        add = False
        for j in range(i + 1, num_nodes):
            if abs(vertex_positions[i] - vertex_positions[j]) <= bandwidth:
                possible_edges.append((i, j))
                if not add:
                    add = True
                    selected_edges.append((i, j))

    # Calculate number of edges to add based on density
    max_edges = num_nodes * (num_nodes - 1) // 2
    target_edges = int(edge_density * max_edges)
    target_edges = min(target_edges, len(possible_edges))

    # Add remaining random edges that respect bandwidth
    remaining_edges = [e for e in possible_edges if e not in selected_edges]
    additional_edges = random.sample(
        remaining_edges,
        max(min(target_edges - len(selected_edges), len(remaining_edges)), 0),
    )
    selected_edges.extend(additional_edges)

    instance["graph"]["nodes"] = list(range(num_nodes))

    instance["graph"]["edges"] = selected_edges

    return instance, vertex_positions


def verify_solution(instance, layout):
    """
    Verify if a graph layout achieves the target bandwidth.
    #
    # Args:
    #     graph (list): Adjacency list representation of the graph
    #     target_bandwidth (int): Maximum allowed bandwidth
    #     layout (list): Permutation of vertices representing their positions

    Returns:
        tuple: (is_valid, error_message)
            - is_valid: Boolean indicating if layout is valid
            - error_message: String explaining why layout is invalid (if applicable)
            # :param instance:
    """

    graph = instance["graph"]
    bandwidth = instance["bandwidth"]
    num_vertices = len(graph["nodes"])

    # Check if layout is a valid permutation
    if len(layout) != num_vertices:
        return False, "Layout length doesn't match number of vertices"
    if sorted(layout) != list(range(num_vertices)):
        return False, "Layout must be a permutation of vertices"

    # Check bandwidth constraint for each edge
    for v1, v2 in graph["edges"]:
        if abs(layout[v1] - layout[v2]) > bandwidth:
            return (
                False,
                f"Edge ({v1}, {v2}) exceeds bandwidth: |{layout[v1]} - {layout[v2]}| > {bandwidth}",
            )

    return True, "Layout is valid"


for i in range(1):
    instance, solution = generate_instance(num_nodes=5, bandwidth=2)
    print(instance)
    print(solution)
    print(verify_solution(instance, solution))
