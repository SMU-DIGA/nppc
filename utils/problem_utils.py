import importlib

def load_np_problem(problem_name):
    """
    Dynamically loads a problem environment from `gym.npc` based on the problem name.

    Args:
        problem_name (str): The problem name (e.g., "3-Satisfiability (3-SAT)")

    Returns:
        generate_instance (function): Function to generate problem instances.
        verify_solution (function): Function to verify solutions.
    """
    module_name = problem_name  # Get the corresponding module name
    try:
        problem_module = importlib.import_module(f"npgym.npc.{module_name}")
        generate_instance = getattr(problem_module, "generate_instance")
        verify_solution = getattr(problem_module, "verify_solution")
        return generate_instance, verify_solution
    except ImportError as e:
        raise ImportError(f"Could not import module '{module_name}': {e}")
    except AttributeError as e:
        raise AttributeError(f"Module '{module_name}' does not contain the required functions: {e}")