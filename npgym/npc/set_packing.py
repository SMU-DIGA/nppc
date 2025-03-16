import random
from typing import List, Set, Tuple


def generate_instance(num_elements: int, num_subsets: int, num_disjoint_sets: int):
    """
    Generates a Set Packing problem instance with at least one valid solution.

    Parameters:
    - num_elements: Total number of unique elements in the universe S.
    - num_subsets: Total number of sets in the collection C.
    - num_disjoint_sets: Number of disjoint sets required in the solution.
    - max_set_size: Maximum size of any subset.

    Returns:
    - instance (dict): The generated Set Packing instance.
    - selected_ids (list): The indices of sets forming a guaranteed solution.
    """
    
    assert num_disjoint_sets <= num_subsets, "num_disjoint_sets must be less than or equal to num_subsets"
   
    max_set_size = num_elements // num_disjoint_sets
    assert max_set_size > 0, "max_set_size must be greater than 0"
    # Step 1: Create a universal set S
    universal_set = set(range(num_elements))

    # Step 2: Generate num_disjoint_sets pairwise disjoint sets (ensuring a valid solution)
    selected_elements = set()
    selected_ids = []
    C = []
    
    for i in range(num_disjoint_sets):
        subset_size = random.randint(1, max_set_size)
        subset = set(random.sample(universal_set - selected_elements, subset_size))
        C.append(subset)
        selected_elements.update(subset)
        selected_ids.append(i)

    # Step 3: Generate additional sets, possibly overlapping
    while len(C) < num_subsets:
        subset_size = random.randint(1, max_set_size)
        subset = set(random.sample(universal_set, subset_size))  # May overlap
        if subset not in C:
            C.append(subset)

    # Step 4: Shuffle the order of subsets
    shuffled_indices = list(range(len(C)))
    random.shuffle(shuffled_indices)

    # Create a mapping from original indices to shuffled indices
    shuffled_sets = {i: list(C[shuffled_indices[i]]) for i in range(len(C))}

    # Adjust selected_ids to match shuffled order
    selected_ids = sorted([shuffled_indices.index(i) for i in selected_ids])

    # Step 5: Construct the final instance
    instance = {
        "universe": list(universal_set),
        "subsets": shuffled_sets,
        "k": num_disjoint_sets,
    }

    return instance, selected_ids



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
    if not isinstance(selected_sets, list):
        return False, "Wrong solution format."

    k = instance["k"]

    # Check if we have exactly k sets
    if len(selected_sets) != k:
        return False, "The selected subsets is not {}".format(k)

    sets = instance["subsets"]
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

def test():
    instance, solution = generate_instance(
        100, 200, 50
    )
    print(instance)
    print(solution)
    print(verify_solution(instance, solution))

if __name__ == "__main__":
    test()