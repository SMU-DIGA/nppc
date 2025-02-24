import os
import torch
import re
import ast
import json
import numpy as np
from vllm import LLM, SamplingParams
from huggingface_hub import snapshot_download

from utils.out_utils import save_outputs, clear_output, extract_json_and_answer
from utils.problem_utils import load_np_problem
from templates.nppc_prompt import nppc_template, example_and_solution, nppc_template_deepseek
from templates.OEQA import OEQA

MODELS = {
    "qwen": "Qwen/Qwen-7B-Chat",
    "llama": "meta-llama/Llama-2-7B-chat-hf",
    "mixtral": "mistralai/Mixtral-8x7B",
    "qwq": "Qwen/QwQ-32B-Preview",
    "deepseek": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    
}

PROBLEM_SHEET = {
            "three_sat": 
            {
            "full_name": "3-Satisfiability (3-SAT)", 
            "description": """Input: A set of m clauses - C1 ,C2,...,Cm - over a set of n Boolean valued variables Xn=< x1,x2,...,xn>, such that each clause depends on exactly three distinct variables from Xn. A clause being a Boolean expression of the form yi+yj+yk where each y is of the form x or -x (i.e. negation of x) with x being some variable in Xn. For example if n=4 and m=3 a possible instance could be the (set of) Boolean expressions: C1=(x1+(-x2)+(-x3)); C2=(x2+x3+(-x4)); C3=((-x1)+x3+x4);\nQuestion: Can each variable xi of Xn be assigned a Boolean value alphai in such a way that every clause evaluates to the Boolean result true under the assignment < xi:=alphai:1<=i<=n>? """
            },
        }


def load_llm(model_name, model_dir="./offline_models"):
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, model_name)

    # Download model if not exists
    if not os.path.exists(model_path):
        print(f"Downloading {MODELS[model_name]} to {model_path}...")
        snapshot_download(repo_id=MODELS[model_name], local_dir=model_path, resume_download=True)
    else:
        print(f"Model {model_name} already downloaded in {model_path}")
    # load model
    device_count = torch.cuda.device_count()
    tensor_parallel_size = device_count if device_count > 1 else 1
    assert device_count > 0, "No GPU found!"

    print(f"Loading model: {model_path} with {tensor_parallel_size} GPUs...")
    llm = LLM(
        model=MODELS[model_name],
        download_dir=model_path,
        tensor_parallel_size=tensor_parallel_size,
        dtype="auto",
        gpu_memory_utilization=0.7,
        trust_remote_code=True
    )
    return llm


def evaluate_llm(prompts, model, output_path):
    sampling_params = SamplingParams(
        temperature=0.6,
        top_p=0.95,
        max_tokens=7500,
    )

    # Run inference
    outputs = model.generate(prompts, sampling_params)
    # save results
    responses = []
    responses.extend([[o.text for o in x.outputs] for x in outputs])
    results = save_outputs(responses, prompts, output_path)
    return results[0]


# def create_demo_text(n_shot, num_variables, num_clauses):
#     demos = ""
#     for i in range(n_shot):
#         instance, solution = generate_instance(num_variables, num_clauses)
#         demos += "Problem: {}".format(instance) + "\n"
#         demos += "Solution: {}".format(solution) + "\n"
#     instance, solution = generate_instance(num_variables, num_clauses)
#     demos += "Problem: {}\n".format(instance)
#     demos += "Solution: \n"
#     return demos, instance

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


def build_prompt(problem, description, demos):
    content = "This is a {} problem. Here is the problem description: \n".format(
        problem
    )
    content = content + description + demos
    prompt_str = OEQA[:]
    prompt_str = prompt_str.replace("{question}", content) 
    return prompt_str
    


if __name__ == "__main__":
    problem_name = "three_sat"
    model_name = "deepseek"
    generate_instance, verify_solution = load_np_problem(problem_name)

    n_shot = 3
    iteration = 500
    model = load_llm(model_name)
    
    for num in np.arange(5, 41, 5):
        num_variables = num
        num_clauses = num
        
        output_dir = os.path.join("./experiments/", model_name, problem_name, f"{n_shot}_shot_deepseek_template")
        output_path = os.path.join(output_dir, f'{n_shot}_shot_{num_variables}_var_{num_clauses}_clause.json')
        os.makedirs(output_dir, exist_ok=True)
        num_true, num_total = 0, 0

        for iter in range(iteration):
            print("=" * 30)
            print("Iteration {}".format(iter))
            print("=" * 30)

            demos, instance = create_demo_text(n_shot, num_variables, num_clauses)
            content = nppc_template_deepseek.replace("<problem_description>", PROBLEM_SHEET[problem_name]["description"])
            content = content.replace("<in_context_examples>", demos).replace(
            "<problem_to_solve>", "{}".format(instance)
            )
            print(content)
            # json_template = {"reasoning": {}, "solution": []}
            # json_template = {"solution": []}
            # json_str = json.dumps(json_template, indent=4)
            # content = content.replace("<json_template>", json_str)

            try:
                response = evaluate_llm(content, model, output_path)
                cleaned_response = extract_json_and_answer(response)

                if cleaned_response is not None:
                    results = verify_solution(instance, cleaned_response)
                    if results[0]:
                        num_true = num_true + 1
                else:
                    print("Wrong Format")
                num_total = num_total + 1
                print("=" * 30)
                print("Accuracy = {}, True = {}, Total = {}".format(num_true / num_total, num_true, num_total))
                print("=" * 30)
                if num_total == 50:
                    res = {
                        "Num of Clauses": f"{num_clauses}",
                        "Num of Variables": f"{num_variables}",
                        "Accuracy": f"{num_true / num_total}",
                        "True Count": f"{num_true}",
                        "Total": f"{num_total}"
                    }

                    filename = os.path.join(output_dir, "summary.json")

                    # Check if the file exists, read existing data, and append new results
                    if os.path.exists(filename):
                        with open(filename, "r") as f:
                            try:
                                existing_data = json.load(f)
                                if not isinstance(existing_data, list):
                                    existing_data = [existing_data]  # Convert single entry to list
                            except json.JSONDecodeError:
                                existing_data = []  # If file is empty or invalid, start fresh
                    else:
                        existing_data = []

                    existing_data.append(res)  # Append the new result

                    # Write updated content back to file
                    with open(filename, "w") as f:
                        json.dump(existing_data, f, indent=2)
                    break
            except Exception as e:
                print(f"Error calling API: {e}")