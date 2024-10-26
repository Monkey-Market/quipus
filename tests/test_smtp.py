import pytest

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

