import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración de página Global
st.set_page_config(page_title="Global People Analytics | Alejandro Álvarez", layout="wide")

@st.cache_data
def load_global_data():
    np.random.seed(42)
    count = 800  # Aumentamos la muestra para que el mapa se vea mejor
    
    # Datos geográficos y departamentos
    countries = ['Spain', 'Italy', 'Germany', 'USA', 'France', 'United Kingdom', 'Japan']
    depts = ['Sales', 'IT', 'HR', 'Marketing', 'Operations', 'Finance']
    
    data = {
        'Employee_ID': range(1, count + 1),
        'Country': np.random.choice(countries, count),
        'Department': np.random.choice(depts, count),
        'Age': np.random.randint(22, 62, count),
        'Gender': np.random.choice(['F', 'M', 'Non-binary'], count, p=[0.47, 0.48, 0.05]),
        'Tenure_Years': np.random.uniform(0.5, 12, count).round(1),
        'Satisfac_Level': np.random.uniform(1, 5, count).round(1),
        'Last_Performance_Score': np.random.randint(1, 6, count),
        'Training_Hours': np.random.randint(10, 120, count),
        'Salary_K': np.random.randint(35, 140, count),
        'Left_Company': np.random.choice([0, 1], count, p=[0.85, 0.15])
    }
    return pd.DataFrame(data)

df = load_global_data()

# --- NAVEGACIÓN LATERAL ---
st.sidebar.title("🌍 Global Workforce Filters")
selected_countries = st.sidebar.multiselect("Select Countries", df['Country'].unique(), default=df['Country'].unique())
selected_depts = st.sidebar.multiselect("Select Departments", df['Department'].unique(), default=df['Department'].unique())

filtered_df = df[(df['Country'].isin(selected_countries)) & (df['Department'].isin(selected_depts))]

# --- TÍTULO PRINCIPAL ---
st.title("🌐 Global People Analytics Strategy Dashboard")
st.markdown("Analysis of workforce distribution, compensation, and talent retention across international markets.")

# --- MÉTRICAS GENERALES ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Global Headcount", len(filtered_df))
m2.metric("Avg. Satisfaction", f"{filtered_df['Satisfac_Level'].mean():.2f} / 5")
m3.metric("Retention Rate", f"{((1 - filtered_df['Left_Company'].mean())*100):.1f}%")
m4.metric("Avg. Annual Salary", f"${filtered_df['Salary_K'].mean():.1f}K")

st.divider()

# --- FILA 1: MAPA Y DISTRIBUCIÓN ---
col_map, col_dist = st.columns([2, 1])

with col_map:
    st.subheader("Workforce Distribution by Country")
    # Agrupamos por país para el mapa
    map_data = filtered_df.groupby('Country').size().reset_index(name='Employee Count')
    fig_map = px.choropleth(map_data, locations="Country", locationmode='country names',
                            color="Employee Count", hover_name="Country",
                            color_continuous_scale="Viridis",
                            title="Global Presence")
    st.plotly_chart(fig_map, use_container_width=True)

with col_dist:
    st.subheader("Gender Diversity")
    fig_pie = px.pie(filtered_df, names='Gender', hole=0.4, title="Workforce Composition")
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# --- FILA 2: COMPENSACIÓN Y PERFORMANCE ---
col_sal, col_perf = st.columns(2)

with col_sal:
    st.subheader("Compensation Analysis by Country")
    fig_box = px.box(filtered_df, x="Country", y="Salary_K", color="Country",
                     title="Salary Distribution per Region")
    st.plotly_chart(fig_box, use_container_width=True)

with col_perf:
    st.subheader("Training vs Performance (by Department)")
    fig_scatter = px.scatter(filtered_df, x="Training_Hours", y="Last_Performance_Score",
                             size="Salary_K", color="Department",
                             hover_data=['Country'], trendline="ols",
                             title="How Training impacts KPI achievement")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- NOTA TÉCNICA ---
st.info("💡 **Insight for HR Leaders:** Use the country filter to compare how 'Training Hours' correlate with 'Performance' in different cultural contexts.")
