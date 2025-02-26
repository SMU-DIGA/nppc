import os
import re
import json
from litellm import batch_completion

models = {
    "gpt-4o": "gpt-4o-2024-08-06",
    "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "o1-mini": "o1-mini-2024-09-12",
    "deepseek-chat": "deepseek/deepseek-chat",
    # "claude": "anthropic/claude-3-sonnet-20240229",
}


def extract_solution_from_response(response):
    # find the json code
    match = re.findall(r"```json\n(.*?)\n```", response, re.DOTALL)
    if match:
        json_str = match[-1]
        try:
            # remove the single line comment
            json_str = re.sub(r"//.*$", "", json_str, flags=re.MULTILINE)
            # remove the multiple line comment
            json_str = re.sub(r"/\*[\s\S]*?\*/", "", json_str)
            data = json.loads(json_str)
            answer = data["solution"]
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


def get_batch_results_from_api(contents, model):
    results = []
    try:
        print("Starting the batch calling of LLM")
        messages = [[{"role": "user", "content": content}] for content in contents]
        responses = batch_completion(messages=messages, model=models[model])

        # print(responses)
        print("End of calling LLM")
        for idx, response in enumerate(responses):
            token_numbers = {
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
            }
            prediction = response.choices[0].message.content
            predicted_solution = extract_solution_from_response(prediction)

            result = {
                # "instance": instance,
                # "examples": examples,
                "response": prediction,
                "solution": predicted_solution,
                "tokens": token_numbers,
            }
            # print(result)
            results.append(result)
        return results
    except Exception as e:
        print(f"Error calling the LLM: {e}")
        return None
