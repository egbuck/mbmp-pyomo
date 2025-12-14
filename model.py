"""
Model Definitions
"""
MONTH = "Jan"
import pyomo.environ as pyo

def create_model(data):
    model = pyo.ConcreteModel()

    # Define sets
    model.O = pyo.Set(initialize=data["sets"]["O"])
    model.OTYPE = pyo.Set(initialize=data["sets"]["OTYPE"])
    model.O_BY_TYPE = pyo.Set(
        model.OTYPE,
        initialize=data["sets"]["O_BY_TYPE"]
    )

    # Parameters
    model.production_cap = pyo.Param(
        model.OTYPE,
        initialize=data["parameters"]["production_cap"]
    )
    # Get the costs for the specified MONTH for each oil in model.O
    month_costs = {oil: cost[MONTH] for oil, cost in data["parameters"]["cost"].items()}
    model.cost = pyo.Param(model.O, initialize=month_costs)
    model.price = pyo.Param(initialize=data["parameters"]["price"])

    model.hardness = pyo.Param(model.O, initialize=data["parameters"]["hardness"])
    model.hardness_min = pyo.Param(initialize=data["parameters"]["hardness_min"])
    model.hardness_max = pyo.Param(initialize=data["parameters"]["hardness_max"])

    # Variables
    model.x = pyo.Var(model.O, domain=pyo.NonNegativeReals)
    model.prod = pyo.Var(domain=pyo.NonNegativeReals)
    
    # Objective
    model.Obj = pyo.Objective(rule=profit_rule, sense=pyo.maximize)
    
    # Constraints
    model.production_cap_constraint = pyo.Constraint(
        model.OTYPE,
        rule=production_cap_rule
    )
    model.balance_constraint = pyo.Constraint(
        expr=model.prod == sum(model.x[o] for o in model.O)
    )
    model.hardness_min_constraint = pyo.Constraint(
        expr=sum(model.hardness[o] * model.x[o] for o in model.O) >= model.hardness_min * model.prod
    )
    model.hardness_max_constraint = pyo.Constraint(
        expr=sum(model.hardness[o] * model.x[o] for o in model.O) <= model.hardness_max * model.prod
    )

    return model


def profit_rule(m):
    return m.price * m.prod - sum(m.cost[o] * m.x[o] for o in m.O)

def production_cap_rule(m, ptype):
    return sum(m.x[o] for o in m.O_BY_TYPE[ptype]) <= m.production_cap[ptype]