"""
Placeholder tests for the TwoTierIndex.
Real tests get filled in during Phase 4 alongside the actual implementation.
"""

import pytest
from shared.index import TwoTierIndex


def test_two_tier_index_instantiates():
    index = TwoTierIndex()
    assert index.national == {}
    assert index.local == {}


def test_add_national_not_implemented_yet():
    index = TwoTierIndex()
    with pytest.raises(NotImplementedError):
        index.add_national("permitted-development", {"text": "example"})


def test_query_not_implemented_yet():
    index = TwoTierIndex()
    with pytest.raises(NotImplementedError):
        index.query("bristol", "article-4", "fence height")