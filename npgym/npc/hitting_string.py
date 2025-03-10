import random
from typing import Set


def generate_instance(n: int, m: int):
    # 首先生成一个解（保证实例有解）
    solution = "".join(random.choice(["0", "1"]) for _ in range(n))

    def generate_string() -> str:
        """生成一个与solution至少在一个位置匹配的字符串"""
        # 选择一个匹配位置
        match_pos = random.randint(0, n - 1)

        # 初始化为全*
        s = ["*"] * n

        # 在匹配位置放入与solution相同的字符
        s[match_pos] = solution[match_pos]

        # 随机填充一些其他位置（确保字符串不会太稀疏）
        num_deterministic = random.randint(1, n // 2)  # 至少1个，最多n/2个确定字符
        positions = random.sample(
            [i for i in range(n) if i != match_pos], min(num_deterministic, n - 1)
        )

        for pos in positions:
            s[pos] = random.choice(["0", "1"])

        return "".join(s)

    # 生成m个不同的字符串
    strings: Set[str] = set()
    while len(strings) < m:
        strings.add(generate_string())

    instance = sorted(list(strings))
    return instance, solution


def verify_solution(instance, solution: str):
    """
    验证解的正确性
    """

    if len(solution) != len(instance[0]):
        return False, "The solution is not valid."
    for s in instance:
        # 检查是否至少有一个位置匹配
        match_found = False
        for i, (c1, c2) in enumerate(zip(s, solution)):
            if c1 != "*" and c1 == c2:
                match_found = True
                break
        if not match_found:
            return False, "Not all strings match."
    return True, "Correct solution."


instance, solution = generate_instance(n=5, m=10)
print(instance)
# print(
#     solution
# )
#
# solution = list(solution)
# solution[-1] = '0'
#
# solution = ''.join(solution)
#
print(solution)
#
#
# print(
#     verify_solution(instance, solution)
# )
