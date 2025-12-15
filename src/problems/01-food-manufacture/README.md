# Oil Blending Optimization Model

## Problem Overview

A food product is manufactured by refining and blending several raw oils.  
Each raw oil has a purchase cost and a hardness value. The final blended product:

- Sells at a fixed price per ton
- Must satisfy hardness quality constraints
- Is produced using separate production lines for vegetable and non-vegetable oils

## Sets

Let the following sets be defined.

$`\mathcal{O}`$ = set of raw oils  

```math
\mathcal{O} = \{\text{VEG\_1}, \text{VEG\_2}, \text{OIL\_1}, \text{OIL\_2}, \text{OIL\_3}\}
```

$`\mathcal{O}_{\text{V}} \subset \mathcal{O}`$ = vegetable oils  

```math
\mathcal{O}_{\text{V}} = \{\text{VEG\_1}, \text{VEG\_2}\}
```

$`\mathcal{O}_{\text{N}} \subset \mathcal{O}`$ = non-vegetable oils  

```math
\mathcal{O}_{\text{N}} = \{\text{OIL\_1}, \text{OIL\_2}, \text{OIL\_3}\}
```

---

## Parameters

All parameters are known constants.

- $`c_o`$: purchase cost per ton of oil $`o \in \mathcal{O}`$
- $`p`$: selling price per ton of final product
- $`h_o`$: hardness value of oil $`o`$
- $`\underline{H}`$: minimum allowable hardness of the final blend
- $`\overline{H}`$: maximum allowable hardness of the final blend
- $`M_V`$: maximum tons of vegetable oil that can be refined
- $`M_N`$: maximum tons of non-vegetable oil that can be refined

---

## Single Period Model

This model is simplified by only considering a single period - there is no storage of oils from one period to the next.

### Decision Variables

All decision variables are continuous and non-negative.

- $`x_o`$: tons of raw oil $`o \in \mathcal{O}`$ refined in the period  
- $`y`$: tons of final blended product produced

---

### Objective Function

Maximize total profit, defined as revenue from the final product minus raw oil purchase costs:

```math
\max \;
p \cdot y
\;-\;
\sum_{o \in \mathcal{O}} c_o \cdot x_o
```

---

### Constraints

#### 1. Production Capacity Constraints

Vegetable and non-vegetable oils must be processed on separate production lines with limited capacity.

**Vegetable oils:**
```math
\sum_{o \in \mathcal{O}_{\text{V}}} x_o
\;\le\;
M_V
```

**Non-vegetable oils:**
```math
\sum_{o \in \mathcal{O}_{\text{N}}} x_o
\;\le\;
M_N
```

---

#### 2. Mass Balance Constraint

All refined oil is blended into the final product. No waste or loss occurs.

```math
\sum_{o \in \mathcal{O}} x_o = y
```

---

#### 3. Hardness Constraints

The hardness of the blended product is a linear weighted average of the component oils and must lie within specified bounds.

**Lower bound:**
```math
\sum_{o \in \mathcal{O}} h_o \cdot x_o
\;\ge\;
\underline{H} \cdot y
```

**Upper bound:**
```math
\sum_{o \in \mathcal{O}} h_o \cdot x_o
\;\le\;
\overline{H} \cdot y
```

---

#### 4. Non-Negativity

```math
x_o \ge 0 \quad \forall o \in \mathcal{O}
```
```math
y \ge 0
```

---

### Notation to Pyomo Mapping

| Mathematical Symbol | Description                              | Pyomo Name / Structure        |
|--------------------|------------------------------------------|-------------------------------|
| $`\mathcal{O}`$  | Set of raw oils                           | `model.O`                     |
| $`\mathcal{O}_{\text{V}}`$ | Vegetable oils subset            | `model.O_VEG`                 |
| $`\mathcal{O}_{\text{N}}`$ | Non-vegetable oils subset        | `model.O_NON`                 |
| $`x_o`$          | Tons of oil $o$ refined                | `model.x[o]`                  |
| $`y`$            | Final product output                     | `model.prod`      |
| $`c_o`$| Cost per ton of oil                      | `model.cost[o]`               |
| $`p`$ | Selling price per ton                    | `model.price`                 |
| $`h_o`$ | Hardness of oil $o$             | `model.hardness[o]`           |
| $`\underline{H}`$| Minimum blend hardness                   | `model.hardness_min`           |
| $`\overline{H}`$ | Maximum blend hardness                   | `model.hardness_max`           |
| $`M_V`$ | Veg processing capacity        | `model.production_cap['VEG']` |
| $`M_N`$ | Non-veg processing capacity    | `model.production_cap['NON']` |

---

### Notes on Implementation

- Oil categories are represented as **subsets**, not logic inside constraints.
- Hardness constraints remain linear due to the mass balance equation.
- This single-period model forms the foundation for the multi-period model with inventory and storage costs.

## Multi-Period Model

We will now consider what happens when we are optimizing for multiple period planning, for example, each month between January and June.

### Additional Sets

Let the following additional sets be defined.

$`\mathcal{T}`$ = set of time periods

```math
\mathcal{T} = \{\text{Jan}, \text{Feb}, \text{Mar}, \text{Apr}, \text{May}, \text{Jun}\}
```

---

### Additional Parameters

All additional parameters are known constants.

- $`\ell_o`$: holding cost per ton of oil $`o \in \mathcal{O}`$
- $`\overline{R}_o`$: maximum storage (in tons) allowed for oil $`o \in \mathcal{O}`$
- $`c_{t,o}`$: cost of buying oil $`o \in \mathcal{O}`$ in period  $`t \in \mathcal{T}`$

