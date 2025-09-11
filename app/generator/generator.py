from dataclasses import dataclass, field

from pathlib import Path
from app.agent.content_generator_agent import ContentGeneratorAgent
from app.agent.plan_agent import PlanAgent
from domain.dataclass.book_state import BookState
from langgraph.graph import StateGraph, START

from domain.enum.book_type import BookType
from infra.temp.temp_file_writter import TempFileWritter

def aggregator(state: BookState) -> dict:
    results = state.get("results", [])
    ebook = "\n\n".join([r["content"] for r in results])
    return {"ebook": ebook}


class Generator:
    MAP_SYSTEM_PROMPT: dict[BookType, str] = {
        BookType.PersonnalDevelopment: """You are a professional writer and personal development expert with a clear, engaging, and motivational style.  
            Your task is to write a complete book (or e-book) on the topic given by the user.  

            Structure the book in a way that is accessible and inspiring for a general audience:  
            - Start with a powerful introduction that captures attention and explains the relevance of the topic.  
            - Divide the book into clear chapters, each covering one key idea or principle.  
            - Use practical examples, real-life stories, metaphors, and simple frameworks to make the concepts easy to understand.  
            - Provide actionable exercises, reflections, or step-by-step guidance at the end of chapters where appropriate.  
            - Maintain a tone that is positive, empowering, and practical, avoiding overly academic or abstract language.  
            - Conclude with a strong closing chapter that summarizes the key takeaways and inspires the reader to take action.  

            The output should be well-structured, formatted like a professional non-fiction book, and ready to be refined into a manuscript.
            """
    }

    def generate(self, prompt: str, book_type: BookType) -> None:
        builder = StateGraph(BookState)
        builder.add_node("plan_agent", PlanAgent().generate_by_state)
        builder.add_node("sequential_content_generator", ContentGeneratorAgent().generate)
        builder.add_node("aggregator", aggregator)

        builder.add_edge(START, "plan_agent")
        builder.add_edge("plan_agent", "sequential_content_generator")

        compiled = builder.compile()
        final_state = compiled.invoke({"brief": f"{self.MAP_SYSTEM_PROMPT[book_type]}\nUser brief : {prompt}"})
        TempFileWritter().write_content_in_file(final_state.get("ebook", "<no ebook>"), Path('tempfile/book.md'))


