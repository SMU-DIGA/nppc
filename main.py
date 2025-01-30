import os


npc_problems = os.listdir("./npgym/npc")

problem_idx = 0
for p in npc_problems:
    if 'init' in p or 'pycache' in p:
        continue
    else:
        print(f'{problem_idx}: {p}')
        problem_idx += 1