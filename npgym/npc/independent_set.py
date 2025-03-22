import random

def generate_instance(num_nodes: int, ind_set_size: int, edge_prob: float = 0.5):
    # Constraints
    assert isinstance(num_nodes, int) and num_nodes >= 2, "num_nodes must be an integer ≥ 2"
    assert isinstance(ind_set_size, int) and 1 <= ind_set_size <= num_nodes, "ind_set_size must be an integer between 1 and num_nodes"
    assert isinstance(edge_prob, float) and 0.0 <= edge_prob <= 1.0, "edge_prob must be a float between 0 and 1"
    
    graph = dict()
    graph["nodes"] = [i for i in range(num_nodes)]
    graph["edges"] = set()
    independent_vertices = set(random.sample(range(num_nodes), ind_set_size))
    non_independent_vertices = set(range(num_nodes)) - independent_vertices

    # independent set内部不能有边
    # 在independent set和其他顶点之间随机添加边
    for v1 in independent_vertices:
        for v2 in non_independent_vertices:
            if random.random() < edge_prob:
                graph["edges"].add((min(v1, v2), max(v1, v2)))

    # 在non-independent vertices之间随机添加边
    for v1 in non_independent_vertices:
        for v2 in non_independent_vertices:
            if v1 < v2 and random.random() < edge_prob:
                graph["edges"].add((v1, v2))
    instance = {"graph": graph, "size": ind_set_size}
    return instance, list(independent_vertices)

def verify_solution(instance, independent_set):
    """验证是否为独立集"""
    graph = instance["graph"]
    num_vertices = len(graph["nodes"])
    if not independent_set:
        return False, "The independent set cannot be empty."
    
    if not isinstance(independent_set, list):
        return False, "Wrong solution format."

    if max(independent_set) >= num_vertices or min(independent_set) < 0:
        return False, "The vertex index exceeds the max number."

    if len(independent_set) < instance["size"]:
        return (
            False,
            f'The size of the independent set is smaller than {instance["size"]}.',
        )
    # 检查独立集中任意两点是否有边相连
    for u in independent_set:
        for v in independent_set:
            if u < v and (u, v) in graph["edges"]:
                return (
                    False,
                    f"There is edge between {u} and {v}.",
                )
    return True, "Correct solution."

def test():
    edges, solution = generate_instance(10, 5)
    print(edges, solution)
    is_valid, msg = verify_solution(edges, solution)
    print("验证独立集:", msg)