import os
from models.template import Template
from services.template_manager import TemplateManager
from services.s3_delivery import AWSConfig, S3Delivery


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

    mytuple = []
    for file in os.walk("output/"):
        for f in file[2]:
            mytuple.append((f"output/{f}", f))

    print("Uploading files to S3...")

    S3Delivery(AWSConfig.from_profile()).upload_many_files(
        files=mytuple,
        bucket_name="airbyte-storage-s3",
    )

