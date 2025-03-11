import random


def generate_instance(num_elements):
    # elements = list(range(num_elements))

    # 用enumerate创建(索引,值)对的列表
    indexed = list(enumerate(range(num_elements)))
    # 随机打乱
    random.shuffle(indexed)
    # 解压缩得到打乱后的列表和对应的原始索引
    indices, shuffled = zip(*indexed)

    length = random.randint(num_elements // 4, num_elements // 2)

    product_value = 1

    for i in range(length):
        product_value *= shuffled[i]

    instance = {"elements": list(range(num_elements)), "K": product_value}

    return instance, indices[:length]


def verify_solution(instance, solution):
    elements = instance["elements"]
    if (
        (not (0 < len(solution) < len(elements)))
        and (max(solution) < len(elements) and min(solution) >= 0)
        and (len(set(solution)) == len(solution))
    ):
        return False, "The solution is not valid."

    product_value = 1

    for idx in solution:
        product_value *= elements[idx]

    if product_value == instance["K"]:
        return True, "Correct solution."
    else:
        return False, "The solution is not correct."


# instance, solution = generate_instance(num_elements=20)
#
# solution = list(solution) + [6]
# print(solution)
#
# print(verify_solution(instance, solution))
