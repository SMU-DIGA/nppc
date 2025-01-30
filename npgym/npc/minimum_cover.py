import random


def generate_instance(num_elements, num_sets, k):
    """
    Generate an instance of the decision version of Minimum Set Cover problem.
    The instance is guaranteed to have at least one solution.

    Args:
        num_elements (int): Number of elements in the universe
        num_sets (int): Number of sets to generate
        k (int): The target number of sets for the decision problem
        seed (int, optional): Random seed for reproducibility

    Returns:
        tuple: (universe, sets, k) where
            - universe is a set of elements (represented as integers)
            - sets is a list of sets
            - k is the target number of sets
    """

    # Create universe of elements
    universe = set(range(num_elements))

    # First, generate k sets that together cover all elements
    # This ensures at least one solution exists
    remaining_elements = universe.copy()
    solution_sets = []
    elements_per_set = max(1, num_elements // k)

    for i in range(k):
        if i == k - 1:
            # Last set takes all remaining elements
            new_set = remaining_elements
        else:
            # Take a random subset of remaining elements
            size = min(elements_per_set, len(remaining_elements))
            new_set = set(random.sample(list(remaining_elements), size))

        solution_sets.append(new_set)
        remaining_elements -= new_set

    # Generate additional random sets
    all_sets = solution_sets.copy()
    for _ in range(num_sets - k):
        # Create a random set with size between 1 and num_elements/2
        size = random.randint(1, max(1, num_elements // 2))
        new_set = set(random.sample(list(universe), size))
        all_sets.append(new_set)

    # Shuffle the sets
    random.shuffle(all_sets)

    instance = {"universe": universe, "subsets": all_sets, "k": k}

    return instance, solution_sets


def verify_solution(instance, solution_indices):
    """
    Verify if the given solution is valid for the decision version of Minimum Set Cover.

    Args:
        universe (set): Set of all elements to be covered
        sets (list): List of sets available to choose from
        k (int): Maximum number of sets allowed in the solution
        solution_indices (list): Indices of the sets chosen in the solution

    Returns:
        tuple: (is_valid, message) where
            - is_valid is a boolean indicating if the solution is valid
            - message is a string explaining why the solution is invalid (if applicable)
    """

    universe = instance['universe']
    k = instance['k']
    sets = instance['subsets']
    # Check if solution uses at most k sets
    if len(solution_indices) > k:
        return (
            False,
            f"Solution uses {len(solution_indices)} sets, but only {k} are allowed",
        )

    # Check if indices are valid
    if not all(0 <= i < len(sets) for i in solution_indices):
        return False, "Invalid set indices in solution"

    # Check if solution covers all elements
    covered = set().union(*[sets[i] for i in solution_indices])
    if covered != universe:
        missing = universe - covered
        return False, f"Solution does not cover all elements. Missing: {missing}"

    return True, "Valid solution"


instance, solution = generate_instance(num_elements=20, num_sets=30, k=5 )

print(instance)
print(solution)
