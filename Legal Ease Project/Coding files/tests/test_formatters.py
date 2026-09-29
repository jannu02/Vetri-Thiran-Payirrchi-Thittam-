from docx import Document

from backend.services.docx_formatter import format_docx
from backend.services.html_formatter import format_html_preview
from backend.services.pdf_formatter import format_pdf
from backend.services.txt_formatter import format_txt


SAMPLE = """# NON-DISCLOSURE AGREEMENT

## 1. Confidentiality

Company A and Company B agree to protect confidential information.
"""


def test_txt_formatter():
    result = format_txt(SAMPLE)
    assert isinstance(result, bytes)
    assert b"NON-DISCLOSURE" in result


def test_html_formatter_escapes_html():
    result = format_html_preview("<script>alert(1)</script>")
    assert "<script>" not in result
    assert "&lt;script&gt;" in result


def test_docx_formatter_creates_valid_docx():
    result = format_docx(SAMPLE, "Non-Disclosure Agreement")
    path = "/tmp/test_legalease.docx"
    with open(path, "wb") as file:
        file.write(result)
    document = Document(path)
    assert "NON-DISCLOSURE AGREEMENT" in "\n".join(
        paragraph.text for paragraph in document.paragraphs
    )


def test_pdf_formatter_creates_pdf():
    result = format_pdf(SAMPLE, "Non-Disclosure Agreement")
    assert result.startswith(b"%PDF")
