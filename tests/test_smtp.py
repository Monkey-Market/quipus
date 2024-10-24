import unittest
from unittest.mock import patch
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os

from services.smtp_delivery import SMTPConfig, EmailMessageBuilder, EmailSender


class TestEmailMessageBuilder(unittest.TestCase):

    def setUp(self):
        """Setup an EmailMessageBuilder instance for testing."""
        self.builder = EmailMessageBuilder(
            "test@example.com", ["recipient@example.com"]
        )

    def test_initialization(self):
        """Test initialization of the EmailMessageBuilder class."""
        self.assertEqual(self.builder.from_address, "test@example.com")
        self.assertEqual(self.builder.to_addresses, ["recipient@example.com"])
        self.assertEqual(self.builder.subject, "")
        self.assertEqual(self.builder.body, "")
        self.assertEqual(self.builder.body_type, "plain")
        self.assertEqual(self.builder.attachments, [])
        self.assertEqual(self.builder.custom_headers, {})

    def test_from_address_setter(self):
        """Test setting a valid from address."""
        with self.assertRaises(TypeError):
            self.builder.from_address = 123

        with self.assertRaises(ValueError):
            self.builder.from_address = ""

        self.builder.from_address = "new@example.com"
        self.assertEqual(self.builder.from_address, "new@example.com")

    def test_to_addresses_setter(self):
        """Test setting valid to addresses."""
        with self.assertRaises(TypeError):
            self.builder.to_addresses = "not_a_list"

        with self.assertRaises(ValueError):
            self.builder.to_addresses = []

        with self.assertRaises(TypeError):
            self.builder.to_addresses = [123]

        with self.assertRaises(ValueError):
            self.builder.to_addresses = [""]

        self.builder.to_addresses = ["new@example.com"]
        self.assertEqual(self.builder.to_addresses, ["new@example.com"])

    def test_subject_setter(self):
        """Test setting a valid subject."""
        with self.assertRaises(TypeError):
            self.builder.subject = 123

        self.builder.subject = "New Subject"
        self.assertEqual(self.builder.subject, "New Subject")

    def test_body_setter(self):
        """Test setting a valid body."""
        with self.assertRaises(TypeError):
            self.builder.body = 123

        self.builder.body = "New Body"
        self.assertEqual(self.builder.body, "New Body")

    def test_body_type_setter(self):
        """Test setting a valid body type."""
        with self.assertRaises(TypeError):
            self.builder.body_type = 123

        with self.assertRaises(ValueError):
            self.builder.body_type = "invalid"

        self.builder.body_type = "html"
        self.assertEqual(self.builder.body_type, "html")

    def test_attachments_setter(self):
        """Test setting valid attachments."""
        with self.assertRaises(TypeError):
            self.builder.attachments = "not_a_list"

        self.builder.attachments = []
        self.assertEqual(self.builder.attachments, [])

    def test_custom_headers_setter(self):
        """Test setting valid custom headers."""
        with self.assertRaises(TypeError):
            self.builder.custom_headers = "not_a_dict"

        with self.assertRaises(TypeError):
            self.builder.custom_headers = {123: "value"}

        with self.assertRaises(ValueError):
            self.builder.custom_headers = {"": "value"}

        self.builder.custom_headers = {"X-Test": "value"}
        self.assertEqual(self.builder.custom_headers, {"X-Test": "value"})

    def test_add_recipient(self):
        """Test adding a recipient."""
        with self.assertRaises(TypeError):
            self.builder.add_recipient(123)

        with self.assertRaises(ValueError):
            self.builder.add_recipient("")

        self.builder.add_recipient("new@example.com")
        self.assertIn("new@example.com", self.builder.to_addresses)

    def test_with_subject(self):
        """Test setting a subject using the with_subject method."""
        self.builder.with_subject("New Subject")
        self.assertEqual(self.builder.subject, "New Subject")

    def test_with_body(self):
        """Test setting a body using the with_body method."""
        self.builder.with_body("New Body", "html")
        self.assertEqual(self.builder.body, "New Body")
        self.assertEqual(self.builder.body_type, "html")

    def test_add_attachment(self):
        """Test adding an attachment."""
        mime_base = MIMEBase("application", "octet-stream")
        with self.assertRaises(TypeError):
            self.builder.add_attachment("not_mime_base")

        self.builder.add_attachment(mime_base, "filename.txt")
        self.assertIn((mime_base, "filename.txt"), self.builder.attachments)

    def test_add_attachment_from_path(self):
        """Test adding an attachment from a file path."""
        with self.assertRaises(TypeError):
            self.builder.add_attachment_from_path(123)

        with self.assertRaises(ValueError):
            self.builder.add_attachment_from_path("")

        with self.assertRaises(FileNotFoundError):
            self.builder.add_attachment_from_path("non_existent_file.txt")

        temp_file_path = "temp_test_file.txt"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write("Test content")

        self.builder.add_attachment_from_path(temp_file_path)
        self.assertTrue(
            any(
                filename == "temp_test_file.txt"
                for _, filename in self.builder.attachments
            )
        )

        os.remove(temp_file_path)

    def test_add_custom_header(self):
        """Test adding a custom header."""
        with self.assertRaises(TypeError):
            self.builder.add_custom_header(123, "value")

        with self.assertRaises(ValueError):
            self.builder.add_custom_header("", "value")

        with self.assertRaises(TypeError):
            self.builder.add_custom_header("X-Test", 123)

        with self.assertRaises(ValueError):
            self.builder.add_custom_header("X-Test", "")

        self.builder.add_custom_header("X-Test", "value")
        self.assertEqual(self.builder.custom_headers["X-Test"], "value")

    def test_build(self):
        """Test building an email message."""
        self.builder.with_subject("Test Subject").with_body("Test Body", "plain")
        email_message = self.builder.build()
        self.assertIsInstance(email_message, MIMEMultipart)
        self.assertEqual(email_message["From"], "test@example.com")
        self.assertEqual(email_message["To"], "recipient@example.com")
        self.assertEqual(email_message["Subject"], "Test Subject")

    def test_str_method(self):
        """Test the __str__ method of the EmailMessageBuilder class."""
        expected_str = str(
            {
                "from_address": "test@example.com",
                "to_addresses": ["recipient@example.com"],
                "cc_addresses": [],
                "subject": "",
                "body": "",
                "body_type": "plain",
                "attachments": [],
                "custom_headers": {},
            }
        )
        self.assertEqual(str(self.builder), expected_str)


