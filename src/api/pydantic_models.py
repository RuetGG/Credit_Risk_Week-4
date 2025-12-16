from pydantic import BaseModel
from typing import Optional

class CustomerFeatures(BaseModel):
    total_transaction_amount: float
    avg_transaction_amount: float
    transaction_count: float
    std_transaction_amount: float
    product_airtime: float
    product_data_bundles: float
    product_financial_services: float
    product_movies: float
    product_other: float
    product_ticket: float
    product_transport: float
    product_tv: float
    product_utility_bill: float
    provider: float
    channel: float

class RiskResponse(BaseModel):
    is_high_risk_prob: float
