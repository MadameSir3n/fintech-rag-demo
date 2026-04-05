from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import time
from typing import List

from models import InvoiceRequest, InvoiceResponse, StoredInvoice, InvoiceListResponse
from database import get_db, init_db, InvoiceRecord
from extraction import extract_invoice_fields, validate_extracted_fields

app = FastAPI(
    title="FinTech RAG Demo API",
    description="Structured financial data extraction and validation API",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "FinTech RAG Demo API"}

@app.post("/validate", response_model=InvoiceResponse)
async def validate_invoice(request: InvoiceRequest, db: Session = Depends(get_db)):
    """
    Validate invoice data and extract fields using LLM.
    """
    start_time = time.time()
    
    # Extract fields using LLM
    extracted_fields, confidence = extract_invoice_fields(request.invoice_text)
    
    # Validate extracted fields
    errors = validate_extracted_fields(extracted_fields)
    
    # Determine if valid (no error-level errors)
    is_valid = not any(error["severity"] == "error" for error in errors)
    
    # Store in database
    db_invoice = InvoiceRecord(
        invoice_number=extracted_fields.get("invoice_number", ""),
        invoice_date=extracted_fields.get("invoice_date", ""),
        supplier_name=extracted_fields.get("supplier_name", ""),
        total_amount=extracted_fields.get("total_amount", 0.0),
        currency=extracted_fields.get("currency", "USD"),
        confidence=confidence,
        raw_text=request.invoice_text
    )
    
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    
    processing_time = time.time() - start_time
    
    return InvoiceResponse(
        is_valid=is_valid,
        errors=errors,
        confidence=confidence,
        normalized_fields=extracted_fields,
        processing_time=processing_time
    )

@app.get("/invoices", response_model=InvoiceListResponse)
async def list_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all processed invoices.
    """
    invoices = db.query(InvoiceRecord).offset(skip).limit(limit).all()
    
    stored_invoices = [
        StoredInvoice(
            id=inv.id,
            invoice_number=inv.invoice_number,
            invoice_date=inv.invoice_date,
            supplier_name=inv.supplier_name,
            total_amount=inv.total_amount,
            currency=inv.currency,
            created_at=inv.created_at,
            confidence=inv.confidence
        )
        for inv in invoices
    ]
    
    return InvoiceListResponse(
        invoices=stored_invoices,
        count=len(stored_invoices)
    )

@app.get("/invoices/{invoice_id}", response_model=StoredInvoice)
async def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Get specific invoice details.
    """
    invoice = db.query(InvoiceRecord).filter(InvoiceRecord.id == invoice_id).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return StoredInvoice(
        id=invoice.id,
        invoice_number=invoice.invoice_number,
        invoice_date=invoice.invoice_date,
        supplier_name=invoice.supplier_name,
        total_amount=invoice.total_amount,
        currency=invoice.currency,
        created_at=invoice.created_at,
        confidence=invoice.confidence
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)