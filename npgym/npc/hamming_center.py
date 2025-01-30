import random


def generate_instance(n=8, k=3, r=2):
    """
    Generate a solvable instance of the Hamming Centre problem.

    Parameters:
    - n: length of binary strings
    - k: number of strings in set S
    - r: maximum allowed Hamming distance

    Returns:
    - tuple (S, r) where:
        S: list of k binary strings of length n
        r: maximum allowed Hamming distance
    """
    # First generate a solution y to ensure instance is solvable
    y = ''.join(random.choice('01') for _ in range(n))

    # Generate k strings with Hamming distance at most r from y
    S = []
    for _ in range(k):
        x = list(y)
        # Randomly flip up to r bits
        num_flips = random.randint(0, r)
        flip_positions = random.sample(range(n), num_flips)

        for pos in flip_positions:
            x[pos] = '1' if x[pos] == '0' else '0'

        S.append(''.join(x))

    instance = {
        'S': S,
        'r': r
    }
    return instance, y


def verify_solution(instance, y):
    """
    Verify if string y is a valid Hamming Centre for the given instance.

    Parameters:
    - instance: tuple (S, r) where:
        S: list of binary strings
        r: maximum allowed Hamming distance
    - y: proposed solution (binary string)

    Returns:
    - tuple (is_valid, violations) where:
        is_valid: boolean indicating if y is a valid solution
        violations: list of indices in S where Hamming distance exceeds r
    """
    S, r = instance['S'], instance['r']

    # Check if y has the correct length
    if len(y) != len(S[0]):
        return False, 'The length is not correct.'

    # Check if y is a binary string
    if not all(bit in '01' for bit in y):
        return False, 'The solution is not binary.'

    violations = []

    # Check Hamming distance for each string in S
    for i, x in enumerate(S):
        distance = sum(a != b for a, b in zip(x, y))
        if distance > r:
            violations.append(i)

    if len(violations) == 0:
        return True, 'Correct solution.'
    else:
        return False, 'Some string is violated.'


instance, solution = generate_instance()

print(instance)
print(solution)
