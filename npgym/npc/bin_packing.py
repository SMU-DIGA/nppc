import random

import numpy as np


def generate_instance(num_items: int, bin_capacity: int, num_bins: int):
    remaining = [bin_capacity] * num_bins
    mask = [False] * num_bins
    num_items_for_bins = [0] * num_bins

    def softmax(x, mask=None):
        """
        计算softmax值

        参数:
        x -- 输入数组/列表

        返回:
        归一化的概率分布（softmax结果）
        """
        # 为了数值稳定性，减去最大值
        x_np = np.array(x, dtype=np.float64)

        if mask is not None:
            # 将被屏蔽的位置设为非常小的值(负无穷)，这样exp后接近0
            x_np = np.where(mask, -np.inf, x_np)
        valid_max = np.max(x_np[x_np != -np.inf])
        x_shifted = x_np - valid_max
        # 计算指数
        exp_x = np.exp(x_shifted)
        # 归一化
        return exp_x / np.sum(exp_x)

    # assign items for bins
    for n_item in range(num_items):
        probs = softmax(remaining, mask)

        # 根据概率分布采样一个索引
        sampled_index = np.random.choice(range(num_bins), p=probs)

        num_items_for_bins[sampled_index] += 1
        remaining[sampled_index] -= 1
        if remaining[sampled_index] == 0:
            mask[sampled_index] = True

    item_weights = []
    item_to_bin = []
    for n_bin in range(num_bins):
        remaining_weight = bin_capacity
        for n_item in range(num_items_for_bins[n_bin]):
            item_weight = random.randint(
                1, remaining_weight - (num_items_for_bins[n_bin] - n_item + 1)
            )
            remaining_weight -= item_weight
            item_weights.append(item_weight)
            item_to_bin.append(n_bin)

    zipped_items = list(zip(item_to_bin, item_weights))
    random.shuffle(zipped_items)

    instance = {
        "bins": [i for i in range(num_bins)],
        "bin_capacity": bin_capacity,
        "item_weights": [zipped_item[1] for zipped_item in zipped_items],
    }

    solution = [zipped_item[0] for zipped_item in zipped_items]
    return instance, solution


def verify_solution(instance, solution):
    num_bins = len(instance["bins"])
    item_weights = instance["item_weights"]
    bin_capacity = instance["bin_capacity"]

    try:
        if len(solution) != len(item_weights):
            return False, "BIN PACKING ERROR 1: The solution is not valid."

        if max(solution) > num_bins - 1:
            return False, "BIN PACKING ERROR 2: No this bin."

        bin_weights = [0] * num_bins

        for idx, bin_idx in enumerate(solution):
            bin_weights[bin_idx] += item_weights[idx]

        if max(bin_weights) > bin_capacity:
            return False, f"BIN PACKING ERROR 3: The total size exceeds B."

        return True, "Correct solution."

    except:
        return False, "VERIFICATION: Verification error."


def test():
    # 示例用法
    num_items = 10
    bin_capacity = 20
    num_bins = 3
    instance, solution = generate_instance(num_items, bin_capacity, num_bins)
    print("Instance:", instance)
    print("Solution:", solution)
    # solution = [0, 1, 1, 2, 2, 2 , 2 , 2, 2, 3]
    result = verify_solution(instance, solution)
    print(result)
