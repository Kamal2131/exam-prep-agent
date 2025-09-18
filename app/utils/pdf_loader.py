import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_content: bytes) -> str:
    try:
        pdf_file = BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_parts = []
        for page in pdf_reader.pages:
            text_parts.append(page.extract_text())
        return ''.join(text_parts)
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"