import ast
import json

from backup.utils.problem_utils import load_np_problem


def extract_answers(json_file, instance):
    with open(json_file, "r") as file:
        data = json.load(file)

    num_corrected = 0
    num_total = 0
    num_json = 0
    num_list = 0
    for entry in data:
        try:
            output_text = entry.get("output", [""])[0]
            json_start = output_text.find("{")
            json_end = output_text.rfind("}")
            num_total += 1
            if json_start != -1 and json_end != -1:
                extracted_json = json.loads(output_text[json_start : json_end + 1])
                num_json += 1
                if "solution" in extracted_json:
                    answer_str = extracted_json["solution"]
                    if (
                        isinstance(answer_str, str)
                        and answer_str.startswith("[")
                        and answer_str.endswith("]")
                    ):
                        answer = ast.literal_eval(answer_str)
                        results = verify_solution(instance, answer)
                        num_list += 1
                        if results[0]:
                            num_corrected += 1
                    if isinstance(answer_str, list):
                        results = verify_solution(instance, answer_str)
                        num_list += 1
                        if results[0]:
                            num_corrected += 1
        except json.JSONDecodeError:
            print("Error decoding JSON in one of the entries.")
    print(num_json, num_list, num_corrected, num_total)
    return num_corrected / num_total


# Example usage
files = [5]
answers_list = []
for i in files:
    json_file = f"experiments/deepseek/three_sat/3_shot_nppc_prompt_math/3_shot_{i}_var_{i}_clause.json"  # Replace with your actual JSON file name
    problem_name = "three_sat"
    model_name = "deepseek"
    generate_instance, verify_solution = load_np_problem(problem_name)
    instance, solution = generate_instance(i, i)
    answer = extract_answers(json_file, instance)
    answers_list.append(answer)
print(files)
print(answers_list)
