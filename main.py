import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Geolog AI Dashboard", layout="wide")

st.title("🚀 Geolog Analysis - Sistema de Optimización")
st.markdown("### Desarrollado por David Lopez")

# --- FUNCIÓN PARA GENERAR DATOS DE PRUEBA ---
def generar_datos_demo():
    rows = 500
    df = pd.DataFrame({
        'DEPTH': np.linspace(2000, 2500, rows),
        'WOB': np.random.uniform(15, 25, rows),
        'RPM': np.random.uniform(80, 110, rows),
        'TORQ': np.random.uniform(8, 12, rows),
        'ROP': np.random.uniform(20, 40, rows),
        'TGAS': np.random.uniform(0.5, 1.5, rows)
    })
    # Simulamos una falla de gas a los 2300m
    df.loc[300:320, 'TGAS'] = 12.0 
    # Simulamos una caída de eficiencia (Bit gastado) a los 2400m
    df.loc[400:430, 'ROP'] = df.loc[400:430, 'ROP'] * 0.5
    df.loc[400:430, 'TORQ'] = df.loc[400:430, 'TORQ'] * 2.0
    return df

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Entrada de Datos")
    modo = st.radio("Selecciona origen de datos:", ["Usar Datos Demo", "Subir mi propio CSV"])
    diametro = st.number_input("Diámetro de Mecha (pulg)", value=8.5)

# --- CARGA DE DATOS ---
if modo == "Subir mi propio CSV":
    archivo = st.file_uploader("Carga tu archivo de Geolog", type=['csv'])
    if archivo:
        df = pd.read_csv(archivo)
    else:
        st.warning("Esperando archivo... o selecciona 'Datos Demo' en la izquierda.")
        st.stop()
else:
    df = generar_datos_demo()
    st.success("Mostrando datos de simulación operativa.")

# --- LÓGICA DE INGENIERÍA ---
# Cálculo de MSE (Energía Específica Mecánica)
# Esto es lo que detecta si la mecha está rompiendo roca eficientemente
df['MSE'] = (4 * df['WOB']) / (np.pi * diametro) + (480 * df['RPM'] * df['TORQ']) / (diametro * df['ROP'])

# Alerta de Gas Crítico
gas_avg = df['TGAS'].mean()
df['Alerta_Gas'] = df['TGAS'] > (gas_avg * 3)

# --- DASHBOARD DE MÉTRICAS ---
col1, col2, col3 = st.columns(3)
col1.metric("ROP Promedio", f"{round(df['ROP'].mean(), 1)} m/h")
col2.metric("MSE Promedio", f"{round(df['MSE'].mean(), 0)} psi")
col3.metric("Zonas de Riesgo", int(df['Alerta_Gas'].sum()))

# --- GRÁFICOS INTERACTIVOS ---
st.subheader("Análisis de Rendimiento por Profundidad")

# Gráfico de ROP vs MSE
fig_perf = px.line(df, x='DEPTH', y=['ROP', 'MSE'], 
                  title="Eficiencia de Perforación (MSE) vs Tasa de Penetración (ROP)",
                  color_discrete_map={"ROP": "#00CC96", "MSE": "#EF553B"})
st.plotly_chart(fig_perf, use_container_width=True)

# Gráfico de Gas
st.subheader("Monitoreo de Gas en Tiempo Real")
fig_gas = px.area(df, x='DEPTH', y='TGAS', title="Niveles de Gas Total", color_discrete_sequence=['#AB63FA'])
st.plotly_chart(fig_gas, use_container_width=True)

# --- TABLA DE ALERTAS ---
if df['Alerta_Gas'].any():
    st.error("⚠️ ALERTAS DE GAS DETECTADAS")
    st.dataframe(df[df['Alerta_Gas'] == True][['DEPTH', 'TGAS']])

st.markdown("---")
st.caption("Herramienta de soporte a la decisión - Geolog Intelligence 2026")
