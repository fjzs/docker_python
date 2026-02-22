"""
Test suite for GenerateInstanceRequest model.

Tests the GenerateInstanceRequest class which validates API requests for generating
facility location problem instances.
"""

import pytest
from pydantic import ValidationError

from app.models.generate_instance_request import GenerateInstanceRequest


def test_generate_instance_request__valid_values__creates_request():
    """
    Test that valid request data is accepted.

    Arrange: Valid n_customers and n_facilities
    Act: Create GenerateInstanceRequest
    Assert: Request is created with correct values
    """
    # Arrange & Act
    request = GenerateInstanceRequest(n_customers=10, n_facilities=3)

    # Assert
    assert request.n_customers == 10
    assert request.n_facilities == 3


def test_generate_instance_request__negative_customers__rejected():
    """
    Test that negative customer count is rejected.

    Arrange: n_customers = -1
    Act: Try to create GenerateInstanceRequest
    Assert: ValidationError is raised
    """
    # Arrange & Act & Assert
    with pytest.raises(ValidationError): 
        GenerateInstanceRequest(n_customers=-1, n_facilities=3)


def test_generate_instance_request__zero_customers__rejected():
    """
    Test that zero customer count is rejected.

    Arrange: n_customers = 0
    Act: Try to create GenerateInstanceRequest
    Assert: ValidationError is raised
    """
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        GenerateInstanceRequest(n_customers=0, n_facilities=3)


def test_generate_instance_request__zero_facilities__rejected():
    """
    Test that zero facility count is rejected.

    Arrange: n_facilities = 0
    Act: Try to create GenerateInstanceRequest
    Assert: ValidationError is raised
    """
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        GenerateInstanceRequest(n_customers=10, n_facilities=0)


def test_generate_instance_request__negative_facilities__rejected():
    """
    Test that negative facility count is rejected.

    Arrange: n_facilities = -1
    Act: Try to create GenerateInstanceRequest
    Assert: ValidationError is raised
    """
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        GenerateInstanceRequest(n_customers=10, n_facilities=-1)


def test_generate_instance_request__max_customers__accepted():
    """
    Test that maximum customer count (100) is accepted.

    Arrange: n_customers = 100
    Act: Create GenerateInstanceRequest
    Assert: Request is created successfully
    """
    # Arrange & Act
    request = GenerateInstanceRequest(n_customers=100, n_facilities=10)

    # Assert
    assert request.n_customers == 100
    assert request.n_facilities == 10


def test_generate_instance_request__max_facilities__accepted():
    """
    Test that maximum facility count (100) is accepted.

    Arrange: n_facilities = 100
    Act: Create GenerateInstanceRequest
    Assert: Request is created successfully
    """
    # Arrange & Act
    request = GenerateInstanceRequest(n_customers=10, n_facilities=100)

    # Assert
    assert request.n_customers == 10
    assert request.n_facilities == 100


def test_generate_instance_request__customers_exceeds_max__rejected():
    """
    Test that customer count exceeding 100 is rejected.

    Arrange: n_customers = 101
    Act: Try to create GenerateInstanceRequest
    Assert: ValidationError is raised
    """
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        GenerateInstanceRequest(n_customers=101, n_facilities=10)


def test_generate_instance_request__facilities_exceeds_max__rejected():
    """
    Test that facility count exceeding 100 is rejected.

    Arrange: n_facilities = 101
    Act: Try to create GenerateInstanceRequest
    Assert: ValidationError is raised
    """
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        GenerateInstanceRequest(n_customers=10, n_facilities=101)



