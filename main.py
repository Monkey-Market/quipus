import os
import pandas as pd
from weasyprint import HTML

from models.certificate import Certificate
from models.certificate_factory import CertificateFactory
from models.template import Template


def to_pdf(certificate: Certificate, template: Template, output_path: str) -> None:
    raw_html: str = template.render_html().format(
        completion_date=certificate.completion_date,
        content=certificate.content,
        entity=certificate.entity,
        name=certificate.name,
        duration=certificate.duration,
        validity_checker=certificate.validity_checker,
    )
    html: HTML = HTML(string=raw_html)
    html.write_pdf(target=f"{output_path}.pdf")


def main():
    data: pd.DataFrame = pd.read_csv("data/certificates.csv")
    certificates: list[Certificate] = CertificateFactory.create_certificates(data)
    template: Template = Template("templates/template.html")
    output_path: str = "output"

    os.makedirs(output_path, exist_ok=True)

    for certificate in certificates:
        to_pdf(certificate, template, os.path.join(output_path, certificate.name))


if __name__ == "__main__":
    main()
