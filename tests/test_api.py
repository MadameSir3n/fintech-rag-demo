import asyncio
import pytest
import httpx
from backend.main import app


async def _call(method: str, url: str, **kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        return await getattr(c, method)(url, **kwargs)


def call(method: str, url: str, **kwargs):
    return asyncio.run(_call(method, url, **kwargs))


def test_root():
    """Test root endpoint."""
    response = call("get", "/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_validate_invoice():
    """Test invoice validation endpoint."""
    invoice_data = {
        "invoice_text": """INVOICE
Invoice Number: INV-2023-001
Date: 01/15/2023
From: Tech Solutions Inc.
Total: $1,250.00"""
    }

    response = call("post", "/validate", json=invoice_data)
    assert response.status_code == 200

    data = response.json()
    assert "is_valid" in data
    assert "errors" in data
    assert "confidence" in data
    assert "normalized_fields" in data

def test_list_invoices_empty():
    """Test listing invoices when none exist."""
    response = call("get", "/invoices")
    assert response.status_code == 200

    data = response.json()
    assert "invoices" in data
    assert "count" in data
