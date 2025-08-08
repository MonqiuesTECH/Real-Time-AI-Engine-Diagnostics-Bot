from fpdf import FPDF
from datetime import datetime

def generate_pdf(report_data, filename="engine_report.pdf",
                 company="EngineMind", footer="Powered by ZARI — Confidential"):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, f"{company} – Diagnostic Report", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z", ln=True)
    pdf.ln(4)

    # Body
    pdf.set_font("Arial", "", 12)
    for k, v in report_data.items():
        pdf.cell(0, 8, f"{k}: {v}", ln=True)

    # Footer
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 10, footer, 0, 0, "C")

    pdf.output(filename)
