import random
from typing import List


def format_instance(clauses: List[List[int]]) -> str:
    """
    将3SAT实例格式化为易读的字符串

    Args:
        clauses (List[List[int]]): 3SAT实例

    Returns:
        str: 格式化后的字符串
    """
    formula = []
    for clause in clauses:
        literals = []
        for lit in clause:
            if lit > 0:
                literals.append(f"x{lit}")
            else:
                literals.append(f"¬x{abs(lit)}")
        formula.append(f"({' ∨ '.join(literals)})")
    return " ∧ ".join(formula)


def generate_instance(num_variables, num_clauses):
    """

    :param num_variables:
    :param num_clauses:
    :return:
    """

    # This also ensure that every generated instance has at least one solution
    solution = [random.choice([True, False]) for _ in range(1, num_variables + 1)]
    clauses = []
    for _ in range(num_clauses):
        vars_in_clause = random.sample([i for i in range(1, num_variables + 1)], 3)
        clause = []
        # 随机决定前两个文字是否取反
        for var in vars_in_clause[:2]:
            negated = random.choice([True, False])
            clause.append((var, negated))

        # 最后一个文字确保整个子句在solution下为True
        last_var = vars_in_clause[2]
        # 检查前两个文字在solution下是否都为False
        if all(not (solution[var - 1] ^ negated) for var, negated in clause):
            # 如果都为False，确保最后一个文字为True
            negated = not solution[last_var - 1]
        else:
            # 否则随机取反
            negated = random.choice([True, False])
        clause.append((last_var, negated))
        clauses.append(tuple([(-var if negated else var) for var, negated in clause]))

    instance = {"variables": [i + 1 for i in range(num_variables)], "clauses": clauses}
    return instance, solution


def verify_solution(instance, solution):
    if type(instance) is tuple:
        instance = instance[0]
    num_variables = len(instance["variables"])
    clauses = instance["clauses"]

    try:
        if num_variables != len(solution):
            return False, "Ths solution is not valid."

        unsatisfied_clauses = []

        # 检查每个子句
        for i, clause in enumerate(clauses):
            clause_satisfied = False
            for literal in clause:
                var = abs(literal)
                if (literal > 0 and solution[var - 1]) or (
                    literal < 0 and not solution[var - 1]
                ):
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                unsatisfied_clauses.append(i)

        if len(unsatisfied_clauses) == 0:
            return True, "Correct solution."
        else:
            return (
                False,
                f"The following clauses are not satisfied: {unsatisfied_clauses}.",
            )
    except:
        return False, "verification error"


# 生成实例
# instance, solution = generate_instance(3, 3)
# print("generate 3sat instances：")
# print(instance)
# print(solution)

# 创建一个解（所有变量都设为True）
# solution = {i: True for i in range(1, 21)}
# print("\n test solution：", solution)

# instance = {'variables': [1, 2, 3], 'clauses': [(2, 1, 3), (-2, 1, -3), (-2, 3, 1)]}
#
# solution = [True, True, False]
#
# # 验证解
# result = verify_solution(instance, solution)
# print(result)
