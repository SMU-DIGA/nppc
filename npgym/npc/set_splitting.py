import random


def generate_valid_numbers(x1, x2, x3):
    while True:
        a = random.randint(1, min(x1-1, x3-1))  # Ensure a < x1 and a < x3
        b = random.randint(1, min(x2-1, x3-a))  # Ensure b < x2 and a + b < x3
        
        if a + b < x3:
            return a, b

def generate_instance(num_elements, num_subsets):
    """
    Generate an instance of the Set Splitting problem with at least one solution.

    Args:
        n (int): Number of elements in the universal set S.
        m (int): Number of subsets in collection C.

    Returns:
        tuple: (universal_set, subsets), where:
            - universal_set (set): The full set of elements.
            - subsets (list of sets): The collection of m subsets.
    """

    assert num_elements >= 2, "The universal set must contain at least 2 elements."
    assert num_subsets >= 1, "There must be at least one subset."

    # Step 1: Create the universal set S with unique elements
    universal_set = set(range(1, num_elements + 1))  # Elements labeled from 1 to n

    # Step 2: Randomly partition S into two initial disjoint sets S1 and S2
    shuffled_list = list(universal_set)
    random.shuffle(shuffled_list)
    split_idx = num_elements // 2
    S1 = set(shuffled_list[:split_idx])
    S2 = set(shuffled_list[split_idx:])
    # Step 3: Generate subsets ensuring each subset has at least one element from S1 and S2
    subsets = []
    for _ in range(num_subsets):
        size_s1, size_s2 = generate_valid_numbers(len(S1), len(S2), num_elements)
        from_S1 = random.sample(S1, k=size_s1)
        from_S2 = random.sample(S2, k=size_s2)
        subset = set(from_S1 + from_S2)
        subsets.append(subset)
    
    subsets_dict = {}
    for subset in subsets:
        subsets_dict[len(subsets_dict)] = list(subset)

    instance = {"universe": list(universal_set), "subsets": subsets_dict}
    
    return instance, [list(S1), list(S2)]


def verify_solution(instance, partition):
    if not isinstance(partition, list) or len(partition) != 2:
        return False, "Partition must be a list of two lists."

    # Ensure each element in partition is a list
    if not all(isinstance(sublist, list) for sublist in partition):
        return False, "Each element in the partition must be a list."
    
    # Check if partition only contains valid elements
    partition_A = set(partition[0])
    universe = instance["universe"]
    subsets = instance["subsets"]
    if not partition_A.issubset(set(universe)):
        return False, "The partition is not valid."

    # Create partition B
    partition_B = set(universe) - partition_A

    # Check if each subset has at least one element in both partitions
    for subset_key in subsets:
        subset = subsets[subset_key]
        if not (set(subset) & partition_A and set(subset) & partition_B):
            return False, "Some subset is in both partitions."

    return True, "Correct solution."

def test():
    instance, solution = generate_instance(10, 300)
    print(instance)
    print(solution)
    print(verify_solution(instance, [[], []]))
    

if __name__ == "__main__":
    test()