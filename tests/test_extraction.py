import pytest
from backend.extraction import extract_invoice_fields, validate_extracted_fields

def test_extract_invoice_fields():
    """Test invoice field extraction."""
    invoice_text = """INVOICE
Invoice Number: INV-2023-001
Date: 01/15/2023
From: Tech Solutions Inc.
Total: $1,250.00"""
    
    fields, confidence = extract_invoice_fields(invoice_text)
    
    assert 'invoice_number' in fields
    assert 'invoice_date' in fields
    assert 'supplier_name' in fields
    assert 'total_amount' in fields
    assert isinstance(confidence, float)
    assert 0 <= confidence <= 100

def test_validate_extracted_fields_valid():
    """Test validation of valid extracted fields."""
    fields = {
        'invoice_number': 'INV-2023-001',
        'invoice_date': '2023-01-15',
        'supplier_name': 'Tech Solutions Inc.',
        'total_amount': 1250.00,
        'currency': 'USD'
    }
    
    errors = validate_extracted_fields(fields)
    
    # Should have no error-level errors for valid data
    error_count = sum(1 for error in errors if error['severity'] == 'error')
    assert error_count == 0

def test_validate_extracted_fields_invalid():
    """Test validation of invalid extracted fields."""
    fields = {
        'invoice_number': 'INVALID#NUMBER',
        'invoice_date': 'invalid-date',
        'supplier_name': 'Test Company',
        'total_amount': -100.00,  # Negative amount is invalid
        'currency': 'USD'
    }
    
    errors = validate_extracted_fields(fields)
    
    # Should have at least one error
    error_count = sum(1 for error in errors if error['severity'] == 'error')
    assert error_count > 0