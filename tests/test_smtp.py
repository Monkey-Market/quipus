import pytest
import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from quipus import SMTPConfig, EmailMessageBuilder, EmailSender


@pytest.fixture
def smtp_config():
    return SMTPConfig(
        server="smtp.example.com",
        port=587,
        username="user@example.com",
        password="password",
        use_tls=True,
        use_ssl=False,
        timeout=10,
    )


@pytest.fixture
def email_builder():
    return EmailMessageBuilder(
        from_address="sender@example.com",
        to_addresses=["recipient@example.com"],
    )


# ============== Tests for SMTPConfig ==============


def test_smtp_config_valid(smtp_config):
    assert smtp_config.server == "smtp.example.com"
    assert smtp_config.port == 587
    assert smtp_config.username == "user@example.com"
    assert smtp_config.password == "password"
    assert smtp_config.use_tls is True
    assert smtp_config.use_ssl is False
    assert smtp_config.timeout == 10


def test_smtp_config_server_invalid_type():
    with pytest.raises(TypeError):
        SMTPConfig(
            server=123,
            port=587,
            username="user@example.com",
            password="password",
        )


def test_smtp_config_server_empty_string():
    with pytest.raises(ValueError):
        SMTPConfig(
            server="   ",
            port=587,
            username="user@example.com",
            password="password",
        )


def test_smtp_config_port_invalid_type():
    with pytest.raises(TypeError):
        SMTPConfig(
            server="smtp.example.com",
            port="587",
            username="user@example.com",
            password="password",
        )


def test_smtp_config_port_invalid_value():
    with pytest.raises(ValueError):
        SMTPConfig(
            server="smtp.example.com",
            port=70000,
            username="user@example.com",
            password="password",
        )


def test_smtp_config_username_invalid_type():
    with pytest.raises(TypeError):
        SMTPConfig(
            server="smtp.example.com",
            port=587,
            username=123,
            password="password",
        )


def test_smtp_config_username_empty_string():
    with pytest.raises(ValueError):
        SMTPConfig(
            server="smtp.example.com",
            port=587,
            username="",
            password="password",
        )


def test_smtp_config_password_invalid_type():
    with pytest.raises(TypeError):
        SMTPConfig(
            server="smtp.example.com",
            port=587,
            username="user@example.com",
            password=123,
        )


def test_smtp_config_use_tls_invalid_type():
    with pytest.raises(TypeError):
        SMTPConfig(
            server="smtp.example.com",
            port=587,
            username="user@example.com",
            password="password",
            use_tls="True",
        )


def test_smtp_config_use_ssl_invalid_type():
    with pytest.raises(TypeError):
        SMTPConfig(
            server="smtp.example.com",
            port=587,
            username="user@example.com",
            password="password",
            use_ssl="False",
        )


def test_smtp_config_timeout_invalid_type():
    with pytest.raises(TypeError):
        SMTPConfig(
            server="smtp.example.com",
            port=587,
            username="user@example.com",
            password="password",
            timeout="10",
        )


def test_smtp_config_timeout_invalid_value():
    with pytest.raises(ValueError):
        SMTPConfig(
            server="smtp.example.com",
            port=587,
            username="user@example.com",
            password="password",
            timeout=-5,
        )


# ============== Tests for EmailMessageBuilder ==============


def test_email_message_builder_valid(email_builder):
    assert email_builder.from_address == "sender@example.com"
    assert email_builder.to_addresses == ["recipient@example.com"]
    assert email_builder.cc_addresses == []
    assert email_builder.subject == ""
    assert email_builder.body == ""
    assert email_builder.body_type == "plain"
    assert email_builder.attachments == []
    assert email_builder.custom_headers == {}


def test_add_recipient(email_builder):
    email_builder.add_recipient("another@example.com")
    assert email_builder.to_addresses == [
        "recipient@example.com",
        "another@example.com",
    ]


def test_add_recipient_invalid(email_builder):
    with pytest.raises(TypeError):
        email_builder.add_recipient(123)

    with pytest.raises(ValueError):
        email_builder.add_recipient("")


def test_add_cc(email_builder):
    email_builder.add_cc("cc@example.com")
    assert email_builder.cc_addresses == ["cc@example.com"]


