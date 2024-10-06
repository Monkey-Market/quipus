from models.template import Template
from src.services.template_manager import TemplateManager


def main():
    (
        TemplateManager()
        .from_source("csv", path_to_file="data/certificates.csv")
        .with_multiple_templates(
            [
                Template(html_path="templates/template_es.html"),
                Template(html_path="templates/template_en.html"),
            ]
        )
        .decide_template_with(lambda item: f"templates/template_{item["lang"]}.html")
        .decide_filename_with(lambda item: f"{item["name"]}_{item["content"]}")
        .to_pdf("output", create_dir=True)
    )

if __name__ == "__main__":
    main()
