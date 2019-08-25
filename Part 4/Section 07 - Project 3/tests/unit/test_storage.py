"""
Tests for Storage class
Command line: python -m pytest tests/unit/test_storage.py
"""
import pytest

from app.models import inventory


@pytest.fixture
def storage_values():
    return {
        'name': 'Thumbdrive',
        'manufacturer': 'Sandisk',
        'total': 10,
        'allocated': 3,
        'capacity_gb': 512
    }


@pytest.fixture
def storage(storage_values):
    return inventory.Storage(**storage_values)


def test_create(storage, storage_values):
    for attr_name in storage_values:
        assert getattr(storage, attr_name) == storage_values.get(attr_name)


@pytest.mark.parametrize(
    'gb, exception', [(10.5, TypeError), (-1, ValueError), (0, ValueError)]
)
def test_create_invalid_storage(gb, exception, storage_values):
    storage_values['capacity_gb'] = gb
    with pytest.raises(exception):
        inventory.Storage(**storage_values)


def test_repr(storage):
    assert storage.category in repr(storage)
    assert str(storage.capacity_gb) in repr(storage)

