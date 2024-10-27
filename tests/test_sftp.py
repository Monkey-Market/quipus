import hashlib

import paramiko
import pytest

from quipus import SFTPDelivery


@pytest.fixture
def sftp_delivery():
    return SFTPDelivery(
        host="sftp.example.com",
        username="user",
        password="password",
        port=22,
        private_key=None,
    )


class MockSFTPClient:
    def __init__(self):
        self.files = {}
        self.closed = False

    def get(self, remote_file, local_file):
        if remote_file not in self.files:
            raise FileNotFoundError(f"Remote file {remote_file} does not exist.")
        with open(local_file, "wb") as f:
            f.write(self.files[remote_file])

    def put(self, local_file, remote_file):
        with open(local_file, "rb") as f:
            self.files[remote_file] = f.read()

    def open(self, remote_file, mode="r"):
        if "r" in mode and remote_file not in self.files:
            raise FileNotFoundError(f"Remote file {remote_file} does not exist.")
        from io import BytesIO

        if "r" in mode:
            return BytesIO(self.files[remote_file])
        else:

            def write(data):
                self.files[remote_file] = data

            return type("MockFile", (), {"write": write})

    def close(self):
        self.closed = True


class MockSSHClient:
    def __init__(self):
        self.connected = False
        self.sftp_client = MockSFTPClient()
        self.closed = False

    def set_missing_host_key_policy(self, policy):
        pass

    def connect(self, hostname, port, username, password=None, pkey=None):
        self.connected = True
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.pkey = pkey

    def open_sftp(self):
        return self.sftp_client

    def close(self):
        self.closed = True


# ============== Tests for SFTPDelivery ==============


def test_sftp_delivery_valid_initialization(sftp_delivery):
    assert sftp_delivery.host == "sftp.example.com"
    assert sftp_delivery.port == 22
    assert sftp_delivery.username == "user"
    assert sftp_delivery.password == "password"
    assert sftp_delivery.private_key is None


def test_sftp_delivery_invalid_host():
    with pytest.raises(TypeError):
        SFTPDelivery(host=123, username="user", password="password")
    with pytest.raises(ValueError):
        SFTPDelivery(host="   ", username="user", password="password")


def test_sftp_delivery_invalid_port():
    with pytest.raises(TypeError):
        SFTPDelivery(
            host="sftp.example.com", username="user", password="password", port="22"
        )
    with pytest.raises(ValueError):
        SFTPDelivery(
            host="sftp.example.com", username="user", password="password", port=70000
        )


def test_sftp_delivery_invalid_username():
    with pytest.raises(TypeError):
        SFTPDelivery(host="sftp.example.com", username=123, password="password")
    with pytest.raises(ValueError):
        SFTPDelivery(host="sftp.example.com", username="", password="password")


def test_sftp_delivery_invalid_password():
    with pytest.raises(TypeError):
        SFTPDelivery(host="sftp.example.com", username="user", password=123)
    with pytest.raises(ValueError):
        SFTPDelivery(host="sftp.example.com", username="user", password="")


def test_sftp_delivery_invalid_private_key():
    with pytest.raises(TypeError):
        SFTPDelivery(
            host="sftp.example.com",
            username="user",
            password="password",
            private_key=123,
        )
    with pytest.raises(ValueError):
        SFTPDelivery(
            host="sftp.example.com",
            username="user",
            password="password",
            private_key="   ",
        )


def test_sftp_delivery_connect(monkeypatch, sftp_delivery):
    from quipus.services import sftp_delivery as sftp_module

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClient)
    monkeypatch.setattr(sftp_module, "SFTPClient", MockSFTPClient)

    sftp_delivery.connect()
    assert sftp_delivery.connection.connected is True
    assert sftp_delivery.sftp_client is not None


def test_sftp_delivery_connect_invalid_credentials(monkeypatch, sftp_delivery):
    class MockSSHClientFailure(MockSSHClient):
        def connect(self, hostname, port, username, password=None, pkey=None):
            raise paramiko.AuthenticationException("Authentication failed.")

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClientFailure)

    with pytest.raises(paramiko.AuthenticationException):
        sftp_delivery.connect()


def test_sftp_delivery_upload_file(monkeypatch, sftp_delivery, tmp_path):
    from quipus.services import sftp_delivery as sftp_module

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClient)
    monkeypatch.setattr(sftp_module, "SFTPClient", MockSFTPClient)

    sftp_delivery.connect()

    local_file = tmp_path / "test.txt"
    local_file.write_text("Test content.")

    remote_file = "/remote/test.txt"

    sftp_delivery.upload_file(str(local_file), remote_file)

    assert remote_file in sftp_delivery.sftp_client.files
    assert sftp_delivery.sftp_client.files[remote_file] == b"Test content."


