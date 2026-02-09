from fpdf import FPDF
import io

def generar_pdf(df_alertas):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado Profesional
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Reporte de Analitica: Geolog Surface Logging", ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "Consultor: David Jose Lopez Ramirez | DNI: 96048982", ln=True, align='C')
    pdf.ln(10)

    # Cuerpo del Reporte
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Resumen de Alertas y Operacion", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 11)
    if not df_alertas.empty:
        pdf.multi_cell(0, 10, f"Se han detectado {len(df_alertas)} eventos de interes (incrementos de gas o variaciones de eficiencia).")
        pdf.ln(5)
        # Listar las primeras profundidades con alerta
        profundidades = df_alertas['DEPTH'].head(10).tolist()
        pdf.multi_cell(0, 10, f"Profundidades criticas detectadas (m): {profundidades}")
    else:
        pdf.cell(200, 10, "No se detectaron anomalias criticas en el intervalo analizado.", ln=True)

    # Convertir a bytes para Streamlit
    return pdf.output(dest='S').encode('latin-1')
