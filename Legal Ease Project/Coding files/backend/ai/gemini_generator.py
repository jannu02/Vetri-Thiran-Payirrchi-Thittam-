from google import genai
from google.genai import types

from backend.config import settings


SYSTEM_INSTRUCTION = """
You are LegalEase, a careful legal-document drafting assistant.

Your task is to draft a structured legal document from the user's supplied
document type, parties, terms, and effective date.

Rules:
1. Do not invent party names, dates, amounts, addresses, obligations, or facts.
2. Preserve user-provided facts accurately.
3. If a legally important fact is missing, use a neutral placeholder such as
   [TO BE COMPLETED] rather than inventing it.
4. Produce a professional draft with a title and clear numbered sections.
5. Include appropriate general sections when useful, such as definitions,
   obligations, confidentiality, term, termination, notices, governing law,
   dispute resolution, amendments, and signatures. Only include sections that
   fit the document type.
6. Do not claim the document is legally valid in a particular jurisdiction.
7. Do not provide legal advice outside the requested draft.
8. Return plain text/Markdown-style content only. Do not wrap the entire answer
   in a code fence.
"""


class GeminiDocumentGenerator:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.gemini_model

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Add it to the .env file."
            )

        self.client = genai.Client(api_key=self.api_key)

    def build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        return f"""
Draft a {document_type}.

Document type:
{document_type}

Parties:
{parties}

Terms and conditions:
{terms}

Effective date:
{effective_date}

Return a complete, editable draft. Use a clear title, numbered headings,
clauses, and signature placeholders. Do not invent facts not supplied above.
"""

    def generate(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        prompt = self.build_prompt(
            document_type, parties, terms, effective_date
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                max_output_tokens=6000,
            ),
        )

        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty document.")

        if len(text) > settings.max_document_chars:
            text = text[: settings.max_document_chars]

        return text
