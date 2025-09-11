

from app.generator.generator import Generator


class StoryGenerator(Generator):
    system_prompt: str = '...'

    def generate(self) -> None:
        ...