class TestSMTPConfig(unittest.TestCase):

    def setUp(self):
        """Setup an SMTPConfig instance for testing."""
        self.config = SMTPConfig(
            server="smtp.example.com",
            port=587,
            username="user",
            password="pass",
            use_tls=False,
            use_ssl=False,
            timeout=30,
        )

    def test_initialization(self):
        """Test initialization of the SMTPConfig class."""
        self.assertEqual(self.config.server, "smtp.example.com")
        self.assertEqual(self.config.port, 587)
        self.assertEqual(self.config.username, "user")
        self.assertEqual(self.config.password, "pass")
        self.assertIsInstance(self.config.use_ssl, bool)
        self.assertIsInstance(self.config.use_tls, bool)
        self.assertEqual(self.config.timeout, 30)

    def test_server_setter(self):
        """Test setting a valid server address."""
        with self.assertRaises(TypeError):
            self.config.server = 123

        with self.assertRaises(ValueError):
            self.config.server = ""

        self.config.server = "new.smtp.example.com"
        self.assertEqual(self.config.server, "new.smtp.example.com")

    def test_port_setter(self):
        """Test setting a valid port."""
        with self.assertRaises(TypeError):
            self.config.port = "not_an_int"

        with self.assertRaises(ValueError):
            self.config.port = 70000

        self.config.port = 465
        self.assertEqual(self.config.port, 465)

    def test_username_setter(self):
        """Test setting a valid username."""
        with self.assertRaises(TypeError):
            self.config.username = 123

        with self.assertRaises(ValueError):
            self.config.username = ""

        self.config.username = "new_user"
        self.assertEqual(self.config.username, "new_user")

    def test_password_setter(self):
        """Test setting a valid password."""
        with self.assertRaises(TypeError):
            self.config.password = 123

        self.config.password = "new_pass"
        self.assertEqual(self.config.password, "new_pass")

    def test_use_tls_setter(self):
        """Test setting a valid use_tls value."""
        with self.assertRaises(TypeError):
            self.config.use_tls = "not_a_bool"

        self.config.use_tls = False
        self.assertFalse(self.config.use_tls)

    def test_use_ssl_setter(self):
        """Test setting a valid use_ssl value."""
        with self.assertRaises(TypeError):
            self.config.use_ssl = "not_a_bool"

        self.config.use_ssl = True
        self.assertTrue(self.config.use_ssl)

    def test_timeout_setter(self):
        """Test setting a valid timeout value."""
        with self.assertRaises(TypeError):
            self.config.timeout = "not_an_int"

        with self.assertRaises(ValueError):
            self.config.timeout = -1

        self.config.timeout = 60
        self.assertEqual(self.config.timeout, 60)

    def test_str_method(self):
        """Test the __str__ method of the SMTPConfig class."""
        expected_str = str(
            {
                "server": "smtp.example.com",
                "port": 587,
                "username": "user",
                "password": "pass",
                "use_tls": False,
                "use_ssl": False,
                "timeout": 30,
            }
        )
        self.assertEqual(str(self.config), expected_str)


