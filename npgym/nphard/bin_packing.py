import random


def generate_bin_packing_instance(
        num_items: int, bin_capacity: int, min_size: int = 1, max_size: int = None
):
    """生成装箱问题实例"""
    if max_size is None:
        max_size = bin_capacity

    items = [random.randint(min_size, max_size) for _ in range(num_items)]
    return items, bin_capacity


def verify_bin_packing(items: list, bin_capacity: int, solution: list):
    """验证装箱方案是否可行

    Args:
        items: 物品大小列表
        bin_capacity: 箱子容量
        solution: 分配方案，solution[i]表示第i个物品被分配到的箱子编号
    """
    if len(items) != len(solution):
        return False, "the items in solutions is not the same with items"

    # 计算每个箱子的使用情况
    bins = {}
    for item_idx, bin_idx in enumerate(solution):
        bins[bin_idx] = bins.get(bin_idx, 0) + items[item_idx]

        if bins[bin_idx] > bin_capacity:
            return (
                False,
                f"box {bin_idx} exceed the capacity: {bins[bin_idx]} > {bin_capacity}",
            )

    return True, f"correct solution，use {len(bins)} box"


# 使用示例
# 生成实例：10个物品，箱子容量为10
items, capacity = generate_bin_packing_instance(10, 10, min_size=1, max_size=7)
print("物品大小:", items)
print("箱子容量:", capacity)

# 验证解：分配方案中的数字表示箱子编号

solution = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]  # 每两个物品放一个箱子
is_valid, message = verify_bin_packing(items, capacity, solution)
print("验证结果:", message)
