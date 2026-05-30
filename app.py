import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="University Dashboard", layout="wide")

st.title("University Student Analytics Dashboard")

data = pd.read_csv("university_student_data.csv")

st.sidebar.header("Filtros")

year = st.sidebar.multiselect(
    "Year",
    data['Year'].unique(),
    default=data['Year'].unique()
)

term = st.sidebar.multiselect(
    "Term",
    data['Term'].unique(),
    default=data['Term'].unique()
)

department = st.sidebar.multiselect(
    "Department",
    data['Department'].unique(),
    default=data['Department'].unique()
)

filtered = data[
    (data['Year'].isin(year)) &
    (data['Term'].isin(term)) &
    (data['Department'].isin(department))
]

col1, col2, col3 = st.columns(3)

col1.metric("Retention Avg", round(filtered['Retention_Rate'].mean(),2))
col2.metric("Satisfaction Avg", round(filtered['Satisfaction_Score'].mean(),2))
col3.metric("Total Students", int(filtered['Enrolled_Students'].sum()))

st.subheader("Retention Rate Over Time")

fig1, ax1 = plt.subplots()
ret = filtered.groupby('Year')['Retention_Rate'].mean().reset_index()
sns.lineplot(data=ret, x='Year', y='Retention_Rate', marker='o', ax=ax1)
st.pyplot(fig1)

st.subheader("Student Satisfaction")

fig2, ax2 = plt.subplots()
sat = filtered.groupby('Year')['Satisfaction_Score'].mean().reset_index()
sns.barplot(data=sat, x='Year', y='Satisfaction_Score', ax=ax2)
st.pyplot(fig2)

st.subheader("Spring vs Fall")

fig3, ax3 = plt.subplots()
term_data = filtered.groupby('Term')['Enrolled_Students'].sum().reset_index()
ax3.pie(term_data['Enrolled_Students'], labels=term_data['Term'], autopct='%1.1f%%')
st.pyplot(fig3)