def test_add_cc_invalid(email_builder):
    with pytest.raises(TypeError):
        email_builder.add_cc(123)

    with pytest.raises(ValueError):
        email_builder.add_cc("")


def test_with_subject(email_builder):
    email_builder.with_subject("Test Subject")
    assert email_builder.subject == "Test Subject"


def test_with_body(email_builder):
    email_builder.with_body("This is the body.", body_type="html")
    assert email_builder.body == "This is the body."
    assert email_builder.body_type == "html"


def test_with_body_path(monkeypatch, email_builder):
    monkeypatch.setattr(os.path, "exists", lambda path: True)

    class MockFile:
        def read(self):
            return "Hello, {name}!"

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    def mock_open(*args, **kwargs):
        return MockFile()

    monkeypatch.setattr("builtins.open", mock_open)

    email_builder.with_body_path(
        "path/to/body.txt",
        body_type="plain",
        replacements={"name": "foo"},
    )

    assert email_builder.body == "Hello, foo!"
    assert email_builder.body_type == "plain"


def test_with_body_path_invalid(email_builder):
    with pytest.raises(TypeError):
        email_builder.with_body_path(123)

    with pytest.raises(ValueError):
        email_builder.with_body_path("")


def test_add_attachment(email_builder):
    attachment = MIMEText("Attachment content")
    email_builder.add_attachment(attachment, filename="test.txt")
    assert len(email_builder.attachments) == 1
    assert email_builder.attachments[0][0] == attachment
    assert email_builder.attachments[0][1] == "test.txt"


def test_add_attachment_invalid(email_builder):
    with pytest.raises(TypeError):
        email_builder.add_attachment(123)

    with pytest.raises(ValueError):
        email_builder.add_attachment(MIMEText("Attachment content"), filename="   ")


def test_add_attachment_from_path(monkeypatch, email_builder):
    def mock_exists(path):
        return True

    def mock_open(*args, **kwargs):
        class MockFile:
            def read(self):
                return b"File content"

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        return MockFile()

    monkeypatch.setattr(os.path, "exists", mock_exists)
    monkeypatch.setattr("builtins.open", mock_open)

    email_builder.add_attachment_from_path("path/to/file.txt", filename="file.txt")

    assert len(email_builder.attachments) == 1
    attachment, filename = email_builder.attachments[0]
    assert filename == "file.txt"
    assert isinstance(attachment, MIMEApplication)


def test_add_custom_header(email_builder):
    email_builder.add_custom_header("X-Custom-Header", "HeaderValue")
    assert email_builder.custom_headers == {"X-Custom-Header": "HeaderValue"}


def test_add_custom_header_invalid(email_builder):
    with pytest.raises(TypeError):
        email_builder.add_custom_header(123, "value")

    with pytest.raises(ValueError):
        email_builder.add_custom_header("X-Header", "")

    with pytest.raises(TypeError):
        email_builder.add_custom_header("X-Header", 456)


def test_build(email_builder):
    email_builder.with_subject("Test Subject")
    email_builder.with_body("Test Body")
    email_message = email_builder.build()

    assert isinstance(email_message, MIMEMultipart)
    assert email_message["From"] == "sender@example.com"
    assert email_message["To"] == "recipient@example.com"
    assert email_message["Subject"] == "Test Subject"

    payload = email_message.get_payload()
    assert len(payload) == 1
    assert payload[0].get_payload() == "Test Body"


def test_email_builder_from_address_invalid():
    with pytest.raises(TypeError):
        EmailMessageBuilder(
            from_address=123,
            to_addresses=["recipient@example.com"],
        )

    with pytest.raises(ValueError):
        EmailMessageBuilder(
            from_address="",
            to_addresses=["recipient@example.com"],
        )


def test_email_builder_to_addresses_invalid_type():
    with pytest.raises(TypeError):
        EmailMessageBuilder(
            from_address="sender@example.com",
            to_addresses="recipient@example.com",
        )


def test_email_builder_to_addresses_empty():
    with pytest.raises(ValueError):
        EmailMessageBuilder(
            from_address="sender@example.com",
            to_addresses=[],
        )


