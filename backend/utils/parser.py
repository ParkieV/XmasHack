import os
import json
from backend.config import DATA_PATH
import pdfplumber
import aspose.words as aw


class FileParser:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.file_path = os.path.join(DATA_PATH, self.file_name)

    def get_doc_text(self) -> str:
        doc = aw.Document(self.file_name)
        return doc.get_text()

    def get_pdf_text(self) -> str:
        with pdfplumber.open(self.file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
            return text

    def parser_doc_docx_rtf(self) -> dict:
        res = {
                "file_id": self.file_name,
                "file_body": self.get_doc_text(),
                }
        return res

    def parse_pdf(self) -> dict:
        res = {
                "file_id": self.file_name,
                "file_body": self.get_pdf_text(),
                }
        return res

    def parse(self) -> dict:
        ext = self.file_name[-self.file_name.rfind('.'):]
        if ext == "pdf":
            return self.parse_pdf()
        elif ext in ["doc", "docx", "rtf"]:
            return self.parser_doc_docx_rtf()
        else:
            raise ValueError("Unexcepted file extension")

