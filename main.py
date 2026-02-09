import streamlit as st
import pandas as pd
import numpy as np
from engine import calcular_metricas
from report_gen import generar_pdf

st.set_page_config(page_title="Geolog Intelligence Hub", layout="wide")
st.title("📊 Geolog Intelligence Hub")
st.markdown("### David Jose Lopez Ramirez | Consultoría Oil & Gas")

archivo = st.sidebar.file_uploader("Subir Registro (LAS o CSV)", type=["csv", "txt"])
diametro = st.sidebar.number_input("Diámetro de Mecha (pulg)", value=8.5)

def desduplicar_columnas(columnas):
    resultado = []
    conteo = {}
    for col in columnas:
        col_limpia = str(col).split('.')[0].strip().upper()
        if not col_limpia: col_limpia = "COL"
        if col_limpia in conteo:
            conteo[col_limpia] += 1
            resultado.append(f"{col_limpia}_{conteo[col_limpia]}")
        else:
            conteo[col_limpia] = 0
            resultado.append(col_limpia)
    return resultado

if archivo:
    try:
        raw = archivo.getvalue().decode("utf-8").splitlines()
        linea_a = next((i for i, l in enumerate(raw) if l.startswith('~A')), -1)
        
        archivo.seek(0)
        if linea_a != -1:
            df = pd.read_csv(archivo, sep='\s+', skiprows=linea_a + 1, header=None)
            curvas = [l.split('.')[0].strip().upper() for l in raw if '.' in l and l[0].isalpha()]
            df.columns = desduplicar_columnas(curvas[:len(df.columns)])
        else:
            df = pd.read_csv(archivo)
            df.columns = desduplicar_columnas(df.columns)

        # Procesar datos con David's Engine
        df_res = calcular_metricas(df, diametro)

        # Dashboard
        c1, c2, c3 = st.columns(3)
        c1.metric("Profundidad Max", f"{df_res['DEPTH'].max() if 'DEPTH' in df_res.columns else 'N/A'} m")
        c2.metric("MSE Promedio", f"{int(df_res['MSE'].mean()) if 'MSE' in df_res.columns else 0} psi")
        
        tiene_alertas = 'ALERTA_GAS' in df_res.columns and df_res['ALERTA_GAS'].any()
        c3.metric("Riesgo", "ALTO" if tiene_alertas else "BAJO")

        # Botón de Descarga de PDF
        st.markdown("---")
        if st.button("📄 Generar Reporte PDF"):
            # Filtramos solo las filas con alerta para el reporte
            df_alertas = df_res[df_res['ALERTA_GAS'] == True] if 'ALERTA_GAS' in df_res.columns else pd.DataFrame()
            pdf_data = generar_pdf(df_alertas)
            st.download_button(label="⬇️ Descargar Reporte para Cliente", 
                               data=pdf_data, 
                               file_name="Reporte_Tecnico_Geolog.pdf", 
                               mime="application/pdf")

        st.dataframe(df_res.head(20))
    except Exception as e:
        st.error(f"Error en procesamiento: {e}")
else:
    st.info("👋 David, el sistema está listo. Carga un archivo para generar el análisis y el PDF.")

    
