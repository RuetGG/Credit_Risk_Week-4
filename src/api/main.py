from fastapi import FastAPI
import mlflow.sklearn
import pandas as pd
from src.api.pydantic_models import CustomerFeatures, RiskResponse

app = FastAPI()

model_uri = "models:/RandomForest_Model/2"  
model = mlflow.sklearn.load_model(model_uri)

@app.post("/predict", response_model=RiskResponse)
def predict_risk(features: CustomerFeatures):
    data = pd.DataFrame([features.dict()])
    prob = model.predict_proba(data)[:, 1][0]
    return {"is_high_risk_prob": prob}
