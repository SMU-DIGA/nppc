import random
from typing import List, Tuple


def generate_instance(n: int, max_value: int = 100):
    # 确保 n 是偶数，否则无法均分
    if n < 2:
        raise ValueError("n must be at least 2 to form a partition.")

    # 随机生成 A1 和 A2 的大小（元素个数）
    # 确保 A1 和 A2 的元素个数之和为 n
    size_A1 = random.randint(1, n - 1)
    size_A2 = n - size_A1

    # 生成 A1 和 A2 的元素，确保它们的和相等
    # 先生成 A1 的元素
    while True:
        A1 = [random.randint(1, max_value) for _ in range(size_A1)]
        sum_A1 = sum(A1)
        if sum_A1 >= size_A2:
            break

    # 生成 A2 的元素，确保 sum(A2) == sum(A1)
    A2 = []
    remaining_sum = sum_A1
    for idx in range(size_A2 - 1):
        value = random.randint(1, min(remaining_sum - (size_A2 - 1 - idx), max_value))
        A2.append(value)
        remaining_sum -= value
    A2.append(remaining_sum)

    # 合并 A1 和 A2 成最终的实例 A
    A = A1 + A2
    # 打乱顺序，避免 A1 和 A2 在 A 中是连续的

    indexed = list(enumerate(A))
    # 随机打乱
    random.shuffle(indexed)
    # 解压缩得到打乱后的列表和对应的原始索引
    indices, shuffled = zip(*indexed)

    partition = []
    for i in range(len(A)):
        if indices[i] < len(A1):
            partition.append(True)
            # A1_set.remove(num)  # 避免重复元素的问题
        else:
            partition.append(False)

    return list(shuffled), partition


def verify_solution(numbers: List[int], partition: List[bool]) -> Tuple[bool, str]:
    """Verify if the partition is valid

    Args:
        numbers: List of integers to be partitioned
        partition: Boolean list where True indicates number goes to first subset

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(numbers) != len(partition):
        return False, "Partition length doesn't match input length"

    sum1 = sum(num for num, include in zip(numbers, partition) if include)
    sum2 = sum(num for num, include in zip(numbers, partition) if not include)

    if sum1 == sum2:
        return True, f"Valid partition with sum {sum1}"
    else:
        return False, f"Invalid partition: {sum1} ≠ {sum2}"


# numbers, solution = generate_instance(6)
# print(f"Numbers: {numbers}")
#
# # Example solution (may not be valid)
# # solution = [True, False, True, False, True, False]
# valid, msg = verify_solution(numbers, solution)
# print(f"Validation result: {msg}")




numbers, solution = generate_instance(6)
print(f"Numbers: {numbers}")
print(solution)
valid, msg = verify_solution(numbers, solution)

print(f"Validation result: {msg}")


