from domain.dataclass.book_state import BookState
from infra.model.gpt_4o_model import Gpt4oModel
from langchain.prompts import ChatPromptTemplate
from langgraph.types import Command


class ContentGeneratorAgent:
    system_prompt: str = """You are a book writter. Given the pla, the title and the previous content, write some content. You will only return the written content."""

    def __init__(self) -> None:
        pass
        
    def generate(self,state: BookState) -> Command:
        tasks = state.get("tasks", [])
        results = state.get("results", [])

        # si plus de tâches -> on va à l'agrégateur
        if not tasks:
            return Command(update={"tasks": tasks, "results": results}, goto="aggregator")

        task = tasks[0]
        previous_content = "\n".join(r["content"] for r in results)
        global_plan = state.get("plan")

            
        prompt = ChatPromptTemplate.from_template("""
        Tu écris un ebook en suivant ce plan global :
        {global_plan}

        Contexte déjà écrit :
        {previous_content}

        Maintenant rédige le chapitre : {chapter_title}
        Sois cohérent, respecte la continuité et le ton.
        """)
                                                  

        # composition Runnable (prompt | llm)
        model = Gpt4oModel().llm
        chain = prompt | model
        response = chain.invoke({
            "global_plan": global_plan,
            "previous_content": previous_content,
            "chapter_title": task["title"],
        })

        # extraire le texte selon le type de retour (fallbacks simples)
        print(response)
        if isinstance(response, str):
            content = response
        else:
            content = getattr(response, "content", str(response))

        results.append({"chapter_id": task["id"], "content": content})
        new_tasks = tasks[1:]

        # si il reste des tâches -> goto self, sinon -> aggregator
        next_node = "sequential_content_generator" if new_tasks else "aggregator"
        return Command(update={"tasks": new_tasks, "results": results}, goto=next_node)
