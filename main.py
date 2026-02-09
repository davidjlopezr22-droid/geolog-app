import streamlit as st
import pandas as pd
import numpy as np
from engine import calcular_metricas

# Configuración de Marca - David Jose Lopez Ramirez
st.set_page_config(page_title="Geolog Intelligence Hub", layout="wide")
st.title("📊 Geolog Intelligence Hub")
st.markdown("### Desarrollado por: David Jose Lopez Ramirez")

# Panel Lateral
st.sidebar.header("Configuración")
archivo = st.sidebar.file_uploader("Subir CSV o LAS", type=["csv", "txt"])
diametro = st.sidebar.number_input("Diámetro de Mecha (pulg)", value=8.5)
boton_demo = st.sidebar.button("🚀 Modo Demo")

df = None

# Procesamiento de Archivo
if archivo:
    try:
        # Detectar si es un archivo tipo LAS (como PRUEVA 1)
        content = archivo.getvalue().decode("utf-8").splitlines()
        skip = 0
        for i, line in enumerate(content):
            if line.startswith('~A'): # Los datos empiezan después de esta marca
                skip = i + 1
                break
        
        archivo.seek(0)
        df = pd.read_csv(archivo, sep='\s+', skiprows=skip) if skip > 0 else pd.read_csv(archivo)
        
        # LIMPIEZA DE COLUMNAS: Quita unidades y espacios (ej: 'ROPA.m/h' -> 'ROPA')
        df.columns = [c.split('.')[0].strip().upper() for c in df.columns]
        
        # Mapeo de sinónimos para que coincidan con engine.py
        mapeo = {'GASTOTAL': 'TGAS', 'ROP': 'ROPA', 'WEIGHT': 'WOB'}
        df.rename(columns=mapeo, inplace=True)
        
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

elif boton_demo:
    df = pd.DataFrame({
        'DEPTH': np.linspace(1000, 1100, 50),
        'WOB': np.random.uniform(10, 20, 50),
        'ROPA': np.random.uniform(15, 30, 50),
        'TGAS': np.random.uniform(1, 5, 50)
    })

# Ejecución y Visualización
if df is not None:
    # Llamar al motor corregido
    df_res = calcular_metricas(df, diametro)

    # Mostrar Métricas de forma segura (usando .get para evitar KeyErrors)
    c1, c2, c3 = st.columns(3)
    
    prof = df_res['DEPTH'].max() if 'DEPTH' in df_res.columns else "N/A"
    c1.metric("Profundidad", f"{prof} m")
    
    mse_avg = int(df_res['MSE'].mean()) if 'MSE' in df_res.columns else 0
    c2.metric("MSE Promedio", f"{mse_avg} psi")
    
    riesgo = "ALTO" if df_res['Alerta_Gas'].any() else "BAJO"
    c3.metric("Riesgo de Gas", riesgo)

    # Gráfico de MSE vs Profundidad
    if 'MSE' in df_res.columns and 'DEPTH' in df_res.columns:
        st.subheader("Gráfico de Energía Específica (MSE)")
        st.line_chart(df_res.set_index('DEPTH')['MSE'])

    st.write("#### Vista previa de datos procesados")
    st.dataframe(df_res.head())
else:
    st.info("David, carga el archivo para iniciar el análisis técnico.")

st.markdown("---")
st.caption("Propiedad de David Jose Lopez Ramirez | DNI: 96048982")
    
