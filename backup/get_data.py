import numpy as np
import pickle


def get_data_with_try(problem, levels, model):
    seeds = [42, 53, 64]
    results = {}
    min_len = len(levels)

    model_to_file = {
        "qwq-32b": "qwq",
        "deepseek-r1-32b": "deepseek-r1-32",
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4o": "gpt-4o",
        "claude": "claude",
        "deepseek-v3": "deepseek-v3",
        "deepseek-r1": "deepseek-r1",
        "o1-mini": "o1-mini",
    }

    for seed in seeds:
        results[seed] = []

        for level in levels:
            try:
                f = open(
                    "../results/{}/{}/model_{}_problem_{}_level_{}_shots_1_seed_{}.pkl".format(
                        problem,
                        model_to_file[model],
                        model_to_file[model],
                        problem,
                        level,
                        seed,
                    ),
                    "rb",
                )
                data = pickle.load(f)
                true_num = 0
                for i in range(30):
                    # if model == 'gpt-4o':
                    #     print(data[level][i]["instance"])
                    if data[level][i]["correctness"]:
                        true_num = true_num + 1
                # print("level {}, accuracy = {}".format(level, true_num / 30))
                results[seed].append(true_num / 30)
            except:
                min_len = min(min_len, len(results[seed]))
                break
        # print(seed_result)
    if min_len > 0:
        results = np.array([results[seed][:min_len] for seed in seeds]).reshape(
            3, 1, min_len
        )
        return results

    return None
