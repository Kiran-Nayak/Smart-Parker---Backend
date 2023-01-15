from fastapi import HTTPException

# Register user schema
def register_user_schema(token: str, message: str, id: str) -> dict:
    return {
        "status": True,
        "message": message,
        "data": {
            "token": token,
            "user_id": id
        }
     }

# Login Schema
def login_schema(token: str, message: str, id: str):
    return {
        "status": True,
        "message": message,
        "data": {
            "token": token,
            "user_id": id
        }
    }

def guest_schema(token):
    return {
        "status": True,
        "message": "guest registered successfully",
        "data": {
            "token": token
        }
    }

def error_schema(status: int, msg: str):
    return {
        "status": False,
        "message": msg
    }