from pydantic import BaseModel

class User(BaseModel):
    email_id: str
    name: str
    mobile_no: str
    gender: str
    dob: str