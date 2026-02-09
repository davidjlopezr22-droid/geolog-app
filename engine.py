import numpy as np
import streamlit as st

def calcular_metricas(df, diametro_mecha):
    # 1. Definimos los nombres estándar que busca el motor
    # Nota: Estos nombres vienen de la limpieza que hacemos en main.py
    col_wob = 'WOB'
    col_rop = 'ROPA' # En tu archivo de prueba se llama ROPA
    col_rpm = 'RPM'
    col_tgas = 'TGAS'

    # 2. Lógica de Alerta de Gas (Propiedad de David López)
    if col_tgas in df.columns:
        # Simulamos una alerta si el gas sube abruptamente (ej. > 5 veces el promedio)
        promedio_gas = df[col_tgas].mean()
        df['Alerta_Gas'] = df[col_tgas] > (promedio_gas * 3)
    else:
        df['Alerta_Gas'] = False

    # 3. Cálculo Seguro de MSE (Mechanical Specific Energy)
    # Verificamos si existen las columnas mínimas para no lanzar KeyError
    if col_wob in df.columns and col_rop in df.columns:
        # Cálculo básico de carga sobre mecha
        df['MSE'] = (4 * df[col_wob]) / (np.pi * (diametro_mecha**2))
        
        # Si también hay rotación y torque, se añade el componente rotacional
        if col_rpm in df.columns and 'TORQ' in df.columns:
            df['MSE'] += (480 * df[col_rpm] * df['TORQ']) / ((diametro_mecha**2) * df[col_rop])
            
        st.success("✅ Análisis técnico de MSE completado.")
    else:
        # Si faltan datos, creamos la columna en 0 para que los gráficos no fallen
        df['MSE'] = 0
        st.warning(f"⚠️ MSE no calculado: El archivo no contiene '{col_wob}' o '{col_rop}'.")
        
    return df
