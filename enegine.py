import numpy as np

def calcular_metricas(df, diametro_mecha=8.5):
    # Cálculo de Energía Específica Mecánica (MSE)
    df['MSE'] = (4 * df['WOB']) / (np.pi * diametro_mecha**2) + \
                (480 * df['RPM'] * df['TORQ']) / (diametro_mecha**2 * df['ROP'])

    # Alerta de Gas (3x sobre el promedio móvil)
    df['Alerta_Gas'] = df['TGAS'] > (df['TGAS'].rolling(window=20).mean() * 3)

    # Detección de ineficiencia (MSE sube y ROP baja)
    df['Deterioro'] = (df['MSE'].diff() > 0) & (df['ROP'].diff() < 0)

    return df
