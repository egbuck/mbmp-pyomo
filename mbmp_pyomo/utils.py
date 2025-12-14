import pyomo.environ as pyo
import yaml

SOLVER_PATH = "C:\\Users\\Ethan\\Documents\\solvers\\glpk-4.65\\w64\\glpsol.exe"

def solve_model(model, solver_name="glpk"):
    """Solver configuration and execution."""
    solver = pyo.SolverFactory(solver_name, executable=SOLVER_PATH)
    return solver.solve(model, tee=True)


def read_data(file_path="data.yaml"):
    """Data Loading from a YAML file."""
    with open(file_path) as file:
        return yaml.safe_load(file)