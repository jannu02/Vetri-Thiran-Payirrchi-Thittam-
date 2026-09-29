from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from backend.ai.gemini_generator import GeminiDocumentGenerator
from backend.schemas import DocumentRequest, DocumentResponse, ExportRequest
from backend.services.docx_formatter import format_docx
from backend.services.html_formatter import format_html_preview
from backend.services.pdf_formatter import format_pdf
from backend.services.txt_formatter import format_txt

router = APIRouter()


@router.post("/generate", response_model=DocumentResponse, tags=["documents"])
def generate_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()
        content = generator.generate(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date.isoformat(),
        )
        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            html_preview=format_html_preview(content),
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}",
        ) from exc


@router.post("/export/{file_format}", tags=["documents"])
def export_document(file_format: str, request: ExportRequest):
    normalized = file_format.lower().strip()

    try:
        if normalized == "txt":
            data = format_txt(request.content)
            media_type = "text/plain; charset=utf-8"
            extension = "txt"
        elif normalized == "docx":
            data = format_docx(request.content, request.document_type)
            media_type = (
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
            extension = "docx"
        elif normalized == "pdf":
            data = format_pdf(request.content, request.document_type)
            media_type = "application/pdf"
            extension = "pdf"
        else:
            raise HTTPException(
                status_code=400,
                detail="Supported formats are: txt, docx, pdf.",
            )

        filename = f"legalease_document.{extension}"
        return Response(
            content=data,
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {exc}",
        ) from exc
