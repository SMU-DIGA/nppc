import random


def generate_instance(m, B):
    elements = []

    lower_bound = B // 4
    upper_bound = B // 2

    for i in range(m):
        ele1 = random.randint(lower_bound, upper_bound)
        ele2 = random.randint(lower_bound, upper_bound)

        ele3 = B - ele1 - ele2

        elements += [ele1, ele2, ele3]

    # 用enumerate创建(索引,值)对的列表
    indexed = list(enumerate(elements))
    # 随机打乱
    random.shuffle(indexed)
    # 解压缩得到打乱后的列表和对应的原始索引
    indices, shuffled = zip(*indexed)

    solution = [[] for _ in range(m)]

    for i in range(len(indices)):
        solution[indices[i] // 3].append(i)

    elements_perm = [0] * (3 * m)

    for i in range(len(elements_perm)):
        elements_perm[i] = shuffled[i]

    instance = {"elements": elements_perm, "m": m, "B": B}

    return instance, solution


def verify_solution(instance, solution):
    elements = instance["elements"]
    m = instance["m"]
    B = instance["B"]

    for sol in solution:
        if len(sol) != 3:
            return False, "The solution is invalid."

        if not (max(sol) < len(elements) and min(sol) >= 0):
            return False, "The solution is invalid."

        if not (elements[sol[0]] + elements[sol[1]] + elements[sol[2]] == B):
            return False, "The solution is not correct."
    else:
        return True, "Correct solution."


instance, solution = generate_instance(m=2, B=30)
print(instance)
print(solution)
print(verify_solution(instance, solution))
