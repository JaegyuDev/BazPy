from __future__ import annotations

from typing import Any, Dict, Iterable
import httpx

from .exceptions import BazaarError
from .models import BazaarProduct, BazaarSnapshot


class BazaarClient:
    BASE_URL = "https://api.hypixel.net/v2/skyblock/bazaar"

    def __init__(self, api_key: str | None = None, *, timeout: int = 10):
        self.api_key = api_key
        self._client = httpx.Client(timeout=timeout)

    def _headers(self) -> dict[str, str]:
        return {"API-Key": self.api_key} if self.api_key else {}

    def get_bazaar_raw(self) -> Dict[str, Any]:
        resp = self._client.get(self.BASE_URL, headers=self._headers())
        if resp.status_code != 200:
            raise BazaarError(
                f"Failed with status {resp.status_code}: {resp.text}"
            )
        return resp.json()

    def get_bazaar(self) -> BazaarSnapshot:
        data = self.get_bazaar_raw()
        try:
            return BazaarSnapshot.model_validate(data)
        except Exception as e:
            raise BazaarError(
                f"Failed to parse snapshot: {e}"
            ) from e

    def get_product(self, product_id: str) -> BazaarProduct:
        snapshot = self.get_bazaar()
        try:
            return snapshot.products[product_id]
        except KeyError as e:
            raise BazaarError(
                f"Product not found: {product_id}"
            ) from e

    def iter_products(self) -> Iterable[BazaarProduct]:
        return self.get_bazaar().products.values()