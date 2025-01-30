import random


def generate_instance(n: int, k: int, min_len: int = 5, max_len: int = 10):
    """
    Generate an instance of the Shortest Common Superstring decision problem.

    Args:
        n: Number of strings to generate
        min_len: Minimum length of each string
        max_len: Maximum length of each string
        k: Target length for the superstring

    Returns:
        tuple of (list of strings, target length k)
    """

    import string

    if k < max_len:
        raise "k should be larger than max_len"
    # Generate base string that will ensure at least one solution exists
    base_len = random.randint(k - max_len, k)
    base = "".join(random.choices(string.ascii_lowercase, k=base_len))

    # Generate n strings that are substrings of base
    strings = []
    for _ in range(n):
        # Random length between min_len and max_len
        length = random.randint(min_len, max_len)
        # Random starting position in base string
        if len(base) < length:
            start = 0
        else:
            start = random.randint(0, len(base) - length)
        # Extract substring
        substring = base[start : start + length]
        strings.append(substring)

    # Shuffle the strings
    random.shuffle(strings)

    instance = {"strings": strings, "k": k}

    return instance, base


def verify_solution(instance, solution: str):
    """
    Verify if a given solution is valid for the Shortest Common Superstring instance.


    Returns:
        bool indicating whether solution is valid
    """
    # Check if solution length is at most k
    k = instance["k"]
    strings = instance["strings"]
    if len(solution) > k:
        return False, "The solution is invalid."

    # Check if each input string is a substring of the solution
    for s in strings:
        if s not in solution:
            return False, "Some string is not the substring of the solution"

    return True, "Correct solution."


instance, solution = generate_instance(n=20, k=15)

print(verify_solution(instance, solution))
