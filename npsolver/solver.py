from litellm import batch_completion
import re
import json
from npsolver.prompt import nppc_template, example_and_solution, problem_descriptions
from npsolver import MODELS
from huggingface_hub import snapshot_download
from pathlib import Path
import asyncio
from openai import AsyncOpenAI
import os


# Continue with your vLLM code
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


def initialize_offline_model(model_name: str, model_dir):
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
    ), SamplingParams(temperature=0.6, top_p=0.95, max_tokens=7500)


class NPSolver:
    def __init__(self, problem_name, model_name):
        if model_name in MODELS["online"]:
            self.is_online = True
        elif model_name in MODELS["offline"]:
            self.is_online = False
        else:
            raise NotImplementedError

        self.model_name = model_name
        self.problem_name = problem_name

        self.local_llm = None
        self.sampling_params = None
        if not self.is_online:
            self.local_llm, self.sampling_params = initialize_offline_model(
                model_name=model_name, model_dir=Path("./models")
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
            return self.get_batch_outputs_from_api(contents)
        else:
            return self.get_batch_outputs_from_offline_model(contents)

    def get_batch_outputs_from_api(self, contents):
        assert self.is_online
        outputs = []
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

    def get_batch_outputs_from_offline_model(self, contents):
        assert not self.is_online
        try:
            responses = self.local_llm.generate(contents, self.sampling_params)
            outputs = []

            for response in responses:
                response_text = response.outputs[0].text
                solution = extract_solution_from_response(response_text)

                outputs.append(
                    {
                        "response": response_text,
                        "solution": solution,
                        "tokens": {
                            "prompt": len(response.prompt_token_ids),
                            "completion": len(response.outputs[0].token_ids),
                        },
                    }
                )

            return outputs
        except Exception as e:
            print(f"Error calling the LLM: {e}")
            return None
