from domain.dataclass.book_state import BookState
from infra.model.gpt_4o_model import Gpt4oModel
from langchain.prompts import ChatPromptTemplate
from langgraph.types import Command


class ContentGeneratorAgent:
    def __init__(self) -> None:
        pass

    def generate(self, state: BookState) -> Command:
        tasks = state.get("tasks", [])
        results = state.get("results", [])

        # si plus de tâches -> on va à l'agrégateur
        if not tasks:
            return Command(
                update={"tasks": tasks, "results": results}, goto="aggregator"
            )

        task = tasks[0]
        previous_content = results[-1]["content"] if results else ""
        global_plan = state.get("plan")

        prompt = ChatPromptTemplate.from_template(
            """
        You'll written book or ebook following this plan (for coherence only, do not rewrite it) :
        {global_plan}
        You will write only the chapter that i will provide you.
        If it's a ghost chapter, just write the content.
        In case of ghosts chapter, just consider you're continuing the chapter before.
        You will be consistent, respecting the tone and vocabulary already used.
        You will try to fit at best the number of words.
        If it's not a ghost chapter, you can write the chapter title.
        If it's the first chapter, you can write the title of the book.
        For the context, there's what have been writting just before :
        {previous_content}

        Now, write the following chapter : {chapter_title}
        Is it a ghost chapter : {is_ghost}
        Number of words : {number_words}
        You will write it as a mardown format.
        """
        )

        # composition Runnable (prompt | llm)
        model = Gpt4oModel().llm
        chain = prompt | model
        response = chain.invoke(
            {
                "global_plan": global_plan,
                "previous_content": previous_content,
                "chapter_title": task["title"],
                "is_ghost": task["is_ghost"],
                "number_words": task["number_words"],
            }
        )

        # extraire le texte selon le type de retour (fallbacks simples)
        if isinstance(response, str):
            content = response
        else:
            content = getattr(response, "content", str(response))

        results.append({"chapter_id": task["id"], "content": content})
        new_tasks = tasks[1:]

        # si il reste des tâches -> goto self, sinon -> aggregator
        next_node = "sequential_content_generator" if new_tasks else "aggregator"
        return Command(update={"tasks": new_tasks, "results": results}, goto=next_node)
