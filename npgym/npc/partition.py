import random
from typing import List, Tuple
import itertools


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
        A[i] += -diff
    # Now, sum_A1 == sum_A2

    # Optional: Shuffle A so that the partition is not immediately obvious.
    # random.shuffle(A)
    A1 = [A[i] for i in A1_indices]
    A2 = [A[i] for i in A2_indices]

    return A, [sorted(A1), sorted(A2)]


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
