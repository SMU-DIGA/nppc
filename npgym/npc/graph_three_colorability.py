import random
from itertools import product

import numpy as np


def generate_instance(num_nodes: int, num_edges: int):
    """生成 3-COL 实例和有效解"""

    # 生成节点
    nodes = list(range(num_nodes))

    # 生成有效解：随机分配颜色（0, 1, 2）
    chunk_size = num_nodes // 3
    remainder = num_nodes % 3

    # 初始划分
    first_chunk = chunk_size + (1 if remainder > 0 else 0)
    second_chunk = chunk_size + (1 if remainder > 1 else 0)
    third_chunk = chunk_size

    solution = [0] * first_chunk + [1] * second_chunk + [2] * third_chunk
    first_chunk_nodes = list(range(first_chunk))
    second_chunk_nodes = list(range(first_chunk, first_chunk + second_chunk))
    third_chunk_nodes = list(
        range(first_chunk + second_chunk, first_chunk + second_chunk + third_chunk)
    )
    first_edge_set_number = first_chunk * second_chunk
    second_edge_set_number = second_chunk * third_chunk
    third_edge_set_number = third_chunk * first_chunk

    assert num_edges <= (
        first_edge_set_number + second_edge_set_number + third_edge_set_number
    )
    edge_number_for_sets = [0] * 3
    mask = [False] * 3
    remaining_edges = [
        first_edge_set_number,
        second_edge_set_number,
        third_edge_set_number,
    ]

    def softmax(x, mask=None):
        # 为了数值稳定性，减去最大值
        x_np = np.array(x, dtype=np.float64)

        if mask is not None:
            # 将被屏蔽的位置设为非常小的值(负无穷)，这样exp后接近0
            x_np = np.where(mask, -np.inf, x_np)
        valid_max = np.max(x_np[x_np != -np.inf])
        x_shifted = x_np - valid_max
        # 计算指数
        exp_x = np.exp(x_shifted)
        # 归一化
        return exp_x / np.sum(exp_x)

    # assign items for bins
    for n_edge in range(num_edges):
        probs = softmax(remaining_edges, mask)

        # 根据概率分布采样一个索引
        sampled_index = np.random.choice(range(3), p=probs)

        edge_number_for_sets[sampled_index] += 1
        remaining_edges[sampled_index] -= 1
        if remaining_edges[sampled_index] == 0:
            mask[sampled_index] = True

    # 随机生成边

    combination1 = list(product(first_chunk_nodes, second_chunk_nodes))
    random.shuffle(combination1)
    combination2 = list(product(second_chunk_nodes, third_chunk_nodes))
    random.shuffle(combination2)
    combination3 = list(product(first_chunk_nodes, third_chunk_nodes))
    random.shuffle(combination3)

    edges = (
        combination1[: edge_number_for_sets[0]]
        + combination2[: edge_number_for_sets[1]]
        + combination3[: edge_number_for_sets[2]]
    )

    shuffle_nodes = list(range(num_nodes))
    random.shuffle(shuffle_nodes)

    shuffle_edges = []
    for edge in edges:
        if shuffle_nodes[edge[0]] < shuffle_nodes[edge[1]]:
            shuffle_edges.append((shuffle_nodes[edge[0]], shuffle_nodes[edge[1]]))
        else:
            shuffle_edges.append((shuffle_nodes[edge[1]], shuffle_nodes[edge[0]]))

    shuffle_solutions = {}
    for i in range(num_nodes):
        shuffle_solutions[shuffle_nodes[i]] = solution[i]
    final_solution = []
    for i in range(num_nodes):
        final_solution.append(shuffle_solutions[i])

    # 返回生成的实例和有效解
    instance = {"nodes": nodes, "edges": shuffle_edges, "color_indices": [0, 1, 2]}
    return instance, final_solution


def verify_solution(instance, solution):
    nodes = instance["nodes"]
    edges = instance["edges"]

    try:
        # 检查每个边的两个节点颜色是否不同
        for u, v in edges:
            if solution[u] == solution[v]:
                return False, "The two nodes of an edge have the same color"
        return True, "Correct solution."
    except:
        return False, "Verification error."


# 示例用法


def test():
    for _ in range(1):
        num_nodes = 10
        num_edges = 15
        instance, solution = generate_instance(num_nodes, num_edges)
        print("Instance:", instance)
        print("Solution:", solution)
        # # 示例用法
        is_valid = verify_solution(instance, solution)
        print(is_valid)
