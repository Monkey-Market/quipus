import pytest
from quipus import Template


@pytest.fixture
def sample_html_file(tmp_path):
    html_file = tmp_path / "template.html"
    html_file.write_text("<html><body>{name}</body></html>")
    return html_file


@pytest.fixture
def sample_css_file(tmp_path):
    css_file = tmp_path / "template.css"
    css_file.write_text("body { color: black; }")
    return css_file


@pytest.fixture
def sample_assets_dir(tmp_path):
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    return assets_dir


def test_template_initialization(sample_html_file, sample_css_file, sample_assets_dir):
    template = Template(
        html_path=str(sample_html_file),
        css_path=str(sample_css_file),
        assets_path=str(sample_assets_dir),
    )

    assert template.html_path == str(sample_html_file)
    assert template.css_path == str(sample_css_file)
    assert template.assets_path == str(sample_assets_dir)


def test_template_initialization_missing_optional_paths(sample_html_file):
    template = Template(html_path=str(sample_html_file))
    assert template.html_path == str(sample_html_file)
    assert template.css_path is None
    assert template.assets_path is None


@pytest.mark.parametrize(
    "attribute, value, expected_exception, message",
    [
        ("html_path", 123, TypeError, "'html_path' must be a string."),
        ("html_path", "", ValueError, "'html_path' cannot be an empty string."),
        ("css_path", 123, TypeError, "When setted, 'css_path' must be a string."),
        (
            "css_path",
            "",
            ValueError,
            "When setted, 'css_path' cannot be an empty string.",
        ),
        ("assets_path", 123, TypeError, "When setted, 'assets_path' must be a string."),
        (
            "assets_path",
            "",
            ValueError,
            "When setted, 'assets_path' cannot be an empty string.",
        ),
    ],
)
def test_template_attribute_validation(
    sample_html_file,
    sample_css_file,
    sample_assets_dir,
    attribute,
    value,
    expected_exception,
    message,
):
    template = Template(
        html_path=str(sample_html_file),
        css_path=str(sample_css_file),
        assets_path=str(sample_assets_dir),
    )
    with pytest.raises(expected_exception, match=message):
        setattr(template, attribute, value)


def test_template_from_template_path(tmp_path):
    html_file = tmp_path / ".html"
    css_file = tmp_path / ".css"
    assets_dir = tmp_path / "assets"
    html_file.write_text("<html><body>{name}</body></html>")
    css_file.write_text("body { color: black; }")
    assets_dir.mkdir()

    template = Template.from_template_path(str(tmp_path))

    assert template.html_path == str(html_file)
    assert template.css_path == str(css_file)
    assert template.assets_path == str(assets_dir)


def test_template_render_html(sample_html_file):
    template = Template(html_path=str(sample_html_file))
    assert template.render_html() == "<html><body>{name}</body></html>"


def test_template_render_html_with_values(sample_html_file):
    template = Template(html_path=str(sample_html_file))
    rendered_html = template.render_html_with_values({"name": "Juan"})
    assert rendered_html == "<html><body>Juan</body></html>"


def test_template_render_html_with_values_missing_key(sample_html_file):
    template = Template(html_path=str(sample_html_file))
    with pytest.raises(KeyError):
        template.render_html_with_values({})


def test_template_render_css(sample_html_file, sample_css_file):
    template = Template(html_path=str(sample_html_file), css_path=str(sample_css_file))
    assert template.render_css() == "body { color: black; }"


def test_template_render_css_no_path(sample_html_file):
    template = Template(html_path=str(sample_html_file))
    with pytest.raises(
        ValueError, match="Template CSS path is not initialized. Provide a valid path."
    ):
        template.render_css()


def test_template_str(sample_html_file, sample_css_file, sample_assets_dir):
    template = Template(
        html_path=str(sample_html_file),
        css_path=str(sample_css_file),
        assets_path=str(sample_assets_dir),
    )
    expected_str = str(
        {
            "html_path": str(sample_html_file),
            "css_path": str(sample_css_file),
            "assets_path": str(sample_assets_dir),
        }
    )
    assert str(template) == expected_str
