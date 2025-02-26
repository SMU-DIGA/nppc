import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        type=int,
        required=False,
        default=42,
        help="seed",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=False,
        default="gpt-4o-mini",
        help="name for LLM",
    )
    parser.add_argument(
        "--problem",
        type=int,
        required=False,
        default=0,
        help="the problem name idx",
    )
    parser.add_argument(
        "--n_shots",
        type=int,
        required=False,
        default=1,
        help="number of in-context examples",
    )

    parser.add_argument(
        "--n_trials",
        type=int,
        required=False,
        default=30,
        help="number of trials for each level",
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        required=False,
        default=10,
        help="the problem name",
    )

    parser.add_argument(
        "--max_tries",
        type=int,
        required=False,
        default=3,
        help="max tries for one batch",
    )

    parser.add_argument(
        "--result_folder",
        type=str,
        required=False,
        default="results",
        help="folder path to store the results",
    )

    parser.add_argument("--verbose", type=bool, required=False, default=False)

    return parser.parse_args()
