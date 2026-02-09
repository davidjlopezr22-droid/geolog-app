import streamlit as st
import pandas as pd
import numpy as np
from engine import calcular_metricas
from report_gen import generar_pdf

st.set_page_config(page_title="Geolog Intelligence Hub", layout="wide")
st.title("📊 Geolog Intelligence Hub")
st.markdown("### Consultoria: David Jose Lopez Ramirez")

# --- FUNCION ANTIDUPLICADOS ---
def limpiar_columnas(columnas):
    finales = []
    conteo = {}
    for c in columnas:
        nombre = str(c).split('.')[0].strip().upper()
        if not nombre: nombre = "COL"
        if nombre in conteo:
            conteo[nombre] += 1
            finales.append(f"{nombre}_{conteo[nombre]}")
        else:
            conteo[nombre] = 0
            finales.append(nombre)
    return finales

# --- SIDEBAR ---
st.sidebar.header("Configuracion")
archivo = st.sidebar.file_uploader("Cargar Archivo (LAS o CSV)", type=["csv", "txt"])
diametro = st.sidebar.number_input("Diametro Mecha (pulg)", value=8.5)
st.sidebar.markdown("---")
modo_demo = st.sidebar.checkbox("🚀 Activar Modo Demo")

df = None

# --- CARGA DE DATOS ---
if archivo:
    try:
        raw = archivo.getvalue().decode("utf-8").splitlines()
        linea_a = next((i for i, l in enumerate(raw) if l.startswith('~A')), -1)
        archivo.seek(0)
        
        if linea_a != -1: # Es un LAS
            df = pd.read_csv(archivo, sep='\s+', skiprows=linea_a + 1, header=None)
            curvas = [l.split('.')[0].strip().upper() for l in raw if '.' in l and l[0].isalpha()][:len(df.columns)]
            df.columns = limpiar_columnas(curvas)
        else: # Es un CSV
            df = pd.read_csv(archivo)
            df.columns = limpiar_columnas(df.columns)
    except Exception as e:
        st.error(f"Error al cargar archivo: {e}")

elif modo_demo:
    # Generacion de datos ficticios profesionales
    size = 100
    df = pd.DataFrame({
        'DEPTH': np.arange(2000, 2000 + size),
        'WOB': np.random.uniform(15, 25, size),
        'ROPA': np.random.uniform(20, 40, size),
        'GASTOTAL': np.random.uniform(10, 100, size)
    })
    df.loc[40:50, 'GASTOTAL'] = 800 # Simulacion de Kick
    st.sidebar.info("Utilizando datos de demostracion")

# --- PROCESAMIENTO ---
if df is not None:
    df_res = calcular_metricas(df, diametro)

    # Indicadores Clave
    c1, c2, c3 = st.columns(3)
    c1.metric("Profundidad Actual", f"{df_res['DEPTH'].max() if 'DEPTH' in df_res.columns else 'N/D'} m")
    c2.metric("MSE Promedio", f"{int(df_res['MSE'].mean())} psi")
    c3.metric("Riesgo", "ALTO" if df_res['ALERTA_GAS'].any() else "BAJO")

    # Grafico y PDF
    st.subheader("Analisis de Eficiencia Mecanica")
    if 'DEPTH' in df_res.columns:
        st.line_chart(df_res.set_index('DEPTH')['MSE'])

    if st.button("📄 Generar y Descargar Reporte PDF"):
        pdf_bytes = generar_pdf(df_res)
        st.download_button("⬇️ Descargar PDF", data=pdf_bytes, file_name="Reporte_Geolog.pdf", mime="application/pdf")

    st.dataframe(df_res.head(20))
else:
    st.info("Hola David. Sube un archivo o activa el 'Modo Demo' para ver el analisis.")

st.markdown("---")
st.caption("Propiedad Intelectual: David Jose Lopez Ramirez | DNI: 96048982")

    
