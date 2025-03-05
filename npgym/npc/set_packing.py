import random
from typing import List, Set, Tuple


def generate_instance(num_elements: int, num_subsets: int, num_disjoint_sets: int):
    """
    Generate a set packing instance with at least one valid solution.

    # Args:
    #     n (int): Number of elements in the universe
    #     m (int): Number of sets to generate
    #     k (int): Size of a valid solution (number of disjoint sets)
    #
    # Returns:
    #     Tuple[List[Set[int]], int]: A tuple containing:
    #         - List of sets representing the instance
    #         - Target k value (number of disjoint sets to find)
    """
    if num_disjoint_sets > num_subsets:
        raise ValueError("k cannot be larger than m")
    # if k * n < n:  # Ensure we can create k disjoint sets
    #     raise ValueError("k is too small to guarantee a solution")

    # First, generate k disjoint sets to ensure at least one solution exists
    universe = set(range(num_elements))
    sets = []
    available_elements = list(universe)

    # Generate k disjoint sets first
    for _ in range(num_disjoint_sets):
        # For each set, randomly choose elements from available elements
        set_size = random.randint(
            1, max(1, len(available_elements) // (num_disjoint_sets * 2))
        )
        new_set = set(random.sample(available_elements, set_size))

        # Remove used elements from available_elements
        available_elements = [x for x in available_elements if x not in new_set]
        sets.append(new_set)

        # solution.append(new_set)

    # Generate remaining m-k sets randomly
    for _ in range(num_subsets - num_disjoint_sets):
        set_size = random.randint(1, num_elements // 2)
        new_set = set(random.sample(list(universe), set_size))
        sets.append(new_set)

    # Shuffle the sets to hide the solution

    set_indices = [i for i in range(len(sets))]
    random.shuffle(set_indices)
    shuffle_sets = {}
    solution = []
    selected_sets = []
    for idx, i in enumerate(set_indices):
        shuffle_sets[idx] = list(sets[i])
        if i < num_disjoint_sets:
            solution.append(idx)
            selected_sets.append(list(sets[i]))

    instance = {
        "Universe": list(universe),
        "Subsets": shuffle_sets,
        "K": num_disjoint_sets,
    }
    # print(selected_sets)

    return instance, solution


def verify_solution(instance, selected_sets):
    """
    Verify if the given solution is valid for the set packing instance.

    # Args:
    #     sets (List[Set[int]]): List of sets representing the instance
    #     selected_sets (List[int]): Indices of selected sets in the solution
    #     k (int): Required number of disjoint sets

    Returns:
        bool: True if the solution is valid, False otherwise
    """

    k = instance["K"]

    # Check if we have exactly k sets
    if len(selected_sets) != k:
        return False, "The selected subsets is not {}".format(k)

    sets = instance["Subsets"]
    # Check if all indices are valid
    if not all(0 <= i < len(sets) for i in selected_sets):
        return False, "Some indices are invalid."

    # Check if sets are disjoint
    union = set()
    for idx in selected_sets:
        if not set(sets[idx]).isdisjoint(union):
            return False, "The sets are not disjoint."
        union.update(sets[idx])

    return True, "Correct solution."


# instance, solution = generate_instance(
#     num_elements=10, num_subsets=20, num_disjoint_sets=2
# )
# print(instance)
# print(solution)
# print(verify_solution(instance, solution))
