import os
import PyPDF2
import docx
from pathlib import Path

class SystemService:
    def read_file_content(self, file_path: str) -> str:
        """Read content from PDF, DOCX, or TXT files"""
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return self._read_pdf(file_path)
        elif ext == '.docx':
            return self._read_docx(file_path)
        elif ext == '.txt':
            return self._read_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _read_pdf(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return ' '.join(page.extract_text() for page in reader.pages)

    def _read_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return ' '.join(paragraph.text for paragraph in doc.paragraphs)

    def _read_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

system_service = SystemService()
