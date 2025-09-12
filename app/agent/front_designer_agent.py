from domain.dataclass.book_state import BookState
from infra.model.gpt_4o_model import Gpt4oModel
from langchain.prompts import ChatPromptTemplate
from langgraph.types import Command


class HtmlConverterAgent:

    def __init__(self) -> None:
        pass

    def convert(self, state: BookState) -> Command:
        llm = Gpt4oModel().llm
        ebook = state.get("ebook", "")
        if not ebook:
            return Command(
                update={
                    "ebook_html": "<html><body><p>No ebook content</p></body></html>"
                }
            )

        # découper en chapitres (ou par taille)
        chunks = ebook.split("\n\n# ")  # exemple simple si headings
        html_parts = []
        prompt = ChatPromptTemplate.from_template(
            """
        You are a converter that takes plain text and produces clean HTML.
        You will return the html into <section> to be add with others.
        Input text:
        {chunk}
        Return only HTML.
        """
        )
        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            response = (prompt | llm).invoke({"chunk": chunk})
            html_parts.append(
                response.content if hasattr(response, "content") else str(response)
            )

        # recombiner
        full_html = "<html><body>" + "\n".join(html_parts) + "</body></html>"
        full_html = full_html.replace("```html", "").replace("```", "")

        return Command(update={"ebook_html": full_html})
