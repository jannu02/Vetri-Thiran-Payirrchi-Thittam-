from datetime import date
from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=5000)
    terms: str = Field(..., min_length=2, max_length=15000)
    effective_date: date

    @field_validator("document_type", "parties", "terms")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    html_preview: str


class ExportRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    content: str = Field(..., min_length=1, max_length=30000)


class ErrorResponse(BaseModel):
    detail: str
