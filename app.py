import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuración profesional
st.set_page_config(page_title="Executive People Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    np.random.seed(42)
    count = 500
    depts = ['Sales', 'IT', 'HR', 'Marketing', 'Operations', 'Finance']
    
    data = {
        'Employee_ID': range(1, count + 1),
        'Department': np.random.choice(depts, count),
        'Age': np.random.randint(22, 60, count),
        'Gender': np.random.choice(['F', 'M', 'Non-binary'], count, p=[0.48, 0.48, 0.04]),
        'Tenure_Years': np.random.uniform(0.5, 15, count).round(1),
        'Satisfac_Level': np.random.uniform(1, 5, count).round(1),
        'Last_Performance_Score': np.random.randint(1, 6, count),
        'Training_Hours': np.random.randint(10, 100, count),
        'Salary_K': np.random.randint(30, 120, count),
        'Left_Company': np.random.choice([0, 1], count, p=[0.82, 0.18])
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR ---
st.sidebar.header("🎯 Talent Strategy Filters")
dept_filter = st.sidebar.multiselect("Department", df['Department'].unique(), default=df['Department'].unique())
filtered_df = df[df['Department'].isin(dept_filter)]

# --- HEADER ---
st.title("🚀 Executive People Analytics Dashboard")
st.markdown("### Strategic Insight: Talent Retention & Performance Correlation")

# --- METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Headcount", len(filtered_df))
m2.metric("Turnover Rate", f"{(filtered_df['Left_Company'].mean()*100):.1f}%")
m3.metric("Avg Performance", f"{filtered_df['Last_Performance_Score'].mean():.1f}/5")
m4.metric("Avg Salary", f"${filtered_df['Salary_K'].mean():.1f}K")

st.divider()

# --- VISUALIZATIONS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Training vs. Performance (ROI)")
    # Gráfico de burbujas para ver 3 dimensiones: Horas, Desempeño y Salario
    fig1 = px.scatter(filtered_df, x="Training_Hours", y="Last_Performance_Score", 
                     size="Salary_K", color="Department", hover_name="Employee_ID",
                     trendline="ols", # Línea de tendencia (IA/Estadística)
                     title="Impact of Training on Employee Performance")
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Satisfaction & Attrition Analysis")
    # Histograma para ver la distribución de satisfacción entre los que se van y se quedan
    fig2 = px.histogram(filtered_df, x="Satisfac_Level", color="Left_Company", 
                       marginal="rug", barmode="overlay",
                       labels={"Left_Company": "Attrition (1=Yes)"},
                       title="Employee Satisfaction Distribution")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- ADVANCED: CORRELATION HEATMAP ---
st.subheader("🔗 Feature Correlation Matrix")
corr = df[['Age', 'Tenure_Years', 'Satisfac_Level', 'Last_Performance_Score', 'Training_Hours', 'Salary_K', 'Left_Company']].corr()
fig3 = px.imshow(corr, text_auto=True, aspect="auto", 
                color_continuous_scale='RdBu_r', 
                title="Identifying Key Drivers of Turnover")
st.plotly_chart(fig3, use_container_width=True)

st.info("**Data Scientist Note:** The heatmap above uses Pearson correlation to identify which variables (like Satisfaction or Salary) are most strongly linked to an employee leaving the company.")
