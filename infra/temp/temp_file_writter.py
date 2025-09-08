

from pathlib import Path
from domain.enum.writting_method import WrittingMethod


class TempFileWritter:


    def write_content_in_file(self, file: Path, method: WrittingMethod = WrittingMethod.Append) -> None:
        ...