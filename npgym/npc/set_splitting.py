import random


def generate_instance(num_elements, num_subsets):
    """
    Generate an instance of the Set Splitting decision problem.

    # Args:
    #     n (int): Number of elements in the universe
    #     m (int): Number of subsets
    #     seed (int, optional): Random seed for reproducibility
    #
    # Returns:
    #     tuple: (universe, subsets)
    #         - universe: list of integers representing elements
    #         - subsets: list of sets containing elements from universe
    """

    # Create universe of n elements
    universe = list(range(1, num_elements + 1))

    # Generate m random subsets that guarantee at least one solution exists
    subsets = []

    # First, create a valid partition to ensure solution exists
    partition_A = set(random.sample(universe, num_elements // 2))
    partition_B = set(universe) - partition_A

    # Generate m-2 random subsets

    # partial_subset = num_subsets // 2
    # for _ in range(partial_subset):
    #     subset_size = random.randint(2, num_elements - 1)
    #     subset = set(random.sample(universe, subset_size))
    #     subsets.append(subset)
    for _ in range(num_subsets):
        # Add two subsets that cross the partition to make problem non-trivial
        subset1 = set(random.sample(list(partition_A), len(partition_A) // 2))
        subset1.update(random.sample(list(partition_B), len(partition_B) // 2))

        subsets.append(list(subset1))

    # Shuffle the subsets
    random.shuffle(subsets)

    subsets_dict = {}
    for subset in subsets:
        subsets_dict[len(subsets_dict)] = subset

    instance = {"universe": list(set(universe)), "subsets": subsets_dict}

    return instance, [list(partition_A), list(partition_B)]


def verify_solution(instance, partition):
    """ """
    partition_A = set(partition[0])
    # Check if partition only contains valid elements
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


instance, solution = generate_instance(num_elements=10, num_subsets=4)
# universe = instance["universe"]
# solution = set(random.sample(universe, len(universe) // 2))
print(instance)
print(solution)
print(verify_solution(instance, solution))
