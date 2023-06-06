from pydantic import BaseModel
class CheckSpot(BaseModel):
    parking_id: str
    vehicle_type: str
    spot_id: str