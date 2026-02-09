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
    df = pd.read_csv(archivo)
    # Diccionario de traducción: "Lo que busca el código": ["Lo que puede decir el Excel"]
    traduccion = {
        'RPM': ['ROT', 'RPM_SURF', 'RPM_MEAS', 'VEL_ROT', 'ROTACION'],
        'DEPTH': ['PROF', 'HOLE_DEPTH', 'BIT_DEPTH', 'PROFUNDIDAD'],
        'WOB': ['WEIGHT', 'PESO', 'CARGA'],
        'TORQ': ['TORQUE', 'TORSION'],
        'ROP': ['VEL_PERF', 'RATE_OF_PENETRATION'],
        'TGAS': ['GAS', 'TOTAL_GAS', 'GAS_TOT']
    }

    # Esta lógica renombra automáticamente si encuentra un sinónimo
    for oficial, sinonimos in traduccion.items():
        for col in df.columns:
            if col.upper() in sinonimos or col.upper() == oficial:
                df.rename(columns={col: oficial}, inplace=True)
    # Limpiamos los nombres (quita espacios y pone todo en mayúsculas)
    df.columns = [c.strip().upper() for c in df.columns]
    
    # ESTO ES NUEVO: Te mostrará en la pantalla qué columnas encontró
    st.write("### Columnas detectadas en tu archivo:")
    st.info(f"{list(df.columns)}")
    
    # Definimos lo que necesitamos
    columnas_necesarias = ['DEPTH', 'WOB', 'RPM', 'TORQ', 'ROP', 'TGAS']
    
    # Verificamos qué falta
    faltantes = [col for col in columnas_necesarias if col not in df.columns]
    
    if not faltantes:
        try:
            df_res = calcular_metricas(df, diametro)
            st.success("✅ Datos procesados con éxito")
            # ... (aquí sigue el resto de tu código de gráficos)
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
    else:
        st.error(f"❌ Error: Faltan las siguientes columnas: {faltantes}")
        st.warning("Debes renombrar las columnas en tu CSV original para que coincidan.")
    
    
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
