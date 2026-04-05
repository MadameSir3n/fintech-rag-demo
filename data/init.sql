-- Initialize database tables
CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(50) NOT NULL,
    invoice_date VARCHAR(20) NOT NULL,
    supplier_name VARCHAR(255) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    confidence DECIMAL(5, 2) NOT NULL,
    raw_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_invoice_number ON invoices(invoice_number);
CREATE INDEX IF NOT EXISTS idx_supplier_name ON invoices(supplier_name);
CREATE INDEX IF NOT EXISTS idx_created_at ON invoices(created_at);