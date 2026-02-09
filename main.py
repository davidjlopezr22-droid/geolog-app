import streamlit as st
import pandas as pd
import numpy as np
from engine import calcular_metricas
# from report_gen import generar_pdf # Asegúrate de tener este archivo o coméntalo si no lo usas

# 1. Configuración de Marca
st.set_page_config(page_title="Geolog Intelligence Hub", layout="wide")
st.title("📊 Geolog Intelligence Hub")
st.markdown("### Consultoría Técnica: David Jose Lopez Ramirez")

# 2. Barra Lateral (Inputs)
st.sidebar.header("Panel de Control")
archivo = st.sidebar.file_uploader("Cargar archivo (CSV o LAS)", type=["csv", "txt"])
diametro = st.sidebar.number_input("Diámetro de Mecha (pulg)", value=8.5)

st.sidebar.markdown("---")
boton_demo = st.sidebar.button("🚀 Activar Modo Demo (Presentación)")

df = None

# 3. Lógica de Carga de Datos (Soporta Formato LAS y CSV normal)
if archivo:
    try:
        # Leemos el contenido para detectar el formato
        raw_content = archivo.getvalue().decode("utf-8").splitlines()
        data_start = 0
        col_names = []

        # Buscamos la sección de datos (~A) y nombres de curvas (~C)
        for i, line in enumerate(raw_content):
            if line.startswith('~C'):
                j = i + 1
                while j < len(raw_content) and not raw_content[j].startswith('~'):
                    c_line = raw_content[j].strip()
                    if c_line:
                        name = c_line.split('.')[0].split()[0] # Extrae 'ROPA' de 'ROPA.m/h'
                        col_names.append(name.upper())
                    j += 1
            if line.startswith('~A'):
                data_start = i + 1
                break

        archivo.seek(0) # Resetear puntero
        if data_start > 0:
            # Es un archivo LAS (como PRUEVA 1)
            df = pd.read_csv(archivo, sep='\s+', skiprows=data_start, names=col_names)
        else:
            # Es un CSV estándar
            df = pd.read_csv(archivo)
        
        st.sidebar.success("✅ Archivo procesado correctamente")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

elif boton_demo:
    # Datos de simulación para presentaciones
    filas = 100
    df = pd.DataFrame({
        'DEPTH': np.linspace(2000, 2100, filas),
        'WOB': np.random.uniform(15, 25, filas),
        'RPM': np.random.uniform(80, 120, filas),
        'ROPA': np.random.uniform(20, 40, filas),
        'TGAS': np.random.uniform(0.5, 2.0, filas)
    })
    df.loc[70:80, 'TGAS'] = df.loc[70:80, 'TGAS'] * 8
    st.sidebar.info("💡 Modo Demo Activo")

# 4. Procesamiento y Normalización
if df is not None:
    # Traducción de sinónimos para mayor compatibilidad
    traduccion = {
        'RPM': ['SURF_RPM', 'ROT', 'RPM_SURF', 'ROTACION'],
        'ROPA': ['ROP', 'ROP_AVG', 'VEL_PERF', 'RATE_OF_PENETRATION'],
        'WOB': ['WEIGHT', 'PESO', 'CARGA', 'BIT_WEIGHT'],
        'TGAS': ['GAS', 'TOTAL_GAS', 'GAS_TOT', 'GASTOTAL']
    }

    df.columns = [c.strip().upper() for c in df.columns]
    for oficial, sinonimos in traduccion.items():
        for col in df.columns:
            if col in sinonimos:
                df.rename(columns={col: oficial}, inplace=True)

    # Llamada al motor de cálculos
    df_res = calcular_metricas(df, diametro)

    # 5. Visualización del Dashboard
    st.write("### Análisis de Operación - David José López Ramírez")
    
    col_d, col_m, col_r = st.columns(3)
    col_d.metric("Profundidad Máx", f"{df_res['DEPTH'].max() if 'DEPTH' in df_res.columns else 'N/A'} m")
    
    mse_val = int(df_res['MSE'].mean()) if 'MSE' in df_res.columns else 0
    col_m.metric("MSE Promedio", f"{mse_val} psi")
    
    riesgo = "ALTO" if df_res['Alerta_Gas'].any() else "BAJO"
    col_r.metric("Nivel de Riesgo", riesgo, delta_color="inverse")

    # Gráficos
    if 'MSE' in df_res.columns and df_res['MSE'].any():
        st.subheader("Tendencia de Energía Específica (MSE)")
        st.area_chart(df_res.set_index('DEPTH' if 'DEPTH' in df_res.columns else df_res.index)['MSE'])
    
    st.write("#### Datos Procesados")
    st.dataframe(df_res.head(10))
else:
    st.info("👋 Bienvenido David. Por favor carga un archivo para iniciar el análisis.")

# Créditos
st.markdown("---")
st.caption("Propiedad Intelectual: David Jose Lopez Ramirez | DNI: 96048982 | v1.2")
    
