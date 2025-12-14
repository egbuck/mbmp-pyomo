"""
Entry point for optimization run
"""

from data import read_data
from model import create_model
from solve import solve_model

def main():
    data = read_data("data.yaml")
    model = create_model(data)
    results = solve_model(model)

    model.display()
    #print(results)

if __name__ == "__main__":
    main()
