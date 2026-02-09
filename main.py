import streamlit as st
import pandas as pd
import numpy as np
from engine import calcular_metricas
from report_gen import generar_pdf

# 1. Configuración de Marca (Tu nombre y proyecto)
st.set_page_config(page_title="Geolog Intelligence Hub", layout="wide")
st.title("📊 Geolog Intelligence Hub")
st.markdown("### Consultoría Técnica: David Jose Lopez Ramirez")

# 2. Barra Lateral (Inputs)
st.sidebar.header("Panel de Control")
archivo = st.sidebar.file_uploader("Cargar archivo real (CSV)", type="csv")
diametro = st.sidebar.number_input("Diámetro de Mecha (pulg)", value=8.5)

st.sidebar.markdown("---")
# BOTÓN DE DEMO: Si no tienes archivos a mano
boton_demo = st.sidebar.button("🚀 Activar Modo Demo (Presentación)")

# 3. Lógica de Selección de Datos
df = None

if archivo:
    df = pd.read_csv(archivo)
    st.sidebar.success("✅ Archivo real cargado")
elif boton_demo:
    # Generamos datos inventados pero realistas para mostrar el potencial
    filas = 100
    df = pd.DataFrame({
        'DEPTH': np.linspace(2000, 2100, filas),
        'WOB': np.random.uniform(15, 25, filas),
        'RPM': np.random.uniform(80, 120, filas),
        'TORQ': np.random.uniform(5, 15, filas),
        'ROP': np.random.uniform(20, 40, filas),
        'TGAS': np.random.uniform(0.5, 2.0, filas)
    })
    # Insertamos fallas para que la demo se vea interesante
    df.loc[70:80, 'TGAS'] = df.loc[70:80, 'TGAS'] * 8 # Simulamos un Kick
    df.loc[40:50, 'ROP'] = df.loc[40:50, 'ROP'] * 0.3 # Simulamos desgaste de mecha
    df.loc[40:50, 'TORQ'] = df.loc[40:50, 'TORQ'] * 3
    st.sidebar.info("💡 Mostrando datos de simulación")

# 4. Procesamiento de Datos (Lo que ya teníamos antes)
if df is not None:
    # Traducción automática de columnas (Sinónimos)
    traduccion = {
        'RPM': ['SURF_RPM', 'ROT', 'RPM_SURF', 'ROTACION'],
        'ROP': ['ROP_AVG', 'VEL_PERF', 'RATE_OF_PENETRATION'],
        'DEPTH': ['PROF', 'HOLE_DEPTH', 'BIT_DEPTH'],
        'WOB': ['WEIGHT', 'PESO', 'CARGA'],
        'TORQ': ['TORQUE', 'TORSION'],
        'TGAS': ['GAS', 'TOTAL_GAS', 'GAS_TOT']
    }

    # Limpiar y renombrar
    df.columns = [c.strip().upper() for c in df.columns]
    for oficial, sinonimos in traduccion.items():
        for col in df.columns:
            if col in sinonimos or col == oficial:
                df.rename(columns={col: oficial}, inplace=True)

    # Ejecutar el motor de engine.py
    df_res = calcular_metricas(df, diametro)

    # 5. Visualización Profesional (Lo que ve el cliente)
    st.write("### Análisis de Operación en Tiempo Real")
    c1, c2, c3 = st.columns(3)
    c1.metric("Profundidad Actual", f"{df_res['DEPTH'].max()} m")
    
    if 'MSE' in df_res.columns and not df_res['MSE'].isnull().all():
        c2.metric("Eficiencia MSE", f"{int(df_res['MSE'].mean())} psi")
        st.subheader("Gráfico de Energía Específica Mecánica (MSE)")
        st.line_chart(df_res.set_index('DEPTH')['MSE'])
    else:
        c2.metric("Eficiencia MSE", "N/A")
        st.warning("⚠️ Faltan datos de TORQ o RPM para calcular MSE.")

    c3.metric("Riesgo detectado", "ALTO" if df_res['Alerta_Gas'].any() else "BAJO")

    # Botón de PDF
    st.markdown("---")
    if st.button("📄 Descargar Reporte para Cliente"):
        alertas = df_res[df_res['Alerta_Gas'] == True]
        pdf_bytes = generar_pdf(alertas)
        st.download_button("Bajar PDF", data=pdf_bytes, file_name="Reporte_Geolog.pdf")
else:
    st.info("👋 David, carga un archivo CSV o presiona 'Activar Modo Demo' para comenzar la presentación.")
    # --- SECCIÓN DE CRÉDITOS Y CONTACTO ---
st.markdown("---")
with st.expander("ℹ️ Información del Desarrollador y Propiedad Intelectual"):
    st.write("""
    Desarrollador Principal: David Jose Lopez Ramirez  
    DNI: 96048982  
    Proyecto: Geolog Surface Logging Analytics  
    Versión: 1.0.0 (Febrero 2026)
    
    Este software ha sido desarrollado como una herramienta de optimización para la industria del Oil & Gas. 
    Todos los algoritmos de cálculo de MSE y detección de riesgos son propiedad del desarrollador.
    
    Para consultoría técnica o licencias corporativas, contactar al desarrollador.
    """)
    
