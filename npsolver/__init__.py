MODELS = {
    "online": {
        "gpt-4o": "gpt-4o-2024-08-06",
        "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
        "o1-mini": "o1-mini-2024-09-12",
        "deepseek-chat": "deepseek/deepseek-chat",
        "claude": "anthropic/claude-3-sonnet-20240229",
    },
    "offline": {
        "deepseek": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    },
}

from npsolver.solver import NPSolver
