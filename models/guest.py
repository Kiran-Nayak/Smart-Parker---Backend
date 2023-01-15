from pydantic import BaseModel

class Guest(BaseModel):
    device_id: str