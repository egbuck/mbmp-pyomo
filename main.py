"""
Entry point for optimization run
"""

from data import read_data
from models import create_single_period_model
from solve import solve_model

def main():
    data = read_data("data.yaml")
    model = create_single_period_model(data)
    solve_model(model)

    model.display()

if __name__ == "__main__":
    main()
