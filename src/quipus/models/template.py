import os
from typing import Any, Optional, Self


class Template:
    """
    Class that represents an HTML template with its associated paths for CSS and assets.

    Attributes:
        html_path (str): Path to the HTML file.
        css_path (str): Path to the CSS file.
        assets_path (str): Path to the assets folder.
    """

    def __init__(
        self,
        html_path: str,
        css_path: Optional[str] = None,
        assets_path: Optional[str] = None,
    ):
        """
        Initializes an instance of the Template class.

        Args:
            html_path (str): Path to the HTML file.
            css_path (Optional[str]): Path to the CSS file.
            assets_path (Optional[str]): Path to the assets folder.
        """
        self.html_path = html_path
        self.css_path = css_path
        self.assets_path = assets_path

    @classmethod
    def from_template_path(cls, template_path: str) -> Self:
        """
        Creates an instance of Template from a base path.

        Args:
            template_path (str): The base path where the template files are located.

        Returns:
            Template: An instance of the Template class with the derived paths.

        Raises:
            TypeError: If 'template_path' is not a string.
            ValueError: If 'template_path' is an empty string.
            FileNotFoundError: If directory at 'template_path' does not exist.
        """
        if not isinstance(template_path, str):
            raise TypeError(
                "'template_path' must be a string.",
                f"Current type: {type(template_path)}.",
            )

        if not template_path.strip():
            raise ValueError("'template_path' cannot be an empty string.")

        if not os.path.isdir(template_path):
            raise FileNotFoundError(f"'{template_path}' directory does not exist.")

        return cls(
            html_path=f"{template_path}/.html",
            css_path=f"{template_path}/.css",
            assets_path=f"{template_path}/assets",
        )

    @property
    def html_path(self) -> str:
        """
        Get the path to the HTML template file.

        Returns:
            str: The path to the HTML template file.
        """
        return self.__html_path

    @html_path.setter
    def html_path(self, value: str):
        """
        Set the path to the HTML template file.

        Args:
            value (str): The path to the HTML template file.

        Raises:
            TypeError: If 'value' is not a string.
            ValueError: If 'value' is an empty string.
            FileNotFoundError: If the file at 'value' does not exist.
        """
        if not isinstance(value, str):
            raise TypeError(
                "'html_path' must be a string.",
                f"Current type: {type(value)}.",
            )

        if not value.strip():
            raise ValueError("'html_path' cannot be an empty string.")

        if not os.path.isfile(value):
            raise FileNotFoundError(f"'{value}' file does not exist.")

        self.__html_path = value

    @property
    def css_path(self) -> Optional[str]:
        """
        Get the path to the CSS template file.

        Returns:
            str: The path to the CSS template file.
        """
        return self.__css_path

    @css_path.setter
    def css_path(self, value: Optional[str] = None):
        """
        Set the path to the CSS file.

        Args:
            value (Optional[str]): The path to the CSS file or None.

        Raises:
            TypeError: If 'value' is not a string (when not None).
            ValueError: If 'value' is an empty string.
            FileNotFoundError: If the file at 'value' does not exist.
        """
        if value is None:
            self.__css_path = value
            return

        if not isinstance(value, str):
            raise TypeError(
                "When setted, 'css_path' must be a string.",
                f"Current type: {type(value)}.",
            )

        if not value.strip():
            raise ValueError("When setted, 'css_path' cannot be an empty string.")

        if not os.path.isfile(value):
            raise FileNotFoundError(f"'{value}' file does not exist.")

        self.__css_path = value

    @property
    def assets_path(self) -> Optional[str]:
        """
        Get the path to the assets directory.

        Returns:
            str: The path to the assets directory.
        """
        return self.__assets_path

    @assets_path.setter
    def assets_path(self, value: Optional[str] = None):
        """
        Set the path to the assets directory.

        Args:
            value (Optional[str]): The path to the assets directory or None.

        Raises:
            TypeError: If 'value' is not a string (when not None).
            ValueError: If 'value' is an empty string.
            FileNotFoundError: If the file at 'value' does not exist.
        """
        if value is None:
            self.__assets_path = None
            return

        if not isinstance(value, str):
            raise TypeError(
                "When setted, 'assets_path' must be a string.",
                f"Current type: {type(value)}.",
            )

        if not value.strip():
            raise ValueError("When setted, 'assets_path' cannot be an empty string.")

        if not os.path.isdir(value):
            raise FileNotFoundError(f"'{value}' directory does not exist.")

        self.__assets_path = value

    def render_html(self) -> str:
        """
        Renders the template by reading the content of the HTML file.

        Returns:
            str: The content of the HTML file.
        """
        with open(self.html_path) as html:
            return html.read()

    def render_html_with_values(self, values: dict[str, Any]):
        """
        Renders an HTML template with the provided dictionary of string key-value pairs.

        This method substitutes placeholders in the HTML template with corresponding
        values from the provided dictionary. Placeholders in the template should follow
        the format `{placeholder_name}`.

        Args:
            values (dict[str, Any]): A dictionary where each key is a string.
                The keys correspond to the placeholder names in the HTML template, and
                the values are the content that will replace these placeholders.

        Returns:
            str: The rendered HTML string with all placeholders substituted.

        Raises:
            TypeError: If 'values' is not a dictionary or not all keys are strings.
            KeyError: If not all placeholders in the HTML template could be substituted.
        """
        if not isinstance(values, dict):
            raise TypeError(
                "'values' must be a dictionary.",
                f"Current type: {type(values)}",
            )

        if not all(isinstance(k, str) for k in values.keys()):
            raise TypeError("All keys in the dictionary must be a string.")

        return self.render_html().format(**values)

    def render_css(self) -> str:
        """
        Renders the CSS by reading the content of the CSS file.

        Returns:
            str: The content of the CSS file.

        Raises:
            ValueError: If 'self.css_path' is None.
        """
        if self.css_path is None:
            raise ValueError(
                "Template CSS path is not initialized. Provide a valid path."
            )

        with open(self.css_path) as css:
            return css.read()

    def __str__(self) -> str:
        """
        Represents the Template instance as a string.

        Returns:
            str: A string representation of the instance as a dictionary,
                including 'html_path', 'css_path', and 'assets_path' keys.
        """
        return str(
            {
                "html_path": self.html_path,
                "css_path": self.css_path,
                "assets_path": self.assets_path,
            }
        )