def test_email_builder_to_addresses_invalid_values():
    with pytest.raises(TypeError):
        EmailMessageBuilder(
            from_address="sender@example.com",
            to_addresses=["recipient@example.com", 123],
        )

    with pytest.raises(ValueError):
        EmailMessageBuilder(
            from_address="sender@example.com",
            to_addresses=["recipient@example.com", ""],
        )


# ============== Tests for EmailSender ==============


def test_email_sender_send_tls(monkeypatch, smtp_config):
    smtp_config.use_ssl = False
    smtp_config.use_tls = True

    instances = []

    class MockSMTP:
        def __init__(self, server, port, timeout=None):
            self.server = server
            self.port = port
            self.timeout = timeout
            self.starttls_called = False
            self.login_called_with = None
            self.sendmail_called_with = None
            self.quit_called = False
            instances.append(self)

        def starttls(self):
            self.starttls_called = True

        def login(self, username, password):
            self.login_called_with = (username, password)

        def sendmail(self, from_addr, to_addrs, msg):
            self.sendmail_called_with = (from_addr, to_addrs, msg)

        def quit(self):
            self.quit_called = True

    monkeypatch.setattr(smtplib, "SMTP", MockSMTP)

    email_message = MIMEMultipart()
    email_message["From"] = "sender@example.com"
    email_message["To"] = "recipient@example.com"
    email_message["Subject"] = "Test"

    email_sender = EmailSender(smtp_config)
    email_sender.send(email_message)

    mock_smtp_instance = instances[0]

    assert mock_smtp_instance.server == smtp_config.server
    assert mock_smtp_instance.port == smtp_config.port
    assert mock_smtp_instance.timeout == smtp_config.timeout
    assert mock_smtp_instance.starttls_called is True
    assert mock_smtp_instance.login_called_with == (
        smtp_config.username,
        smtp_config.password,
    )
    assert mock_smtp_instance.sendmail_called_with == (
        "sender@example.com",
        ["recipient@example.com"],
        email_message.as_string(),
    )
    assert mock_smtp_instance.quit_called is True


def test_email_sender_send_ssl(monkeypatch, smtp_config):
    smtp_config.use_ssl = True
    smtp_config.use_tls = False

    instances = []

    class MockSMTP_SSL:
        def __init__(self, server, port, timeout=None):
            self.server = server
            self.port = port
            self.timeout = timeout
            self.login_called_with = None
            self.sendmail_called_with = None
            self.quit_called = False
            instances.append(self)

        def login(self, username, password):
            self.login_called_with = (username, password)

        def sendmail(self, from_addr, to_addrs, msg):
            self.sendmail_called_with = (from_addr, to_addrs, msg)

        def quit(self):
            self.quit_called = True

    monkeypatch.setattr(smtplib, "SMTP_SSL", MockSMTP_SSL)

    email_message = MIMEMultipart()
    email_message["From"] = "sender@example.com"
    email_message["To"] = "recipient@example.com"
    email_message["Subject"] = "Test"

    email_sender = EmailSender(smtp_config)
    email_sender.send(email_message)

    mock_smtp_instance = instances[0]

    assert mock_smtp_instance.server == smtp_config.server
    assert mock_smtp_instance.port == smtp_config.port
    assert mock_smtp_instance.timeout == smtp_config.timeout
    assert mock_smtp_instance.login_called_with == (
        smtp_config.username,
        smtp_config.password,
    )
    assert mock_smtp_instance.sendmail_called_with == (
        "sender@example.com",
        ["recipient@example.com"],
        email_message.as_string(),
    )
    assert mock_smtp_instance.quit_called is True


def test_email_sender_send_plain(monkeypatch, smtp_config):
    smtp_config.use_ssl = False
    smtp_config.use_tls = False

    instances = []

    class MockSMTP:
        def __init__(self, server, port, timeout=None):
            self.server = server
            self.port = port
            self.timeout = timeout
            self.starttls_called = False
            self.login_called_with = None
            self.sendmail_called_with = None
            self.quit_called = False
            instances.append(self)

        def login(self, username, password):
            self.login_called_with = (username, password)

        def sendmail(self, from_addr, to_addrs, msg):
            self.sendmail_called_with = (from_addr, to_addrs, msg)

        def quit(self):
            self.quit_called = True

    monkeypatch.setattr(smtplib, "SMTP", MockSMTP)

    email_message = MIMEMultipart()
    email_message["From"] = "sender@example.com"
    email_message["To"] = "recipient@example.com"
    email_message["Subject"] = "Test"

    email_sender = EmailSender(smtp_config)
    email_sender.send(email_message)

    mock_smtp_instance = instances[0]

    assert mock_smtp_instance.server == smtp_config.server
    assert mock_smtp_instance.port == smtp_config.port
    assert mock_smtp_instance.timeout == smtp_config.timeout
    assert mock_smtp_instance.login_called_with == (
        smtp_config.username,
        smtp_config.password,
    )
    assert mock_smtp_instance.sendmail_called_with == (
        "sender@example.com",
        ["recipient@example.com"],
        email_message.as_string(),
    )
    assert mock_smtp_instance.quit_called is True


