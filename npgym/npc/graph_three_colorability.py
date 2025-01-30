import random


def generate_instance(num_nodes: int, edge_prob: float = 0.5):
    graph = dict()
    graph["nodes"] = [i for i in range(num_nodes)]
    graph["edges"] = set()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_prob:
                graph["edges"].add((i, j))
    colors = {i: random.randint(0, 2) for i in range(num_nodes)}
    # 随机添加边，保证相邻顶点颜色不同
    for v1 in range(num_nodes):
        for v2 in range(v1 + 1, num_nodes):
            if colors[v1] != colors[v2] and random.random() < edge_prob:  # 70%概率添加边
                graph["edges"].add((v1, v2))

    return graph, colors


def verify_solution(graph, coloring):
    """
    验证3着色方案是否合法

    参数:
    edges: 边的列表，每条边表示为(v1, v2)
    coloring: 列表，coloring[i]表示顶点i的颜色(0,1,2)

    返回:
    valid: 布尔值，表示着色方案是否合法
    error_msg: 如果不合法，返回错误信息
    """
    edges = graph["edges"]

    num_vertices = len(graph["nodes"])

    if not coloring:
        return False, "The coloring cannot be empty."

    if len(coloring) != num_vertices:
        return False, "The coloring is not matching the nodes."

    if not all(c in [0, 1, 2] for c in coloring):
        return False, "Colors more than three."

    # 检查相邻顶点是否有相同颜色
    for v1, v2 in edges:
        if coloring[v1] == coloring[v2]:
            return (
                False,
                f"Neighboring nodes {v1} and {v2} have the same color {coloring[v1]}",
            )

    return True, "Correct solution."


n_vertices = 5
edges, solution = generate_instance(n_vertices)
print(f"生成的图的边: {edges}")

# 测试一个合法的着色方案
valid_coloring = [0, 1, 2, 0, 1]
is_valid, msg = verify_solution(edges, valid_coloring)
print(f"\n测试合法方案:")
print(f"着色方案: {valid_coloring}")
print(f"验证结果: {msg}")

# 测试一个非法的着色方案
invalid_coloring = [0, 0, 1, 2, 1]
is_valid, msg = verify_solution(edges, invalid_coloring)
print(f"\n测试非法方案:")
print(f"着色方案: {invalid_coloring}")
print(f"验证结果: {msg}")
