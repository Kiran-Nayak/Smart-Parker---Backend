from fastapi import APIRouter, Request, HTTPException, Depends
from config.database import db
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import *
from models.get_parking_spot import *
from schemas.parking_spot_schema import *

api_router = APIRouter()

# @api_router.post("/addParkingSpot", dependencies=[Depends(JWTBearer())])
# def add_parking_spot(parkingSpot: AddParkingSpot, request: Request):
#     auth = request.headers.get('Authorization').split(" ")
#     auth_key = ""
#     if len(auth) >= 2:
#         auth_key = auth[1]
#     elif len(auth) == 0:
#         auth_key = ""
#     else:
#         auth_key = auth[0]
#     if decodeLoginJWT(auth_key) == 1 or decodeLoginJWT(auth_key) == 0:
#         collection_name = db[parkingSpot._id]
#         id = collection_name.insert_one(dict(parkingSpot))
#         return inserted_parking_spot_schema("Parking spot inserted successfully", str(id.inserted_id))
#     else:
#         raise HTTPException(401, error_schema("Unauthorized token"))

@api_router.post("/parking_spot", dependencies= [Depends(JWTBearer())])
async def register_user(parkingSpot: ParkingSpot, request: Request):
    auth = request.headers.get('Authorization').split(" ")
    auth_key = ""
    if len(auth) >= 2:
        auth_key = auth[1]
    elif len(auth) == 0:
        auth_key = ""
    else:
        auth_key = auth[0]
    if decodeLoginJWT(auth_key) == 1 or decodeLoginJWT(auth_key) == 0:
        name = str(parkingSpot.vehicle_type + "_" + parkingSpot.parking_id)
        collection_name = db[name]
        print("%s_%s"%(parkingSpot.vehicle_type,parkingSpot.parking_id))
        start_index = (parkingSpot.page - 1) * 20
        dic = collection_name.find().skip(start_index).limit(20)
        return response_schema(dic)
    else:
        raise HTTPException(401, error_schema("Unauthorized token"))
    