
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración
st.set_page_config(
    page_title="University Dashboard",
    layout="wide"
)

st.title("University Student Analytics Dashboard")

# Cargar dataset
df = pd.read_csv("university_student_data.csv")

# Eliminar espacios accidentales en nombres de columnas
df.columns = df.columns.str.strip()

# Sidebar
st.sidebar.header("Filters")

years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

terms = st.sidebar.multiselect(
    "Select Terms",
    options=df["Term"].unique(),
    default=df["Term"].unique()
)

# Filtrado
filtered_df = df[
    (df["Year"].isin(years)) &
    (df["Term"].isin(terms))
]

# Si no hay datos
if filtered_df.empty:
    st.warning("No data available with selected filters.")
    st.stop()

# KPIs
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()
total_enrolled = filtered_df["Enrolled"].sum()

col1.metric(
    "Average Retention",
    f"{avg_retention:.1f}%"
)

col2.metric(
    "Average Satisfaction",
    f"{avg_satisfaction:.1f}%"
)

col3.metric(
    "Total Enrolled",
    f"{int(total_enrolled)}"
)

# Opciones visuales
st.subheader("Visualization Settings")

colA, colB = st.columns(2)

with colA:
    show_grid = st.checkbox(
        "Show Grid",
        value=True
    )

with colB:
    line_color = st.color_picker(
        "Choose Line Color",
        "#1f77b4"
    )

# Gráfico 1
st.subheader("Retention Rate Trends")

fig1, ax1 = plt.subplots(figsize=(10, 5))

sns.lineplot(
    data=filtered_df,
    x="Year",
    y="Retention Rate (%)",
    hue="Term",
    marker="o",
    ax=ax1
)

ax1.grid(show_grid)
ax1.set_title("Retention Rate Over Time")

st.pyplot(fig1)

# Gráfico 2
st.subheader("Student Satisfaction")

fig2, ax2 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=filtered_df,
    x="Year",
    y="Student Satisfaction (%)",
    hue="Term",
    ax=ax2
)

ax2.grid(show_grid)

st.pyplot(fig2)

# Gráfico 3
st.subheader("Department Enrollment")

dept_data = filtered_df[
    [
        "Engineering Enrolled",
        "Business Enrolled",
        "Arts Enrolled",
        "Science Enrolled"
    ]
].sum()

fig3, ax3 = plt.subplots(figsize=(7, 7))

ax3.pie(
    dept_data,
    labels=dept_data.index,
    autopct="%1.1f%%"
)

st.pyplot(fig3)

# Tabs
tab1, tab2 = st.tabs(
    ["Filtered Data", "Complete Dataset"]
)

with tab1:
    st.dataframe(
        filtered_df.reset_index(drop=True),
        use_container_width=True
    )

with tab2:
    st.dataframe(
        df,
        use_container_width=True
    )

# Footer
st.caption(
    "Interactive dashboard created with Streamlit for university data analysis."
)