# El algoritmo simplex.

# Aquí irá:

# pivoteo
# iteraciones
# solución óptima

# RESUELVE EL PROBLEMA DE PROGRAMACIÓN LINEAL.

import numpy as np


class SimplexSolver:

    def __init__(self, objective, constraints):

        self.objective = objective
        self.constraints = constraints
        self.num_variables = len(objective)
        self.num_constraints = len(constraints)

        # Al iniciar el simplex, si las restricciones son <=,
        # las variables básicas iniciales son las holguras S1, S2, S3...
        self.basic_variables = [
            f"S{i + 1}" for i in range(self.num_constraints)
        ]

        self.tableau = None

    def create_tableau(self):

        rows = self.num_constraints + 1
        cols = self.num_variables + self.num_constraints + 1

        tableau = np.zeros((rows, cols))

        # Restricciones
        for i, constraint in enumerate(self.constraints):

            coeffs = constraint["coefficients"]
            rhs = constraint["rhs"]

            tableau[i, :self.num_variables] = coeffs

            # Variable de holgura
            tableau[i, self.num_variables + i] = 1

            # Lado derecho
            tableau[i, -1] = rhs

        # Función objetivo
        # Para maximización se colocan negativos los coeficientes
        tableau[-1, :self.num_variables] = -np.array(self.objective)

        self.tableau = tableau

    def get_variable_name(self, column_index):

        # Si la columna pertenece a las variables originales
        if column_index < self.num_variables:
            return f"X{column_index + 1}"

        # Si la columna pertenece a variables de holgura
        slack_index = column_index - self.num_variables
        return f"S{slack_index + 1}"

    def is_optimal(self):

        last_row = self.tableau[-1, :-1]

        # En maximización, cuando ya no hay negativos en la fila Z,
        # la solución actual es óptima
        return np.all(last_row >= 0)

    def get_pivot_column(self):

        last_row = self.tableau[-1, :-1]

        # Entra la variable con el coeficiente más negativo
        return np.argmin(last_row)

    def get_pivot_row(self, pivot_col):

        ratios = []

        for i in range(self.num_constraints):

            element = self.tableau[i, pivot_col]

            if element > 0:
                ratio = self.tableau[i, -1] / element
            else:
                ratio = np.inf

            ratios.append(ratio)

        # Sale la variable con la menor razón positiva
        return np.argmin(ratios)

    def pivot(self, pivot_row, pivot_col):

        pivot_element = self.tableau[pivot_row, pivot_col]

        # Convertir el pivote en 1
        self.tableau[pivot_row] = (
            self.tableau[pivot_row] / pivot_element
        )

        # Convertir en 0 los demás elementos de la columna pivote
        for i in range(len(self.tableau)):

            if i != pivot_row:

                factor = self.tableau[i, pivot_col]

                self.tableau[i] = (
                    self.tableau[i]
                    - factor * self.tableau[pivot_row]
                )

    def solve(self):

        self.create_tableau()

        iterations = []

        # Guardamos el tablero inicial
        iterations.append(self.tableau.copy())

        while not self.is_optimal():

            pivot_col = self.get_pivot_column()

            pivot_row = self.get_pivot_row(pivot_col)

            # Actualizamos la variable básica de la fila pivote.
            # La variable que entra reemplaza a la que sale.
            self.basic_variables[pivot_row] = self.get_variable_name(pivot_col)

            self.pivot(pivot_row, pivot_col)

            # Guardamos cada tablero después del pivoteo
            iterations.append(self.tableau.copy())

        solution = np.zeros(self.num_variables)

        # Extraemos la solución final de las columnas básicas
        for j in range(self.num_variables):

            column = self.tableau[:, j]

            if np.count_nonzero(column[:-1]) == 1 and np.sum(column[:-1]) == 1:

                row = np.where(column[:-1] == 1)[0][0]

                solution[j] = self.tableau[row, -1]

        optimal_value = self.tableau[-1, -1]

        return {
            "solution": solution,
            "optimal_value": optimal_value,
            "tableau": self.tableau,
            "iterations": iterations,
            "basic_variables": self.basic_variables
        }