import html
import re


def format_html_preview(text: str) -> str:
    escaped = html.escape(text.strip())

    # Convert simple Markdown-like headings and numbered section headings.
    escaped = re.sub(
        r"(?m)^# (.+)$",
        r"<h1>\1</h1>",
        escaped,
    )
    escaped = re.sub(
        r"(?m)^## (.+)$",
        r"<h2>\1</h2>",
        escaped,
    )

    paragraphs = []
    for block in re.split(r"\n\s*\n", escaped):
        block = block.strip()
        if not block:
            continue
        if block.startswith("<h1>") or block.startswith("<h2>"):
            paragraphs.append(block)
        else:
            paragraphs.append(
                "<p>" + block.replace("\n", "<br>") + "</p>"
            )

    body = "\n".join(paragraphs)
    return f"""
<article class="legal-document">
{body}
</article>
""".strip()
