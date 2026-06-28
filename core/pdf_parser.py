import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file):
    try:
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""

        for page in doc:
            text += page.get_text() + "\n"

        return text.strip()

    except Exception as e:
        return f"PDF parsing error: {str(e)}"