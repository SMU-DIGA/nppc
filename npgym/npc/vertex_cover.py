import random


def generate_instance(num_nodes: int, cover_size: int, edge_prob: float = 0.5):
    graph = dict()
    graph["nodes"] = [i for i in range(num_nodes)]
    graph["edges"] = set()

    cover_vertices = set(random.sample(range(num_nodes), cover_size))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if i in cover_vertices or j in cover_vertices:
                if random.random() < edge_prob:  # 70%概率添加边
                    graph["edges"].add((i, j))

    instance = {"cover_size": cover_size, "graph": graph}
    return instance, list(cover_vertices)


def verify_solution(instance, cover: set):
    cover_size = instance["cover_size"]
    graph = instance["graph"]
    num_vertices = len(graph["nodes"])

    if not cover:
        return False, "The clique cannot be empty."

    if max(cover) >= num_vertices or min(cover) < 0:
        return False, "The vertex index exceeds the max number."

    if len(cover) > cover_size:
        return False, f"The cover size is larger than {cover_size}"

    for u, v in graph["edges"]:
        if u not in cover and v not in cover:
            return False, f"Edge ({u}, {v}) is not covered."

    return True, "Correct solution."


# num_nodes = 5
# cover_size = 3
# graph, solution = generate_instance(num_nodes, cover_size)
# print("图的边:", graph)
# print(solution)
#
# # 验证顶点覆盖
# # cover = {2, 3, 4}
# cover = solution
# is_valid, message = verify_solution(graph, cover, cover_size=cover_size)
# print(f"验证顶点覆盖{cover}:", message)
