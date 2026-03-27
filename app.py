import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la interfaz
st.set_page_config(page_title="HR Analytics Dashboard | Alejandro Álvarez", layout="wide")

st.title("📊 HR Talent Retention & Development Dashboard")
st.markdown("""
This dashboard analyzes the correlation between **Professional Development** and **Employee Retention**, 
supporting data-driven decisions in People Analytics.
""")

# Generación de Dataset Ficticio basado en tu proyecto de CV [cite: 14]
data = {
    'Employee_ID': range(1, 101),
    'Department': ['Sales', 'IT', 'HR', 'Marketing'] * 25,
    'Years_Experience': [2, 5, 1, 10, 3, 8, 4, 6] * 12 + [5, 2],
    'Training_Hours': [10, 40, 5, 50, 20, 35, 15, 45] * 12 + [30, 10],
    'Left_Company': [1, 0, 1, 0, 0, 0, 1, 0] * 12 + [0, 1] 
}
df = pd.DataFrame(data)

# Sidebar para filtros
st.sidebar.header("Data Filters")
selected_dept = st.sidebar.multiselect("Select Department", df['Department'].unique(), default=df['Department'].unique())
filtered_df = df[df['Department'].isin(selected_dept)]

# Métricas Principales
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Employees", len(filtered_df))
with col2:
    turnover = (filtered_df['Left_Company'].mean() * 100)
    st.metric("Turnover Rate", f"{turnover:.1f}%")
with col3:
    avg_training = filtered_df['Training_Hours'].mean()
    st.metric("Avg. Training Hours", f"{avg_training:.1f}h")

st.divider()

# Gráfico de Correlación (Punto clave de tu CV) [cite: 14]
st.subheader("Analysis: Training Hours vs. Retention")
fig = px.box(filtered_df, x="Left_Company", y="Training_Hours", 
             color="Left_Company",
             labels={"Left_Company": "Stayed (0) vs Left (1)", "Training_Hours": "Hours of Training"},
             color_discrete_map={0: "#2ecc71", 1: "#e74c3c"},
             points="all")

st.plotly_chart(fig, use_container_width=True)

st.info("💡 **Insight:** This visualization demonstrates how employees with more training hours tend to have higher retention rates.")
