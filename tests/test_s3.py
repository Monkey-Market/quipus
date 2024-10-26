import pytest
import boto3
from botocore.exceptions import NoCredentialsError

from quipus import AWSConfig, S3Delivery


@pytest.fixture
def aws_config():
    return AWSConfig(
        aws_access_key="fake_access_key",
        aws_secret_access_key="fake_secret_key",
        region="us-east-1",
    )


@pytest.fixture
def s3_delivery(aws_config):
    return S3Delivery(aws_config)


class MockS3Client:
    def __init__(self, *args, **kwargs):
        self.uploaded_files = {}

    def upload_file(self, Filename, Bucket, Key):
        self.uploaded_files[Key] = {"Bucket": Bucket, "Filename": Filename}


# ============== Tests for AWSConfig ==============


def test_aws_config_valid_initialization():
    aws_config = AWSConfig(
        aws_access_key="fake_access_key",
        aws_secret_access_key="fake_secret_key",
        region="us-east-1",
    )
    assert aws_config.aws_access_key_id == "fake_access_key"
    assert aws_config.aws_secret_access_key == "fake_secret_key"
    assert aws_config.aws_region == "us-east-1"


def test_aws_config_invalid_access_key():
    with pytest.raises(TypeError):
        AWSConfig(
            aws_access_key=123, aws_secret_access_key="secret", region="us-east-1"
        )
    with pytest.raises(ValueError):
        AWSConfig(aws_access_key="", aws_secret_access_key="secret", region="us-east-1")


def test_aws_config_invalid_secret_key():
    with pytest.raises(TypeError):
        AWSConfig(
            aws_access_key="access", aws_secret_access_key=123, region="us-east-1"
        )
    with pytest.raises(ValueError):
        AWSConfig(aws_access_key="access", aws_secret_access_key="", region="us-east-1")


def test_aws_config_invalid_region():
    with pytest.raises(TypeError):
        AWSConfig(aws_access_key="access", aws_secret_access_key="secret", region=123)
    with pytest.raises(ValueError):
        AWSConfig(aws_access_key="access", aws_secret_access_key="secret", region="")


def test_aws_config_from_profile(monkeypatch):
    class MockSession:
        def __init__(self, profile_name=None):
            self.profile_name = profile_name

        def get_credentials(self):
            class Credentials:
                access_key = "profile_access_key"
                secret_key = "profile_secret_key"

            return Credentials()

        @property
        def region_name(self):
            return "us-west-2"

    monkeypatch.setattr(boto3, "Session", MockSession)

    aws_config = AWSConfig.from_profile(profile_name="default")
    assert aws_config.aws_access_key_id == "profile_access_key"
    assert aws_config.aws_secret_access_key == "profile_secret_key"
    assert aws_config.aws_region == "us-west-2"


# ============== Tests for S3Delivery ==============


def test_s3_delivery_upload_file(monkeypatch, s3_delivery, tmp_path):
    mock_s3_client = MockS3Client()

    def mock_boto3_client(*args, **kwargs):
        assert args[0] == "s3"
        return mock_s3_client

    monkeypatch.setattr(boto3, "client", mock_boto3_client)

    local_file = tmp_path / "test.txt"
    local_file.write_text("Contenido de prueba.")

    bucket_name = "my-bucket"
    key = "folder/test.txt"

    s3_delivery.upload_file(str(local_file), bucket_name, key)

    assert key in mock_s3_client.uploaded_files
    uploaded_file = mock_s3_client.uploaded_files[key]
    assert uploaded_file["Bucket"] == bucket_name
    assert uploaded_file["Filename"] == str(local_file)


def test_s3_delivery_upload_many_files(monkeypatch, s3_delivery, tmp_path):
    mock_s3_client = MockS3Client()

    def mock_boto3_client(*args, **kwargs):
        return mock_s3_client

    monkeypatch.setattr(boto3, "client", mock_boto3_client)

    local_file1 = tmp_path / "test1.txt"
    local_file1.write_text("Contenido de prueba 1.")

    local_file2 = tmp_path / "test2.txt"
    local_file2.write_text("Contenido de prueba 2.")

    files = [
        (str(local_file1), "folder/test1.txt"),
        (str(local_file2), "folder/test2.txt"),
    ]

    bucket_name = "my-bucket"

    s3_delivery.upload_many_files(files, bucket_name)

    uploaded_files = mock_s3_client.uploaded_files
    assert "folder/test1.txt" in uploaded_files
    assert "folder/test2.txt" in uploaded_files


def test_s3_delivery_upload_file_invalid_parameters(s3_delivery):
    with pytest.raises(TypeError):
        s3_delivery.upload_file(123, "bucket", "key")
    with pytest.raises(ValueError):
        s3_delivery.upload_file("", "bucket", "key")

    with pytest.raises(TypeError):
        s3_delivery.upload_file("path", 123, "key")
    with pytest.raises(ValueError):
        s3_delivery.upload_file("path", "", "key")

    with pytest.raises(TypeError):
        s3_delivery.upload_file("path", "bucket", 123)
    with pytest.raises(ValueError):
        s3_delivery.upload_file("path", "bucket", "")


def test_s3_delivery_upload_file_no_credentials(monkeypatch, s3_delivery, tmp_path):
    def mock_boto3_client(*args, **kwargs):
        raise NoCredentialsError()

    monkeypatch.setattr(boto3, "client", mock_boto3_client)

    local_file = tmp_path / "test.txt"
    local_file.write_text("Contenido de prueba.")
    bucket_name = "my-bucket"
    key = "folder/test.txt"

    with pytest.raises(NoCredentialsError):
        s3_delivery.upload_file(str(local_file), bucket_name, key)


def test_s3_delivery_upload_many_files_invalid_parameters(s3_delivery):
    with pytest.raises(TypeError):
        s3_delivery.upload_many_files("not a list", "bucket")

    with pytest.raises(TypeError):
        s3_delivery.upload_many_files([], 123)

    with pytest.raises(TypeError):
        s3_delivery.upload_many_files([("path", "key")], 123)
