import random
from copy import deepcopy


def generate_instance(num_elements: int, num_sets: int, k: int):
    # 生成集合 S
    S = list(range(0, num_elements))  # 元素为 1, 2, ..., num_elements
    # 生成子集集合 C
    C = []

    random.shuffle(S)
    indices = list(range(1, num_elements - 2))
    random.shuffle(indices)
    indices = [0] + sorted(indices[: k - 1]) + [num_elements]
    for idx in range(1, k + 1):
        C.append(deepcopy(sorted(S[indices[idx - 1]: indices[idx]])))

    for _ in range(k, num_sets):
        subset_size = random.randint(1, num_elements)  # 子集大小随机
        subset = list(random.sample(sorted(S), subset_size))
        C.append(deepcopy(subset))

    shuffle_subset = list(range(num_sets))
    random.shuffle(shuffle_subset)

    dict_c = {}
    solution = []
    for i in range(num_sets):
        dict_c[i] = C[shuffle_subset[i]]
        if shuffle_subset[i] < k:
            solution.append(i)

    # 返回生成的实例和有效解
    instance = {"universe": S, "subsets": dict_c, "k": k}

    return instance, solution


def verify_solution(instance, solution):
    S = instance["universe"]
    C = instance["subsets"]
    k = instance["k"]

    # 检查解的大小是否不超过 k
    if len(solution) > k:
        return False, "The number of subsets in the solution exceeds k"

    # 检查解是否覆盖 S
    covered = set()
    for i in solution:
        covered.update(C[i])
    if covered >= set(S):
        return True, "Valid solution"
    else:
        return False, "The solution does not cover S"


instance, solution = generate_instance(num_elements=20, num_sets=20, k=5)
is_valid = verify_solution(instance, solution)
print("Is the solution valid?", is_valid)