class TestEmailSender(unittest.TestCase):

    def setUp(self):
        """Setup an SMTPConfig and EmailSender instance for testing."""
        self.smtp_config = SMTPConfig(
            server="smtp.example.com",
            port=587,
            username="user",
            password="pass",
            use_tls=False,
            use_ssl=False,
            timeout=30,
        )
        self.email_sender = EmailSender(self.smtp_config)
        self.email_message = (
            EmailMessageBuilder("test@example.com", ["recipient@example.com"])
            .with_subject("Test Subject")
            .with_body("Test Body", "plain")
            .build()
        )

    def test_initialization(self):
        """Test initialization of the EmailSender class."""
        self.assertEqual(self.email_sender.smtp_config, self.smtp_config)

    @patch("services.smtp_delivery.smtplib.SMTP")
    @patch("services.smtp_delivery.smtplib.SMTP_SSL")
    def test_send_email_with_ssl(self, mock_smtp_ssl, mock_smtp):
        """Test sending an email with SSL enabled."""
        self.smtp_config.use_ssl = True
        self.email_sender.send(self.email_message)
        mock_smtp_ssl.assert_called_once_with(
            self.smtp_config.server,
            self.smtp_config.port,
            timeout=self.smtp_config.timeout,
        )
        mock_smtp_ssl.return_value.login.assert_called_once_with(
            self.smtp_config.username,
            self.smtp_config.password,
        )
        mock_smtp_ssl.return_value.sendmail.assert_called_once_with(
            self.email_message["From"],
            self.email_message["To"].split(", "),
            self.email_message.as_string(),
        )
        mock_smtp_ssl.return_value.quit.assert_called_once()

    @patch("services.smtp_delivery.smtplib.SMTP")
    @patch("services.smtp_delivery.smtplib.SMTP_SSL")
    def test_send_email_with_tls(self, mock_smtp_ssl, mock_smtp):
        """Test sending an email with TLS enabled."""
        self.smtp_config.use_tls = True
        self.email_sender.send(self.email_message)
        mock_smtp.assert_called_once_with(
            self.smtp_config.server,
            self.smtp_config.port,
            timeout=self.smtp_config.timeout,
        )
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once_with(
            self.smtp_config.username,
            self.smtp_config.password,
        )
        mock_smtp.return_value.sendmail.assert_called_once_with(
            self.email_message["From"],
            self.email_message["To"].split(", "),
            self.email_message.as_string(),
        )
        mock_smtp.return_value.quit.assert_called_once()

    @patch("services.smtp_delivery.smtplib.SMTP")
    @patch("services.smtp_delivery.smtplib.SMTP_SSL")
    def test_send_email_without_ssl_tls(self, mock_smtp_ssl, mock_smtp):
        """Test sending an email without SSL/TLS."""
        self.email_sender.send(self.email_message)
        mock_smtp.assert_called_once_with(
            self.smtp_config.server,
            self.smtp_config.port,
            timeout=self.smtp_config.timeout,
        )
        mock_smtp.return_value.login.assert_called_once_with(
            self.smtp_config.username,
            self.smtp_config.password,
        )
        mock_smtp.return_value.sendmail.assert_called_once_with(
            self.email_message["From"],
            self.email_message["To"].split(", "),
            self.email_message.as_string(),
        )
        mock_smtp.return_value.quit.assert_called_once()

    def test_str_method(self):
        """Test the __str__ method of the EmailSender class."""
        expected_str = str({"smtp_config": str(self.smtp_config)})
        self.assertEqual(str(self.email_sender), expected_str)


if __name__ == "__main__":
    unittest.main()
