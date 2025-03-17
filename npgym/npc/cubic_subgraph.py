import random


def generate_instance(num_nodes: int, k: int, edge_prob: float = 0.3):
    """
    Generate a graph instance that is guaranteed to have at least one cubic subgraph
    (a subgraph where every vertex has degree exactly 3) of size k.

    Args:
        n: Number of vertices in the graph
        k: Size of the cubic subgraph to guarantee
        density: Edge density (0 to 1) for additional edges beyond the guaranteed solution

    Returns:
        tuple containing:
        - List of nodes (vertices)
        - List of edges (pairs of vertices)
    """

    # Ensure k is valid (k must be at least 4 for a cubic graph to exist)
    if k < 4:
        raise ValueError("k must be at least 4 for a cubic subgraph")
    if k > num_nodes:
        raise ValueError("k cannot be larger than n")
    if k % 2 == 1:
        raise ValueError("k must be even for a cubic graph to exist")

    instance = {"k": k, "graph": {}}
    # Create list of nodes
    nodes = list(range(num_nodes))
    edges = set()  # Using set to avoid duplicate edges

    # Step 1: Create a guaranteed cubic subgraph of size k
    node_perm = list(range(num_nodes))
    random.shuffle(node_perm)
    cubic_vertices = set(node_perm[:k])

    # For each vertex in the cubic subgraph, connect it to exactly 3 other vertices
    # We'll use a systematic approach to ensure every vertex gets exactly 3 edges
    for i in cubic_vertices:
        existing_edges = sum(1 for edge in edges if i in edge)

        while existing_edges < 3:
            # Find available vertices to connect to
            available = [
                j
                for j in cubic_vertices
                if j != i
                and sum(1 for edge in edges if j in edge) < 3
                and (i, j) not in edges
                and (j, i) not in edges
            ]

            if not available:
                # If we can't complete the cubic subgraph, start over
                edges.clear()
                i = cubic_vertices[0]
                continue

            j = random.choice(available)
            edges.add(tuple(sorted([i, j])))
            existing_edges += 1

    # Step 2: Add random edges based on density
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if (i, i) not in edges and random.random() < edge_prob:
                edges.add((i, j))

    instance["graph"]["nodes"] = nodes
    instance["graph"]["edges"] = edges
    return instance, cubic_vertices


def verify_solution(instance, solution: set[int]):
    """
    Verify if a given set of vertices forms a valid cubic subgraph
    (where every vertex in the solution has degree exactly 3 within the subgraph).

    Args:
        nodes: List of all vertices in the graph
        edges: List of edges (pairs of vertices)
        solution: Set of vertex indices forming the proposed cubic subgraph

    Returns:
        bool: True if the solution forms a valid cubic subgraph, False otherwise
    """

    edges = instance["graph"]["edges"]
    if not solution:
        return False, "Solution is empty."
    if len(solution) < instance["k"]:
        return False, f'The solution is with less nodes than {instance["k"]}'
    # Step 1: Get all edges that are part of the solution subgraph
    solution_edges = [
        edge for edge in edges if edge[0] in solution and edge[1] in solution
    ]

    # Step 2: Verify that each vertex in the solution has exactly 3 edges
    for vertex in solution:
        # Count edges connected to this vertex within the solution
        degree = sum(1 for edge in solution_edges if vertex in edge)
        if degree != 3:
            return False, "Not all nodes with degree 3"

    # Step 3: Verify that the subgraph is connected

    # Use DFS to check connectivity
    visited = set()
    start_vertex = next(iter(solution))

    def dfs(v):
        visited.add(v)
        for edge in solution_edges:
            if v == edge[0] and edge[1] in solution:
                if edge[1] not in visited:
                    dfs(edge[1])
            elif v == edge[1] and edge[0] in solution:
                if edge[0] not in visited:
                    dfs(edge[0])

    dfs(start_vertex)

    print(visited)

    # All vertices in solution should be reachable
    if visited == solution:
        return True, "Correct solution."
    else:
        return False, "The subgraph is not connected."


instance, solution = generate_instance(num_nodes=10, k=4)
print(solution)

# solution.add(4)
print(verify_solution(instance, solution))