def test_email_sender_send_multiple_recipients(monkeypatch, smtp_config):
    smtp_config.use_tls = True
    instances = []

    class MockSMTP:
        def __init__(self, server, port, timeout=None):
            self.server = server
            self.port = port
            self.timeout = timeout
            self.login_called_with = None
            self.sendmail_called_with = None
            self.quit_called = False
            self.starttls_called = False
            instances.append(self)

        def starttls(self):
            self.starttls_called = True

        def login(self, username, password):
            self.login_called_with = (username, password)

        def sendmail(self, from_addr, to_addrs, msg):
            self.sendmail_called_with = (from_addr, to_addrs, msg)

        def quit(self):
            self.quit_called = True

    monkeypatch.setattr(smtplib, "SMTP", MockSMTP)

    email_builder = EmailMessageBuilder(
        from_address="sender@example.com",
        to_addresses=["recipient1@example.com", "recipient2@example.com"],
    )
    email_builder.add_cc("cc@example.com")
    email_builder.with_subject("Test Subject")
    email_builder.with_body("Test Body")

    email_message = email_builder.build()
    email_sender = EmailSender(smtp_config)
    email_sender.send(email_message)

    expected_recipients = [
        "recipient1@example.com",
        "recipient2@example.com",
        "cc@example.com",
    ]

    mock_smtp_instance = instances[0]

    assert mock_smtp_instance.starttls_called is True
    assert mock_smtp_instance.login_called_with == (
        smtp_config.username,
        smtp_config.password,
    )
    assert mock_smtp_instance.sendmail_called_with == (
        "sender@example.com",
        expected_recipients,
        email_message.as_string(),
    )
    assert mock_smtp_instance.quit_called is True


def test_email_sender_send_exception(monkeypatch, smtp_config):
    class MockSMTP:
        def __init__(self, server, port, timeout=None):
            pass

        def starttls(self):
            pass

        def login(self, username, password):
            pass

        def sendmail(self, from_addr, to_addrs, msg):
            raise smtplib.SMTPException("Sending failed")

        def quit(self):
            pass

    smtp_config.use_tls = True
    smtp_config.use_ssl = False

    monkeypatch.setattr(smtplib, "SMTP", MockSMTP)

    email_message = MIMEMultipart()
    email_message["From"] = "sender@example.com"
    email_message["To"] = "recipient@example.com"
    email_message["Subject"] = "Test"

    email_sender = EmailSender(smtp_config)

    with pytest.raises(smtplib.SMTPException) as exc_info:
        email_sender.send(email_message)

    assert str(exc_info.value) == "Sending failed"


# ============== Extras ==============


def test_add_attachment_invalid_filename(email_builder):
    attachment = MIMEText("Attachment content")

    with pytest.raises(TypeError):
        email_builder.add_attachment(attachment, filename=123)

    with pytest.raises(ValueError):
        email_builder.add_attachment(attachment, filename="   ")


def test_add_attachment_from_nonexistent_path(monkeypatch, email_builder):
    def mock_exists(path):
        return False

    monkeypatch.setattr(os.path, "exists", mock_exists)

    with pytest.raises(FileNotFoundError):
        email_builder.add_attachment_from_path("nonexistent/path.txt")


def test_add_custom_header_invalid(email_builder):
    with pytest.raises(TypeError):
        email_builder.add_custom_header(123, "value")

    with pytest.raises(ValueError):
        email_builder.add_custom_header("X-Header", "")

    with pytest.raises(TypeError):
        email_builder.add_custom_header("X-Header", 456)
