# report_generator.py
from fpdf import FPDF

def generate_pdf(report_data, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="EngineMind Diagnostic Report", ln=True)
    for k, v in report_data.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
    pdf.output(filename)
