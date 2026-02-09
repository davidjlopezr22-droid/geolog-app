from fpdf import FPDF

def generar_pdf(df_res):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado con tu marca personal
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "GEOLOG SURFACE LOGGING ANALYTICS", ln=True, align='C')
    pdf.set_font("Arial", '', 11)
    pdf.cell(200, 7, "Consultor Tecnico: David Jose Lopez Ramirez", ln=True, align='C')
    pdf.cell(200, 7, "DNI: 96048982", ln=True, align='C')
    pdf.ln(10)

    # Resumen Tecnico
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Resumen del Intervalo Analizado:", ln=True)
    pdf.set_font("Arial", '', 11)
    
    prof_max = df_res['DEPTH'].max() if 'DEPTH' in df_res.columns else "N/D"
    mse_avg = int(df_res['MSE'].mean()) if 'MSE' in df_res.columns else 0
    
    pdf.cell(200, 8, f"- Profundidad Maxima: {prof_max} m", ln=True)
    pdf.cell(200, 8, f"- Eficiencia Mecanica Promedio (MSE): {mse_avg} psi", ln=True)
    
    # Alertas
    if 'ALERTA_GAS' in df_res.columns and df_res['ALERTA_GAS'].any():
        pdf.set_text_color(255, 0, 0)
        pdf.cell(200, 8, "- ESTADO: Se detectaron anomalias criticas de gas.", ln=True)
        pdf.set_text_color(0, 0, 0)
    else:
        pdf.cell(200, 8, "- ESTADO: Operacion dentro de parametros normales.", ln=True)

    # Limpieza de caracteres para evitar errores de codificación
    return pdf.output(dest='S').encode('latin-1', 'ignore')
