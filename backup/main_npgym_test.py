from npgym import NPEnv

env = NPEnv(problem_name="3-Satisfiability (3-SAT)", level=1)

print(env.generate_instance())
