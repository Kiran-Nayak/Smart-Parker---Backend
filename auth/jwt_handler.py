import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Return Auth JWT
def registerJWT(userID: str):
    try:
        payload = {
            "userID" : userID,
            "userType": "customer",
            "org": "Smart Parker"
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    except:
        return None
# Decode Token: 
# True: if user loggedIn
# False: guest user
def decodeLoginJWT(token: str) -> int:
    try:
        decode = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        if decode["org"] == "Smart Parker":
            if decode["userType"] == "guest":
                return 0
            return 1
        else:
            return -1
    except:
        return -1
        
def guestJWT(device: str):
    try:
        payload = {
            "userType": "guest",
            "org": "Smart Parker"
        }
        token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return token
    except:
        return None