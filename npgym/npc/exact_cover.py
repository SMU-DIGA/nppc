import random
from typing import List, Set


def generate_instance(n: int, m: int, k: int) -> tuple[list[set[int]], set[int]]:
    """
    生成一个Exact Cover问题实例

    参数:
    n: 基础集合的大小
    m: 子集的数量
    k: 解中需要的子集数量

    返回:
    tuple(subsets, universe):
        subsets: 子集列表
        universe: 基础集合
    """
    # 创建基础集合
    universe = set(range(1, n + 1))

    # 首先生成一个有效解
    remaining = universe.copy()
    solution_sets = []
    for _ in range(k):
        if not remaining:
            break
        # 随机选择remaining中的一些元素作为新的子集
        subset_size = random.randint(1, min(len(remaining), n // k + 1))
        new_subset = set(random.sample(list(remaining), subset_size))
        solution_sets.append(new_subset)
        remaining -= new_subset

    # 如果还有未覆盖的元素，将它们随机分配给解中的子集
    if remaining:
        for elem in remaining:
            random.choice(solution_sets).add(elem)

    # 生成额外的随机子集
    subsets = solution_sets.copy()
    for _ in range(m - k):
        subset_size = random.randint(1, n // 2)
        new_subset = set(random.sample(list(universe), subset_size))
        subsets.append(new_subset)

    # 随机打乱子集的顺序
    random.shuffle(subsets)

    return subsets, universe


def verify_solution(
    subsets: List[Set[int]], universe: Set[int], solution_indices: List[int]
) -> bool:
    """
    验证给定的解是否是有效的Exact Cover解

    参数:
    subsets: 子集列表
    universe: 基础集合
    solution_indices: 选择的子集索引列表

    返回:
    bool: 解是否有效
    """
    # 检查索引是否有效
    if not all(0 <= i < len(subsets) for i in solution_indices):
        return False

    # 检查是否有重复的索引
    if len(set(solution_indices)) != len(solution_indices):
        return False

    # 计算选中子集的并集
    covered = set()
    for i in solution_indices:
        # 检查是否与已覆盖的元素有重叠
        if covered & subsets[i]:
            return False
        covered |= subsets[i]

    # 检查是否完全覆盖universe
    return covered == universe


# 使用示例
def example_usage():
    # 生成实例：基础集合大小为10，8个子集，需要3个子集的解
    subsets, universe = generate_instance(10, 8, 3)

    print("生成的实例:")
    print(f"基础集合: {universe}")
    print("子集列表:")
    for i, subset in enumerate(subsets):
        print(f"{i}: {subset}")

    # 假设我们找到了一个可能的解
    solution = [0, 2, 4]  # 这只是一个示例，不一定是有效解

    # 验证解
    is_valid = verify_solution(subsets, universe, solution)
    print(f"\n解 {solution} 是否有效: {is_valid}")


if __name__ == "__main__":
    example_usage()
