"""
Tests for SSD class
Command line: python -m pytest tests/unit/test_ssd.py
"""
import pytest

from app.models import inventory


@pytest.fixture
def ssd_values():
    return {
        'name': 'Samsung 860 EVO',
        'manufacturer': 'Samsung',
        'total': 10,
        'allocated': 3,
        'capacity_gb': 1_000,
        'interface': 'SATA III'
    }


@pytest.fixture
def ssd(ssd_values):
    return inventory.SSD(**ssd_values)


def test_create(ssd, ssd_values):
    for attr_name in ssd_values:
        assert getattr(ssd, attr_name) == ssd_values.get(attr_name)


def test_repr(ssd):
    assert ssd.category in repr(ssd)
    assert str(ssd.capacity_gb) in repr(ssd)
    assert ssd.interface in repr(ssd)
