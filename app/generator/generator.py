from abc import ABC 

class Generator(ABC):

    def generate(self) -> None:
        ...