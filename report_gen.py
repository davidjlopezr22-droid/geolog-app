from fpdf import FPDF

def generar_pdf(df_alertas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Reporte de Inteligencia Geológica", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Anomalías de Gas Detectadas:", ln=True)

    for index, row in df_alertas.iterrows():
        pdf.cell(200, 8, txt=f"Profundidad: {row['DEPTH']}m - Gas: {row['TGAS']}%", ln=True)

    return pdf.output(dest='S').encode('latin-1')
