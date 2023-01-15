from pydantic import BaseModel
class NearestParking(BaseModel):
    lat: float
    lng: float
    page: int