

from pathlib import Path
from domain.enum.writting_method import WrittingMethod


class TempFileWritter:


    def write_content_in_file(self, content: str, file: Path, method: WrittingMethod = WrittingMethod.Append) -> None:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        return
        