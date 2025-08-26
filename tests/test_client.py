import os

import pytest
from bazpy import BazaarClient
from bazpy.models import BazaarSnapshot, BazaarProduct


def test_client_init():
    client = BazaarClient()
    assert isinstance(client, BazaarClient)


@pytest.mark.skipif(
    not os.getenv("RUN_INTEGRATION"),
    reason="Set RUN_INTEGRATION=1 to run integration tests",
)
def test_get_bazaar_integration():
    client = BazaarClient()
    snap = client.get_bazaar()
    assert isinstance(snap, BazaarSnapshot)
    assert isinstance(snap.products, dict)
    assert all(isinstance(p, BazaarProduct) for p in snap.products.values())
