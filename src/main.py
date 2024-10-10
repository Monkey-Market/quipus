import os
from models.template import Template
from services.template_manager import TemplateManager
from data_sources.xlsx_data_source import XLSXDataSource


def main():

    xlsx_data_source = XLSXDataSource(
        file_path="data/certificates.xlsx", sheet_name="Sheet1"
    )

    full_data = xlsx_data_source.fetch_data()
    print("Datos completos cargados desde el XLSX:")
    print(full_data.head())

    columns = xlsx_data_source.get_columns()
    print(f"Columnas encontradas en el XLSX: {columns}")

    filtered_data = xlsx_data_source.filter_data('lang == "es"')
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


if __name__ == "__main__":
    main()
