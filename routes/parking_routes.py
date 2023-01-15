from fastapi import APIRouter, Depends, Request, HTTPException
from config.database import db
from models.parkings import Parkings
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import *
from schemas.parking_schema import *
from models.nearest_parking import NearestParking
import math

api_routes = APIRouter()

@api_routes.post("/addParking", dependencies=[Depends(JWTBearer())])
def addParking(parkings: Parkings, request: Request):
    auth = request.headers.get('Authorization').split(" ")
    auth_key = ""
    if len(auth) >= 2:
        auth_key = auth[1]
    elif len(auth) == 0:
        auth_key = ""
    else:
        auth_key = auth[0]
    if decodeLoginJWT(auth_key) == 1 or decodeLoginJWT(auth_key) == 0:
        collection_name = db["parkings"]
        id = collection_name.insert_one(dict(parkings))
        return inserted_parking_schema("Parking inserted successfully", str(id.inserted_id))
    else:
        raise HTTPException(401, error_schema("Unauthorized token"))

@api_routes.post("/getParkings", dependencies=[Depends(JWTBearer())])
def getParkings(parking: NearestParking,request: Request):
    auth = request.headers.get('Authorization').split(" ")
    auth_key = ""
    if len(auth) >= 2:
        auth_key = auth[1]
    elif len(auth) == 0:
        auth_key = ""
    else:
        auth_key = auth[0]
    if decodeLoginJWT(auth_key) == 1 or decodeLoginJWT(auth_key) == 0:
        collection_name = db["parkings"]
        min_lat = parking.lat - (0.009 * 2)
        max_lat = parking.lat + (0.009 * 2)
        min_lng = parking.lng - ((0.009 * 2) / math.cos(parking.lng * (math.pi / 180)))
        max_lng = parking.lng + ((0.009 * 2) / math.cos(parking.lng * (math.pi / 180)))
        startIndex = (parking.page - 1) * 10
        todo = response_schema(collection_name.find({
            "$and": [
                { "latitude": { "$lt": max_lat } },
                { "latitude": { "$gt": min_lat } },
                { "longitude": { "$lt": max_lng } },
                { "longitude": { "$gt": min_lng } }
            ]
        }).skip(startIndex).limit(10))
        return todo
    else:
        raise HTTPException(401, error_schema("Unauthorized token"))