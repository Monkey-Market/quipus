import csv
import os
from typing import Any
from weasyprint import HTML

from models.template import Template


def csv_to_dict(path_to_csv: str):
    with open(path_to_csv, "r") as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
    return data


def to_pdf(values: dict[str, Any], template: Template, output_path: str) -> None:
    html: HTML = HTML(string=template.render_html_with_values(values=values))
    html.write_pdf(target=f"{output_path}.pdf")


def main():
    template: Template = Template("templates/template.html")
    output_path: str = "output"

    os.makedirs(output_path, exist_ok=True)

    for item in csv_to_dict("data/certificates.csv"):
        to_pdf(
            values=item, template=template, output_path=f"{output_path}/{item["name"]}"
        )


if __name__ == "__main__":
    main()
