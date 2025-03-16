import random


def generate_instance(num_nodes: int, k: int):
    """
    Generate a graph instance that contains at least one valid k-closure solution

    Returns:
        Tuple containing:
        - Adjacency matrix of the graph
        - List of sets, where each set contains vertices in a valid component
    """

    instance = {"k": k, "graph": {}}
    # Initialize empty adjacency matrix
    adj_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    # Create a guaranteed solution with at least one component
    min_component_size = k + 1  # Each vertex needs k neighbors
    component_size = random.randint(
        min_component_size, min(num_nodes, min_component_size + 3)
    )

    # Create a valid component where each vertex has at least k neighbors
    node_perm = [i for i in range(num_nodes)]
    random.shuffle(node_perm)
    component_vertices = set(node_perm[:component_size])
    for i in component_vertices:
        # Connect to at least k random other vertices in the component
        others = list(component_vertices - {i})
        num_connections = random.randint(k, len(others))
        connections = random.sample(others, num_connections)

        for j in connections:
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1

    # Add some random edges to remaining vertices
    remaining_vertices = set(range(component_size, num_nodes))
    if remaining_vertices:
        for i in remaining_vertices:
            # Randomly connect to some vertices with less than k edges
            possible_connections = list(range(num_nodes))
            possible_connections.remove(i)
            num_connections = random.randint(0, min(k - 1, len(possible_connections)))
            connections = random.sample(possible_connections, num_connections)

            for j in connections:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1

    # instance["graph"]["adj_matrix"] = adj_matrix
    instance["graph"]["nodes"] = [i for i in range(num_nodes)]

    edges = set()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            edges.add((i, j))
    instance["graph"]["edges"] = edges
    return instance, component_vertices


def verify_solution(instance, solution):
    edges = instance["graph"]["edges"]

    # Check if components are disjoint
    seen_vertices = set()
    if any(v in seen_vertices for v in solution):
        return False
    seen_vertices.update(solution)

    # Check if each vertex in each component has at least k neighbors within its component

    for vertex in solution:
        neighbors = set()
        for other in solution:
            if vertex != other and (
                    (vertex, other) in edges or (other, vertex) in edges
            ):
                neighbors.add(other)
        if len(neighbors) < instance["k"]:
            return False, "Some nodes with less neighbors."

    return True, "Correct solution."


instance, solution = generate_instance(num_nodes=20, k=5)
print(instance)
print(solution)
#
# solution.add(2)
print(verify_solution(instance, solution))
