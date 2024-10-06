from email.mime.base import MIMEBase
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Literal, Self, Optional


class SMTPConfig:
    """
    SMTP configuration class.

    Attributes:
        server (str): SMTP server address.
        port (int): SMTP server port.
        username (str): SMTP server username.
        password (str): SMTP server password.
        use_tls (bool): Use TLS for the connection.
        use_ssl (bool): Use SSL for the connection.
        timeout (Optional[int]): Connection timeout.
    """

    def __init__(
        self,
        server: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool = False,
        use_ssl: bool = False,
        timeout: Optional[int] = None,
    ):
        """
        Initializes an instance of the SMTPConfig class.

        Args:
            server (str): SMTP server address.
            port (int): SMTP server port.
            username (str): SMTP server username.
            password (str): SMTP server password.
            use_tls (bool): Use TLS for the connection.
            use_ssl (bool): Use SSL for the connection.
            timeout (Optional[int]): Connection timeout.
        """
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        self.timeout = timeout

    @property
    def server(self) -> str:
        """
        Get the SMTP server address.

        Returns:
            str: SMTP server address.
        """
        return self.__server

    @server.setter
    def server(self, server: str) -> None:
        """
        Set the SMTP server address.

        Args:
            server (str): SMTP server address.

        Raises:
            TypeError: If 'server' is not a string.
            ValueError: If 'server' is an empty string.
        """
        if not isinstance(server, str):
            raise TypeError(
                "'server' must be a string.",
                f"Current type: {type(server)}.",
            )

        if not server.strip():
            raise ValueError("'server' cannot be an empty string.")

        self.__server = server

    @property
    def port(self) -> int:
        """
        Get the SMTP server port.

        Returns:
            int: SMTP server port.
        """
        return self.__port

    @port.setter
    def port(self, port: int) -> None:
        """
        Set the SMTP server port.

        Args:
            port (int): SMTP server port.

        Raises:
            TypeError: If 'port' is not an integer.
            ValueError: If 'port' is not between 1 and 65535.
        """
        if not isinstance(port, int):
            raise TypeError(
                "'port' must be an integer.",
                f"Current type: {type(port)}.",
            )

        if port not in range(1, 65536):
            raise ValueError(
                "'port' must be between 1 and 65535.",
                f"Current value: {port}.",
            )

        self.__port = port

    @property
    def username(self) -> str:
        """
        Get the SMTP server username.

        Returns:
            str: SMTP server username.
        """
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        """
        Set the SMTP server username.

        Args:
            username (str): SMTP server username.

        Raises:
            TypeError: If 'username' is not a string.
            ValueError: If 'username' is an empty string.
        """
        if not isinstance(username, str):
            raise TypeError(
                "'username' must be a string.",
                f"Current type: {type(username)}.",
            )

        if not username.strip():
            raise ValueError("'username' cannot be an empty string.")

        self.__username = username

    @property
    def password(self) -> str:
        """
        Get the SMTP server password.

        Returns:
            str: SMTP server password.
        """
        return self.__password

    @password.setter
    def password(self, password: str) -> None:
        """
        Set the SMTP server password.

        Args:
            password (str): SMTP server password.

        Raises:
            TypeError: If 'password' is not a string.
        """
        if not isinstance(password, str):
            raise TypeError(
                "'password' must be a string.",
                f"Current type: {type(password)}.",
            )

        self.__password = password

    @property
    def use_tls(self) -> bool:
        """
        Get the use of TLS for the connection.

        Returns:
            bool: Use TLS for the connection.
        """
        return self.__use_tls

    @use_tls.setter
    def use_tls(self, use_tls: bool) -> None:
        """
        Set the use of TLS for the connection.

        Args:
            use_tls (bool): Use TLS for the connection.

        Raises:
            TypeError: If 'use_tls' is not a boolean."""
        if not isinstance(use_tls, bool):
            raise TypeError(
                "'use_tls' must be a boolean.",
                f"Current type: {type(use_tls)}.",
            )

        self.__use_tls = use_tls

    @property
    def use_ssl(self) -> bool:
        """
        Get the use of SSL for the connection.

        Returns:
            bool: Use SSL for the connection.
        """
        return self.__use_ssl

    @use_ssl.setter
    def use_ssl(self, use_ssl: bool) -> None:
        """
        Set the use of SSL for the connection.

        Args:
            use_ssl (bool): Use SSL for the connection.

        Raises:
            TypeError: If 'use_ssl' is not a boolean."""
        if not isinstance(use_ssl, bool):
            raise TypeError(
                "'use_ssl' must be a boolean.",
                f"Current type: {type(use_ssl)}.",
            )

        self.__use_ssl = use_ssl

    @property
    def timeout(self) -> Optional[int]:
        """
        Get the connection timeout.

        Returns:
            Optional[int]: Connection timeout.
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: Optional[int]) -> None:
        """
        Set the connection timeout.

        Args:
            timeout (Optional[int]): Connection timeout.

        Raises:
            TypeError: If 'timeout' is not an integer or None.
            ValueError: If 'timeout' is less than 0.
        """
        if timeout is None:
            self.__timeout = timeout
            return

        if not isinstance(timeout, int):
            raise TypeError(
                "'timeout' must be an integer or None.",
                f"Current type: {type(timeout)}.",
            )

        if timeout < 0:
            raise ValueError(
                "'timeout' must be greater than or equal to 0.",
                f"Current value: {timeout}.",
            )

        self.__timeout = timeout

    def __str__(self) -> str:
        """
        Get a string representation of the SMTPConfig instance.

        Returns:
            str: String representation of the SMTPConfig instance.
        """
        return str(
            {
                "server": self.server,
                "port": self.port,
                "username": self.username,
                "password": self.password,
                "use_tls": self.use_tls,
                "use_ssl": self.use_ssl,
                "timeout": self.timeout,
            }
        )


class EmailMessageBuilder:
    """
    Email message builder class.

    Attributes:
        from_address (str): Email sender address.
        to_addresses (list[str]): Email recipient addresses.
        cc_addresses (list[str]): Email CC addresses.
        subject (str): Email subject.
        body (str): Email body.
        body_type (Literal["html", "plain"]): Email body type.
        attachments (list[tuple[MIMEBase, Optional[str]]]): Email attachments.
        custom_headers (Optional[dict[str, str]]): Email custom headers.
    """

    __SUPPORTED_BODY_TYPES: list[str] = ["plain", "html"]

    def __init__(self, from_address: str, to_addresses: list[str]):
        """
        Initializes an instance of the EmailMessageBuilder class.

        Args:
            from_address (str): Email sender address.
            to_addresses (list[str]): Email recipient addresses.
        """
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.cc_addresses = []
        self.subject = ""
        self.body = ""
        self.body_type = "plain"
        self.attachments = []
        self.custom_headers = {}

    @property
    def from_address(self) -> str:
        """
        Get the email sender address.

        Returns:
            str: Email sender address.
        """
        return self.__from_address

    @from_address.setter
    def from_address(self, from_address: str) -> None:
        """
        Set the email sender address.

        Args:
            from_address (str): Email sender address.

        Raises:
            TypeError: If 'from_address' is not a string.
            ValueError: If 'from_address' is an empty string.
        """
        if not isinstance(from_address, str):
            raise TypeError(
                "'from_address' must be a string.",
                f"Current type: {type(from_address)}.",
            )

        if not from_address.strip():
            raise ValueError("'from_address' cannot be an empty string.")

        self.__from_address = from_address

    @property
    def to_addresses(self) -> list[str]:
        """
        Get the email recipient addresses.

        Returns:
            list[str]: Email recipient addresses.
        """
        return self.__to_addresses

    @to_addresses.setter
    def to_addresses(self, to_addresses: list[str]) -> None:
        """
        Set the email recipient addresses.

        Args:
            to_addresses (list[str]): Email recipient addresses.

        Raises:
            TypeError: If 'to_addresses' is not a list.
            ValueError: If 'to_addresses' is empty.
            TypeError: If 'to_addresses' contains non-string values.
            ValueError: If 'to_addresses' contains empty strings.
        """
        if not isinstance(to_addresses, list):
            raise TypeError(
                "'to_addresses' must be a list.",
                f"Current type: {type(to_addresses)}.",
            )

        if not to_addresses:
            raise ValueError("'to_addresses' cannot be empty.")

        if not all(isinstance(addr, str) for addr in to_addresses):
            raise TypeError(
                "'to_addresses' must contain only strings.",
                f"Invalid values: {to_addresses}.",
            )

        if not all(addr.strip() for addr in to_addresses):
            raise ValueError("'to_addresses' cannot contain empty strings.")

        self.__to_addresses = to_addresses

    @property
    def cc_addresses(self) -> list[str]:
        """
        Get the email CC addresses.

        Returns:
            list[str]: Email CC addresses.
        """
        return self.__cc_addresses

    @cc_addresses.setter
    def cc_addresses(self, cc_addresses: list[str]) -> None:
        """
        Set the email CC addresses.

        Args:
            cc_addresses (list[str]): Email CC addresses.

        Raises:
            TypeError: If 'cc_addresses' is not a list.
            TypeError: If 'cc_addresses' contains non-string values.
            ValueError: If 'cc_addresses' contains empty strings.
        """
        if not isinstance(cc_addresses, list):
            raise TypeError(
                "'cc_addresses' must be a list.",
                f"Current type: {type(cc_addresses)}.",
            )

        if not all(isinstance(addr, str) for addr in cc_addresses):
            raise TypeError(
                "'cc_addresses' must contain only strings.",
                f"Invalid values: {cc_addresses}.",
            )

        if not all(addr.strip() for addr in cc_addresses):
            raise ValueError("'cc_addresses' cannot contain empty strings.")

        self.__cc_addresses = cc_addresses

    @property
    def subject(self) -> str:
        """
        Get the email subject.

        Returns:
            str: Email subject.
        """
        return self.__subject

    @subject.setter
    def subject(self, subject: str) -> Self:
        """
        Set the email subject.

        Args:
            subject (str): Email subject.

        Raises:
            TypeError: If 'subject' is not a string.
        """
        if not isinstance(subject, str):
            raise TypeError(
                "'subject' must be a string.",
                f"Current type: {type(subject)}.",
            )

        self.__subject = subject

    @property
    def body(self) -> str:
        """
        Get the email body.

        Returns:
            str: Email body.
        """
        return self.__body

    @body.setter
    def body(self, body: str) -> None:
        """
        Set the email body.

        Args:
            body (str): Email body.

        Raises:
            TypeError: If 'body' is not a string.
        """
        if not isinstance(body, str):
            raise TypeError(
                "'body' must be a string.",
                f"Current type: {type(body)}.",
            )

        self.__body = body

    @property
    def body_type(self) -> str:
        """
        Get the email body type.

        Returns:
            str: Email body type.
        """
        return self.__body_type

    @body_type.setter
    def body_type(self, body_type: Literal["html", "plain"]) -> None:
        """
        Set the email body type.

        Args:
            body_type (Literal["html", "plain"]): Email body type.

        Raises:
            TypeError: If 'body_type' is not a string.
            ValueError: If 'body_type' is not 'plain' or 'html'.
        """
        if not isinstance(body_type, str):
            raise TypeError(
                "'body_type' must be a string.",
                f"Current type: {type(body_type)}.",
            )

        if body_type not in self.__SUPPORTED_BODY_TYPES:
            raise ValueError(
                "'body_type' must be either 'plain' or 'html'.",
                f"Current value: {body_type}.",
            )

        self.__body_type = body_type

    @property
    def attachments(self) -> list[tuple[MIMEBase, Optional[str]]]:
        """
        Get the email attachments.

        Returns:
            list[tuple[MIMEBase, Optional[str]]]: Email attachments.
        """
        return self.__attachments

    @attachments.setter
    def attachments(self, attachments: list[tuple[MIMEBase, Optional[str]]]) -> None:
        """
        Set the email attachments.

        Args:
            attachments (list[tuple[MIMEBase, Optional[str]]]): Email attachments.

        Raises:
            TypeError: If 'attachments' is not a list."""
        if not isinstance(attachments, list):
            raise TypeError(
                "'attachments' must be a list.",
                f"Current type: {type(attachments)}.",
            )

        self.__attachments = attachments

    @property
    def custom_headers(self) -> dict[str, str]:
        """
        Get the email custom headers.

        Returns:
            dict[str, str]: Email custom headers.
        """
        return self.__custom_headers

    @custom_headers.setter
    def custom_headers(self, custom_headers: Optional[dict[str, str]] = None) -> None:
        """
        Set the email custom headers.

        Args:
            custom_headers (Optional[dict[str, str]]): Email custom headers.

        Raises:
            TypeError: If 'custom_headers' is not a dictionary.
            TypeError: If 'custom_headers' contains non-string values.
            ValueError: If 'custom_headers' contains empty strings.
        """
        if custom_headers is None:
            self.__custom_headers = None
            return

        if not isinstance(custom_headers, dict):
            raise TypeError(
                "'custom_headers' must be a dictionary.",
                f"Current type: {type(custom_headers)}.",
            )

        if not all(
            isinstance(header, str) and isinstance(value, str)
            for header, value in custom_headers.items()
        ):
            raise TypeError(
                "'custom_headers' must contain only strings.",
                f"Invalid values: {custom_headers}.",
            )

        if not all(
            header.strip() and value.strip() for header, value in custom_headers.items()
        ):
            raise ValueError("'custom_headers' cannot contain empty strings.")

        self.__custom_headers = custom_headers

    def add_recipient(self, to_address: str) -> Self:
        """
        Add a recipient to the email message.

        Args:
            to_address (str): Email recipient address.
        """
        if not isinstance(to_address, str):
            raise TypeError(
                "'to_address' must be a string.",
                f"Current type: {type(to_address)}.",
            )

        if not to_address.strip():
            raise ValueError("'to_address' cannot be an empty string.")

        self.to_addresses.append(to_address)

        return self

    def add_cc(self, cc_address: str) -> Self:
        """
        Add a recipient to the email message.

        Args:
            cc_address (str): Email recipient address.
        """
        if not isinstance(cc_address, str):
            raise TypeError(
                "'cc_address' must be a string.",
                f"Current type: {type(cc_address)}.",
            )

        if not cc_address.strip():
            raise ValueError("'cc_address' cannot be an empty string.")

        self.cc_addresses.append(cc_address)

        return self

    def with_subject(self, subject: str) -> Self:
        """
        Set the email subject.

        Args:
            subject (str): Email subject.

        Returns:
            Self: EmailMessageBuilder instance.
        """
        self.subject = subject
        return self

    def with_body(
        self, body: str, body_type: Literal["plain", "html"] = "plain"
    ) -> Self:
        """
        Set the email body.

        Args:
            body (str): Email body.
            body_type (Literal["plain", "html"]): Email body type.

        Returns:
            Self: EmailMessageBuilder instance.
        """
        self.body = body
        self.body_type = body_type
        return self

    def with_body_path(
        self,
        body_path: str,
        body_type: Literal["plain", "html"] = "plain",
        replacements: dict = None,
    ) -> Self:
        """
        Set the email body from a file path and replace placeholders.

        Args:
            body_path (str): Email body path.
            body_type (Literal["plain", "html"]): Email body type.
            replacements (dict): Dictionary of replacements for placeholders.

        Returns:
            Self: EmailMessageBuilder instance.

        Raises:
            TypeError: If 'body_path' is not a string.
            ValueError: If 'body_path' is an empty string.
            FileNotFoundError: If the body path does not exist.
        """
        if not isinstance(body_path, str):
            raise TypeError(
                "'body_path' must be a string.",
                f"Current type: {type(body_path)}.",
            )

        if not body_path.strip():
            raise ValueError("'body_path' cannot be an empty string.")

        if not os.path.exists(body_path):
            raise FileNotFoundError(f"Body path '{body_path}' does not exist.")

        with open(body_path, "r") as body_file:
            self.body = body_file.read()

        if replacements:
            for key, value in replacements.items():
                self.body = self.body.replace(f"{{{key}}}", value)

        self.body_type = body_type
        return self

    def __convert_attachment_path_to_mime_application(
        self, attachment_path: str
    ) -> MIMEApplication:
        """
        Convert an attachment path to a MIMEApplication instance.

        Args:
            attachment_path (str): Attachment path.

        Returns:
            MIMEApplication: MIMEApplication instance.

        Raises:
            TypeError: If 'attachment_path' is not a string.
            ValueError: If 'attachment_path' is an empty string.
            FileNotFoundError: If the attachment path does not exist.
        """
        if not isinstance(attachment_path, str):
            raise TypeError(
                "'attachment_path' must be a string.",
                f"Current type: {type(attachment_path)}.",
            )

        if not attachment_path.strip():
            raise ValueError("'attachment_path' cannot be an empty string.")

        if not os.path.exists(attachment_path):
            raise FileNotFoundError(
                f"Attachment path '{attachment_path}' does not exist."
            )

        with open(attachment_path, "rb") as attachment_file:
            attachment = MIMEApplication(attachment_file.read())

        return attachment

    def add_attachment(
        self, attachment: MIMEBase, filename: Optional[str] = None
    ) -> Self:
        """
        Add an attachment to the email message.

        Args:
            attachment (MIMEBase): Attachment to add.
            filename (Optional[str]): Attachment filename.

        Returns:
            Self: EmailMessageBuilder instance.

        Raises:
            TypeError: If 'attachment' is not an instance of MIMEBase.
            TypeError: If 'filename' is not a string.
            ValueError: If 'filename' is an empty string.
        """
        if not isinstance(attachment, MIMEBase):
            raise TypeError(
                "'attachment' must be an instance of MIMEBase.",
                f"Current type: {type(attachment)}.",
            )

        if filename is not None and not isinstance(filename, str):
            raise TypeError(
                "'filename' must be a string.",
                f"Current type: {type(filename)}.",
            )

        if not filename.strip():
            raise ValueError("'filename' cannot be an empty string.")

        self.attachments.append((attachment, filename))
        return self

    def add_attachment_from_path(
        self, attachment_path: str, filename: Optional[str] = None
    ) -> Self:
        """
        Add an attachment to the email message from a file path.

        Args:
            attachment_path (str): Attachment path.
            filename (Optional[str]): Attachment filename.

        Returns:
            Self: EmailMessageBuilder instance.

        Raises:
            TypeError: If 'attachment_path' is not a string.
            ValueError: If 'attachment_path' is an empty string.
        """
        attachment = self.__convert_attachment_path_to_mime_application(attachment_path)

        if filename is None:
            filename = os.path.basename(attachment_path)

        self.attachments.append((attachment, filename))
        return self

    def add_custom_header(self, header: str, value: str) -> Self:
        """
        Add a custom header to the email message.

        Args:
            header (str): Custom header.
            value (str): Custom header value.

        Returns:
            Self: EmailMessageBuilder instance.

        Raises:
            TypeError: If 'header' is not a string.
            ValueError: If 'header' is an empty string.
            TypeError: If 'value' is not a string.
            ValueError: If 'value' is an empty string.
        """
        if not isinstance(header, str):
            raise TypeError(
                "'header' must be a string.",
                f"Current type: {type(header)}.",
            )

        if not header.strip():
            raise ValueError("'header' cannot be an empty string.")

        if not isinstance(value, str):
            raise TypeError(
                "'value' must be a string.",
                f"Current type: {type(value)}.",
            )

        if not value.strip():
            raise ValueError("'value' cannot be an empty string.")

        if self.custom_headers is not None:
            self.custom_headers[header] = value
        return self

    def __pre_build_validation(self) -> None:
        """
        Perform pre-build validation checks.

        Raises:
            ValueError: If 'from_address' or 'to_addresses' are not set.
            ValueError: If custom headers do not have values.
        """
        if not self.from_address or not self.to_addresses:
            raise ValueError(
                "Both 'from_address' and 'to_addresses' must be set.",
                f"Current values: {self.from_address}, {self.to_addresses}.",
            )

        if (self.custom_headers is not None and self.custom_headers != {}) and not any(
            self.custom_headers.values()
        ):
            raise ValueError(
                "Custom headers must have values.",
                f"Current values: {self.custom_headers}.",
            )

    def build(self) -> MIMEMultipart:
        """
        Build the email message.

        Returns:
            MIMEMultipart: Email message.

        Raises:
            ValueError: If pre-build validation checks fail.
        """
        self.__pre_build_validation()

        email_message = MIMEMultipart()
        email_message["From"] = self.from_address
        email_message["To"] = ", ".join(self.to_addresses)
        email_message["Cc"] = ", ".join(self.cc_addresses)
        email_message["Subject"] = self.subject

        for header, value in self.custom_headers.items() if self.custom_headers else []:
            email_message[header] = value

        body = MIMEText(self.body, self.body_type)
        email_message.attach(body)

        for attachment, filename in self.attachments:
            attachment.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}",
            )
            email_message.attach(attachment)

        return email_message

    def __str__(self) -> str:
        """
        Get a string representation of the EmailMessageBuilder instance.

        Returns:
            str: String representation of the EmailMessageBuilder instance.
        """
        return str(
            {
                "from_address": self.from_address,
                "to_addresses": self.to_addresses,
                "cc_addresses": self.cc_addresses,
                "subject": self.subject,
                "body": self.body,
                "body_type": self.body_type,
                "attachments": self.attachments,
                "custom_headers": self.custom_headers,
            }
        )


class EmailSender:
    """
    Email sender class.

    Attributes:
        smtp_config (SMTPConfig): SMTP configuration.
    """

    def __init__(
        self,
        smtp_config: SMTPConfig,
    ):
        """
        Initializes an instance of the EmailSender class.

        Args:
            smtp_config (SMTPConfig): SMTP configuration.
        """
        self.smtp_config = smtp_config

    def send(self, email_message: MIMEMultipart) -> None:
        """
        Send an email message.

        Args:
            email_message (MIMEMultipart): Email message.

        Raises:
            smtplib.SMTPException: If an error occurs while sending the email.

        ## Usage:

        ```python
        smtp_config = SMTPConfig(
            server="smtp.office365.com",
            port=587,
            username="your_username",
            password="your_password",
            use_tls=True,
        )
        email_message = (
            EmailMessageBuilder(
                from_address="sender@example.com",
                to_addresses=['recipient@example.com']
            )
            .with_subject("Your subject")
            .with_body("<h1>Hello world</h1>", body_type="html")
            .add_attachment_from_path("path/to/attachment", "attachment_filename")
            .build()
        )

        email_sender = EmailSender(smtp_config)
        email_sender.send(email_message)
        ```
        """
        if self.smtp_config.use_ssl:
            server = smtplib.SMTP_SSL(
                self.smtp_config.server,
                self.smtp_config.port,
                timeout=self.smtp_config.timeout,
            )
        else:
            server = smtplib.SMTP(
                self.smtp_config.server,
                self.smtp_config.port,
                timeout=self.smtp_config.timeout,
            )

            if self.smtp_config.use_tls:
                server.starttls()

        server.login(
            self.smtp_config.username,
            self.smtp_config.password,
        )
        server.sendmail(
            email_message["From"],
            email_message["To"].split(", "),
            email_message.as_string(),
        )
        server.quit()

    def __str__(self) -> str:
        """
        Get a string representation of the EmailSender instance.

        Returns:
            str: String representation of the EmailSender instance.
        """
        return str(
            {
                "smtp_config": str(self.smtp_config),
            }
        )
