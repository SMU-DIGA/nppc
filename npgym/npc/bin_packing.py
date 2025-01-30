import random


def generate_instance(
    num_items,
    bin_capacity,
    num_bins,
    min_item_size=1,
    max_item_size=None,
):
    """
    Generate a bin packing decision instance.

    Args:
        num_items (int): Number of items to generate
        bin_capacity (int): Capacity of each bin
        num_bins (int): Number of bins available
        min_item_size (int): Minimum size of items
        max_item_size (int): Maximum size of items (defaults to bin_capacity)
        seed (int): Random seed for reproducibility
        solvable (bool): Whether to guarantee the instance is solvable

    Returns:
        list: List of item sizes
    """

    if max_item_size is None:
        max_item_size = bin_capacity

    if max_item_size > bin_capacity:
        raise ValueError("max_item_size cannot be larger than bin_capacity")

    # Generate items ensuring solution exists with given number of bins
    items = []
    current_bin = 0
    current_bin_space = bin_capacity

    solution = []
    for _ in range(num_items):
        # Move to next bin if current bin is full or nearly full
        if current_bin_space < min_item_size:
            current_bin += 1
            if current_bin >= num_bins:
                break
            current_bin_space = bin_capacity

        # Calculate maximum possible item size for this slot
        max_possible = min(max_item_size, current_bin_space)

        # Generate item size
        item_size = random.randint(min_item_size, max_possible)
        items.append(item_size)
        current_bin_space -= item_size
        solution.append(current_bin)

    # If we need more items, add small items that can fit somewhere
    while len(items) < num_items:
        item_size = random.randint(
            min_item_size,
            min(max_item_size, bin_capacity // (num_items - len(items) + 1)),
        )
        items.append(item_size)

    # Shuffle items to make the instance more interesting
    random.shuffle(items)

    instance = {"items": items, "bin_capacity": bin_capacity, "num_bins": num_bins}

    return instance, None


def verify_solution(instance, solution):
    """
    Verify if a bin packing solution is valid for the decision version.

    Args:
        items (list): List of item sizes
        bin_capacity (int): Capacity of each bin
        num_bins (int): Number of bins available
        solution (list): List of bin assignments (each element is a bin number)

    Returns:
        tuple: (is_valid, error_message)
            - is_valid: Boolean indicating if solution is valid
            - error_message: String explaining why solution is invalid (if applicable)
    """
    items = instance["items"]
    num_bins = instance["num_bins"]
    bin_capacity = instance["bin_capacity"]
    if len(items) != len(solution):
        return False, "Number of items doesn't match solution length"

    # Check if all bin assignments are valid numbers
    if any(not isinstance(x, int) or x < 0 or x >= num_bins for x in solution):
        return False, f"Invalid bin numbers in solution (must be 0 to {num_bins - 1})"

    # Calculate bin loads
    bin_loads = {}
    for item_idx, bin_num in enumerate(solution):
        if bin_num not in bin_loads:
            bin_loads[bin_num] = 0
        bin_loads[bin_num] += items[item_idx]

        # Check if bin capacity is exceeded
        if bin_loads[bin_num] > bin_capacity:
            return (
                False,
                f"Bin {bin_num} exceeds capacity: {bin_loads[bin_num]} > {bin_capacity}",
            )

    return True, "Solution is valid"


# instance, _ = generate_instance(num_items=10, bin_capacity=5, num_bins=8)
#
# print(instance)
