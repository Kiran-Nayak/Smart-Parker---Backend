from pydantic import BaseModel
class Booking(BaseModel):
    is_active: bool
    user_id: str
    parking_id: str
    spot_id: str
    parking_name: str
    user_name: str
    vehicle_number: str
    type: str