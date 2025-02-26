from litellm import batch_completion
import re
import json
from npsolver.prompt import nppc_template, example_and_solution, problem_descriptions
from npsolver import MODELS


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


class NPSolver:
    def __init__(self, problem_name, model):
        if model in MODELS["online"]:
            self.is_online = True
        elif model in MODELS["offline"]:
            self.is_online = False
        else:
            raise NotImplementedError

        self.model_name = model
        self.problem_name = problem_name

        self.local_llm = None

    def get_prediction(self, inputs):
        contents = []
        for idx in range(len(inputs)):
            problem_to_solve = inputs[idx]["instance"]
            examples = inputs[idx]["examples"]
            demo_content = ""
            for example in examples:
                demo = example_and_solution.replace(
                    "<example_problem>", "{}".format(example[0])
                ).replace("<example_solution>", json.dumps(example[1]))
                demo_content += demo
            content = nppc_template.replace(
                "<problem_description>", problem_descriptions[self.problem_name]
            ).replace("<problem_name>", self.problem_name)
            content = content.replace("<in_context_examples>", demo_content).replace(
                "<problem_to_solve>", "{}".format(problem_to_solve)
            )
            contents.append(content)

        if self.is_online:
            return self.get_batch_outputs_from_api(contents)

    def get_batch_outputs_from_api(self, contents):
        assert self.is_online
        outputs = []
        try:
            print("Starting the batch calling of LLM")
            messages = [[{"role": "user", "content": content}] for content in contents]
            responses = batch_completion(
                messages=messages, model=MODELS["online"][self.model_name]
            )
            # print(responses)
            print("End of calling LLM")
            for idx, response in enumerate(responses):
                token_numbers = {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                }
                prediction = response.choices[0].message.content
                predicted_solution = extract_solution_from_response(prediction)

                output = {
                    "response": prediction,
                    "solution": predicted_solution,
                    "tokens": token_numbers,
                }
                # print(result)
                outputs.append(output)
            return outputs
        except Exception as e:
            print(f"Error calling the LLM: {e}")
            return None

    def get_batch_outputs_from_offline_model(self):
        assert not self.is_online
        print()
