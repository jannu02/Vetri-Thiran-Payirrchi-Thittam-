from datetime import date

import pytest
from pydantic import ValidationError

from backend.schemas import DocumentRequest


def test_document_request_accepts_valid_data():
    request = DocumentRequest(
        document_type="Non-Disclosure Agreement",
        parties="Company A and Company B",
        terms="Confidential information must not be disclosed without authorization.",
        effective_date=date(2026, 10, 1),
    )
    assert request.document_type == "Non-Disclosure Agreement"


def test_document_request_rejects_empty_terms():
    with pytest.raises(ValidationError):
        DocumentRequest(
            document_type="Agreement",
            parties="A and B",
            terms="   ",
            effective_date=date(2026, 10, 1),
        )
