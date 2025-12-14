# Single-Period Oil Blending Optimization Model

## Problem Overview

A food product is manufactured by refining and blending several raw oils.  
Each raw oil has a purchase cost and a hardness value. The final blended product:

- Sells at a fixed price per ton
- Must satisfy hardness quality constraints
- Is produced using separate production lines for vegetable and non-vegetable oils
- Cannot be stored

This document describes the **single-period** (one month) optimization model.

---

## Sets

Let:

- $`(\mathcal{O})`$ = set of raw oils  

  ```math
  \mathcal{O} = \{\text{VEG\_1}, \text{VEG\_2}, \text{OIL\_1}, \text{OIL\_2}, \text{OIL\_3}\}
  ```

- $`\mathcal{O}_{\text{VEG}} \subset \mathcal{O}`$ = vegetable oils  

  ```math
  \mathcal{O}_{\text{VEG}} = \{\text{VEG\_1}, \text{VEG\_2}\}
  ```

- $`\mathcal{O}_{\text{NON}} \subset \mathcal{O}`$ = non-vegetable oils  

  ```math
  \mathcal{O}_{\text{NON}} = \{\text{OIL\_1}, \text{OIL\_2}, \text{OIL\_3}\}
  ```

---

## Parameters

All parameters are known constants.

- $`\text{cost}_o`$: purchase cost per ton of oil $`o \in \mathcal{O}`$
- $`\text{price}`$: selling price per ton of final product
- $`\text{hardness}_o`$: hardness value of oil $`o`$
- $`\underline{H}`$: minimum allowable hardness of the final blend
- $`\overline{H}`$: maximum allowable hardness of the final blend
- $`\text{cap}_{\text{VEG}}`$: maximum tons of vegetable oil that can be refined
- $`\text{cap}_{\text{NON}}`$: maximum tons of non-vegetable oil that can be refined

---

## Decision Variables

All decision variables are continuous and non-negative.

- $`x_o`$: tons of raw oil $`o \in \mathcal{O}`$ refined in the period  
- $`y`$: tons of final blended product produced

---

## Objective Function

Maximize total profit, defined as revenue from the final product minus raw oil purchase costs:

```math
\max \;
\text{price} \cdot y
\;-\;
\sum_{o \in \mathcal{O}} \text{cost}_o \cdot x_o
```

---

## Constraints

### 1. Production Capacity Constraints

Vegetable and non-vegetable oils must be processed on separate production lines with limited capacity.

**Vegetable oils:**
```math
\sum_{o \in \mathcal{O}_{\text{VEG}}} x_o
\;\le\;
\text{cap}_{\text{VEG}}
```

**Non-vegetable oils:**
```math
\sum_{o \in \mathcal{O}_{\text{NON}}} x_o
\;\le\;
\text{cap}_{\text{NON}}
```

---

### 2. Mass Balance Constraint

All refined oil is blended into the final product. No waste or loss occurs.

```math
\sum_{o \in \mathcal{O}} x_o = y
```

---

### 3. Hardness Constraints

The hardness of the blended product is a linear weighted average of the component oils and must lie within specified bounds.

**Lower bound:**
```math
\sum_{o \in \mathcal{O}} \text{hardness}_o \cdot x_o
\;\ge\;
\underline{H} \cdot y
```

**Upper bound:**
```math
\sum_{o \in \mathcal{O}} \text{hardness}_o \cdot x_o
\;\le\;
\overline{H} \cdot y
```

---

### 4. Non-Negativity

```math
x_o \ge 0 \quad \forall o \in \mathcal{O}
```
```math
y \ge 0
```

---

## Notation to Pyomo Mapping

| Mathematical Symbol | Description                              | Pyomo Name / Structure        |
|--------------------|------------------------------------------|-------------------------------|
| $`\mathcal{O}`$  | Set of raw oils                           | `model.O`                     |
| $`\mathcal{O}_{\text{VEG}}`$ | Vegetable oils subset            | `model.O_VEG`                 |
| $`\mathcal{O}_{\text{NON}}`$ | Non-vegetable oils subset        | `model.O_NON`                 |
| $`x_o`$          | Tons of oil $o$ refined                | `model.x[o]`                  |
| $`y`$            | Final product output                     | `model.prod` or `model.y`     |
| $`\text{cost}_o`$| Cost per ton of oil                      | `model.cost[o]`               |
| $`\text{price}`$ | Selling price per ton                    | `model.price`                 |
| $`\text{hardness}_o`$ | Hardness of oil $o$             | `model.hardness[o]`           |
| $`\underline{H}`$| Minimum blend hardness                   | `model.hardness_lb`           |
| $`\overline{H}`$ | Maximum blend hardness                   | `model.hardness_ub`           |
| $`\text{cap}_{\text{VEG}}`$ | Veg processing capacity        | `model.production_cap['VEG']` |
| $`\text{cap}_{\text{NON}}`$ | Non-veg processing capacity    | `model.production_cap['NON']` |

---

## Notes on Implementation

- Oil categories are represented as **subsets**, not logic inside constraints.
- Hardness constraints remain linear due to the mass balance equation.
- This single-period model forms the foundation for the multi-period model with inventory and storage costs.