---

### Decision Variables

All decision variables are continuous and non-negative.

- $`B_{t,o}`$: tons of raw oil $`o \in \mathcal{O}`$ bought in period $`t \in \mathcal{T}`$
- $`S_{t,o}`$: tons of raw oil $`o \in \mathcal{O}`$ stored in period $`t \in \mathcal{T}`$
- $`U_{t,o}`$: tons of raw oil $`o \in \mathcal{O}`$ refined (used) in period $`t \in \mathcal{T}`$
- $`y_t`$: tons of final blended product produced in period $`t \in \mathcal{T}`$

---

### Objective Function

Maximize total profit, defined as revenue from the final product minus raw oil purchase costs minus storage costs:

```math
\max \;
p \cdot \sum_{t \in \mathcal{T}} y_t
\;-\;
\sum_{t \in \mathcal{T}} \sum_{o \in \mathcal{O}} c_{t,o} \cdot B_{t,o}
\;-\;
\sum_{t \in \mathcal{T}} \sum_{o \in \mathcal{O}} \ell_{o} \cdot S_{t,o}
```

---

### Constraints

#### 1. Production Capacity Constraints

Vegetable and non-vegetable oils must be processed on separate production lines with limited capacity.

**Vegetable oils:**
```math
\sum_{o \in \mathcal{O}_{\text{V}}} U_{t,o}
\;\le\;
M_V
\quad \forall t \in \mathcal{T}
```

**Non-vegetable oils:**
```math
\sum_{o \in \mathcal{O}_{\text{N}}} U_{t,o}
\;\le\;
M_N
\quad \forall t \in \mathcal{T}
```

---

#### 2. Mass Balance Constraint

No waste or loss occurs - the previous period's stored oil plus the raw oils bought must equal what is used and stored in the current period.

```math
S_{t-1,o} + B_{t,o} = S_{t,o} + U_{t,o}
\quad \forall t \in \mathcal{T},\ o \in \mathcal{O}
```

Additionally, the sum of oils used in each period must equal the output for that period.

```math
\sum_{o \in \mathcal{O}} U_{t,o} = y_t
\quad \forall t \in \mathcal{T}
```

---

#### 3. Hardness Constraints

The hardness of the blended product is a linear weighted average of the component oils and must lie within specified bounds.

**Lower bound:**
```math
\sum_{o \in \mathcal{O}} h_o \cdot U_{t,o}
\;\ge\;
\underline{H} \cdot y_t
\quad \forall t \in \mathcal{T}
```

**Upper bound:**
```math
\sum_{o \in \mathcal{O}} h_o \cdot U_{t,o}
\;\le\;
\overline{H} \cdot y_t
\quad \forall t \in \mathcal{T}
```

---

#### 4. Storage capacity

We cannot store more than is allowed for any oil $`o`$ in any period $`t`$.

```math
S_{t,o} \le \overline{R}_o
\quad \forall t \in \mathcal{T},\ o \in \mathcal{O}
```

---

#### 5. Non-Negativity and Fixed Storage

The problem defines that we start with 500 tons of each oil in storage, and that we must end with 500 tons of each oil in storage.

```math
U_{t,o} \ge 0
\quad \forall t \in \mathcal{T},\ o \in \mathcal{O}
```
```math
B_{t,o} \ge 0
\quad \forall t \in \mathcal{T},\ o \in \mathcal{O}
```
```math
S_{t,o} \ge 0
\quad \forall t \in \mathcal{T},\ o \in \mathcal{O}
```
```math
y_t \ge 0 \quad \forall t \in \mathcal{T}
```
```math
S_{0,o} = S_{6,o} = 500 \quad \forall o \in \mathcal{O}
```

---

### Notation to Pyomo Mapping

| Mathematical Symbol | Description                              | Pyomo Name / Structure        |
|--------------------|------------------------------------------|-------------------------------|
| $`\mathcal{O}`$  | Set of raw oils                               | `model.O`                     |
| $`\mathcal{T}`$  | Set of time periods                           | `model.T`                     |
| $`\mathcal{O}_{\text{V}}`$ | Vegetable oils subset               | `model.O_VEG`                 |
| $`\mathcal{O}_{\text{N}}`$ | Non-vegetable oils subset           | `model.O_NON`                 |
| $`U_{t,o}`$          | Tons of oil $o$ refined in period $t$     | `model.u[o]`                  |
| $`B_{t,o}`$          | Tons of oil $o$ bought in period $t$      | `model.b[o]`                  |
| $`S_{t,o}`$          | Tons of oil $o$ stored in period $t$      | `model.s[o]`                  |
| $`y_t`$            | Final product output in period $t$          | `model.prod`      |
| $`c_{t,o}`$    | Cost per ton of oil $o$ in period $t$           | `model.cost[o]`               |
| $`p`$ | Selling price per ton                    | `model.price`                 |
| $`h_o`$ | Hardness of oil $o$             | `model.hardness[o]`           |
| $`\underline{H}`$| Minimum blend hardness                   | `model.hardness_min`           |
| $`\overline{H}`$ | Maximum blend hardness                   | `model.hardness_max`           |
| $`M_V`$ | Veg processing capacity        | `model.production_cap['VEG']` |
| $`M_N`$ | Non-veg processing capacity    | `model.production_cap['NON']` |
| $`\ell_o`$ | storage (holding) cost per ton of oil $o$ per period             | `model.storage_cost[o]`         |
| $`\overline{R}_o`$ | maximum storage capacity for oil $o$        | `model.storage_cap[o]`         |

---