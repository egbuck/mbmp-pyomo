"""
Entry point for optimization run
"""

from mbmp_pyomo.utils import read_data, solve_model
from models import create_single_period_model

def main():
    data = read_data("data.yaml")
    model = create_single_period_model(data)
    solve_model(model)

    model.display()

if __name__ == "__main__":
    main()
