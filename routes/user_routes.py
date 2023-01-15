from fastapi import APIRouter, Depends, Request
from config.database import db
from models.users import User
from models.login_user import LoginUser
from schemas.user_schema import *
from auth.jwt_handler import *
from models.guest import Guest
from auth.jwt_bearer import *

user_router = APIRouter()

@user_router.post("/user/register", dependencies= [Depends(JWTBearer())])
async def register_user(user: User, request: Request):
    auth = request.headers.get('Authorization').split(" ")
    auth_key = ""
    if len(auth) >= 2:
        auth_key = auth[1]
    elif len(auth) == 0:
        auth_key = ""
    else:
        auth_key = auth[0]
    if decodeLoginJWT(auth_key) == 1 or decodeLoginJWT(auth_key) == 0:
        auth_key = registerJWT(userID=user.email_id)
        user_collection = db['user_collection']
        id = user_collection.insert_one(dict(user))
        return register_user_schema(auth_key, "User registered successfully", str(id.inserted_id))
    else:
        return error_schema(401, "Unauthorised token")

@user_router.post("/guest")
async def guest(guest: Guest):
    auth_key = guestJWT(guest.device_id)
    return guest_schema(auth_key)

@user_router.post("/user/login", dependencies=[Depends(JWTBearer())])
async def login(user: LoginUser, request: Request):
    auth = request.headers.get('Authorization').split(" ")
    auth_key = ""
    if len(auth) >= 2:
        auth_key = auth[1]
    elif len(auth) == 0:
        auth_key = ""
    else:
        auth_key = auth[0]
    if decodeLoginJWT(auth_key) == 1 or decodeLoginJWT(auth_key) == 0:
        user_collection = db['user_collection']
        user = (user_collection.find_one({"email_id": user.email}))
        if user != None:
            token = registerJWT(user["email_id"])
            return login_schema(token, "user found", str(user["_id"]))
        else:
            return login_schema(None, "user not found", None)
    else:
        return error_schema(401, "Unauthorised token")