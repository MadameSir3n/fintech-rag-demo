from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InvoiceItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total_price: float

class InvoiceRequest(BaseModel):
    invoice_text: str

class ValidationError(BaseModel):
    field: str
    message: str
    severity: str  # "error", "warning"

class InvoiceResponse(BaseModel):
    is_valid: bool
    errors: List[ValidationError]
    confidence: float  # 0-100
    normalized_fields: dict
    processing_time: float

class StoredInvoice(BaseModel):
    id: int
    invoice_number: str
    invoice_date: str
    supplier_name: str
    total_amount: float
    currency: str
    created_at: datetime
    confidence: float

class InvoiceListResponse(BaseModel):
    invoices: List[StoredInvoice]
    count: int