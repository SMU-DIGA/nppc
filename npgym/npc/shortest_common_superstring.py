import random
import string


def generate_instance(n: int, k: int):
    """生成 Shortest Common Superstring 实例和优化后的解 w"""

    # 生成随机字符串 w，长度为 k
    def generate_random_string(length: int):
        """生成一个指定长度的随机字符串"""
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    w = generate_random_string(k)

    # 从 w 中提取 n 个子串作为 R
    R = []
    for _ in range(n):
        # 随机选择子串的起始和结束位置
        start = random.randint(0, k - 1)
        end = random.randint(start + 1, k)
        s = w[start:end]
        R.append(s)

    # 优化 w 的长度
    def optimize_w(w: str, R: list):
        """优化 w 的长度，删除未被 R 中子串覆盖的字符"""
        # 标记 w 中哪些字符被 R 的子串覆盖
        marked = [False] * len(w)
        for s in R:
            start = w.find(s)  # 找到子串 s 在 w 中的起始位置
            if start != -1:
                for i in range(start, start + len(s)):
                    marked[i] = True

        # 构建优化后的 w，只保留被标记的字符
        optimized_w = ''.join([w[i] for i in range(len(w)) if marked[i]])
        return optimized_w

    # 优化 w
    optimized_w = optimize_w(w, R)

    # 返回生成的实例和优化后的解
    instance = {
        'Strings': R,
        'K': k
    }
    return instance, optimized_w

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

# 示例用法
n = 5
k = 20
instance, solution = generate_instance(n, k)
print("Instance:", instance)
print("Solution:", solution)
print(verify_solution(instance, solution))
