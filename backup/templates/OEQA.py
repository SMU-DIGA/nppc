#  Open-Ended Question Answering Template
OEQA = """
## Question: 
{question}
## Instruction 
Please answer this question by first reasoning and then providing your answer.
Present your reasoning and solution in the following json format. 
Please show your final answer in the `answer` field, e.g.,`"answer": "42"`.
```json
{
    "reasoning": "___",
    "solution": "___"
}
```
"""

DEEPSEEK_MATH = """
## Probelm 
{question}
## Instruction 
Please reason step by step, and put your final solution in the "solution" field in the following json format and of the same format as the example solutions.
```json
{
    "solution": "___"
}
```
"""

OEQA_DIRECT = """

## Question: 

{question}


## Instruction 

Please solve this question directly by providing your answer.
Please show your final answer in the `answer` field. without explanation in the following json format. 

```json
{
    "answer": "___"
}
```
"""
