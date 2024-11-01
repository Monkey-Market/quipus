import pytest
import polars as pl

from quipus import CertificateFactory, Certificate


@pytest.fixture
def sample_row():
    return {
        "completion_date": "2024-10-27",
        "content": "Test content 1",
        "entity": "Test entity 1",
        "name": "Test name 1",
        "duration": "Test duration 1",
        "validity_checker": "https://example.com/check",
    }


@pytest.fixture
def sample_dataframe():
    data = {
        "completion_date": ["2024-10-27", "2024-10-25"],
        "content": ["Test content 1", "Test content 2"],
        "entity": ["Test entity 1", "Test entity 2"],
        "name": ["Test name 1", "Test name 2"],
        "duration": ["Test duration 1", "Test duration 2"],
        "validity_checker": [
            "https://example.com/check1",
            "https://example.com/check2",
        ],
    }
    return pl.DataFrame(data)


def test_create_one_certificate(sample_row):
    certificate = CertificateFactory.create_one_certificate(sample_row)
    assert isinstance(certificate, Certificate)
    assert certificate.completion_date == "2024-10-27"
    assert certificate.content == "Test content 1"
    assert certificate.entity == "Test entity 1"
    assert certificate.name == "Test name 1"
    assert certificate.duration == "Test duration 1"
    assert certificate.validity_checker == "https://example.com/check"


def test_create_certificates(sample_dataframe):
    certificates = CertificateFactory.create_certificates(sample_dataframe)

    assert isinstance(certificates, list)
    assert len(certificates) == len(sample_dataframe)
    assert all(isinstance(cert, Certificate) for cert in certificates)

    assert certificates[0].completion_date == "2024-10-27"
    assert certificates[0].content == "Test content 1"
    assert certificates[0].entity == "Test entity 1"
    assert certificates[0].name == "Test name 1"
    assert certificates[0].duration == "Test duration 1"
    assert certificates[0].validity_checker == "https://example.com/check1"

    assert certificates[1].completion_date == "2024-10-25"
    assert certificates[1].content == "Test content 2"
    assert certificates[1].entity == "Test entity 2"
    assert certificates[1].name == "Test name 2"
    assert certificates[1].duration == "Test duration 2"
    assert certificates[1].validity_checker == "https://example.com/check2"
