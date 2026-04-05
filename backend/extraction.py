import re
from typing import Dict, List, Tuple
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Initialize LLM (in production, you'd use a proper API key)
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY", "sk-fake-key-for-demo"),
    temperature=0,
    model_name="gpt-3.5-turbo"
)

def extract_invoice_fields(invoice_text: str) -> Tuple[Dict, float]:
    """
    Extract fields from invoice text using LLM.
    Returns extracted fields and confidence score.
    """
    # In a real implementation, this would use LangChain with OpenAI
    # For demo purposes, we'll simulate extraction with pattern matching
    
    # Simulated extraction with confidence scoring
    fields = {}
    confidence_scores = []
    
    # Extract invoice number
    invoice_number_match = re.search(r'[Ii]nvoice\s*[Nn]umber[:\s]*([A-Z0-9\-]+)', invoice_text)
    if invoice_number_match:
        fields['invoice_number'] = invoice_number_match.group(1)
        confidence_scores.append(95)
    else:
        fields['invoice_number'] = "INV-" + str(hash(invoice_text))[-6:]
        confidence_scores.append(30)
    
    # Extract date
    date_match = re.search(r'[Dd]ate[:\s]*([0-9]{1,2}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})', invoice_text)
    if date_match:
        fields['invoice_date'] = date_match.group(1)
        confidence_scores.append(90)
    else:
        fields['invoice_date'] = "2023-01-01"
        confidence_scores.append(25)
    
    # Extract supplier
    supplier_match = re.search(r'[Ff]rom[:\s]*([A-Za-z\s]+(?:Inc\.?|LLC|Ltd\.?|Corporation))', invoice_text)
    if supplier_match:
        fields['supplier_name'] = supplier_match.group(1).strip()
        confidence_scores.append(85)
    else:
        fields['supplier_name'] = "Demo Supplier Inc."
        confidence_scores.append(20)
    
    # Extract total amount
    total_match = re.search(r'[Tt]otal[:\s\$]*([0-9,]+\.?[0-9]*)', invoice_text)
    if total_match:
        try:
            fields['total_amount'] = float(total_match.group(1).replace(',', ''))
            confidence_scores.append(92)
        except:
            fields['total_amount'] = 1000.00
            confidence_scores.append(30)
    else:
        fields['total_amount'] = 1000.00
        confidence_scores.append(25)
    
    fields['currency'] = "USD"
    confidence_scores.append(100)  # Currency is assumed
    
    # Calculate average confidence
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 50.0
    
    return fields, avg_confidence

def validate_extracted_fields(fields: Dict) -> List[Dict]:
    """
    Validate extracted fields and return errors.
    """
    errors = []
    
    # Validate invoice number format
    if 'invoice_number' in fields:
        if not re.match(r'^[A-Z0-9\-]+$', fields['invoice_number']):
            errors.append({
                "field": "invoice_number",
                "message": "Invoice number format is invalid",
                "severity": "error"
            })
    
    # Validate date format
    if 'invoice_date' in fields:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$|^\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}$', fields['invoice_date']):
            errors.append({
                "field": "invoice_date",
                "message": "Date format should be YYYY-MM-DD or MM/DD/YYYY",
                "severity": "warning"
            })
    
    # Validate total amount
    if 'total_amount' in fields:
        if fields['total_amount'] <= 0:
            errors.append({
                "field": "total_amount",
                "message": "Total amount must be greater than zero",
                "severity": "error"
            })
    
    return errors