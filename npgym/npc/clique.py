import random


def generate_instance(num_nodes: int, clique_size: int, edge_prob: float = 0.5):
    graph = dict()
    graph["nodes"] = [i for i in range(num_nodes)]
    graph["edges"] = set()

    clique_vertices = set(random.sample(range(num_nodes), clique_size))

    # 添加clique内的所有边
    for v1 in clique_vertices:
        for v2 in clique_vertices:
            if v1 < v2:  # 避免重复边和自环
                graph["edges"].add((v1, v2))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_prob:
                graph["edges"].add((i, j))

    return graph, clique_vertices


def verify_solution(graph: dict, clique: set, clique_size: int):
    num_vertices = len(graph["nodes"])

    if not clique:
        return False, "The clique cannot be empty."

    if len(clique) < clique_size:
        return False, f"The clique size is smaller than {clique_size}"

    if max(clique) >= num_vertices or min(clique) < 0:
        return False, "The vertex index exceeds the max number."

    for u in clique:
        for v in clique:
            if u < v and (u, v) not in graph["edges"]:
                return False, f"No edge between {u} and {v}."
    return True, "Correct solution."


# graph, solution = generate_instance(10, 4, 0.6)
# print("edges:", graph)
# print(solution)
#
# # 验证团
# clique = {0, 4, 6, 9}
# is_valid, message = verify_clique(graph, clique, 4)
# print(f"{clique}:", message)
