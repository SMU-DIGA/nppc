# import os
#
# script_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(script_dir)
# print(os.getcwd())

import random
from typing import List, Tuple


def generate_instance(
        n: int,
):
    """
    生成3D matching实例
    n: 每个集合的大小
    返回: (所有三元组列表, matching解)
    """
    X = list(range(n))
    Y = list(range(n, 2 * n))
    Z = list(range(2 * n, 3 * n))

    # 先生成一个完美匹配作为解
    solution = []
    y_unused = Y.copy()
    z_unused = Z.copy()
    random.shuffle(y_unused)
    random.shuffle(z_unused)

    for i in range(n):
        solution.append([X[i], y_unused[i], z_unused[i]])

    # 生成额外的三元组
    all_triples = solution.copy()

    # 随机添加其他三元组
    for _ in range(n * 3):  # 添加3n个额外三元组
        x = random.choice(X)
        y = random.choice(Y)
        z = random.choice(Z)
        triple = (x, y, z)
        if triple not in all_triples:
            all_triples.append(list(triple))

    return all_triples, solution


def verify_solution(
        triples: List[Tuple[int, int, int]], matching: List[Tuple[int, int, int]]
) -> bool:
    """
    验证给定的matching是否合法
    """

    n = []
    for i in range(len(triples)):
        n.append(triples[i][0])
    n = len(set(n))

    # 检查matching中的三元组是否都在原始集合中
    if not all(m in triples for m in matching):
        return False, f"Not all triples in the matching are in the original set."

    # 检查matching大小是否为n
    if len(matching) != n:
        return False, f"The size of matching is not n."

    # 检查每个元素是否只用了一次
    used_x = set()
    used_y = set()
    used_z = set()

    for x, y, z in matching:
        if x in used_x or y in used_y or z in used_z:
            return False, f"Not mutual exclusion."
        used_x.add(x)
        used_y.add(y)
        used_z.add(z)

    return True, f"Valid matching."


# 使用示例
n = 3
all_triples, solution = generate_instance(n)

print(f"生成的3D Matching实例:")
print(f"所有三元组: {all_triples}")
print(f"\n解: {solution}")
print(f"验证解是否正确: {verify_solution(all_triples, solution)}")

# 验证错误的解
wrong_solution = solution[:-1]  # 移除一个匹配
print(f"\n验证错误的解: {verify_solution(all_triples, wrong_solution)}")
