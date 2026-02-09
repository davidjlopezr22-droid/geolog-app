import streamlit as st
import pandas as pd
from engine import calcular_metricas
from report_gen import generar_pdf

# Configuración profesional
st.set_page_config(page_title="Geolog Analytics Pro", layout="wide")

st.title("📊 Geolog Intelligence Hub")
st.markdown("---")

# Barra lateral
st.sidebar.header("Configuración de Operación")
archivo = st.file_uploader("Cargar archivo de salida de Geolog (CSV)", type="csv")
diametro = st.sidebar.number_input("Diámetro de Mecha (pulgadas)", value=8.5)

if archivo:
    # Leer datos
    df = pd.read_csv(archivo)
    
    # Procesar con el motor que creamos en engine.py
    try:
        df_res = calcular_metricas(df, diametro)
        
        # Dashboard de métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("Profundidad Actual", f"{df_res['DEPTH'].max()} m")
        col2.metric("MSE Promedio", f"{int(df_res['MSE'].mean())} psi")
        col3.metric("Alertas Críticas", df_res['Alerta_Gas'].sum())

        # Gráfico de Eficiencia
        st.subheader("Análisis de Energía Específica (MSE)")
        st.line_chart(df_res.set_index('DEPTH')['MSE'])

        # Sección de Reporte
        st.markdown("---")
        if st.button("📄 Generar Reporte PDF para Cliente"):
            alertas = df_res[df_res['Alerta_Gas'] == True]
            pdf_bytes = generar_pdf(alertas)
            st.download_button(
                label="Descargar PDF",
                data=pdf_bytes,
                file_name=f"Reporte_Pozo_{df_res['DEPTH'].max()}m.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"Error en los datos: Asegúrate de que las columnas se llamen DEPTH, WOB, RPM, TORQ, ROP y TGAS. Error: {e}")

else:
    st.info("👋 David, carga un archivo CSV para activar el motor de inteligencia.")
