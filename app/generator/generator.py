from abc import ABC 

class Generator(ABC):
    system_prompt: str

    def generate(self) -> None:
        ...