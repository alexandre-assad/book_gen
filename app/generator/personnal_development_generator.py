from app.agent.content_generator_agent import ContentGeneratorAgent
from app.agent.plan_agent import PlanAgent
from domain.dataclass.book_state import BookState
from langgraph.graph import StateGraph, START

from app.generator.generator import Generator

def aggregator(state: BookState) -> dict:
    results = state.get("results", [])
    ebook = "\n\n".join([r["content"] for r in results])
    return {"ebook": ebook}

class PersonnalDevelopmentGenerator(Generator):
 

    def generate(self) -> None:
        builder = StateGraph(BookState)
        builder.add_node("plan_agent", PlanAgent().generate_by_state)
        builder.add_node("sequential_content_generator", ContentGeneratorAgent().generate)
        builder.add_node("aggregator", aggregator)

        builder.add_edge(START, "plan_agent")
        builder.add_edge("plan_agent", "sequential_content_generator")
        builder.add_edge("sequential_content_generator", "aggregator")

        compiled = builder.compile()
        final_state = compiled.invoke({"brief": "Écris un ebook Sur le QI, ~1000 mots"})
        print("EBOOK:\n", final_state.get("ebook", "<no ebook>"))


