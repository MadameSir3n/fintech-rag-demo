# FinTech RAG Demo

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18%2B-blue.svg)](https://reactjs.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5%2B-purple.svg)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue.svg)](https://postgresql.org)

A Dockerized fintech RAG validation pipeline with FastAPI, LangChain, OpenAI, and PostgreSQL for structured financial data extraction and validation.

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│   React     │───▶│   FastAPI    │───▶│  LangChain   │───▶│ PostgreSQL  │
│  Frontend   │    │     API      │    │  + OpenAI    │    │     DB      │
└─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘
```

## Features

- Structured invoice data extraction using LLMs
- Confidence scoring for extracted fields
- Data validation API with error reporting
- PostgreSQL persistence for normalized records
- React frontend for demo visualization

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/fintech-rag-demo.git
cd fintech-rag-demo

# Start the application
docker-compose up

# The app will be available at:
# - Frontend: http://localhost:3000
# - API Docs: http://localhost:8000/docs
```

## API Endpoints

- `POST /validate` - Validate invoice data and extract fields
- `GET /invoices` - List all processed invoices
- `GET /invoices/{id}` - Get specific invoice details

## Project Structure

```
fintech-rag-demo/
├── docker-compose.yml          # Docker orchestration
├── backend/                    # FastAPI application
│   ├── main.py                 # API entry point
│   ├── models.py               # Data models
│   ├── extraction.py           # LLM extraction logic
│   ├── database.py             # Database connection
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React application
│   ├── src/
│   │   ├── App.js              # Main component
│   │   └── components/         # UI components
│   └── package.json            # Node dependencies
├── data/                       # Sample data
│   └── mock_invoices.csv       # Sample invoices
└── tests/                      # Test suite
    ├── test_extraction.py      # Extraction tests
    └── test_api.py             # API tests
```

## Future Work

- [ ] Add extraction accuracy metrics
- [ ] Implement cost tracking per invoice
- [ ] Add latency monitoring
- [ ] Support additional document formats (PDF, images)
- [ ] Batch processing capabilities

## Metrics

- Average extraction time: < 2 seconds
- Confidence threshold: > 80%
- Cost per invoice: ~$0.005