from domain.dataclass.book_state import BookState
from infra.model.gpt_4o_model import Gpt4oModel
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


class PlanAgent:
    def __init__(self) -> None:
        pass

    def generate_by_state(self, state: BookState) -> dict:
        schemas = [
            ResponseSchema(name="title", description="Book Title"),
            ResponseSchema(
                name="chapters",
                description="List of the chapters, each chapter is an object {id: str, title: str, summary: str, is_ghost: bool, number_words: int}",
            ),
        ]

        parser = StructuredOutputParser.from_response_schemas(schemas)
        format_instructions = parser.get_format_instructions()

        llm = Gpt4oModel().llm

        prompt = ChatPromptTemplate.from_template(
            """
        You are a book planner specialist. You will return valid JSON with 'title' and 'chapters' list. 
        Here's an exemple of json Format : 
        {format_instructions}
        You will : 
        - Follow the plan, and instructions if there are some (like number of chapters, words, etc.)
        - Construct if needed ghosts chapters : Part that are note new chapters but the following of the last one
        For the following prompt, return the plan : 
        {brief}
        """
        )

        chain = prompt | llm | parser
        brief = state.get("brief", "")
        plan = chain.invoke(
            {"brief": brief, "format_instructions": format_instructions}
        )
        print(plan)
        return {"plan": plan, "tasks": plan["chapters"], "results": []}
