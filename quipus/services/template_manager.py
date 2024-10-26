import os
from typing import Any, Callable, Literal, Self
from weasyprint import HTML
from ..models import Template
from ..data_sources import CSVDataSource


class TemplateManager:
    __SUPPORTED_SOURCE_TYPES: list[str] = ["csv"]

    def __init__(self) -> None:
        self.templates = []
        self.decide_template_func = None
        self.decide_filename_func = None

    @property
    def data(self) -> list[dict[str, Any]]:
        return self.__data

    @data.setter
    def data(self, value: list[dict[str, Any]]):
        if not isinstance(value, list):
            raise TypeError(
                "'value' must be a list of dictionary with string keys.",
                f"Current type: {type(value)}",
            )

        for item in value:
            if not all(isinstance(k, str) for k in item.keys()):
                raise TypeError("All keys in the dictionary must be a string.")

        self.__data = value

    @property
    def templates(self) -> list[Template]:
        return self.__templates

    @templates.setter
    def templates(self, value: list[Template]):
        if not isinstance(value, list):
            raise TypeError(
                "'value' must be a list of Template",
                f"Current type: {type(value)}",
            )

        if not all(isinstance(item, Template) for item in value):
            raise ValueError(
                "All elements in 'value' must be instances of the Template class."
            )

        self.__templates = value

    @property
    def decide_template_func(self) -> Callable[[dict[str, str]], str] | None:
        return self.__decide_template_func

    @decide_template_func.setter
    def decide_template_func(self, value: Callable[[dict[str, str]], str] | None):
        self.__decide_template_func = value

    @property
    def decide_filename_func(self) -> Callable[[dict[str, str]], str] | None:
        return self.__decide_filename_func

    @decide_filename_func.setter
    def decide_filename_func(self, value: Callable[[dict[str, str]], str] | None):
        self.__decide_filename_func = value

    def from_source(self, source_type: Literal["csv"], **kwargs) -> Self:
        if not isinstance(source_type, str):
            raise TypeError(
                "'source_type' must be a string",
                f"Current type: {type(source_type)}",
            )

        if source_type not in self.__SUPPORTED_SOURCE_TYPES:
            raise NotImplementedError(
                f"'{source_type}' source not supported.",
                f"Supported types: {self.__SUPPORTED_SOURCE_TYPES}",
            )

        mapper = {"csv": self.from_csv}

        if source_type == "csv":
            if not "path_to_file" in kwargs:
                raise KeyError(
                    f"'path_to_file' is required when 'source_type' is {source_type}.",
                )

        mapper[source_type](**kwargs)

        return self

    def from_csv(self, path_to_file: str) -> Self:
        csv_data_source = CSVDataSource(file_path=path_to_file)
        self.data = csv_data_source.fetch_data().to_dict(orient="records")

        return self

    def with_multiple_templates(self, templates: list[Template]):
        if not isinstance(templates, list):
            raise TypeError(
                "'templates' must be a list of Templates.",
                f"Current type: {type(templates)}",
            )

        if not all(isinstance(template, Template) for template in templates):
            raise TypeError(
                "All items in 'templates' must be instances of the Template class.",
            )

        for template in templates:
            self.with_template(template)

        return self

    def with_template(self, template: Template):
        if not isinstance(template, Template):
            raise TypeError(
                "'template' must be an instance of Template class.",
                f"Current type: {type(template)}",
            )

        self.templates.append(template)

        return self

    def to_pdf(self, output_path: str, create_dir: bool = False) -> Self:
        if not isinstance(output_path, str):
            raise TypeError(
                "'output_path' must be a string.",
                f"Current type: {type(output_path)}.",
            )

        if not isinstance(create_dir, bool):
            raise TypeError(
                "'create_dir' must be a boolean.",
                f"Current type: {type(create_dir)}.",
            )

        if not self.decide_filename_func:
            raise ValueError(
                "A method must be implemented to determine the names of the files to be generated. Use the decide_filename_with method to do so."
            )

        if create_dir:
            os.makedirs(output_path, exist_ok=True)
        elif not os.path.exists(output_path):
            raise FileNotFoundError(f"'{output_path}' directory does not exist.")

        if len(self.templates) == 1:
            for item in self.data:
                html: HTML = HTML(
                    string=self.templates[0].render_html_with_values(values=item),
                    base_url=self.templates[0].html_path,
                )
                html.write_pdf(
                    target=f"{output_path}/{self.decide_filename_func(item)}.pdf"
                )
        elif len(self.templates) > 1:
            if not self.decide_template_func:
                raise Exception(
                    "Multiple Templates have been established, but there is no way to determine which one to use for each element. Use the decide_template_with method to do so."
                )
            for item in self.data:
                template: Template = self.__get_template_by_html_path(
                    self.decide_template_func(item)
                )
                html: HTML = HTML(
                    string=template.render_html_with_values(values=item),
                    base_url=template.html_path,
                )
                html.write_pdf(
                    target=f"{output_path}/{self.decide_filename_func(item)}.pdf"
                )
        else:
            raise ValueError(
                "When trying to convert to pdf, you must specify at least one template."
            )

        return self

    def __get_template_by_html_path(self, html_path: str):
        for template in self.templates:
            if template.html_path == html_path:
                return template

        raise ValueError(
            f"There is no Template with the path '{html_path}' in the provided templates."
        )

    def decide_template_with(self, func: Callable[[dict[str, Any]], str]) -> Self:
        self.decide_template_func = func
        return self

    def decide_filename_with(self, func: Callable[[dict[str, Any]], str]) -> Self:
        self.decide_filename_func = func
        return self
