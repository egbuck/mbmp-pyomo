"""
Solver Configuration
"""
import pyomo.environ as pyo
SOLVER_PATH = "C:\\Users\\Ethan\\Documents\\solvers\\glpk-4.65\\w64\\glpsol.exe"

def solve_model(model, solver_name="glpk"):
    solver = pyo.SolverFactory(solver_name, executable=SOLVER_PATH)
    return solver.solve(model, tee=True)
