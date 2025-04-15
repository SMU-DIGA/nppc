import asyncio
import json
import os
import re
from pathlib import Path

from huggingface_hub import snapshot_download
from litellm import batch_completion
from openai import AsyncOpenAI

from npsolver import MODELS
from npsolver.prompt import nppc_template, example_and_solution, problem_descriptions


# Continue with your vLLM code
def extract_solution_from_response_old(response):
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
            return answer, None
        except (json.JSONDecodeError, KeyError, SyntaxError) as e:
            print(f"Error parsing JSON or answer field: {e}")
            # return None
            return None, f"Error parsing JSON or answer field: {e}"
    else:
        print("No JSON found in the text.")
        # return None
        return None, "JSON Error: No JSON found in the text."


def extract_solution_from_response(response):
    # find the json code
    match = re.findall(r"```json\n(.*?)\n```", response, re.DOTALL)

    # print(match)
    if not match:
        match = re.findall(r"json\s*({[^{}]*})", response, re.DOTALL)
    if not match:
        match = re.findall(r"\{[^{}]*\}", response, re.DOTALL)

    if match:
        json_str = match[-1]
        try:
            # remove the single line comment
            json_str = re.sub(r"//.*$", "", json_str, flags=re.MULTILINE)
            # remove the multiple line comment
            json_str = re.sub(r"/\*[\s\S]*?\*/", "", json_str)
            data = json.loads(json_str)
            answer = data["solution"]
            return answer, None
        except (json.JSONDecodeError, KeyError, SyntaxError) as e:
            print(f"Error parsing JSON or answer field: {e}")
            # return None
            return None, f"Error parsing JSON or answer field: {e}"
    else:
        print("No JSON found in the text.")
        # return None
        return None, "JSON Error: No JSON found in the text."


def initialize_offline_model(model_name: str, model_dir, seed):
    import torch
    from vllm import LLM, SamplingParams

    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / model_name

    if not model_path.exists():
        snapshot_download(
            repo_id=MODELS["offline"][model_name],
            local_dir=str(model_path),
            resume_download=True,
        )
    else:
        print(f"\n{'=' * 20} Loading model from {str(model_path)} {'=' * 20}")

    device_count = torch.cuda.device_count()
    if device_count == 0:
        raise RuntimeError("No available GPUs found")

    return LLM(
        model=MODELS["offline"][model_name],
        download_dir=str(model_path),
        tensor_parallel_size=max(device_count, 1),
        dtype="auto",
        gpu_memory_utilization=0.8,
        trust_remote_code=True,
        enforce_eager=True,
    ), SamplingParams(temperature=0.6, top_p=0.95, max_tokens=7500, seed=seed)


class NPSolver:
    def __init__(self, problem_name, model_name, seed):
        if model_name in MODELS["online"].keys():
            self.is_online = True
        elif model_name in MODELS["offline"].keys():
            self.is_online = False
        else:
            raise NotImplementedError

        self.model_name = model_name
        self.problem_name = problem_name

        self.local_llm = None
        self.sampling_params = None
        if not self.is_online:
            self.local_llm, self.sampling_params = initialize_offline_model(
                model_name=model_name,
                model_dir=Path(
                    "/proj/cloudrobotics-nest/users/x_ruiwa/nppc_main/offline_models"
                ),
                seed=seed,
            )

        self.client = None

        if self.is_online and model_name.startswith("deepseek"):
            self.client = AsyncOpenAI(
                api_key=os.environ.get("ARK_API_KEY"),
                base_url="https://ark.cn-beijing.volces.com/api/v3",
            )
        if self.is_online and model_name.startswith("maas"):
            self.client = AsyncOpenAI(
                api_key=os.environ.get("MAAS_API_KEY"),
                base_url="https://genaiapi.cloudsway.net/v1/ai/RpGtTVMGiAYxmInr",
            )

    async def async_evaluate_llm(self, contents):
        assert self.client is not None

        async def call_gpt(prompt):
            response = await self.client.chat.completions.create(
                model=MODELS["online"][self.model_name],
                messages=[{"role": "user", "content": prompt}],
            )
            return response

        return await asyncio.gather(*[call_gpt(content) for content in contents])

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
            print("Get results from api")
            return self.get_batch_outputs_from_api(contents)
        else:
            print("Get results from local model")
            return self.get_batch_outputs_from_offline_model(contents)

    def get_batch_outputs_from_api(self, contents):
        try:
            print("Starting the batch calling of LLM")
            messages = [[{"role": "user", "content": content}] for content in contents]
            if self.is_online and (
                self.model_name.startswith("deepseek")
                or self.model_name.startswith("maas")
            ):
                responses = asyncio.run(self.async_evaluate_llm(contents))
            else:
                responses = batch_completion(
                    messages=messages, model=MODELS["online"][self.model_name]
                )
            # print(responses)
            print("End of calling LLM")
            outputs = []
            for idx, response in enumerate(responses):
                # print(response)
                token_numbers = {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                }
                prediction = response.choices[0].message.content
                predicted_solution, json_error_message = extract_solution_from_response(
                    prediction
                )

                output = {
                    "full_response": response,
                    "response": prediction,
                    "solution": predicted_solution,
                    "tokens": token_numbers,
                    "error_msg": {"llm": None, "json": json_error_message},
                }
                # print(result)
                outputs.append(output)
            return outputs
        except Exception as e:
            # return None
            outputs = [
                {
                    "solution": None,
                    "error_msg": {"llm": f"LLM error: {e}", "json": None},
                }
                for _ in range(len(contents))
            ]

            return outputs

    def get_batch_outputs_from_offline_model(self, contents):
        try:
            responses = self.local_llm.generate(contents, self.sampling_params)
            outputs = []

            for response in responses:
                prediction = response.outputs[0].text
                predicted_solution, json_error_message = extract_solution_from_response(
                    prediction
                )
                token_numbers = {
                    "prompt": len(response.prompt_token_ids),
                    "completion": len(response.outputs[0].token_ids),
                }
                outputs.append(
                    {
                        "response": prediction,
                        "solution": predicted_solution,
                        "tokens": token_numbers,
                        "error_msg": {"llm": None, "json": json_error_message},
                    }
                )
            return outputs
        except Exception as e:
            # return None
            outputs = [
                {
                    "solution": None,
                    "error_msg": {"llm": f"LLM error: {e}", "json": None},
                }
                for _ in range(len(contents))
            ]
            return outputs
