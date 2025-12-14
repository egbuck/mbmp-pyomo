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

Let the following sets be defined.

### Raw oils

$$
\mathcal{O}
=
\{\text{VEG\_1},\ \text{VEG\_2},\ \text{OIL\_1},\ \text{OIL\_2},\ \text{OIL\_3}\}
$$

### Vegetable oils

$$
\mathcal{O}_{\text{VEG}}
\subset
\mathcal{O}
$$

$$
\mathcal{O}_{\text{VEG}}
=
\{\text{VEG\_1},\ \text{VEG\_2}\}
$$

### Non-vegetable oils

$$
\mathcal{O}_{\text{NON}}
\subset
\mathcal{O}
$$

$$
\mathcal{O}_{\text{NON}}
=
\{\text{OIL\_1},\ \text{OIL\_2},\ \text{OIL\_3}\}
$$

---

## Parameters

All parameters are known constants.

- $cost_{o}$  
  Purchase cost per ton of oil $o$

- $price$  
  Selling price per ton of final product

- $hardness_{o}$  
  Hardness value of oil $o$

- $H_{min}$  
  Minimum allowable hardness of the blended product

- $H_{max}$  
  Maximum allowable hardness of the blended product

- $cap_{\text{VEG}}$  
  Maximum tons of vegetable oil that can be refined

- $cap_{\text{NON}}$  
  Maximum tons of non-vegetable oil that can be refined

---

## Decision Variables

All decision variables are continuous and non-negative.

- $x_{o}$  
  Tons of raw oil $o$ refined during the period

- $y$  
  Tons of final blended product produced

---

## Objective Function

Maximize total profit, defined as revenue from selling the final product minus the cost of raw oils.

$$
\max
\quad
price \cdot y
-
\sum_{o \in \mathcal{O}} cost_{o} \cdot x_{o}
$$

---

## Constraints

### Production Capacity Constraints

Vegetable and non-vegetable oils must be processed on separate production lines with limited capacity.

#### Vegetable oils

$$
\sum_{o \in \mathcal{O}_{\text{VEG}}} x_{o}
\le
cap_{\text{VEG}}
$$

#### Non-vegetable oils

$$
\sum_{o \in \mathcal{O}_{\text{NON}}} x_{o}
\le
cap_{\text{NON}}
$$

---

### Mass Balance Constraint

All refined oil is blended into the final product.

$$
\sum_{o \in \mathcal{O}} x_{o}
=
y
$$

---

### Hardness Constraints

The hardness of the blended product is a linear weighted average of the component oils and must lie within specified bounds.

#### Lower bound

$$
\sum_{o \in \mathcal{O}} hardness_{o} \cdot x_{o}
\ge
H_{min} \cdot y
$$

#### Upper bound

$$
\sum_{o \in \mathcal{O}} hardness_{o} \cdot x_{o}
\le
H_{max} \cdot y
$$

---

### Non-Negativity Constraints

$$
x_{o} \ge 0
\quad
\forall o \in \mathcal{O}
$$

$$
y \ge 0
$$

---

## Notation to Pyomo Mapping

| Mathematical Symbol | Description | Pyomo Name |
|--------------------|-------------|------------|
| $\mathcal{O}$ | Set of raw oils | `model.O` |
| $\mathcal{O}_{\text{VEG}}$ | Vegetable oils | `model.O_VEG` |
| $\mathcal{O}_{\text{NON}}$ | Non-vegetable oils | `model.O_NON` |
| $x_{o}$ | Tons of oil refined | `model.x[o]` |
| $y$ | Final product output | `model.prod` |
| $cost_{o}$ | Oil cost | `model.cost[o]` |
| $price$ | Product price | `model.price` |
| $hardness_{o}$ | Oil hardness | `model.hardness[o]` |
| $H_{min}$ | Minimum hardness | `model.hardness_lb` |
| $H_{max}$ | Maximum hardness | `model.hardness_ub` |
| $cap_{\text{VEG}}$ | Veg capacity | `model.production_cap['VEG']` |
| $cap_{\text{NON}}$ | Non-veg capacity | `model.production_cap['NON']` |

---

## Notes on Implementation

- Oil categories are represented as explicit subsets of the oil set.
- Hardness constraints remain linear due to the mass balance equation.
- This single-period formulation serves as the foundation for the multi-period inventory model.

