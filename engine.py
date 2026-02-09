import numpy as np
import streamlit as st

def calcular_metricas(df, diametro_mecha):
    # Asegurar columnas base para que la interfaz no falle
    if 'MSE' not in df.columns: df['MSE'] = 0.0
    if 'ALERTA_GAS' not in df.columns: df['ALERTA_GAS'] = False

    # Buscadores flexibles
    col_wob = next((c for c in df.columns if 'WOB' in c), None)
    col_rop = next((c for c in df.columns if 'ROPA' in c or 'ROP' in c), None)
    col_gas = next((c for c in df.columns if 'GAS' in c), None)

    # 1. Calculo de Alerta de Gas
    if col_gas and col_gas in df.columns:
        umbral = df[col_gas].mean() * 3
        df['ALERTA_GAS'] = df[col_gas] > umbral

    # 2. Calculo de MSE (Formula de David Lopez)
    if col_wob and col_rop:
        mask = (df[col_rop] > 0)
        df.loc[mask, 'MSE'] = (4 * df.loc[mask, col_wob]) / (np.pi * (diametro_mecha**2))
    
    return df
