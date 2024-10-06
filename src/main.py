import os
from models.template import Template
from services.template_manager import TemplateManager
from services.s3_delivery import AWSConfig, S3Delivery
from data_sources.csv_data_source import CSVDataSource


def main():

    csv_data_source = CSVDataSource(file_path="data/certificates.csv", delimiter=";")

    full_data = csv_data_source.fetch_data()
    print("Datos completos cargados desde el CSV:")
    print(full_data.head())

    columns = csv_data_source.get_columns()
    print(f"Columnas encontradas en el CSV: {columns}")

    filtered_data = csv_data_source.filter_data('lang == "es"')
    print(f"Datos filtrados (solo español):")
    print(filtered_data)

    template_manager = TemplateManager()

    template_manager.data = filtered_data.to_dict(orient="records")

    template_manager.with_multiple_templates(
        [
            Template(html_path="templates/template_es.html"),
            Template(html_path="templates/template_en.html"),
        ]
    ).decide_template_with(
        lambda item: f"templates/template_{item['lang']}.html"
    ).decide_filename_with(
        lambda item: f"{item['name']}_{item['content']}"
    ).to_pdf(
        output_path="output", create_dir=True
    )

    mytuple = []
    for dirpath, _, filenames in os.walk("output/"):
        for filename in filenames:
            mytuple.append((os.path.join(dirpath, filename), filename))

    print("Archivos PDF generados:")
    for file in mytuple:
        print(file)

    print("Subiendo archivos a S3...")
    S3Delivery(AWSConfig.from_profile()).upload_many_files(
        files=mytuple,
        bucket_name="",
    )


if __name__ == "__main__":
    main()
