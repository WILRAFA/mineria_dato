import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="University Dashboard", layout="wide")

st.title("University Student Analytics Dashboard")

# Cargar datos
data = pd.read_csv("university_student_data.csv")

# Eliminar espacios en los nombres de columnas
data.columns = data.columns.str.strip()

# Mostrar columnas disponibles (opcional para depuración)
st.sidebar.write("Columnas encontradas:")
st.sidebar.write(list(data.columns))

st.sidebar.header("Filtros")

# Filtro Año
year = st.sidebar.multiselect(
    "Year",
    options=data["Year"].unique(),
    default=data["Year"].unique()
)

# Filtro Term
term = st.sidebar.multiselect(
    "Term",
    options=data["Term"].unique(),
    default=data["Term"].unique()
)

# Filtrado inicial
filtered = data[
    (data["Year"].isin(year)) &
    (data["Term"].isin(term))
]

# Verificar si existe Department
if "Department" in data.columns:

    department = st.sidebar.multiselect(
        "Department",
        options=data["Department"].unique(),
        default=data["Department"].unique()
    )

    filtered = filtered[
        filtered["Department"].isin(department)
    ]

# Métricas
col1, col2, col3 = st.columns(3)

col1.metric(
    "Retention Avg",
    round(filtered["Retention_Rate"].mean(), 2)
)

col2.metric(
    "Satisfaction Avg",
    round(filtered["Satisfaction_Score"].mean(), 2)
)

col3.metric(
    "Total Students",
    int(filtered["Enrolled_Students"].sum())
)

# Gráfico 1
st.subheader("Retention Rate Over Time")

fig1, ax1 = plt.subplots()

ret = (
    filtered.groupby("Year")["Retention_Rate"]
    .mean()
    .reset_index()
)

sns.lineplot(
    data=ret,
    x="Year",
    y="Retention_Rate",
    marker="o",
    ax=ax1
)

st.pyplot(fig1)

# Gráfico 2
st.subheader("Student Satisfaction")

fig2, ax2 = plt.subplots()

sat = (
    filtered.groupby("Year")["Satisfaction_Score"]
    .mean()
    .reset_index()
)

sns.barplot(
    data=sat,
    x="Year",
    y="Satisfaction_Score",
    ax=ax2
)

st.pyplot(fig2)

# Gráfico 3
st.subheader("Spring vs Fall")

fig3, ax3 = plt.subplots()

term_data = (
    filtered.groupby("Term")["Enrolled_Students"]
    .sum()
    .reset_index()
)

ax3.pie(
    term_data["Enrolled_Students"],
    labels=term_data["Term"],
    autopct="%1.1f%%"
)

st.pyplot(fig3)