def test_sftp_delivery_download_file(monkeypatch, sftp_delivery, tmp_path):
    from quipus.services import sftp_delivery as sftp_module

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClient)
    monkeypatch.setattr(sftp_module, "SFTPClient", MockSFTPClient)

    sftp_delivery.connect()

    remote_file = "/remote/test.txt"
    sftp_delivery.sftp_client.files[remote_file] = b"Test content."

    local_file = tmp_path / "test.txt"

    sftp_delivery.download_file(remote_file, str(local_file))

    assert local_file.read_bytes() == b"Test content."


def test_sftp_delivery_upload_with_verification(monkeypatch, sftp_delivery, tmp_path):
    from quipus.services import (
        sftp_delivery as sftp_module,
    )

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClient)
    monkeypatch.setattr(sftp_module, "SFTPClient", MockSFTPClient)

    sftp_delivery.connect()

    local_file = tmp_path / "test.txt"
    local_file.write_text("Test content.")

    remote_file = "/remote/test.txt"

    result = sftp_delivery.upload(str(local_file), remote_file, algorithm="md5")

    assert result is True


def test_sftp_delivery_upload_with_verification_failure(
    monkeypatch, sftp_delivery, tmp_path
):
    from quipus.services import sftp_delivery as sftp_module

    class MockSFTPClientCorrupt(MockSFTPClient):
        def put(self, local_file, remote_file):
            self.files[remote_file] = b"Corrupted content."

    class MockSSHClientCorrupt(MockSSHClient):
        def __init__(self):
            self.connected = False
            self.sftp_client = MockSFTPClientCorrupt()
            self.closed = False

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClientCorrupt)
    monkeypatch.setattr(sftp_module, "SFTPClient", MockSFTPClientCorrupt)

    sftp_delivery.connect()

    local_file = tmp_path / "test.txt"
    local_file.write_text("Test content.")

    remote_file = "/remote/test.txt"

    result = sftp_delivery.upload(str(local_file), remote_file, algorithm="md5")

    assert result is False


def test_sftp_delivery_close(monkeypatch, sftp_delivery):
    from quipus.services import sftp_delivery as sftp_module

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClient)
    monkeypatch.setattr(sftp_module, "SFTPClient", MockSFTPClient)

    sftp_delivery.connect()
    sftp_delivery.close()

    assert sftp_delivery.sftp_client.closed is True
    assert sftp_delivery.connection.closed is True


def test_sftp_delivery_download_file_without_connection(sftp_delivery, tmp_path):
    remote_file = "/remote/test.txt"
    local_file = tmp_path / "test.txt"

    with pytest.raises(ValueError, match="SFTP connection not established"):
        sftp_delivery.download_file(remote_file, str(local_file))


def test_sftp_delivery_upload_file_without_connection(sftp_delivery, tmp_path):
    local_file = tmp_path / "test.txt"
    local_file.write_text("Test content.")
    remote_file = "/remote/test.txt"

    with pytest.raises(ValueError, match="SFTP connection not established"):
        sftp_delivery.upload_file(str(local_file), remote_file)


def test_sftp_delivery_connect_invalid_private_key(monkeypatch):
    from quipus.services import sftp_delivery as sftp_module

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClient)
    monkeypatch.setattr(
        "paramiko.RSAKey.from_private_key_file",
        lambda x: (_ for _ in ()).throw(paramiko.SSHException("Invalid private key")),
    )
    monkeypatch.setattr(sftp_module, "SFTPClient", MockSFTPClient)

    sftp_delivery = SFTPDelivery(
        host="sftp.example.com",
        username="user",
        password="password",
        private_key="/path/to/invalid/key",
    )

    with pytest.raises(paramiko.SSHException, match="Invalid private key"):
        sftp_delivery.connect()


# ============== Extras ==============


def test_sftp_delivery_upload_invalid_checksum_algorithm(
    monkeypatch, sftp_delivery, tmp_path
):
    from quipus.services import sftp_delivery as sftp_module

    monkeypatch.setattr("paramiko.SSHClient", MockSSHClient)
    monkeypatch.setattr(sftp_module, "SFTPClient", MockSFTPClient)

    sftp_delivery.connect()

    local_file = tmp_path / "test.txt"
    local_file.write_text("Test content.")
    remote_file = "/remote/test.txt"

    with pytest.raises(ValueError):
        sftp_delivery.upload(str(local_file), remote_file, algorithm="invalid_algo")


def test_sftp_delivery_calculate_checksum(sftp_delivery, tmp_path):
    local_file = tmp_path / "test.txt"
    local_file.write_text("Test content.")

    checksum = sftp_delivery._SFTPDelivery__calculate_checksum(
        str(local_file), algorithm="md5"
    )
    expected_checksum = hashlib.md5(b"Test content.").hexdigest()
    assert checksum == expected_checksum

    assert checksum == expected_checksum


def test_sftp_delivery_str(sftp_delivery):
    sftp_str = str(sftp_delivery)
    expected_str = str(
        {
            "host": "sftp.example.com",
            "port": 22,
            "username": "user",
            "private_key": None,
        }
    )
    assert sftp_str == expected_str
