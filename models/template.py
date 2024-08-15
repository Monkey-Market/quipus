import os
from weasyprint import HTML
from models.certificate import Certificate


class Template:
    def __init__(self, template_path: str) -> None:
        with open(template_path) as file:
            self.template = file.read()

    def render(self, certificate: Certificate) -> str:
        return self.template.format(
            completion_date=certificate.completion_date,
            content=certificate.content,
            entity=certificate.entity,
            name=certificate.name,
            duration=certificate.duration,
            validity_checker=certificate.validity_checker,
        )

    def to_pdf(self, certificate: Certificate, output_path: str) -> None:
        html = HTML(string=self.render(certificate))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        html.write_pdf(target=output_path)
