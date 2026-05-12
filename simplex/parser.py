#Interpretar datos del usuario.

#Convertir inputs en matrices y vectores.

import numpy as np


def build_problem(problem_type, objective_coeffs, constraints):
    """
    Construye el problema de programación lineal.
    """

    objective = np.array(objective_coeffs)

    parsed_constraints = []

    for constraint in constraints:
        parsed_constraints.append({
            "coefficients": np.array(constraint["coeffs"]),
            "operator": constraint["operator"],
            "rhs": constraint["rhs"]
        })

    return {
        "type": problem_type,
        "objective": objective,
        "constraints": parsed_constraints
    }