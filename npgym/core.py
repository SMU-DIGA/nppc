import importlib
import os
import sys

from .configs import PROBLEM_LEVELS, PROBLEM2PATH


class NPEnv:
    def __init__(self, problem_name, level):
        self.problem_name = problem_name
        self.level = level

        assert self.level in PROBLEM_LEVELS[self.problem_name]

        self.configs = PROBLEM_LEVELS[self.problem_name][level]
        self._generate_instance, self._verify_solution = self._get_instance_generator()

    def _get_instance_generator(self):
        np_gym_folder = "./npgym/npc"

        if os.path.dirname(np_gym_folder) not in sys.path:
            sys.path.append(np_gym_folder)
        problem_path = PROBLEM2PATH[self.problem_name]
        generate_instance = importlib.import_module(problem_path).generate_instance
        verify_solution = importlib.import_module(problem_path).verify_solution

        return generate_instance, verify_solution

    def generate_instance(self):
        instance, solution = self._generate_instance(**self.configs)
        return instance, solution

    def verify_solution(self, instance, solution):
        return self._verify_solution(instance, solution)

    def batch_generate_instance(self, number):
        instances = []
        for _ in range(number):
            instance, solution = self._generate_instance(**self.configs)
            instances.append((instance, solution))

        return instances

    def batch_verify_solution(self, instances, solutions):
        verified_results = []
        assert len(instances) == len(solutions)

        for idx in range(len(instances)):
            if solutions[idx] is None:
                verified_results.append((False, "The solution is None"))
            else:
                verified_results.append(
                    self._verify_solution(instances[idx], solutions[idx])
                )

        return verified_results
