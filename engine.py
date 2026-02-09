import numpy as np
import streamlit as st

def calcular_metricas(df, diametro_mecha):
    # Inicializamos si no existen
    if 'MSE' not in df.columns:
        df['MSE'] = 0.0
    if 'ALERTA_GAS' not in df.columns:
        df['ALERTA_GAS'] = False

    # Buscadores flexibles de columnas
    col_wob = next((c for c in df.columns if 'WOB' in c), None)
    col_rop = next((c for c in df.columns if 'ROPA' in c or 'ROP' in c), None)
    col_tgas = next((c for c in df.columns if 'GASTOTAL' in c or 'TGAS' in c), None)

    # Alerta de Gas
    if col_tgas and col_tgas in df.columns:
        media = df[col_tgas].mean()
        df['ALERTA_GAS'] = df[col_tgas] > (media * 3)

    # Cálculo de MSE
    if col_wob and col_rop:
        mask = (df[col_rop] > 0) & (df[col_wob].notnull())
        df.loc[mask, 'MSE'] = (4 * df.loc[mask, col_wob]) / (np.pi * (diametro_mecha**2))
        
    return df
