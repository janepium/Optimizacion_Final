#La interfaz Streamlit.

#Aquí van:

#botones
#formularios
#tablas
#navegación

#RECOGE DATOS DEL USUARIO Y LOS PROCESA.

import streamlit as st
import pandas as pd

from simplex.parser import build_problem
from simplex.simplex_solver import SimplexSolver
from simplex.graphics import solve_graphical_method

st.set_page_config(page_title="Simplex Optimizer", layout="wide")

st.title("Simplex Optimizer")
st.write("Ingrese un problema de Programación Lineal")

# =========================
# CONFIGURACIÓN GENERAL
# =========================

problem_type = st.selectbox(
    "Tipo de problema",
    ["Maximizar", "Minimizar"]
)

num_variables = st.number_input(
    "Número de variables",
    min_value=2,
    max_value=10,
    value=2,
    step=1
)

num_constraints = st.number_input(
    "Número de restricciones",
    min_value=1,
    max_value=10,
    value=2,
    step=1
)

st.divider()

# =========================
# FUNCIÓN OBJETIVO
# =========================

st.subheader("Función Objetivo")

objective_coeffs = []

cols = st.columns(num_variables)

for i in range(num_variables):
    coeff = cols[i].number_input(
        f"X{i+1}",
        value=0.0,
        key=f"obj_{i}"
    )
    objective_coeffs.append(coeff)

st.latex(
    "Z = " + " + ".join(
        [f"{objective_coeffs[i]}x_{i+1}" for i in range(num_variables)]
    )
)

st.divider()

# =========================
# RESTRICCIONES
# =========================

st.subheader("Restricciones")

constraints = []

for r in range(num_constraints):
    st.markdown(f"### Restricción {r+1}")

    row = st.columns(num_variables + 2)

    coeffs = []

    for c in range(num_variables):
        value = row[c].number_input(
            f"X{c+1}",
            value=0.0,
            key=f"r{r}c{c}"
        )
        coeffs.append(value)

    operator = row[num_variables].selectbox(
        "Operador",
        ["<=", ">=", "="],
        key=f"op_{r}"
    )

    rhs = row[num_variables + 1].number_input(
        "Resultado",
        value=0.0,
        key=f"rhs_{r}"
    )

    constraints.append({
        "coeffs": coeffs,
        "operator": operator,
        "rhs": rhs
    })

st.divider()

# =========================
# BOTÓN RESOLVER
# =========================
def format_objective(objective, problem_type):
    terms = []

    for i, coefficient in enumerate(objective):
        terms.append(f"{coefficient}x{i+1}")

    return f"{problem_type} Z = " + " + ".join(terms)


def format_constraint(constraint):
    terms = []

    for i, coefficient in enumerate(constraint["coefficients"]):
        terms.append(f"{coefficient}x{i+1}")

    left_side = " + ".join(terms)

    return f"{left_side} {constraint['operator']} {constraint['rhs']}"

if st.button("Resolver Problema"):

    problem_data = build_problem(
        problem_type,
        objective_coeffs,
        constraints
    )

    solver = SimplexSolver(
        objective=problem_data["objective"],
        constraints=problem_data["constraints"]
    )

    result = solver.solve()

    st.success("Problema cargado correctamente")

    st.subheader("Resumen del Problema")

    st.write("### Tipo")
    st.write(problem_data["type"])

    st.write("### Función Objetivo")
    st.write(problem_data["objective"])

    st.write("### Restricciones")
    constraints_df = pd.DataFrame(problem_data["constraints"])
    st.dataframe(constraints_df)

    if num_variables == 2:
        st.subheader("Método gráfico paso a paso")

        graphical_result = solve_graphical_method(
            objective=problem_data["objective"],
            constraints=problem_data["constraints"],
            problem_type=problem_data["type"]
        )

        st.write("## Paso 1: Modelo ingresado")

        st.write("### Función objetivo")
        st.latex(format_objective(problem_data["objective"], problem_data["type"]))

        st.write("### Restricciones")
        for i, constraint in enumerate(problem_data["constraints"]):
            st.latex(f"R_{i+1}: " + format_constraint(constraint))

        st.write("## Paso 2: Rectas frontera")

        st.info(
            "Para aplicar el método gráfico, cada restricción se toma como una "
            "recta frontera. Por ejemplo, una restricción del tipo <= se grafica "
            "primero como igualdad y luego se identifica el lado factible."
        )

        for i, constraint in enumerate(problem_data["constraints"]):
            frontera = constraint.copy()
            frontera["operator"] = "="
            st.latex(f"R_{i+1}: " + format_constraint(frontera))

        st.write("## Paso 3: Vértices factibles encontrados")

        if graphical_result["vertices_table"].empty:
            st.error(
                "No se encontraron vértices factibles. "
                "El problema puede no tener región factible."
            )
        else:
            st.dataframe(graphical_result["vertices_table"])

            st.write("## Paso 4: Evaluación de la función objetivo")

            if problem_data["type"] == "Maximizar":
                criterio = "mayor"
            else:
                criterio = "menor"

            st.info(
                f"La columna Z de la tabla anterior muestra el valor de la función objetivo "
                f"evaluado en cada vértice factible. Como el problema es de "
                f"{problem_data['type'].lower()}, se selecciona el vértice con el "
                f"{criterio} valor de Z."
            )

            x1, x2 = graphical_result["optimal_point"]

            st.write("### Vértice seleccionado")
            st.latex(
                f"({x1:.2f}, {x2:.2f})"
            )

            st.write("### Valor de la función objetivo")
            st.latex(
                f"Z = {graphical_result['optimal_value']:.2f}"
            )

            st.write("## Paso 5: Conclusión")

            x1, x2 = graphical_result["optimal_point"]

            st.success(
                f"Por lo tanto, la solución óptima es producir/asignar "
                f"x1 = {x1:.2f} y x2 = {x2:.2f}, obteniendo "
                f"Z = {graphical_result['optimal_value']:.2f}."
            )

            st.write("## Paso 6: Gráfica de la región factible")

            st.pyplot(graphical_result["figure"])

    else:
        st.info("El método gráfico solo aplica para problemas con dos variables.")
        
    st.subheader("Resultado Óptimo")

    st.write("### Variables de decisión")

    for i, value in enumerate(result["solution"]):
        st.write(f"X{i+1} = {value:.2f}")

    st.write("### Valor Óptimo")
    st.success(f"Z = {result['optimal_value']:.2f}")

    st.subheader("Tableau Final")

    num_slack_variables = len(problem_data["constraints"])

    column_names = []

    for i in range(num_variables):
        column_names.append(f"X{i+1}")

    for i in range(num_slack_variables):
        column_names.append(f"S{i+1}")

    column_names.append("RHS")

    tableau_df = pd.DataFrame(
        result["tableau"],
        columns=column_names
    )

    row_names = result["basic_variables"] + ["Z"]
    tableau_df.index = row_names

    tableau_df.index = row_names

    st.dataframe(tableau_df)