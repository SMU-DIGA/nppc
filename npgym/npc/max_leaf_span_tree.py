import random


def generate_instance(num_nodes: int, target_leaves: int):
    """
    Generate a graph instance for Maximum Leaf Spanning Tree decision problem.
    The instance will guarantee existence of a spanning tree with at least target_leaves leaves.
    """
    num_vertices = num_nodes
    if target_leaves > num_vertices - 1:
        raise ValueError("Target leaves cannot exceed n-1")
    if target_leaves < 2 < num_vertices:
        raise ValueError("Target leaves must be at least 2 for n > 2")

    instance = {"target_leaves": target_leaves, "graph": {}}
    # Create nodes list
    nodes = list(range(num_vertices))
    edges = set()  # Use set to avoid duplicate edges

    # Initialize parent array for our solution
    solution = [-1] * num_vertices

    # Determine number of internal nodes needed
    num_internal = num_vertices - target_leaves
    if num_internal < 1:
        num_internal = 1  # Need at least one internal node

    # Create path of internal nodes
    for i in range(1, num_internal):
        parent = random.randint(0, i - 1)
        solution[i] = parent
        edges.add(tuple(sorted([i, parent])))  # Add undirected edge

    # Add leaf nodes connected to random internal nodes
    for i in range(num_internal, num_vertices):
        parent = random.randint(0, num_internal - 1)
        solution[i] = parent
        edges.add(tuple(sorted([i, parent])))  # Add undirected edge

    # Add some random extra edges to make the graph more interesting
    # but not too many to keep the problem challenging
    extra_edges = random.randint(0, num_vertices)
    for _ in range(extra_edges):
        v1 = random.randint(0, num_vertices - 1)
        v2 = random.randint(0, num_vertices - 1)
        if v1 != v2:
            edges.add(tuple(sorted([v1, v2])))

    # Convert edges set to sorted list for consistency
    edges = sorted(list(edges))

    instance["graph"]["nodes"] = nodes
    instance["graph"]["edges"] = edges

    return instance, solution


def verify_solution(instance, solution):
    """
    Verify if a given tree solution has at least target_leaves leaves and is a valid spanning tree.

    """

    nodes = instance["graph"]["nodes"]
    edges = instance["graph"]["edges"]
    target_leaves = instance["target_leaves"]
    n = len(nodes)

    # Check solution length
    if len(solution) != n:
        return False, "Solution length doesn't match number of vertices"

    # Convert edges to set of tuples for easier lookup
    edge_set = set(tuple(sorted(edge)) for edge in edges)

    # Check if solution represents a tree
    visited = [False] * n
    parent_count = [0] * n

    # Count parents and check for invalid edges
    for v in range(n):
        parent = solution[v]
        if parent != -1:
            # Check if edge exists in graph
            if tuple(sorted([v, parent])) not in edge_set:
                return False, f"Edge ({v}, {parent}) in solution not present in graph"
            parent_count[parent] += 1

    # Do BFS from root to check connectivity
    root = solution.index(-1)
    if solution.count(-1) != 1:
        return False, "Solution must have exactly one root"

    queue = [root]
    visited[root] = True

    while queue:
        v = queue.pop(0)
        for u in range(n):
            if solution[u] == v and not visited[u]:
                visited[u] = True
                queue.append(u)

    # Check if tree spans all vertices
    if not all(visited):
        return False, "Tree doesn't span all vertices"

    # Count leaves (vertices with no children)
    leaf_count = sum(1 for count in parent_count if count == 0)

    # Check leaf count
    if leaf_count < target_leaves:
        return False, f"Tree has {leaf_count} leaves, needs at least {target_leaves}"

    return True, "Solution is valid"


for i in range(10):
    instance, solution = generate_instance(num_nodes=10, target_leaves=3)
    # print(instance)
    print(solution)
    print(verify_solution(instance, solution))
