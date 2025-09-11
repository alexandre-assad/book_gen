

from dataclasses import dataclass
from typing import Type
from app.generator.generator import Generator
from domain.enum.book_type import BookType
from domain.error.unhandled_map_key_error import UnhandledMapKeyError

@dataclass
class AgentOrchestrator:

    def orchestrate(self, prompt: str, book_type: BookType) -> None:
        return Generator().generate(prompt, book_type)