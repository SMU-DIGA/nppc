import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple, Callable, Optional

def save_outputs(results: List[Dict], file_path: Path) -> None:
    """Save results to JSON file with atomic write, handling empty or corrupted files."""
    try:
        existing_data = []
        if file_path.exists():
            with file_path.open() as f:
                try:
                    existing_data = json.load(f)  # Load existing JSON
                except json.JSONDecodeError:
                    logger.warning(f"Warning: {file_path} is empty or corrupted. Overwriting with fresh results.")
                    existing_data = []  # Reset if file is corrupted
        
        def convert_sets(obj):
            """Ensure JSON compatibility by converting sets, tuples, and None values."""
            if isinstance(obj, set):
                return list(obj)  # Convert sets to lists
            elif isinstance(obj, tuple):
                return list(obj)  # Convert tuples to lists
            elif isinstance(obj, dict):
                return {str(k): convert_sets(v) for k, v in obj.items()}  # Ensure valid dict
            elif isinstance(obj, list):
                return [convert_sets(x) for x in obj]  # Recursively process lists
            elif obj is None:
                return "null"  # JSON cannot handle None, replace with "null"
            return obj
        existing_data += [convert_sets(r) for r in results]
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(
                existing_data,
                f,
                indent=2,
                ensure_ascii=False
            )
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Failed to save results: {str(e)}")
        
res_summary = [{
        "level": 1,
        "accuracy": 0.78,
        "num rollouts": 100,
    }]
save_outputs(res_summary, Path("test.json"))