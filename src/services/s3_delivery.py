from typing import Optional
import boto3


class AWSConfig:
    """
    AWS configuration class.

    Attributes:
        AWS_ACCESS_KEY_ID (str): AWS access key.
        AWS_SECRET_ACCESS_KEY (str): AWS secret access key.
        AWS_REGION (str): AWS region.
    """

    def __init__(
        self, aws_access_key: str, aws_secret_access_key: str, region: str
    ) -> None:
        """
        Initialize the AWSConfig object.

        Args:
            aws_access_key (str): AWS access key.
            aws_secret_access_key (str): AWS secret access key.
            region (str): AWS region.
        """
        self.AWS_ACCESS_KEY_ID = aws_access_key
        self.AWS_SECRET_ACCESS_KEY = aws_secret_access_key
        self.AWS_REGION = region

        @property
        def AWS_ACCESS_KEY_ID(self) -> str:
            """
            Get the AWS access key.
            """
            return self._AWS_ACCESS_KEY_ID

        @AWS_ACCESS_KEY_ID.setter
        def AWS_ACCESS_KEY_ID(self, value: str) -> None:
            """
            Set the AWS access key.

            Args:
                value (str): AWS access key.
            """
            if not isinstance(value, str):
                raise TypeError("AWS access key must be a string.")

            if not value or len(value) == 0:
                raise ValueError("AWS access key cannot be empty.")

            self._AWS_ACCESS_KEY_ID = value

        @property
        def AWS_SECRET_ACCESS_KEY(self) -> str:
            """
            Get the AWS secret access key.
            """
            return self._AWS_SECRET_ACCESS_KEY

        @AWS_SECRET_ACCESS_KEY.setter
        def AWS_SECRET_ACCESS_KEY(self, value: str) -> None:
            """
            Set the AWS secret access key.

            Args:
                value (str): AWS secret access key.
            """
            if not isinstance(value, str):
                raise TypeError("AWS secret access key must be a string.")

            if not value or len(value) == 0:
                raise ValueError("AWS secret access key cannot be empty.")

            self._AWS_SECRET_ACCESS_KEY = value

        @property
        def AWS_REGION(self) -> str:
            """
            Get the AWS region.
            """
            return self._AWS_REGION

        @AWS_REGION.setter
        def AWS_REGION(self, value: str) -> None:
            """
            Set the AWS region.

            Args:
                value (str): AWS region.
            """
            if not isinstance(value, str):
                raise TypeError("AWS region must be a string.")

            if not value or len(value) == 0:
                raise ValueError("AWS region cannot be empty.")

            self._AWS_REGION = value

    @staticmethod
    def from_profile(profile_name: Optional[str] = "") -> "AWSConfig":
        """
        Create an AWSConfig object from a profile name.

        Args:
            profile_name (str): Profile name to be used. Will use the default profile if not provided.
        """
        session = boto3.Session(profile_name=profile_name)
        credentials = session.get_credentials()
        region = session.region_name
        return AWSConfig(
            aws_access_key=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            region=region,
        )


class S3Delivery:
    """
    S3 delivery class.

    Attributes:
        _aws_config (AWSConfig): AWS configuration object.
    """

    def __init__(self, aws_config: AWSConfig) -> None:
        """
        Initialize the S3Delivery object.

        Args:
            aws_config (AWSConfig): AWS configuration object.
        """
        self._aws_config = aws_config

    @property
    def aws_config(self) -> AWSConfig:
        """
        Get the AWS configuration object.
        """
        return self._aws_config

    @aws_config.setter
    def aws_config(self, value: AWSConfig) -> None:
        """
        Set the AWS configuration object.

        Args:
            value (AWSConfig): AWS configuration object.
        """
        if not isinstance(value, AWSConfig):
            raise TypeError("AWS configuration must be an AWSConfig object.")

        self._aws_config = value

    def upload_file(self, file_path: str, bucket_name: str, key: str) -> None:
        """
        Upload a file to an S3 bucket.

        Args:
            file_path (str): Path to the file to be uploaded.
            bucket_name (str): Name of the bucket to upload the file to.
            key (str): Key to be used for the file in the bucket.
        """

        if not isinstance(file_path, str):
            raise TypeError("File path must be a string.")
        elif not isinstance(bucket_name, str):
            raise TypeError("Bucket name must be a string.")
        elif not isinstance(key, str):
            raise TypeError("Key must be a string.")

        if not file_path or len(file_path) == 0:
            raise ValueError("File path cannot be empty.")
        elif not bucket_name or len(bucket_name) == 0:
            raise ValueError("Bucket name cannot be empty.")
        elif not key or len(key) == 0:
            raise ValueError("Key cannot be empty.")

        s3 = boto3.client(
            "s3",
            aws_access_key_id=self._aws_config._AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self._aws_config._AWS_SECRET_ACCESS_KEY,
            region_name=self._aws_config._AWS_REGION,
        )
        s3.upload_file(file_path, bucket_name, key)

    def upload_many_files(self, files: list[tuple[str, str]], bucket_name: str) -> None:
        """
        Upload multiple files to an S3 bucket.

        Args:
            files (list): List of tuples containing the file path and key for each file.
            bucket_name (str): Name of the bucket to upload the files to.
        """

        if not isinstance(files, list):
            raise TypeError("Files must be a list.")

        if not isinstance(bucket_name, str):
            raise TypeError("Bucket name must be a string.")

        s3 = boto3.client(
            "s3",
            aws_access_key_id=self._aws_config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self._aws_config.AWS_SECRET_ACCESS_KEY,
            region_name=self._aws_config.AWS_REGION,
        )
        for file_path, key in files:
            s3.upload_file(file_path, bucket_name, key)
