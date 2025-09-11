from infra.model.gpt_4o_model import Gpt4oModel
from langgraph.graph import StateGraph, MessagesState
from json import loads as json_loads


class PlanAgent:
    system_prompt: str = """You are a book planner specialist. You will return valid JSON with 'title' and 'chapters' list. For the following prompt, return the plan : """

    def __init__(self) -> None:
        ...
        
    def generate_by_state(self, state: MessagesState) -> MessagesState:
        brief = state.input["brief"]

        model = Gpt4oModel()
        prompt = self.system_prompt + '\n' + brief
        res = model.chat(prompt)
        plan = json_loads(res)
        state.output["plan"] = plan
        return state