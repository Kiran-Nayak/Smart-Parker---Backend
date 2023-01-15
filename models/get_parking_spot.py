from pydantic import BaseModel

class ParkingSpot(BaseModel):
    parking_id: str
    vehicle_type: str
    page: int