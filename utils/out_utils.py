import ast
import json
import os
import re


def clear_output(output, model_name=None):
    for token in ["<|endoftext|>", "<pad>", "<end_of_turn>"]:
        output = output.replace(token, " ")

    return output.strip()


def save_outputs(outputs, model_inputs, filepath):
    formatted_outputs = []
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                formatted_outputs = json.load(f)
            except json.JSONDecodeError:
                formatted_outputs = []  # Handle corrupt JSON file gracefully
    for ind in range(len(outputs)):
        output_item = {
            "output": [clear_output(o) for o in outputs[ind]],
            "model_input": model_inputs,
        }
        formatted_outputs.append(output_item)

    # Save updated results
    with open(filepath, "w") as f:
        json.dump(formatted_outputs, f, indent=2)
    return output_item["output"]


def extract_json_and_answer(text, tag_name="solution"):
    # match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
    match = re.search(f"<{tag_name}>\\s?(.*?)\\s?</{tag_name}>", text, re.DOTALL)

    if match:
        json_str = match.group(1)
        print("json:", json_str)
        try:
            json_str = (
                json_str.replace("True", "true")
                .replace("False", "false")
                .replace("None", "null")
            )
            data = json.loads(json_str)["solution"]
            if isinstance(data, str):
                answer = ast.literal_eval(data)
            elif isinstance(data, list):
                answer = data
            else:
                print("wrong type solution!")
            return answer
        except (json.JSONDecodeError, KeyError, SyntaxError) as e:
            print(f"Error parsing JSON or answer field: {e}")
            return None
    else:
        print("No JSON found in the text.")
        return None
