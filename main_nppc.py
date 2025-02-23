import os
import re
import json
from nppc_prompt import nppc_template, example_and_solution

models = {
    "openai/gpt-4o": "gpt-4o-2024-08-06",
    "openai/gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "openai/o1-mini": "o1-mini-2024-09-12",
    "deepseek/deepseek-chat": "deepseek/deepseek-chat",
    "claude": "anthropic/claude-3-sonnet-20240229",
}

def three_sat():
    name = "3-Satisfiability (3-SAT)"
    description = """Input: A set of m clauses - C1 ,C2,...,Cm - over a set of n Boolean valued variables Xn=<x1,x2,...,xn>, such that each clause depends on exactly three distinct variables from Xn. A clause being a Boolean expression of the form yi+yj+yk where each y is of the form x or -x (i.e. negation of x) with x being some variable in Xn. For example if n=4 and m=3 a possible instance could be the (set of) Boolean expressions: C1=(x1+(-x2)+(-x3)); C2=(x2+x3+(-x4)); C3=((-x1)+x3+x4);
Question: Can each variable xi of Xn be assigned a Boolean value alphai in such a way that every clause evaluates to the Boolean result true under the assignment < xi:=alphai:1<=i<=n>? """
    return name, description


def strip_json_comments(json_string):
    # 移除单行注释
    result = re.sub(r"//.*$", "", json_string, flags=re.MULTILINE)
    # 移除多行注释
    result = re.sub(r"/\*[\s\S]*?\*/", "", result)
    return result


def extract_json_and_answer(text):
    match = re.findall(r"```json\n(.*?)\n```", text, re.DOTALL)

    # print(match)
    if match:
        json_str = match[-1]
        try:
            # print("This is solution.")
            # print(json_str)
            json_str = strip_json_comments(json_str)

            # print("striped json str")
            # print(json_str)
            data = json.loads(json_str)

            # print(data)
            answer = data["solution"]

            print("This is answer")
            print(answer)
            return answer
        except (json.JSONDecodeError, KeyError, SyntaxError) as e:
            print(f"Error parsing JSON or answer field: {e}")
            return None
    else:
        print("No JSON found in the text.")
        return None


def save_outputs(outputs, model_inputs, filepath):
    formatted_outputs = []
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                formatted_outputs = json.load(f)
            except json.JSONDecodeError:
                formatted_outputs = []
    output_item = {"output": outputs, "model_input": model_inputs}
    formatted_outputs.append(output_item)

    with open(filepath, "w") as f:
        json.dump(formatted_outputs, f, indent=2)
    return output_item["output"]


def evaluate_llm(content, model, output_path):
    with open("api_keys/openai_api_key.txt", "r") as file:
        openai_api_key = file.read().strip()
    with open("api_keys/deepseek_api_key.txt", "r") as file:
        deepseek_api_key = file.read().strip()

    from litellm import completion

    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key

    messages = [{"content": content, "role": "user"}]
    response = completion(model=models[model], messages=messages)

    token_numbers = {
        "prompt": response.usage.prompt_tokens,
        "completion": response.usage.completion_tokens,
    }

    response = response.choices[0].message.content
    response = save_outputs(response, content, output_path)
    return response, token_numbers


def create_demo_text(n_shot, num_variables, num_clauses):
    demos = ""
    for i in range(n_shot):
        instance, solution = generate_instance(num_variables, num_clauses)
        demo = example_and_solution.replace(
            "<example_problem>", "{}".format(instance)
        ).replace("<example_solution>", json.dumps(solution))
        demos += demo
    instance, solution = generate_instance(num_variables, num_clauses)
    return demos, instance


if __name__ == "__main__":
    from npgym.npc.three_sat import generate_instance, verify_solution

    n_shot = 3
    num_variables = 10
    num_clauses = 10
    iteration = 10000
    model = "openai/gpt-4o-mini"
    output_path = model + ".json"
    problem_name, problem_description = three_sat()
    num_true = 0
    num_total = 0
    prompt_tokens = 0
    completion_tokens = 0
    token_total = 0
    for n_iter in range(iteration):
        print("=" * 15)
        print("Iteration {}".format(n_iter))
        print("=" * 15)
        content = nppc_template.replace(
            "<problem_description>", problem_description
        ).replace("<problem_name>", problem_name)
        demos, instance = create_demo_text(n_shot, num_variables, num_clauses)
        content = content.replace("<in_context_examples>", demos).replace(
            "<problem_to_solve>", "{}".format(instance)
        )

        # json_template = {"reasoning": {}, "solution": []}
        # json_template = {"solution": []}
        # json_str = json.dumps(json_template, indent=4)
        # content = content.replace("<json_template>", json_str)

        print("### Content ###")
        print(content)
        try:
            response, token_numbers = evaluate_llm(
                content, model, output_path=output_path
            )
            # print(content)
            print("### Response ###")
            print(response)
            cleaned_response = extract_json_and_answer(response)

            prompt_tokens = token_numbers["prompt"]
            completion_tokens = token_numbers["completion"]
            if cleaned_response is not None:
                # result = ast.literal_eval(results)
                # print("verify")
                # print(instance)
                # print(cleaned_response)
                results = verify_solution(instance, cleaned_response)
                print(results)
                if results[0]:
                    num_true = num_true + 1
            else:
                print("Wrong Format")
            num_total = num_total + 1
            token_total = token_total + completion_tokens
            print("=" * 50)
            print(
                "Accuracy = {}, True = {}, Total = {}".format(
                    num_true / num_total, num_true, num_total
                )
            )
            # print(token_numbers)
            print(
                f"prompt tokens: {prompt_tokens} / completion tokens: {completion_tokens} / total tokens: {token_total}"
            )
            print("=" * 50)
            if num_total == 50:
                break

        except Exception as e:
            print(f"Error calling API: {e}")
