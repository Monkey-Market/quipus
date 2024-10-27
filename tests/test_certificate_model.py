import dataclasses

import pytest

from quipus import Certificate


def test_certificate_initialization():
    certificate = Certificate(
        completion_date="2024-10-27",
        content="Test content 1",
        entity="Test entity 1",
        name="Test name 1",
        duration="Test duration 1",
        validity_checker="https://example.com/check",
    )

    assert certificate.completion_date == "2024-10-27"
    assert certificate.content == "Test content 1"
    assert certificate.entity == "Test entity 1"
    assert certificate.name == "Test name 1"
    assert certificate.duration == "Test duration 1"
    assert certificate.validity_checker == "https://example.com/check"


def test_certificate_initialization_without_optional_fields():
    certificate = Certificate(
        completion_date="2024-10-25",
        content="Test content 2",
        entity="Test entity ",
        name="Test name 2",
    )

    assert certificate.completion_date == "2024-10-25"
    assert certificate.content == "Test content 2"
    assert certificate.entity == "Test entity "
    assert certificate.name == "Test name 2"
    assert certificate.duration is None
    assert certificate.validity_checker is None


def test_certificate_immutable_fields():
    certificate = Certificate(
        completion_date="2024-10-27",
        content="Test content 1",
        entity="Test entity 1",
        name="Test name 1",
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        certificate.name = "New name 1"
