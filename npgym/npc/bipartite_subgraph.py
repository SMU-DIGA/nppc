import random


def generate_instance(num_nodes: int, edge_prob: float = 0.3, k_ratio: float = 0.6):
    """
    Generate a random graph instance with guaranteed bipartite subgraph solution.

    Args:
        n: Number of vertices
        density: Edge density (0-1)
        k_ratio: Ratio of k to total possible edges

    Returns:
        BipartiteSubgraphInstance with guaranteed solution
    """
    # First create a guaranteed bipartite subgraph

    graph = dict()
    graph["nodes"] = [i for i in range(num_nodes)]

    set1_size = num_nodes // 2
    node_perm = [i for i in range(num_nodes)]
    random.shuffle(node_perm)
    set1 = set(node_perm[:set1_size])
    set2 = set(node_perm[set1_size:])

    # Generate guaranteed bipartite edges
    bipartite_edges = []
    for u in set1:
        for v in set2:
            if random.random() < edge_prob:
                bipartite_edges.append((u, v))

    # Add some random edges to make the problem harder
    additional_edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            # Skip if edge already exists in bipartite part
            if (i, j) in bipartite_edges or (j, i) in bipartite_edges:
                continue
            if random.random() < edge_prob / 2:  # Lower density for non-bipartite edges
                additional_edges.append((i, j))

    all_edges = bipartite_edges + additional_edges

    graph["edges"] = all_edges

    # Set k to be slightly less than the number of bipartite edges
    k = int(len(bipartite_edges) * k_ratio)

    instance = {"k": k, "graph": graph}

    return instance, (set1, set2)


def verify_solution(instance, partition):
    """
    Verify if given partition creates a valid bipartite subgraph with at least k edges.

    Args:
        instance: BipartiteSubgraphInstance
        partition: Tuple of two sets representing the partition

    Returns:
        bool: True if solution is valid
    """
    set1, set2 = partition

    # Check if partition is valid (sets are disjoint and cover all vertices)
    if not (set1.isdisjoint(set2) and len(set1.union(set2)) == instance.vertices):
        return False, "The partition is not valid."

    # Count edges between the two sets
    bipartite_edges = 0
    for u, v in instance["graph"]["edges"]:
        if (u in set1 and v in set2) or (u in set2 and v in set1):
            bipartite_edges += 1

    if bipartite_edges >= instance.k:
        return True, "Correct solution."
    else:
        return False, "Too less edges."


instance, solution = generate_instance(num_nodes=20)

print(instance)
print(solution)
