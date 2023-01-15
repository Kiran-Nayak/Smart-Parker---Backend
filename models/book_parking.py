from pydantic import BaseModel
class BookParking(BaseModel):
    parking_spot_id: str
    parking_id: str
    user_id: str
    vehicle_type: str
    vehicle_number: str

class GetBookings(BaseModel):
    user_id: str

class Validate(BaseModel):
    user_id: str
    id: str