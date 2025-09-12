from pathlib import Path
from xhtml2pdf import pisa
from domain.enum.writting_method import WrittingMethod


class TempFileWritter:

    def write_content_in_file(
        self, content: str, file: Path, method: WrittingMethod = WrittingMethod.Reset
    ) -> None:
        if method == WrittingMethod.Reset:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)

    def write_content_in_file_pdf(
        self, content: str, file: Path, method: WrittingMethod = WrittingMethod.Reset
    ) -> None:
        if method == WrittingMethod.Reset:
            with open(file, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(content, dest=pdf_file)
