from dataclasses import dataclass
from app.generator.generator import Generator
from domain.enum.book_type import BookType


@dataclass
class AgentOrchestrator:

    def orchestrate(self, prompt: str, book_type: BookType) -> None:
        return Generator().generate(prompt, book_type)
