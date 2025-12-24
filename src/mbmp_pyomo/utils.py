import pyomo.environ as pyo
import yaml
from pathlib import Path


def read_data(file_path="data.yaml"):
    """Data Loading from a YAML file."""
    with open(file_path) as file:
        return yaml.safe_load(file)


PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
CONFIG = read_data(PROJECT_ROOT / "config.yaml")
SOLVER_NAME = CONFIG.get("solver", {}).get("name", None)
SOLVER_PATH = CONFIG.get("solver", {}).get("executable", None)


def solve_model(model, solver_name=SOLVER_NAME):
    """Solver configuration and execution."""
    if SOLVER_NAME is None:
        raise ValueError(
            "Solver name must be specified in the configuration, under 'solver.name'."
        )
    not_none_params = {
        key: param
        for key, param in {
            "solver_name": solver_name,
            "executable": SOLVER_PATH,
        }.items()
        if param is not None
    }
    solver = pyo.SolverFactory(solver_name, executable=SOLVER_PATH)
    return solver.solve(model, tee=True)
