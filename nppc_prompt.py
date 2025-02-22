nppc_template = """
# <problem_name> Problem Description:
<problem_description>

# Examples:
<in_context_examples>
# Problem to Solve: 
Problem: <problem_to_solve>

# Instruction:
Now please solve the above problem. Reason step by step and present your answer in the "solution" field in the following json format:
```json
{"solution": "___" }
```

"""

example_and_solution = """Problem: <example_problem>
{"solution": <example_solution>}
"""

example_and_solution_run = """
# Example Problem

<example_problem>

# Answer to the Example Problem

{
    "solution": <example_solution>
}
"""
