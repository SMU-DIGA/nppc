import json
from typing import Any, Dict, List, Tuple, Callable, Optional
from pathlib import Path


def save_outputs(results: List[Dict], file_path: Path) -> None:
    """Save results to JSON file with atomic write, handling empty or corrupted files."""
    try:
        existing_data = []
        if file_path.exists():
            with file_path.open() as f:
                try:
                    existing_data = json.load(f)  # Load existing JSON
                except json.JSONDecodeError:
                    logger.warning(
                        f"Warning: {file_path} is empty or corrupted. Overwriting with fresh results."
                    )
                    existing_data = []  # Reset if file is corrupted

        def convert_sets(obj):
            """Ensure JSON compatibility by converting sets, tuples, and None values."""
            if isinstance(obj, set):
                return list(obj)  # Convert sets to lists
            elif isinstance(obj, tuple):
                return list(obj)  # Convert tuples to lists
            elif isinstance(obj, dict):
                return {
                    str(k): convert_sets(v) for k, v in obj.items()
                }  # Ensure valid dict
            elif isinstance(obj, list):
                return [convert_sets(x) for x in obj]  # Recursively process lists
            elif obj is None:
                return "null"  # JSON cannot handle None, replace with "null"
            return obj

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(
                existing_data + [convert_sets(r) for r in results],
                f,
                indent=2,
                ensure_ascii=False,
            )
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Failed to save results: {str(e)}")


batch_results = [
    {
        "instance": {
            "variables": "[1, 2, 3, 4, 5]",
            "clauses": "[(-2, 1, -3), (-1, -5, 4), (5, -2, 3), (-5, 3, 1), (-3, 5, -1)]",
        },
        "solution": "[False, False, True, True, True]",
        "correctness": True,
        "reason": "Correct solution.",
        "tokens": {"prompt": 595, "completion": 1210},
    },
    {
        "instance": {
            "variables": [1, 2, 3, 4, 5],
            "clauses": [(5, -3, 1), (4, 1, -3), (-1, 5, 3), (1, 2, 5), (3, -2, 4)],
        },
        "solution": [True, False, True, False, False],
        "correctness": True,
        "reason": "Correct solution.",
        "tokens": {"prompt": 594, "completion": 1286},
    },
    {
        "instance": {
            "variables": [1, 2, 3, 4, 5],
            "clauses": [(-4, 3, -5), (2, 1, -5), (2, 3, 1), (-2, 3, 1), (-5, -4, 2)],
        },
        "solution": [False, True, True, False, False],
        "correctness": True,
        "reason": "Correct solution.",
        "tokens": {"prompt": 595, "completion": 1759},
    },
    {
        "instance": {
            "variables": [1, 2, 3, 4, 5],
            "clauses": [(4, 1, 2), (-5, 1, 3), (-1, 3, -2), (-3, 2, -5), (-2, 3, 1)],
        },
        "solution": [False, True, True, True, False],
        "correctness": True,
        "reason": "Correct solution.",
        "tokens": {"prompt": 594, "completion": 1032},
    },
]
save_outputs(batch_results, Path("./") / "test.json")
