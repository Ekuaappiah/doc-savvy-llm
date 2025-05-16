import os
import pymupdf
from docx import Document
import re


def clean_text(text: str) -> str:
    """
    Cleans extracted text by removing excessive whitespace,
    fixing hyphenation, and removing non-printable characters.
    """
    # Remove non-printable characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Replace multiple newlines with a single newline
    text = re.sub(r'\n{2,}', '\n', text)

    # Remove excess spaces and tabs
    text = re.sub(r'[ \t]+', ' ', text)

    # Fix broken hyphenated words at line breaks: "hyphen-\nbreak" -> "hyphenbreak"
    text = re.sub(r'-\s*\n\s*', '', text)

    # Convert multiple spaces/newlines into clean paragraph breaks
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    return text.strip()


def parse_file(file_path: str) -> str:
    """
    Dispatch function to handle different file types and clean the text.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        raw_text = extract_text_from_docx(file_path)
    elif ext == ".txt":
        raw_text = extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return clean_text(raw_text)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from PDF using PyMuPDF.
    """
    text = ""
    with pymupdf.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()


def extract_text_from_docx(docx_path: str) -> str:
    """
    Extracts text from DOCX using python-docx.
    """
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def extract_text_from_txt(txt_path: str) -> str:
    """
    Reads plain text files.
    """
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read().strip()

