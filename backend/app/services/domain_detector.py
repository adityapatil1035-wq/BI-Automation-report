import pandas as pd
from typing import Dict, Any, Tuple

DOMAIN_KEYWORDS = {
    "Sales": ["sales", "revenue", "order", "orders", "product", "profit", "discount", "quantity", "deal", "invoice"],
    "E-commerce": ["cart", "conversion", "session", "checkout", "sku", "shipping", "order_id", "traffic", "visitor"],
    "Retail": ["store", "item", "category", "unit", "retail", "price", "pos", "transaction", "merchandise"],
    "Finance": ["balance", "asset", "liability", "expense", "transaction_type", "budget", "tax", "equity", "cash_flow", "account"],
    "Marketing": ["campaign", "lead", "click", "ctr", "cpc", "conversion", "impression", "channel", "ad_spend", "roi"],
    "HR": ["employee", "department", "salary", "attrition", "hire_date", "performance", "tenure", "termination", "job_title"],
    "Healthcare": ["patient", "diagnosis", "doctor", "hospital", "admission", "bed", "treatment", "medicine", "dosage", "claim"],
    "Inventory": ["stock", "warehouse", "reorder", "inventory", "supplier", "lead_time", "stockout", "safety_stock"],
    "Customer Analytics": ["churn", "nps", "lifetime_value", "ltv", "retention", "satisfaction", "segment", "feedback"]
}

def detect_business_domain(df: pd.DataFrame) -> Tuple[str, float, Dict[str, float]]:
    cols_lower = [str(col).lower().replace("_", " ").replace("-", " ") for col in df.columns]
    full_text = " ".join(cols_lower)
    
    domain_scores = {}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0.0
        for kw in keywords:
            if kw in full_text:
                score += 1.5
            for col in cols_lower:
                if kw == col or kw in col.split():
                    score += 2.0
        domain_scores[domain] = score

    best_domain = max(domain_scores, key=domain_scores.get)
    max_score = domain_scores[best_domain]
    
    # Calculate confidence percentage (0 - 100%)
    confidence = min(100.0, round((max_score / 6.0) * 100.0, 1)) if max_score > 0 else 0.0
    
    if max_score == 0:
        best_domain = "Sales"  # Default fallback
        confidence = 50.0

    return best_domain, confidence, domain_scores
