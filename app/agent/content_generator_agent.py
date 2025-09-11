from infra.model.gpt_4o_model import Gpt4oModel
from langgraph.graph import StateGraph, MessagesState
from json import dumps as json_dumps


class ContentGeneratorAgent:
    system_prompt: str = """You are a book writter. Given the pla, the title and the previous content, write some content. You will only return the written content."""

    def __init__(self) -> None:
        ...
        
    def generate(self, state: MessagesState):
        tasks = state.output["tasks"]
        results = state.output["results"]
        if not tasks:  # toutes les tâches terminées
            return state

        task = tasks[0]
        previous_content = "\n".join(r["content"] for r in results)
        prompt = f"""
        Génère le contenu pour le chapitre: {task['title']}.
        Contexte déjà écrit:
        {previous_content}
        """
        # Appel modèle LLM (ici pseudo-code)
        model = Gpt4oModel()
        prompt = f"{self.system_prompt}\nHere the plan : {state.output["plan"]}\n Here the title : {task['title']}\n Here the previous content : {previous_content}"
        content = model.chat(prompt)

        results.append({"chapter_id": task["id"], "content": content})
        state.output["results"] = results
        state.output["tasks"] = tasks[1:]  # enlever la tâche traitée

        # Trick: renvoyer le node vers lui-même tant qu’il reste des tâches
        if state.output["tasks"]:
            state.next("sequential_content_generator")
        return state
