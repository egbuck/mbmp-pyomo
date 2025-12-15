"""
Model Definition for Multi Period Oil Blending Problem
"""
import pyomo.environ as pyo


def profit_rule(m):
    """Objective function: Maximize profit over the planning horizon."""
    def revenue_rule(m):
        return m.price * sum(m.prod[t] for t in m.T)

    def cost_of_raw_goods_rule(m):
        return sum(m.cost[t, o] * m.b[t, o] for o in m.O for t in m.T)

    def cost_of_storage_rule(m):
        return sum(m.storage_cost[o] * m.s[t, o] for o in m.O for t in m.T)

    return revenue_rule(m) - cost_of_raw_goods_rule(m) - cost_of_storage_rule(m)


def production_cap_rule(m, t, ptype):
    return sum(m.u[t, o] for o in m.O_BY_TYPE[ptype]) <= m.production_cap[ptype]


def balance_periods_rule(m, t, o):
    if t == m.T.first():
        return m.b[t, o] + m.start_inventory[o] == m.u[t, o] + m.s[t, o]
    else:
        return m.b[t, o] + m.s[m.T.prev(t), o] == m.u[t, o] + m.s[t, o]

def balance_production_rule(m, t):
    return m.prod[t] == sum(m.u[t, o] for o in m.O)

    
def hardness_min_rule(m, t):
    return sum(m.hardness[o] * m.u[t, o] for o in m.O) >= m.hardness_min * m.prod[t]

def hardness_max_rule(m, t):
    return sum(m.hardness[o] * m.u[t, o] for o in m.O) <= m.hardness_max * m.prod[t]

def create_model(data):
    model = pyo.ConcreteModel()

    # Define sets
    model.O = pyo.Set(initialize=data["sets"]["O"])
    model.T = pyo.Set(initialize=data["sets"]["T"])
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
    cost_data = {
        (t, o): v
        for t, oils in data["parameters"]["cost"].items()
        for o, v in oils.items()
    }
    model.cost = pyo.Param(model.T, model.O, initialize=cost_data)
    model.price = pyo.Param(initialize=data["parameters"]["price"])

    # Hardness parameters
    model.hardness = pyo.Param(model.O, initialize=data["parameters"]["hardness"])
    model.hardness_min = pyo.Param(initialize=data["parameters"]["hardness_min"])
    model.hardness_max = pyo.Param(initialize=data["parameters"]["hardness_max"])

    # Storage parameters
    model.storage_cost = pyo.Param(model.O, initialize=data["parameters"]["storage_cost"])
    model.storage_cap = pyo.Param(model.O, initialize=data["parameters"]["storage_cap"])

    # Initial and End Inventory parameters
    model.start_inventory = pyo.Param(
        model.O,
        initialize=data["parameters"]["start_inventory"]
    )
    model.end_inventory = pyo.Param(
        model.O,
        initialize=data["parameters"]["end_inventory"]
    )

    # Variables
    model.u = pyo.Var(model.T, model.O, domain=pyo.NonNegativeReals)
    model.b = pyo.Var(model.T, model.O, domain=pyo.NonNegativeReals)
    model.s = pyo.Var(model.T, model.O, domain=pyo.NonNegativeReals)
    model.prod = pyo.Var(model.T, domain=pyo.NonNegativeReals)
    
    # Objective
    model.Obj = pyo.Objective(rule=profit_rule, sense=pyo.maximize)
    
    # Constraints
    ## Production capacity constraints
    model.production_cap_constraint = pyo.Constraint(
        model.T,
        model.OTYPE,
        rule=production_cap_rule
    )

    ## Balance constraints
    model.balance_periods_constraint = pyo.Constraint(
        model.T,
        model.O,
        rule=balance_periods_rule
    )
    model.balance_production_constraint = pyo.Constraint(
        model.T,
        rule=balance_production_rule
    )

    ## Hardness constraints
    model.hardness_min_constraint = pyo.Constraint(
        model.T,
        rule=hardness_min_rule
    )
    model.hardness_max_constraint = pyo.Constraint(
        model.T,
        rule=hardness_max_rule
    )

    ## Storage capacity constraints
    model.storage_capacity_constraint = pyo.Constraint(
        model.T,
        model.O,
        rule=lambda m, t, o: m.s[t, o] <= m.storage_cap[o]
    )

    # End inventory constraints
    model.end_inventory_constraint = pyo.Constraint(
        model.O,
        rule=lambda m, o: m.s[m.T.last(), o] == m.end_inventory[o]
    )

    return model
