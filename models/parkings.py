from pydantic import BaseModel
class Parkings(BaseModel):
    name: str
    bike: int
    car: int
    address: str
    latitude: float
    longitude: float