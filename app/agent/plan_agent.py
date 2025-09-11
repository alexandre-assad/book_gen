from domain.dataclass.book_state import BookState
from infra.model.gpt_4o_model import Gpt4oModel
from langgraph.graph import StateGraph, MessagesState
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from json import loads as json_loads


class PlanAgent:
    system_prompt: str = """
    You are a book planner specialist. You will return valid JSON with 'title' and 'chapters' list. 
    Here's an exemple of json format : {
        "title": "Ebook title",
        "chapters": [
            {"id": "ch1", "title": "...", "summary": "Lorem ipsum, ...."},
            {"id": "ch2", "title": "...", "summary": "Lorem ipsum, ...."},
            {"id": "ch3", "title": "...", "summary": "Lorem ipsum, ...."},
        ],
    }
    For the following prompt, return the plan : 
    """

    def __init__(self) -> None:
        pass
        
    def generate_by_state(self, state: BookState) -> dict:
        schemas = [
            ResponseSchema(name="title", description="Book title"),
            ResponseSchema(name="chapters", description="List of the chapters", type="list"),
        ]
        parser = StructuredOutputParser.from_response_schemas(schemas)

        brief = state.get("brief", "")
        model = Gpt4oModel()
        prompt = self.system_prompt + '\n' + brief
        res = model.chat(prompt)
        print(res)
        plan = json_loads(res)
        return {"plan": plan, "tasks": plan["chapters"], "results": []}