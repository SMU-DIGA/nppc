import random
from collections import Counter


def generate_instance(num_elements: int, max_value: int = 100):
    # Constraints
    assert (
        isinstance(num_elements, int) and num_elements >= 1
    ), "num_elements must be an integer ≥ 1."

    # 生成随机实例 A
    A = [random.randint(1, max_value) for _ in range(num_elements)]

    # 随机选择一个子集 B 作为有效解
    # 随机决定子集 B 的大小（至少包含一个元素）
    subset_size = random.randint(1, num_elements)
    B = random.sample(A, subset_size)

    # 计算目标值 K
    K = sum(B)
    instance = {"A": A, "k": K}

    return instance, B


def verify_solution(instance, solution):
    if not isinstance(solution, list):
        return False, "Wrong solution format."

    # A, K = instance  # 解包 instance 得到集合 A 和目标值 K
    A = instance["A"]
    K = instance["k"]
    B = solution  # 解包 solution 得到子集 B

    count_A = Counter(A)
    count_B = Counter(B)

    # 检查 B 是否是 A 的子集（考虑重复元素）
    for element, count in count_B.items():
        if count > count_A[element]:
            return False, f"Not a subset"

    # 检查 B 的和是否等于 K
    if sum(B) != K:
        return False, f"Wrong sum"

    return True, f"Valid subset"


def test():
    instance, solution = generate_instance(num_elements=40)
    print(instance)
    print(solution)
    print(verify_solution(instance, solution))
