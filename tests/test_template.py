import unittest
import os
import tempfile

from models.template import Template


class TestTemplate(unittest.TestCase):

    def setUp(self):
        """Setup a temporary directory and files for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.html_test_path = os.path.join(self.test_dir.name, ".html")
        self.css_test_path = os.path.join(self.test_dir.name, ".css")
        self.assets_test_dir = os.path.join(self.test_dir.name, "assets")

        self.html_test_content = "<html><body>Test HTML {placeholder}</body></html>"
        self.css_test_content = "body { background-color: #fff; }"

        with open(self.html_test_path, "w") as f:
            f.write(self.html_test_content)

        with open(self.css_test_path, "w") as f:
            f.write(self.css_test_content)

        os.mkdir(self.assets_test_dir)

    def tearDown(self):
        """Clean up the temporary directory and files."""
        self.test_dir.cleanup()

    def test_initialization(self):
        """Test initialization of the Template class."""
        template = Template(
            self.html_test_path, self.css_test_path, self.assets_test_dir
        )
        self.assertEqual(template.html_path, self.html_test_path)
        self.assertEqual(template.css_path, self.css_test_path)
        self.assertEqual(template.assets_path, self.assets_test_dir)

    def test_from_template_path(self):
        """Test creating a Template instance using from_template_path method."""
        template = Template.from_template_path(self.test_dir.name)
        self.assertEqual(template.html_path, self.html_test_path)
        self.assertEqual(template.css_path, self.css_test_path)
        self.assertEqual(template.assets_path, self.assets_test_dir)

        with self.assertRaises(TypeError):
            Template.from_template_path(123)

        with self.assertRaises(ValueError):
            Template.from_template_path("")

        with self.assertRaises(FileNotFoundError):
            Template.from_template_path("non_existent_directory")

    def test_html_path_setter(self):
        """Test setting a valid HTML path."""
        template = Template(self.html_test_path)
        self.assertEqual(template.html_path, self.html_test_path)

        with self.assertRaises(TypeError):
            template.html_path = 123

        with self.assertRaises(ValueError):
            template.html_path = ""

        with self.assertRaises(FileNotFoundError):
            template.html_path = "non_existent_file.html"

    def test_css_path_setter(self):
        """Test setting a valid CSS path."""
        template = Template(self.html_test_path, self.css_test_path)
        self.assertEqual(template.css_path, self.css_test_path)

        with self.assertRaises(TypeError):
            template.css_path = 123

        with self.assertRaises(ValueError):
            template.css_path = ""

        with self.assertRaises(FileNotFoundError):
            template.css_path = "non_existent_file.css"

    def test_assets_path_setter(self):
        """Test setting a valid assets path."""
        template = Template(
            self.html_test_path, self.css_test_path, self.assets_test_dir
        )
        self.assertEqual(template.assets_path, self.assets_test_dir)

        with self.assertRaises(TypeError):
            template.assets_path = 123

        with self.assertRaises(ValueError):
            template.assets_path = ""

        with self.assertRaises(FileNotFoundError):
            template.assets_path = "non_existent_directory"

    def test_render_html(self):
        """Test rendering HTML content."""
        template = Template(self.html_test_path)
        content = template.render_html()
        self.assertEqual(content, self.html_test_content)

    def test_render_html_with_values(self):
        """Test rendering HTML content with values."""
        template = Template(self.html_test_path)
        values: dict[str, str] = {"placeholder": "test"}
        self.assertEqual(
            self.html_test_content.format(**values),
            template.render_html_with_values(values=values),
        )

        with self.assertRaises(TypeError) as context:
            template.render_html_with_values(values=120)

        with self.assertRaises(TypeError):
            template.render_html_with_values(values={120: "test"})

    def test_render_css(self):
        """Test rendering CSS content."""
        template = Template(self.html_test_path, self.css_test_path)
        content = template.render_css()
        self.assertEqual(content, self.css_test_content)

        template_without_css = Template(self.html_test_path)
        with self.assertRaises(ValueError):
            template_without_css.render_css()

    def test_str_method(self):
        """Test the __str__ method."""
        template = Template(
            self.html_test_path, self.css_test_path, self.assets_test_dir
        )
        expected_str = str(
            {
                "html_path": self.html_test_path,
                "css_path": self.css_test_path,
                "assets_path": self.assets_test_dir,
            }
        )
        self.assertEqual(str(template), expected_str)


if __name__ == "__main__":
    unittest.main()
