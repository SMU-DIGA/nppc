import random


def generate_instance(num_elements: int, num_sets: int, k: int):
    """生成 Minimum Cover 实例和有效解"""

    # 生成集合 S
    S = set(range(0, num_elements))  # 元素为 1, 2, ..., num_elements

    # 生成子集集合 C
    C = {}
    for i in range(num_sets):
        # 随机生成一个子集
        subset_size = random.randint(1, num_elements)  # 子集大小随机
        subset = set(random.sample(sorted(S), subset_size))
        C[i] = subset

    # 确保生成的实例至少有一个有效解
    # 随机选择一个大小为 k 的子集集合 D，确保 D 覆盖 S
    while True:
        # 随机选择 k 个子集的索引
        D_indices = random.sample(list(C.keys()), k)
        D = [C[i] for i in D_indices]

        # 检查 D 是否覆盖 S
        covered = set()
        for subset in D:
            covered.update(subset)
        if covered >= S:  # 如果 D 覆盖 S
            break

    # 返回生成的实例和有效解
    instance = {
        "universe": S,
        "subsets": C,
        "k": k
    }
    return instance, D_indices


def verify_solution(instance, solution):
    S = instance["universe"]
    C = instance["subsets"]
    k = instance["k"]

    # 检查解的大小是否不超过 k
    if len(solution) > k:
        return False, "The number of subsets in the solution exceeds k"

    # 检查解是否覆盖 S
    covered = set()
    for i in solution:
        covered.update(C[i])
    if covered >= S:
        return True, "Valid solution"
    else:
        return False, "The solution does not cover S"

# 示例用法
num_elements = 5
num_sets = 10
k = 3
instance, solution = generate_instance(num_elements, num_sets, k)
print("Instance:", instance)
print("Solution:", solution)



# 示例用法
is_valid = verify_solution(instance, solution)
print("Is the solution valid?", is_valid)