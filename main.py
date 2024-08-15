import pandas as pd

from models.certificate_factory import CertificateFactory
from models.template import Template


for _, row in pd.read_csv("data/certificates.csv").iterrows():
    certificate = CertificateFactory.create_one_certificate(row)
    template = Template("templates/template.html")
    template.to_pdf(certificate, f"output/{certificate.name}.pdf")
