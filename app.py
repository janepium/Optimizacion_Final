#La interfaz Streamlit.

#Aquí van:

#botones
#formularios
#tablas
#navegación

import streamlit as st
import pandas as pd
from simplex.parser import build_problem

st.set_page_config(page_title="Simplex Optimizer", layout="wide")

st.title("📈 Simplex Optimizer")
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

if st.button("Resolver Problema"):

    problem_data = build_problem(
        problem_type,
        objective_coeffs,
        constraints
    )

    st.success("Problema cargado correctamente")

    st.subheader("Resumen del Problema")

    st.write("### Tipo")
    st.write(problem_data["type"])

    st.write("### Función Objetivo")
    st.write(problem_data["objective"])

    st.write("### Restricciones")

    constraints_df = pd.DataFrame(problem_data["constraints"])
    st.dataframe(constraints_df)