from app.agent.content_generator_agent import ContentGeneratorAgent
from app.agent.plan_agent import PlanAgent
from langgraph.graph import StateGraph, MessagesState

from app.generator.generator import Generator

def aggregator_node(state: MessagesState):
    results = state.output["results"]
    ebook = "\n\n".join([r["content"] for r in results])
    state.output["ebook"] = ebook
    return state

class PersonnalDevelopmentGenerator(Generator):
 

    def generate(self) -> None:
        graph = (
            StateGraph(MessagesState)
            .add_node("plan_agent", PlanAgent().generate_by_state)
            .add_node("sequential_content_generator", ContentGeneratorAgent().generate)
            .add_node("aggregator", aggregator_node)
        )
        result_state = graph.compile()
        print(result_state.invoke("Un ebook de qui parle du QI"))
