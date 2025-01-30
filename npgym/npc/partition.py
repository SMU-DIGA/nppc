import random
from typing import List, Tuple


def generate_instance(n: int, max_value: int = 100):
    """Generate a partition problem instance

    Args:
        n: Number of integers in the set
        max_value: Maximum value for each integer

    Returns:
        List of positive integers
    """
    # Generate random positive integers
    numbers = []
    target_sum = 0
    for _ in range(n - 1):
        num = random.randint(1, max_value)
        numbers.append(num)
        target_sum += num

    # Generate last number to ensure a solution exists
    remainder = target_sum % 2
    if remainder == 0:
        numbers.append(random.randint(1, max_value))
    else:
        numbers.append(random.randint(1, max_value) * 2 + 1)

    random.shuffle(numbers)
    return numbers, None


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


numbers, _ = generate_instance(6)
print(f"Numbers: {numbers}")

# Example solution (may not be valid)
solution = [True, False, True, False, True, False]
valid, msg = verify_solution(numbers, solution)
print(f"Validation result: {msg}")
