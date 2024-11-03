<p align="center">
    <a href="https://pypi.org/project/quipus"><img src="https://i.imgur.com/uSUvgP9.png"></a>
</p>

<p align="center">
  <em>Quipus, data retrieval, template manager and delivery all in one!</em>
</p>

<p align="center">
    <a href="https://pypi.org/project/quipus" target="_blank">
        <img src="https://img.shields.io/pypi/v/quipus?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pypi.org/project/quipus" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/quipus.svg?color=%2334D058" alt="Supported Python versions">
    </a>
    <a href="https://github.com/Monkey-Market/quipus/issues" target="_blank">
      <img src="https://img.shields.io/github/issues/monkey-market/quipus" alt="GitHub issues">
    </a>
    <a href="https://github.com/Monkey-Market/quipus/pulls" target="_blank">
      <img src="https://img.shields.io/github/issues-pr/monkey-market/quipus" alt="GitHub pull requests">
    </a>
</p>

<p align="center">
    <a href="https://github.com/Monkey-Market/quipus/actions/workflows/pytest.yml">
        <img src="https://github.com/Monkey-Market/quipus/actions/workflows/pytest.yml/badge.svg" alt="Pytest Check">
    </a>
    <a href="https://github.com/Monkey-Market/quipus/actions/workflows/pylint.yml">
        <img src="https://github.com/Monkey-Market/quipus/actions/workflows/pylint.yml/badge.svg" alt="Pylint">
    </a>
</p>
<p align="center">
    <img src="https://img.shields.io/github/stars/monkey-market/quipus?style=social" alt="GitHub stars">
</p>


---

**Documentation**: TBD

**Source Code**: <a href="https://github.com/Monkey-Market/quipus" target="_blank">https://github.com/Monkey-Market/quipus</a>

---

Quipus is a Python package that allows you to retrieve data from different sources, manage templates and deliver them in a single package. It is designed to be simple and easy to use, with a focus on performance and reliability.

Key features:
- **Data retrieval**: Retrieve data from different sources such as databases, APIs, and files.
- **Template manager**: Manage templates for different types of documents.
- **Delivery**: Deliver the generated documents to different destinations such as email, file system, cloud storage and more.
- **Easy to use**: Simple and easy to use package with a focus on developer experience.

## Requirements & Dependencies

Quipus is empowered by the foundational work of industry giants. The following are the key dependencies:

- <a href="https://pandas.pydata.org/" class="external-link" target="_blank">Pandas</a> for data manipulation.
- <a href="https://weasyprint.org/" class="external-link" target="_blank">WeasyPrint</a> for document generation.
- <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html" class="external-link" target="_blank">Boto3</a> for AWS cloud storage.

## Installation

You can install Quipus using `pip`:

```console
pip install quipus
```

Or with `poetry`:
```console
poetry add quipus
```

## Usage Example

##### Import the package
```python
import quipus as qp
```

##### Fetch data from CSV and generate PDFs
```python
template_manager = (
    qp.TemplateManager()
    .from_csv("data/data_source.csv")
    .with_template(qp.Template("templates/pdf_template.html"))
    .decide_filename_with(lambda data: f"{data['name']}")
    .to_pdf(output_path="output", create_dir=True)
)
```

##### Set up SMTP configuration
> Note: These can be set up as environment variables for security reasons.
```python
smtp_config = qp.SMTPConfig(
    server="smtp.server.com",
    port=587,
    username="username",
    password="password",
    use_tls=True,
)
email_sender = qp.EmailSender(smtp_config)
```

##### Send emails with attachments
```python
for item in template_manager.data:
    smtp_message = (
        qp.EmailMessageBuilder(
            from_address="example@sender.com", 
            to_addresses=[item["email"], "another_email@example.com"]
        )
        .with_body_path("templates/email_body_template.html", "html", item)
        .with_subject("Your email subject")
        .add_attachment_from_path(f"output/{item['name']}.pdf")
        .build()
    )
    email_sender.send(smtp_message)
```

This is a simple example of how you can use Quipus to fetch data from a CSV file, generate PDFs using a template, and send emails with the generated PDFs as attachments.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](https://github.com/Monkey-Market/quipus/blob/main/CONTRIBUTING.md) for more information.

You can always open an issue or submit a pull request if you have any suggestions or improvements.

## Contributors
<table>
  <tr>
    <td align="center" id="j1loop">
      <a href="https://github.com/j1loop/">
        <img src="https://avatars.githubusercontent.com/u/97411958?v=4" width="75px;" alt=""/>
        <br />
        <sub>
          <b>Jorge U. Alarcón</b>
        </sub>
      </a>
      <br />
    </td>
    <td align="center" id="pandasoncode">
      <a href="https://github.com/pandasoncode/">
        <img src="https://avatars.githubusercontent.com/u/110241663?v=4" width="75px;" alt=""/>
        <br />
        <sub>
          <b>Fernando Nicolás</b>
        </sub>
      </a>
      <br />
    </td>
  </tr>
</table>

## Trivia

The name "*Quipus*" comes from the Quechua word "*khipu*" which refers to a method used by the Incas to keep records and communicate information through a system of knots and strings.

We thought it was a fitting name for a package that helps you manage and deliver data in a structured and organized way.

You can read more about it in [this](https://en.wikipedia.org/wiki/Quipu) wikipedia page.

---

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://github.com/Monkey-Market/quipus/blob/main/LICENSE).
