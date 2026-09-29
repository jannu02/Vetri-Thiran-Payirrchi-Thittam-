from io import BytesIO
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


def format_docx(text: str, doc_type: str) -> bytes:
    document = Document()

    section = document.sections[0]
    section.top_margin = Pt(54)
    section.bottom_margin = Pt(54)
    section.left_margin = Pt(54)
    section.right_margin = Pt(54)

    styles = document.styles
    styles["Normal"].font.name = "Arial"
    styles["Normal"].font.size = Pt(10.5)

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(doc_type.upper())
    run.bold = True
    run.font.size = Pt(16)

    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("# "):
            p = document.add_heading(line[2:].strip(), level=1)
            continue

        if line.startswith("## "):
            p = document.add_heading(line[3:].strip(), level=2)
            continue

        numbered = re.match(r"^(\d+[\.\)]|\d+\.\d+)\s+(.+)$", line)
        if numbered:
            p = document.add_heading(line, level=2)
            continue

        p = document.add_paragraph(line)
        p.paragraph_format.space_after = Pt(6)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Generated with LegalEase").italic = True

    output = BytesIO()
    document.save(output)
    return output.getvalue()
