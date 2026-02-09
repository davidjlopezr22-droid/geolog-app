import streamlit as st
import pandas as pd
import numpy as np
from engine import calcular_metricas

st.set_page_config(page_title="Geolog Intelligence Hub", layout="wide")
st.title("📊 Geolog Intelligence Hub")
st.markdown("### David Jose Lopez Ramirez | Geolog Surface Logging")

archivo = st.sidebar.file_uploader("Subir Archivo (LAS o CSV)", type=["csv", "txt"])
diametro = st.sidebar.number_input("Diámetro de Mecha (pulg)", value=8.5)

def eliminar_columnas_duplicadas(df):
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique(): 
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]
    df.columns = cols
    return df

if archivo:
    try:
        contenido = archivo.getvalue().decode("utf-8").splitlines()
        linea_datos = 0
        nombres_curvas = []

        for i, linea in enumerate(contenido):
            if linea.startswith('~C'):
                j = i + 1
                while j < len(contenido) and not contenido[j].startswith('~'):
                    curva = contenido[j].strip().split('.')[0].split()[0]
                    if curva: nombres_curvas.append(curva.upper())
                    j += 1
            if linea.startswith('~A'):
                linea_datos = i + 1
                break
        
        archivo.seek(0)
        
        if linea_datos > 0:
            df = pd.read_csv(archivo, sep='\s+', skiprows=linea_datos, names=nombres_curvas if nombres_curvas else None)
        else:
            df = pd.read_csv(archivo)
            df.columns = [c.split('.')[0].strip().upper() for c in df.columns]

        # REGLA CRÍTICA: Eliminar duplicados antes de procesar
        df = eliminar_columnas_duplicadas(df)

        df_res = calcular_metricas(df, diametro)

        # Dashboard
        c1, c2, c3 = st.columns(3)
        prof = df_res['DEPTH'].max() if 'DEPTH' in df_res.columns else "N/A"
        c1.metric("Profundidad", f"{prof} m")
        
        mse_prom = int(df_res['MSE'].mean()) if 'MSE' in df_res.columns else 0
        c2.metric("MSE Promedio", f"{mse_prom} psi")
        
        alerta = "ALTO" if 'ALERTA_GAS' in df_res.columns and df_res['ALERTA_GAS'].any() else "BAJO"
        c3.metric("Riesgo detectado", alerta)

        if 'DEPTH' in df_res.columns and 'MSE' in df_res.columns:
            st.subheader("Visualización de Energía Específica")
            st.line_chart(df_res.set_index('DEPTH')['MSE'])
        
        st.write("#### Vista previa de datos")
        st.dataframe(df_res.head())

    except Exception as e:
        st.error(f"Error detectado: {e}")
else:
    st.info("👋 David, por favor carga el archivo para iniciar.")

st.markdown("---")
st.caption("Propiedad Intelectual: David Jose Lopez Ramirez | DNI: 96048982")
    
