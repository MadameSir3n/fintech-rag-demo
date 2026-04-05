import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [invoiceText, setInvoiceText] = useState('');
  const [validationResult, setValidationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [invoices, setInvoices] = useState([]);

  const handleValidate = async () => {
    if (!invoiceText.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/validate', {
        invoice_text: invoiceText
      });
      setValidationResult(response.data);
    } catch (error) {
      console.error('Validation error:', error);
      alert('Error validating invoice');
    }
    setLoading(false);
  };

  const loadSampleInvoice = () => {
    setInvoiceText(`INVOICE

Invoice Number: INV-2023-001
Date: January 15, 2023

From: Tech Solutions Inc.

Items:
Web Development Services - 40 hours @ $75/hour = $3,000.00
Hosting Services - 12 months @ $50/month = $600.00

Subtotal: $3,600.00
Tax (8.5%): $306.00
Total: $3,906.00

Payment Terms: Net 30 Days`);
  };

  const fetchInvoices = async () => {
    try {
      const response = await axios.get('http://localhost:8000/invoices');
      setInvoices(response.data.invoices);
    } catch (error) {
      console.error('Error fetching invoices:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>FinTech RAG Demo</h1>
        <p>Structured Financial Data Extraction and Validation</p>
      </header>

      <main>
        <section className="upload-section">
          <h2>Validate Invoice</h2>
          <textarea
            value={invoiceText}
            onChange={(e) => setInvoiceText(e.target.value)}
            placeholder="Paste invoice text here..."
            rows="10"
            cols="50"
          />
          <br />
          <button onClick={loadSampleInvoice}>Load Sample Invoice</button>
          <button onClick={handleValidate} disabled={loading}>
            {loading ? 'Validating...' : 'Validate Invoice'}
          </button>
        </section>

        {validationResult && (
          <section className="results-section">
            <h2>Validation Results</h2>
            <div className="result-card">
              <p><strong>Status:</strong> {validationResult.is_valid ? 'Valid' : 'Invalid'}</p>
              <p><strong>Confidence:</strong> {validationResult.confidence.toFixed(2)}%</p>
              <p><strong>Processing Time:</strong> {validationResult.processing_time.toFixed(3)}s</p>
              
              {validationResult.errors.length > 0 && (
                <div className="errors">
                  <h3>Validation Errors:</h3>
                  <ul>
                    {validationResult.errors.map((error, index) => (
                      <li key={index} className={error.severity}>
                        <strong>{error.field}:</strong> {error.message} ({error.severity})
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              <div className="extracted-fields">
                <h3>Extracted Fields:</h3>
                <pre>{JSON.stringify(validationResult.normalized_fields, null, 2)}</pre>
              </div>
            </div>
          </section>
        )}

        <section className="history-section">
          <h2>Processed Invoices</h2>
          <button onClick={fetchInvoices}>Load Invoice History</button>
          
          {invoices.length > 0 && (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Invoice Number</th>
                  <th>Date</th>
                  <th>Supplier</th>
                  <th>Total</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                {invoices.map((invoice) => (
                  <tr key={invoice.id}>
                    <td>{invoice.id}</td>
                    <td>{invoice.invoice_number}</td>
                    <td>{invoice.invoice_date}</td>
                    <td>{invoice.supplier_name}</td>
                    <td>{invoice.total_amount} {invoice.currency}</td>
                    <td>{invoice.confidence.toFixed(2)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;