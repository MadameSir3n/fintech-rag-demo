# FinTech RAG Demo

A RAG pipeline that extracts structured financial data from invoice text using an LLM, scores confidence per field, and stores validated records via a REST API.

---

## Problem

Finance teams process thousands of invoices manually — copying vendor names, amounts, and line items into systems of record. Unstructured documents can't be ingested directly, and manual data entry is slow and error-prone at scale.

## Solution

This pipeline accepts raw invoice text, sends it through an LLM extraction prompt via LangChain, scores the confidence of each extracted field, validates the result, and persists structured records to a database through a REST API.

## Key Features

- LLM-powered field extraction (vendor, amount, line items, due dates)
- Per-field confidence scoring on every extraction
- Validation API that rejects low-confidence records before persistence
- PostgreSQL-backed storage for audited, normalized records
- React frontend for demo visualization
- Fully Dockerized for single-command deployment

## Tech Stack

- **Python** — backend logic
- **FastAPI** — REST API layer
- **LangChain + OpenAI** — LLM extraction pipeline
- **PostgreSQL** — structured record storage
- **React** — demo frontend
- **Docker / Docker Compose** — deployment

## Example Flow

```
1. POST /validate  →  { "text": "Invoice from Acme Corp, $2,400.00, due 2024-03-15" }
2. LangChain sends text to OpenAI with structured extraction prompt
3. LLM returns:  { "vendor": "Acme Corp", "amount": 2400.00, "due_date": "2024-03-15" }
4. Confidence scored per field:  vendor=0.97, amount=0.99, due_date=0.91
5. Passes threshold → record written to PostgreSQL
6. Response:  { "invoice_id": "inv_0042", "status": "validated", "confidence": 0.96 }
```

## How to Run

```bash
git clone https://github.com/MadameSir3n/fintech-rag-demo.git
cd fintech-rag-demo
pip install -r backend/requirements.txt
python -m pytest tests/ -v
```

Or with Docker:

```bash
docker-compose up
# API Docs: http://localhost:8000/docs
# Frontend:  http://localhost:3000
```

## Sample Test Output

```
tests/test_api.py::test_validate_invoice PASSED
tests/test_api.py::test_list_invoices PASSED
tests/test_api.py::test_get_invoice PASSED
tests/test_api.py::test_invalid_invoice_rejected PASSED
tests/test_api.py::test_health_check PASSED
tests/test_api.py::test_confidence_scoring PASSED

6 passed in 1.24s
```

## Why This Matters

Unstructured document processing is one of the most common real-world AI use cases in enterprise. This project demonstrates how to build a reliable extraction pipeline with the validation and confidence scoring that production systems actually need — not just a demo that calls an LLM and prints the result.