import random
import string

def generate_instance(n: int, k: int):
    # 生成随机字符串集合 R
    R = []
    for _ in range(n):
        # 随机生成字符串长度，确保总长度不超过 k
        max_len = min(10, k)  # 每个字符串的最大长度
        min_len = 1
        length = random.randint(min_len, max_len)
        s = ''.join(random.choices(string.ascii_lowercase, k=length))
        # s = generate_random_string(1, max_len)
        R.append(s)

    # 构造有效解 w
    # 将所有字符串按顺序连接起来，确保总长度不超过 k
    w = ''.join(R)
    while len(w) > k:
        # 如果 w 的长度超过 k，则缩短 w
        # 随机删除一个字符
        idx = random.randint(0, len(w) - 1)
        w = w[:idx] + w[idx + 1:]

    # 确保 R 中的每个字符串都是 w 的子串
    for s in R:
        if s not in w:
            # 如果某个字符串不是 w 的子串，则重新生成 w
            # 将该字符串插入到 w 的随机位置
            idx = random.randint(0, len(w))
            w = w[:idx] + s + w[idx:]
            # 如果 w 的长度超过 k，则缩短 w
            while len(w) > k:
                idx = random.randint(0, len(w) - 1)
                w = w[:idx] + w[idx + 1:]

    # 返回生成的实例和有效解
    instance = {
        'Strings': R,
        'K': k
    }
    return instance, w


def verify_solution(instance, solution: str):
    """
    Verify if a given solution is valid for the Shortest Common Superstring instance.


    Returns:
        bool indicating whether solution is valid
    """
    # Check if solution length is at most k
    k = instance["K"]
    strings = instance["Strings"]
    if len(solution) > k:
        return False, "The solution is invalid."

    # Check if each input string is a substring of the solution
    for s in strings:
        if s not in solution:
            return False, "Some string is not the substring of the solution"

    return True, "Correct solution."


instance, solution = generate_instance(n=5, k=10)
print(instance)
print(solution)

print(verify_solution(instance, solution))
