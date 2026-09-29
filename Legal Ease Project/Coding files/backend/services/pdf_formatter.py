from io import BytesIO
import re

from fpdf import FPDF


class LegalPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 8, "LegalEase", align="L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def _safe(text: str) -> str:
    # Built-in Helvetica is Latin-1. Replace unsupported characters safely.
    return text.encode("latin-1", "replace").decode("latin-1")


def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = LegalPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 9, _safe(doc_type.upper()), align="C")
    pdf.ln(4)

    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            pdf.ln(2)
            continue

        if line.startswith("# "):
            pdf.set_font("Helvetica", "B", 14)
            pdf.multi_cell(0, 8, _safe(line[2:].strip()))
            continue

        if line.startswith("## ") or re.match(r"^\d+[\.\)]\s+", line):
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 7, _safe(line.lstrip("# ").strip()))
            continue

        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, _safe(line))

    return bytes(pdf.output())
