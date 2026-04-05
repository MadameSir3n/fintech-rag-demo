import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
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
    
    response = client.post("/validate", json=invoice_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "is_valid" in data
    assert "errors" in data
    assert "confidence" in data
    assert "normalized_fields" in data

def test_list_invoices_empty():
    """Test listing invoices when none exist."""
    response = client.get("/invoices")
    assert response.status_code == 200
    
    data = response.json()
    assert "invoices" in data
    assert "count" in data