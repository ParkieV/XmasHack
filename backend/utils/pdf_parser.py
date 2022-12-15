import os
import json
from backend.config import DATA_PATH
import pdfplumber


class PDFParser:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.file_path = os.path.join(DATA_PATH, self.file_name)

    def parse(self) -> dict:
        with pdfplumber.open(self.file_path) as pdf:
            text = pdf.pages[0].extract_text()
        with open(os.path.join(DATA_PATH, "classes.json"), "r") as file:
            json_file = json.loads(file.read())
        _class = json_file[self.file_name]
        _class = _class[_class.find('/') + 1:]
        res = {
                "file_id": self.file_name,
                "file_body": text,
                "file_class": _class
                }
        return res
