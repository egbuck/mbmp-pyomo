"""
Entry point for optimization run
"""

from mbmp_pyomo.utils import read_data, solve_model
from models import create_single_period_model, create_multi_period_model
from pathlib import Path
import argparse


SCRIPT_DIR = Path(__file__).parent.absolute()
parser = argparse.ArgumentParser(description="Food Manufacture Optimization")
parser.add_argument(
    "--data-file",
    type=str,
    default="data.yaml",
    help="Path to the data file (YAML format)",
)
parser.add_argument(
    "--model-type",
    type=str,
    choices=["single-period", "multi-period"],
    default="single-period",
    help="Type of model to use",
)


def main():
    args = parser.parse_args()
    data_file_path = SCRIPT_DIR / args.data_file
    data = read_data(data_file_path)
    model = create_multi_period_model(data) if args.model_type == "multi-period" else create_single_period_model(data)
    solve_model(model)

    model.display()


if __name__ == "__main__":
    main()
