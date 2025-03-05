import random


def generate_instance(
    num_cities: int, target_length: int, min_distance=1, max_distance=100
):
    """
    Generate a TSP decision instance with guaranteed solution under target_length.

    Args:
        num_cities (int): Number of cities
        target_length (float): Target tour length threshold
        min_distance (int): Minimum distance between cities
        max_distance (int): Maximum distance between cities
        seed (int): Random seed for reproducibility

    Returns:
        list: 2D distance matrix where distances[i][j] is distance from city i to j
    """

    if num_cities < 3:
        raise ValueError("Number of cities must be at least 3")

    instance = {"length": target_length}

    # Initialize distance matrix with zeros
    distances = [[0] * num_cities for _ in range(num_cities)]

    # First, generate a known feasible tour under target_length
    cities_order = list(range(num_cities))
    random.shuffle(cities_order)

    # Distribute target length among edges to ensure feasibility
    remaining_length = target_length * 0.9  # Leave some margin
    edges_in_tour = num_cities

    # Assign distances between consecutive cities in the feasible tour
    for i in range(num_cities):
        city1 = cities_order[i]
        city2 = cities_order[(i + 1) % num_cities]

        # Assign a random portion of remaining length
        if i == num_cities - 1:
            # Last edge gets remaining length
            distance = remaining_length
        else:
            max_for_edge = remaining_length - (min_distance * (edges_in_tour - i - 1))
            distance = random.uniform(min_distance, min(max_for_edge, max_distance))

        remaining_length -= distance
        distances[city1][city2] = distance
        distances[city2][city1] = distance  # Make it symmetric

    # Fill remaining distances with values ensuring triangle inequality
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            if distances[i][j] == 0:  # If not already set
                # Find min and max possible distances satisfying triangle inequality
                min_possible = 0
                max_possible = float("inf")

                for k in range(num_cities):
                    if k != i and k != j:
                        # Triangle inequality constraints
                        if distances[i][k] > 0 and distances[k][j] > 0:
                            min_possible = max(
                                min_possible, abs(distances[i][k] - distances[k][j])
                            )
                            max_possible = min(
                                max_possible, distances[i][k] + distances[k][j]
                            )

                if max_possible == float("inf"):
                    max_possible = max_distance

                min_possible = max(min_possible, min_distance)
                max_possible = min(max_possible, max_distance)

                if min_possible > max_possible:
                    min_possible = max_possible

                distance = random.uniform(min_possible, max_possible)
                distances[i][j] = distance
                distances[j][i] = distance

    instance["distances"] = distances
    return instance, cities_order


def verify_solution(instance, tour):
    """
    Verify if a TSP tour is valid and under target length.

    Args:
        distances (list): 2D distance matrix
        target_length (float): Maximum allowed tour length
        tour (list): List of city indices representing the tour

    Returns:
        tuple: (is_valid, error_message)
            - is_valid: Boolean indicating if solution is valid
            - error_message: String explaining why solution is invalid (if applicable)
    """

    distances = instance["distances"]
    target_length = instance["length"]
    num_cities = len(distances)

    # Check if tour length matches number of cities
    if len(tour) != num_cities:
        return False, "Tour must visit exactly all cities once"

    if not (max(tour) < num_cities and min(tour) >= 0):
        return False, "Invalid city index."

    # Check if all cities are visited exactly once
    if sorted(tour) != list(range(num_cities)):
        return False, "Tour must contain each city exactly once"

    # Calculate total tour length
    total_length = 0
    for i in range(num_cities):
        city1 = tour[i]
        city2 = tour[(i + 1) % num_cities]
        total_length += distances[city1][city2]

    # Check if tour length is within target
    if total_length > target_length:
        return (
            False,
            f"Tour length {total_length} exceeds target length {target_length}",
        )

    return True, "Solution is valid"


instance, solution = generate_instance(num_cities=5, target_length=10)

print(instance)
print(solution)

print(verify_solution(instance, solution))
solution = [0, 1, 2, 3, 4]
print(verify_solution(instance, solution))
