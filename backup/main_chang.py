import random
import re
import ast

models = {
    "openai/gpt-4o": "gpt-4o-2024-08-06",
    "openai/gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "openai/o1-mini": "o1-mini-2024-09-12",
    "deepseek/deepseek-chat": "deepseek/deepseek-chat",
}


def evaluate_llm(content, model):
    with open("../api_keys/openai_api_key.txt", "r") as file:
        openai_api_key = file.read().strip()
    with open("../api_keys/deepseek_api_key.txt", "r") as file:
        deepseek_api_key = file.read().strip()

    from litellm import completion
    import os

    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key

    messages = [{"content": content, "role": "user"}]
    response = completion(model=models[model], messages=messages)
    # print(response)
    token_numbers = {
        "prompt": response.usage.prompt_tokens,
        "completion": response.usage.completion_tokens,
    }

    response = response.choices[0].message.content
    return response, token_numbers


def create_demo_text(n_shot, num_variables, num_clauses):
    demos = ""
    for i in range(n_shot):
        instance, solution = generate_instance(num_variables, num_clauses)
        demos += "Problem: {}".format(instance) + "\n"
        demos += "Solution: {}".format(solution) + "\n"
    instance, solution = generate_instance(num_variables, num_clauses)
    demos += "Problem: {}\n".format(instance)
    demos += "Solution: \n"
    return demos, instance


def build_prompt(problem, description):
    content = "This is a {} problem. Here is the problem description: \n".format(
        problem
    )
    content = content + description
    content += (
        "\nGive me the final solution in <solution> XXX </solution> format, "
        "where XXX should be the same format as the solutions in the examples.\n"
    )
    # content += "Here are some demo examples: \n"
    return content


if __name__ == "__main__":
    problem = "3-Satisfiability (3-SAT)"
    from npgym.npc.three_sat import generate_instance, verify_solution

    n_shot = 3
    num_variables = 5
    num_clauses = 5
    iteration = 50
    model = "openai/gpt-4o-mini"
    description = """Input: A set of m clauses - C1 ,C2,...,Cm - over a set of n Boolean valued variables Xn=< x1,x2,...,xn>, such that each clause depends on exactly three distinct variables from Xn. A clause being a Boolean expression of the form yi+yj+yk where each y is of the form x or -x (i.e. negation of x) with x being some variable in Xn. For example if n=4 and m=3 a possible instance could be the (set of) Boolean expressions: C1=(x1+(-x2)+(-x3)); C2=(x2+x3+(-x4)); C3=((-x1)+x3+x4);
Question: Can each variable xi of Xn be assigned a Boolean value alphai in such a way that every clause evaluates to the Boolean result true under the assignment < xi:=alphai:1<=i<=n>? """

    num = 0
    prompt_tokens = 0
    completion_tokens = 0
    for n_iter in range(iteration):
        print("=" * 30)
        print("Iteration {}".format(n_iter))
        print("=" * 30)

        content = build_prompt(problem, description)
        demos, instance = create_demo_text(n_shot, num_variables, num_clauses)
        content = content + demos
        print("######## Content ########")
        print(content)

        try:
            response, token_numbers = evaluate_llm(content, model)

            prompt_tokens = token_numbers["prompt"]
            completion_tokens = token_numbers["completion"]
            pattern = r"<solution>\s*(\[.*?\])\s*</solution>"
            match = re.search(pattern, response)
            if match:
                results = match.group(1)
            else:
                results = None

            print("######## Results ########")
            print(results)
            if results is not None:
                result = ast.literal_eval(results)
                result = verify_solution(instance, result)
                print(result)
                if result[0]:
                    num = num + 1
            else:
                print("Wrong Format")
            print("=" * 30)
            print("Accuracy = {}".format(num / (n_iter + 1)))
            print(token_numbers)
            print(
                f"prompt tokens: {prompt_tokens} / completion tokens: {completion_tokens}"
            )
            print("=" * 30)

        except Exception as e:
            print(f"Error calling API: {e}")
        # print("######## Response ########")
        # print(response)
