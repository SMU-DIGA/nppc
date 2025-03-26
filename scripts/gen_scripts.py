seed_list = [42, 53, 64]
model_list = ["deepseek-v3", "deepseek-r1", "gpt-4o", "gpt-4o-mini", "claude"]

problem_list = [16]
# problem_list = [12]

for model in model_list:
    filename = "run_{}.sh".format(model)
    pare_folder = "./logs"

    f = open(file=filename, mode="w")
    f.write("mkdir -p {}\n\n".format(pare_folder))
    for problem in problem_list:
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

            f.write("nohup python3 -u main_nppc_final.py ")
            f.write(config)
            f.write(" > " + pare_folder)
            f.write("/log_" + config_l + ".txt")
            f.write("&\n")
        # f.write("wait\n\n")
