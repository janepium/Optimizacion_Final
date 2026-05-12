#El algoritmo simplex.

#Aquí irá:

#pivoteo
#iteraciones
#solución óptima

#RESUELVE EL PROBLEMA DE PROGRAMACIÓN LINEAL.
import numpy as np


class SimplexSolver:

    def __init__(self, objective, constraints):

        self.objective = objective
        self.constraints = constraints

        self.num_variables = len(objective)
        self.num_constraints = len(constraints)

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

            tableau[i,
                    self.num_variables + i] = 1

            tableau[i, -1] = rhs

        # Función objetivo
        tableau[-1, :self.num_variables] = -self.objective

        self.tableau = tableau

    def is_optimal(self):

        last_row = self.tableau[-1, :-1]

        return np.all(last_row >= 0)

    def get_pivot_column(self):

        last_row = self.tableau[-1, :-1]

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

        return np.argmin(ratios)

    def pivot(self, pivot_row, pivot_col):

        pivot_element = self.tableau[pivot_row, pivot_col]

        self.tableau[pivot_row] = (
            self.tableau[pivot_row] / pivot_element
        )

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

        iterations.append(self.tableau.copy())

        while not self.is_optimal():

            pivot_col = self.get_pivot_column()

            pivot_row = self.get_pivot_row(pivot_col)

            self.pivot(pivot_row, pivot_col)

            iterations.append(self.tableau.copy())

        solution = np.zeros(self.num_variables)

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
            "iterations": iterations
        }