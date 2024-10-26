import pytest

import boto3

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
    def __init__(self):
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
