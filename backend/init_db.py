#!/usr/bin/env python3
"""
Initialize database and load sample data
"""

import csv
import os
from database import init_db, SessionLocal, InvoiceRecord

def load_sample_data():
    """Load sample invoice data from CSV file."""
    # Initialize database
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Load sample data from CSV
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mock_invoices.csv')
        
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                invoice = InvoiceRecord(
                    invoice_number=row['invoice_number'],
                    invoice_date=row['invoice_date'],
                    supplier_name=row['supplier_name'],
                    total_amount=float(row['total_amount']),
                    currency=row['currency'],
                    confidence=95.0,  # High confidence for sample data
                    raw_text=f"Sample invoice {row['invoice_number']} for {row['supplier_name']}"
                )
                db.add(invoice)
            
            db.commit()
            print(f"Loaded {reader.line_num - 1} sample invoices")
    
    except FileNotFoundError:
        print("Sample data file not found, creating empty database")
    except Exception as e:
        print(f"Error loading sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_sample_data()