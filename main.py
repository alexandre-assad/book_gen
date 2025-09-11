from json import load
from xhtml2pdf import pisa
from model import DeepSeekModel


def get_config():
    with open("config.json", encoding="utf-8") as f:
        return load(f)


def convert_html_to_pdf(html_string: str, pdf_path: str, html_path: str) -> None:
    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)
    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_string)

    return not pisa_status.err


CONFIG = get_config()


def assemble_html(htmls: list[str]) -> str:
    base_content = CONFIG.get("html_base_content")
    for html in htmls:
        base_content += html
    base_content += CONFIG.get("html_end_content")
    return base_content


def generate_html() -> str:
    system_prompt = CONFIG.get("system_prompt")
    markdown_to_css_prompt = CONFIG.get("markdown_to_css_prompt")
    parts = CONFIG.get("parts")
    last_content = "aucun"
    htmls = []
    model = DeepSeekModel()
    for part in parts:
        final_prompt = (
            system_prompt
            + f"Votre partie à rédiger : {part}  \nPartie précédente : {last_content}"
        )
        response = model.chat(final_prompt)
        last_content = response
        htmls.append(
            model.chat(markdown_to_css_prompt + response)
            .replace("```html", "")
            .replace("```", "")
        )
        print(htmls[-1])
    return assemble_html(htmls)


def main():
    html_code = generate_html()
    convert_html_to_pdf(html_code, "title.pdf", "title.html")


if __name__ == "__main__":
    main()
