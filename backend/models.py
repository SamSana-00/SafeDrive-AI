from pydantic import BaseModel
from datetime import datetime

class RiskData(BaseModel):
    driver_id: str
    risk_score: float
    eye_duration: float
    yawn_count: int
    head_tilt: float
    timestamp: datetime
