import random


def generate_instance(num_elements, b):
    """
    Generate a clustering instance ensuring at least one valid 3-partition exists.

    Args:
        n (int): Number of elements in set X
        B (int): Maximum allowed distance between any pair in same cluster

    Returns:
        tuple: (distances, B)
            - distances: Dictionary with (i,j) tuples as keys and distances as values
            - B: The input bound B
    """

    # Generate three groups of points with guaranteed small distances within groups
    group_size = num_elements // 3
    remaining = num_elements % 3
    group_sizes = [group_size + (1 if i < remaining else 0) for i in range(3)]

    # Track which element belongs to which group during generation
    element_groups = []
    for i in range(3):
        element_groups.extend([i] * group_sizes[i])

    random.shuffle(element_groups)

    # Generate distances
    distances = {}
    for i in range(num_elements):
        for j in range(i + 1, num_elements):
            if element_groups[i] == element_groups[j]:
                # If in same group, ensure distance is ≤ B
                distances[(i, j)] = random.randint(1, b)
            else:
                # If in different groups, distance can be larger
                distances[(i, j)] = random.randint(b + 1, 2 * b)

    instance = {
        "b": b,
        "elements": [i for i in range(num_elements)],
        "distances": distances,
    }
    return instance, element_groups


def verify_solution(instance, partition):
    """
    Verify if a given 3-partition solution is valid.

    Args:
        distances (dict): Dictionary with (i,j) tuples as keys and distances as values
        B (int): Maximum allowed distance between any pair in same cluster
        partition (list): List of length n where partition[i] ∈ {0,1,2} indicates
                         which set (X₁, X₂, or X₃) element i belongs to

    Returns:
        tuple: (is_valid, message)
            - is_valid: Boolean indicating if partition is valid
            - message: Explanation of why partition is invalid, or "Valid solution" if valid
    """
    # Check if partition assigns each element to one of three sets
    if not all(x in {0, 1, 2} for x in partition):
        return False, "Each element must be assigned to set 0, 1, or 2"

    distances = instance["distances"]
    B = instance["b"]
    # Check if all three sets are used
    used_sets = set(partition)
    if len(used_sets) != 3:
        return False, f"Must use exactly 3 sets, but used {len(used_sets)} sets"

    # Check distances within each set
    n = len(partition)
    for i in range(n):
        for j in range(i + 1, n):
            if partition[i] == partition[j]:  # If in same set
                if (i, j) not in distances:
                    return False, f"Missing distance for pair ({i},{j})"
                if distances[(i, j)] > B:
                    return (
                        False,
                        f"Distance {distances[(i, j)]} between elements {i} and {j} in set X_{partition[i] + 1} exceeds bound B={B}",
                    )

    return True, "Valid solution"


instance, solution = generate_instance(num_elements=10, b=5)

print(instance)
print(solution)

# random.shuffle(solution)

print(verify_solution(instance, solution))
