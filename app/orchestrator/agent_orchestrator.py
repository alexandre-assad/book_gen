

from dataclasses import dataclass
from typing import Type
from app.generator.generator import Generator
from app.generator.personnal_development_generator import PersonnalDevelopmentGenerator
from app.generator.story_generator import StoryGenerator
from domain.enum.book_type import BookType
from domain.error.unhandled_map_key_error import UnhandledMapKeyError

@dataclass
class AgentOrchestrator:
    MAP_GENERATOR_BY_BOOK_TYPE: dict[BookType, Type[Generator]] = {BookType.Story : StoryGenerator, BookType.PersonnalDevelopment : PersonnalDevelopmentGenerator}

    def orchestrate(self, book_type: BookType) -> None:
        if book_type not in self.MAP_GENERATOR_BY_BOOK_TYPE:
            raise UnhandledMapKeyError(f"Cannot generator for this following book type : {book_type.value}")
        return self.MAP_GENERATOR_BY_BOOK_TYPE[book_type]().generate()