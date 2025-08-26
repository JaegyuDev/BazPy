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

@pytest.mark.skipif(
    not os.getenv("RUN_NON_TESTS"),
    reason="Set RUN_NON_TESTS=1 to run non-tests, ie 'how many products are available'",
)
def test_get_product_count():
    client = BazaarClient()
    snap = client.get_bazaar_raw()
    print(f"\nnumber of keys: {len(snap['products'].keys())}")
    keys = snap["products"].keys()
    n = len(keys)
    avg_bytes = (sum(len(k.encode("utf-8")) for k in keys) / n) if n else 0
    print(f"average key size (bytes): {avg_bytes:.2f}")

