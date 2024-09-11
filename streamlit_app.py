import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df_meteo = pd.read_csv('/mnt/data/df_meteo.csv')
conso_jour = pd.read_csv('/mnt/data/conso_jour.csv')
df_conso_clean = pd.read_csv('/mnt/data/df_conso_clean.csv')

# Page layout
st.set_page_config(page_title="Tableau de bord ENEDIS", layout="wide")

# Title
st.title("Tableau de bord interactif ENEDIS - Visualisation de la consommation et de la météo")

# Sidebar - Filters
st.sidebar.header("Filtres")
ville_selection = st.sidebar.selectbox("Sélectionnez une ville", df_meteo['Ville'].unique())
date_range = st.sidebar.date_input("Sélectionnez la période", [df_meteo['DATE'].min(), df_meteo['DATE'].max()])

# Filter data based on selection
df_meteo_filtered = df_meteo[(df_meteo['Ville'] == ville_selection) & 
                             (df_meteo['DATE'] >= str(date_range[0])) & 
                             (df_meteo['DATE'] <= str(date_range[1]))]

conso_filtered = conso_jour[(conso_jour['DATE'] >= str(date_range[0])) & 
                            (conso_jour['DATE'] <= str(date_range[1]))]

# Section 1 - Weather visualization
st.header(f"Visualisation Météo pour {ville_selection}")
fig_temp = px.line(df_meteo_filtered, x='DATE', y='MAX_TEMPERATURE_C', title="Température Maximale")
fig_precip = px.bar(df_meteo_filtered, x='DATE', y='PRECIP_TOTAL_DAY_MM', title="Précipitations journalières")

st.plotly_chart(fig_temp, use_container_width=True)
st.plotly_chart(fig_precip, use_container_width=True)

# Section 2 - Energy Consumption visualization
st.header("Visualisation de la consommation d'énergie")
fig_conso = px.line(conso_filtered, x='DATE', y='Consommation (Wh)', title="Consommation quotidienne d'énergie")
st.plotly_chart(fig_conso, use_container_width=True)

# Section 3 - Comparative Analysis
st.header("Analyse comparative")
fig_comparative = px.line(df_meteo_filtered, x='DATE', y='MAX_TEMPERATURE_C', color_discrete_sequence=['blue'], 
                          title="Température vs Consommation")
fig_comparative.add_scatter(x=conso_filtered['DATE'], y=conso_filtered['Consommation (Wh)'], mode='lines', 
                            name="Consommation", line=dict(color='red'))

st.plotly_chart(fig_comparative, use_container_width=True)


# Save the code as a Python file for running in Streamlit
with open("/mnt/data/streamlit_dashboard.py", "w") as file:
    file.write(dashboard_code)

# Provide confirmation and path
"/mnt/data/streamlit_dashboard.py has been created with the code."
