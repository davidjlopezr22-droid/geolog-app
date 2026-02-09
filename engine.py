import numpy as np
import streamlit as st

def calcular_metricas(df, diametro_mecha):
    # 1. Definimos los nombres que el motor espera encontrar
    col_wob = 'WOB'
    col_rop = 'ROPA' 
    col_rpm = 'RPM'
    col_tgas = 'TGAS'

    # 2. INICIALIZACIÓN CRÍTICA: Creamos las columnas con valores base
    # Esto evita el KeyError si el archivo no tiene estos datos
    if 'MSE' not in df.columns:
        df['MSE'] = 0.0
    if 'Alerta_Gas' not in df.columns:
        df['Alerta_Gas'] = False

    # 3. Lógica de Alerta de Gas (Propiedad Intelectual: David López)
    if col_tgas in df.columns:
        promedio_gas = df[col_tgas].mean()
        # Alerta si el gas actual es 3 veces superior al promedio
        df['Alerta_Gas'] = df[col_tgas] > (promedio_gas * 3)

    # 4. Cálculo de MSE con validación de existencia de columnas
    if col_wob in df.columns and col_rop in df.columns:
        # Solo calculamos donde ROPA sea mayor a 0 para evitar errores matemáticos
        mask = df[col_rop] > 0
        df.loc[mask, 'MSE'] = (4 * df.loc[mask, col_wob]) / (np.pi * (diametro_mecha**2))
        
        # Si existen RPM y TORQUE, sumamos la parte rotacional del MSE
        if col_rpm in df.columns and 'TORQ' in df.columns:
            df.loc[mask, 'MSE'] += (480 * df.loc[mask, col_rpm] * df.loc[mask, 'TORQ']) / ((diametro_mecha**2) * df.loc[mask, col_rop])
        
        st.success("✅ Cálculos de eficiencia finalizados.")
    else:
        # Mensaje informativo para el usuario sin bloquear la App
        st.warning(f"⚠️ Nota: El archivo no contiene '{col_wob}' o '{col_rop}'. El cálculo de MSE se omitió.")
        
    return df
