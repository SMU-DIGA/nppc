import random


def generate_instance(num_nodes: int, k: int, edge_prob: float = 0.3):
    """
    Generate a graph instance that is guaranteed to have at least one dominating set of size k.

    Args:
        n: Number of vertices in the graph
        k: Size of the dominating set to guarantee
        density: Edge density (0 to 1) for additional edges beyond the guaranteed solution

    Returns:
        tuple containing:
        - List of nodes (vertices)
        - List of edges (pairs of vertices)
    """

    instance = {"K": k, "Graph": {}}
    # Ensure k is valid for the graph size
    if k > num_nodes:
        raise ValueError("k cannot be larger than n")

    # Create list of nodes
    nodes = list(range(num_nodes))
    edges = set()  # Using set to avoid duplicate edges

    # Step 1: Select k vertices that will form a guaranteed dominating set
    # dominating_number = random.randint(1, k)
    dominating_number = k
    dominating_vertices = random.sample(nodes, dominating_number)

    # Step 2: Ensure every non-dominating vertex is connected to at least one dominating vertex
    non_dominating = list(set(nodes) - set(dominating_vertices))
    for v in non_dominating:
        # Connect to at least one random dominating vertex
        dom_vertex = random.choice(dominating_vertices)
        edges.add(
            tuple(sorted([v, dom_vertex]))
        )  # Sort to ensure consistent edge representation

    # Step 3: Add random edges based on density
    possible_edges = [(i, j) for i in nodes for j in nodes if i < j]
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            # Skip if edge already exists
            if (i, j) in edges:
                continue

            # Add edge with probability based on density
            if random.random() < edge_prob:
                edges.add((i, j))

    instance["Graph"]["nodes"] = nodes
    instance["Graph"]["edges"] = edges

    return instance, dominating_vertices


def verify_solution(instance, solution: set[int]):
    """
    Verify if a given set of vertices forms a valid dominating set.

    Args:
        nodes: List of all vertices in the graph
        edges: List of edges (pairs of vertices)
        solution: Set of vertex indices forming the proposed dominating set

    Returns:
        bool: True if the solution is a valid dominating set, False otherwise
    """
    # Create a set of all nodes
    if not solution:
        return False, "The solution is empty."
    if len(solution) > instance["K"]:
        return False, "Too many nodes."

    nodes = instance["Graph"]["nodes"]
    edges = instance["Graph"]["edges"]
    all_nodes = set(nodes)

    # Get set of vertices dominated by the solution
    dominated = set(solution.copy())  # vertices in solution dominate themselves

    # Add vertices that are adjacent to any vertex in solution
    for v in solution:
        for edge in edges:
            if v in edge:
                # Add the other endpoint of the edge
                dominated.add(edge[0] if edge[1] == v else edge[1])

    # Solution is valid if all vertices are dominated
    if dominated == all_nodes:
        return True, "Correct solution."
    else:
        return False, "Not all nodes are dominated"


instance, solution = generate_instance(num_nodes=10, k=5)

print(instance)
print(solution)

print(verify_solution(instance, solution))
