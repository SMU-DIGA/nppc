nppc_template = """
# Problem Description
<problem_description>

# Examples
<in_context_examples>
# Problem to Solve 
Problem: <problem_to_solve>

# Instruction
Please reason step by step, and put your final solution in the "solution" field in the following json format and of the same format as the example solutions.
```json
{
    "solution": "___"
}
```
"""

nppc_template_deepseek = """
# Problem Description
<problem_description>

# Examples
<in_context_examples>
# Problem to Solve 
Problem: <problem_to_solve>

# Instruction
A conversation between User and Assistant. The user asks a question, and the Assistant solves it.
The assistant first thinks about the reasoning process in the mind and then provides the user with the solution. The reasoning process and solution are enclosed within <think> </think> and <solution> </solution> tags, respectively, i.e., <think> reasoning process here </think>
<solution>solution here</solution>.
Do not explain your reasoning inside the solution tags, provide only the final solution. When an example is provided, you should strictly follow the format of the output/solution in that example.
"""

example_and_solution = """Problem: <example_problem>
Solution:
{
    "solution": <example_solution>
}
"""

example_and_solution_run = """
# Example Problem

<example_problem>

# Answer to the Example Problem

{
    "solution": <example_solution>
}
"""