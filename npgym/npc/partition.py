import random
from typing import List, Tuple
import itertools

# def generate_instance(n: int, max_value: int = 100):
#     # Constraints
#     assert isinstance(n, int) and n >= 2, "n must be an integer ≥ 2."
#     assert isinstance(max_value, int) and max_value >= 1, "max_value must be an integer ≥ 1."

#     # 确保 n 是偶数，否则无法均分
#     if n < 2:
#         raise ValueError("n must be at least 2 to form a partition.")

#     # 随机生成 A1 和 A2 的大小（元素个数）
#     # 确保 A1 和 A2 的元素个数之和为 n
#     size_A1 = random.randint(1, n - 1)
#     size_A2 = n - size_A1

#     # 生成 A1 和 A2 的元素，确保它们的和相等
#     # 先生成 A1 的元素
#     while True:
#         A1 = [random.randint(1, max_value) for _ in range(size_A1)]
#         sum_A1 = sum(A1)
#         if sum_A1 >= size_A2:
#             break

#     # 生成 A2 的元素，确保 sum(A2) == sum(A1)
#     A2 = []
#     remaining_sum = sum_A1
#     for idx in range(size_A2 - 1):
#         value = random.randint(1, min(remaining_sum - (size_A2 - 1 - idx), max_value))
#         A2.append(value)
#         remaining_sum -= value
#     A2.append(remaining_sum)

#     # 合并 A1 和 A2 成最终的实例 A
#     A = A1 + A2
#     # 打乱顺序，避免 A1 和 A2 在 A 中是连续的

#     indexed = list(enumerate(A))
#     # 随机打乱
#     random.shuffle(indexed)
#     # 解压缩得到打乱后的列表和对应的原始索引
#     indices, shuffled = zip(*indexed)

#     partition = []
#     # partition = [[], []]

#     for i in range(len(A)):
#         if indices[i] < len(A1):
#             partition.append(True)
#             # partition[0].append(shuffled[i])
#             # A1_set.remove(num)  # 避免重复元素的问题
#         else:
#             partition.append(False)
#             # partition[1].append(shuffled[i])
#     # partition = [sorted(partition[0]), sorted(partition[1])]
#     # partition = [partition[1], partition[0]] if len(partition[0]) > len(partition[1]) else partition
#     return list(shuffled), partition

import random

def generate_instance(n: int, max_value: int = 100):
    """
    Generates an instance of the Partition Problem that has at least one solution.
    
    Args:
        n (int): Number of elements in the instance.
        max_value (int): Upper bound for the randomly generated numbers (before adjustment).
        
    Returns:
        A (list of int): A list of n positive integers that is partitionable into two subsets with equal sum.
    """
    if n < 2:
        raise ValueError("n must be at least 2.")
    
    # Step 1: Generate a list A of n random positive integers.
    A = [random.randint(1, max_value) for _ in range(n)]
    
    # Step 2: Randomly partition the indices into two groups.
    indices = list(range(n))
    random.shuffle(indices)
    # Let A1 be the first half (or nearly half) and A2 the remaining indices.
    half = n // 2
    A1_indices = indices[:half]
    A2_indices = indices[half:]
    
    # Step 3: Compute the sum of A1 and A2.
    sum_A1 = sum(A[i] for i in A1_indices)
    sum_A2 = sum(A[i] for i in A2_indices)
    
    # Step 4: Adjust one element so that the two sums are equal.
    diff = sum_A1 - sum_A2
    if diff > 0:
        # Increase sum_A2: choose an element from A2 and add diff.
        # (You might also consider decreasing an element in A1, but here we choose to increase.)
        i = random.choice(A2_indices)
        A[i] += diff
    elif diff < 0:
        # Increase sum_A1 by adding the absolute difference to one element in A1.
        i = random.choice(A1_indices)
        A[i] += (-diff)
    # Now, sum_A1 == sum_A2

    # Optional: Shuffle A so that the partition is not immediately obvious.
    # random.shuffle(A)
    A1 = [A[i] for i in A1_indices]
    A2 = [A[i] for i in A2_indices]
    
    return A, [sorted(A1), sorted(A2)]



# def verify_solution(numbers: List[int], partition: List[bool]) -> Tuple[bool, str]:
#     """Verify if the partition is valid

#     Args:
#         numbers: List of integers to be partitioned
#         partition: Boolean list where True indicates number goes to first subset

#     Returns:
#         Tuple of (is_valid, error_message)
#     """
#     if len(numbers) != len(partition):
#         return False, "Partition length doesn't match input length"

#     sum1 = sum(num for num, include in zip(numbers, partition) if include)
#     sum2 = sum(num for num, include in zip(numbers, partition) if not include)

#     if sum1 == sum2:
#         return True, f"Valid partition with sum {sum1}"
#     else:
#         return False, f"Invalid partition: {sum1} ≠ {sum2}"

def verify_solution(numbers, partition):
    """Verify if the partition is valid

    Args:
        numbers: List of integers to be partitioned
        partition: Boolean list where True indicates number goes to first subset

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(partition, list) or len(partition) != 2:
        return False, "Partition must be a list of two lists."

    # Ensure each element in partition is a list
    if not all(isinstance(sublist, list) for sublist in partition):
        return False, "Each element in the partition must be a list."
    
    flattened_list = list(itertools.chain(*partition))
    if sorted(numbers) != sorted(flattened_list):
        return False, "Not a partition of the original set."

    sum1 = sum(partition[0])
    sum2 = sum(partition[1])
    
    if sum1 == sum2:
        return True, f"Valid partition with sum {sum1}"
    else:
        return False, f"Invalid partition: {sum1} ≠ {sum2}"

def test():
    instances, partition = generate_instance(10, 100)
    print(instances)
    print(partition)
    res = verify_solution(instances, [[1], [2]])
    print(res)

if __name__ == "__main__":
    test()