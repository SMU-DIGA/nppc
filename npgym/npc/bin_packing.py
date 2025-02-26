import random


def generate_instance(num_items: int, bin_capacity: int, num_bins: int):
    # 生成随机物品大小
    U = [random.randint(1, bin_capacity) for _ in range(num_items)]

    # 使用贪心算法（首次适应算法）分配物品到箱子中
    solution = [[] for _ in range(num_bins)]
    for item in U:
        # 尝试将物品放入第一个能容纳它的箱子
        placed = False
        for bin_items in solution:
            if sum(bin_items) + item <= bin_capacity:
                bin_items.append(item)
                placed = True
                break
        if not placed:
            # 如果没有箱子能容纳该物品，则无法生成有效解
            # 重新生成实例
            return generate_instance(num_items, bin_capacity, num_bins)

    # 返回生成的实例和有效解
    instance = {"U": U, "B": bin_capacity, "K": num_bins}
    return instance, solution


def verify_solution(instance, solution):
    U = instance["U"]
    B = instance["B"]
    K = instance["K"]

    # 检查解是否包含所有物品且不重复
    all_items = []

    for bin_items in solution:
        all_items.extend(bin_items)

    # 检查物品是否一致（包括重复物品）
    if sorted(all_items) != sorted(U):
        return False, f"Items are inconsistent."

    # 检查每个箱子的总大小是否不超过 B
    for bin_items in solution:
        if sum(bin_items) > B:
            return False, f"The total size exceeds B."

    return True, f"Valid bin packing."


# 示例用法
num_items = 10
bin_capacity = 20
num_bins = 3
instance, solution = generate_instance(num_items, bin_capacity, num_bins)
print("Instance:", instance)
print("Solution:", solution)
result = verify_solution(instance, solution)
print(result)
