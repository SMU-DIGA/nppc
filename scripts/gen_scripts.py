seed_list = [42, 53, 64]
model_list = ["o3-mini"]

problem_list = [0, 1, 8, 9, 11, 12, 15, 16, 19, 22, 23, 24]
problem_list = [11]

for model in model_list:
    filename = "run_{}.sh".format(model)
    pare_folder = "./logs"

    f = open(file=filename, mode="w")
    f.write("mkdir -p {}\n\n".format(pare_folder))
    for p_idx, problem in enumerate(problem_list):
        # if model == "deepseek-v3" and problem not in [12]:
        #     continue
        # if model == "deepseek-r1" and problem not in [9]:
        #     continue
        for seed in seed_list:
            config = ""
            config += "--model {} ".format(model)
            config += "--problem {} ".format(problem)
            config += "--seed {} ".format(seed)

            config_l = ""
            config_l += "model_{}_".format(model)
            config_l += "problem_{}_".format(problem)
            config_l += "seed_{}_".format(seed)

            f.write("nohup python3 -u main_nppc_final_v3.py ")
            f.write(config)
            f.write(" > " + pare_folder)
            f.write("/log_" + config_l + ".txt")
            f.write("&\n")
        if (p_idx + 1) % 4 == 0:
            f.write("wait\n\n")
