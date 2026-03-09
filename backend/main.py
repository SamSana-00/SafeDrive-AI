from fastapi import FastAPI
from models import RiskData
from database import risk_collection
from datetime import datetime

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SafeDrive AI Backend Running"}

@app.post("/log-risk")
def log_risk(data: RiskData):

    risk_dict = data.dict()
    risk_dict["timestamp"] = datetime.utcnow()

    risk_collection.insert_one(risk_dict)

    if data.risk_score >= 80:
        status = "CRITICAL"
    elif data.risk_score >= 60:
        status = "HIGH"
    elif data.risk_score >= 30:
        status = "WARNING"
    else:
        status = "SAFE"

    return {
        "status": status,
        "message": "Risk logged successfully"
    }

@app.get("/get-history")
def get_history():
    logs = list(risk_collection.find({}, {"_id": 0}))
    return {"data": logs}
