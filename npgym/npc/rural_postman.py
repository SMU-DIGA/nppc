from typing import List, Tuple, Dict, Set
import random


# TODO: need revision
def generate_instance(
    num_vertices: int,
    num_required_edges: int,
    num_optional_edges: int,
    min_weight: int,
    max_weight: int,
    budget: int = None,
) -> Dict:
    """
    Generate a Rural Postman Problem instance with guaranteed feasible solution.

    Args:
        num_vertices: Number of vertices in the graph
        num_required_edges: Number of required edges
        num_optional_edges: Number of optional edges
        min_weight: Minimum weight for edges
        max_weight: Maximum weight for edges
        budget: Budget constraint for the decision version (if None, will be set automatically)

    Returns:
        Dict containing:
        - vertices: List of vertices
        - required_edges: List of tuples (u, v, weight) for required edges
        - optional_edges: List of tuples (u, v, weight) for optional edges
        - budget: Integer representing the budget constraint
    """
    if num_vertices < 2:
        raise ValueError("Number of vertices must be at least 2")
    if num_required_edges < 1:
        raise ValueError("Must have at least 1 required edge")

    vertices = list(range(num_vertices))
    used_pairs = set()
    required_edges = []

    # First, create a connected component with required edges
    # Build a path to ensure connectivity
    for i in range(num_vertices - 1):
        weight = random.randint(min_weight, max_weight)
        required_edges.append((i, i + 1, weight))
        used_pairs.add((i, i + 1))
        used_pairs.add((i + 1, i))

    # Add remaining required edges randomly
    attempts = 0
    max_attempts = 100
    while len(required_edges) < num_required_edges and attempts < max_attempts:
        u = random.choice(vertices)
        v = random.choice(vertices)
        if u != v and (u, v) not in used_pairs:
            weight = random.randint(min_weight, max_weight)
            required_edges.append((u, v, weight))
            used_pairs.add((u, v))
            used_pairs.add((v, u))
        attempts += 1

    # Generate optional edges
    optional_edges = []
    attempts = 0
    while len(optional_edges) < num_optional_edges and attempts < max_attempts:
        u = random.choice(vertices)
        v = random.choice(vertices)
        if u != v and (u, v) not in used_pairs:
            weight = random.randint(min_weight, max_weight)
            optional_edges.append((u, v, weight))
            used_pairs.add((u, v))
            used_pairs.add((v, u))
        attempts += 1

    # If budget is not provided, set it based on a feasible solution
    if budget is None:
        # Simple feasible solution: traverse each required edge twice
        simple_solution_cost = sum(w for _, _, w in required_edges) * 2
        budget = simple_solution_cost + random.randint(
            0, max_weight * num_optional_edges
        )

    return {
        "vertices": vertices,
        "required_edges": required_edges,
        "optional_edges": optional_edges,
        "budget": budget,
    }


def verify_solution(instance: Dict, solution: List[Tuple[int, int]]) -> bool:
    """
    Verify if a given solution is valid for the Rural Postman Problem instance.

    Args:
        instance: Dict containing the problem instance (as returned by generate_instance)
        solution: List of edges in order of traversal, each edge as (u, v)

    Returns:
        bool: True if solution is valid, False otherwise
    """
    if not solution:
        return False

    # Create dictionaries for efficient edge lookup
    required_edges = {}
    for u, v, w in instance["required_edges"]:
        required_edges[(u, v)] = w
        required_edges[(v, u)] = w  # Add both directions

    optional_edges = {}
    for u, v, w in instance["optional_edges"]:
        optional_edges[(u, v)] = w
        optional_edges[(v, u)] = w  # Add both directions

    # Check if solution forms a valid tour
    # First vertex should equal last vertex
    if solution[0][0] != solution[-1][1]:
        return False

    # Check connectivity of the tour
    for i in range(len(solution) - 1):
        if solution[i][1] != solution[i + 1][0]:
            return False

    # Check if all required edges are traversed and calculate total cost
    required_covered = set()
    total_cost = 0

    for u, v in solution:
        edge = (u, v)
        if edge in required_edges:
            required_covered.add((min(u, v), max(u, v)))  # Store undirected edge
            total_cost += required_edges[edge]
        elif edge in optional_edges:
            total_cost += optional_edges[edge]
        else:
            return False  # Used an edge that doesn't exist

    # Convert required edges to undirected format for comparison
    actual_required = {(min(u, v), max(u, v)) for u, v, _ in instance["required_edges"]}

    # Check if all required edges are covered
    if not actual_required.issubset(required_covered):
        return False

    # Check budget constraint
    if total_cost > instance["budget"]:
        return False

    return True
