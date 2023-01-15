from fastapi import APIRouter, Depends, Request, HTTPException
from auth.jwt_bearer import JWTBearer
from models.book_parking import *
from config.database import db
from auth.jwt_handler import *
from schemas.booking_schema import *
from bson import ObjectId
import time

book_routes = APIRouter()

@book_routes.post("/bookings", dependencies= [Depends(JWTBearer())])
def bookings(book: BookParking, request: Request):
    auth = request.headers.get('Authorization').split(" ")
    auth_key = ""
    if len(auth) >= 2:
        auth_key = auth[1]
    elif len(auth) == 0:
        auth_key = ""
    else:
        auth_key = auth[0]
    if decodeLoginJWT(auth_key) == 1:
        user = db["user_collection"].find_one({"_id": ObjectId(book.user_id)})
        if user == None:
            return HTTPException(404, error_schema("User not found"))
        else:
            parking = db['parkings'].find_one({"_id": ObjectId(book.parking_id)})
            parkingDetails = db[f"{book.vehicle_type}_{book.parking_id}"].find_one({"_id": ObjectId(book.parking_spot_id)})
            count = parking[book.vehicle_type]
            if count == 0:
                return {
                "status": False,
                "message": "unable to book"
            }
            count -= 1
            db['parkings'].find_one_and_update({"_id": ObjectId(book.parking_id)}, {
                '$set': {
                    book.vehicle_type: count
                }
            })
            db[f"{book.vehicle_type}_{book.parking_id}"].find_one_and_update({"_id": ObjectId(book.parking_spot_id)}, {
                '$set': {
                    "is_occupied": True,
                    "vehicle_number": book.vehicle_number
                }
            })
            db[f"booking_{book.user_id}"].insert_one(
                {
                    "is_active": True,
                    "user_id": str(user["_id"]),
                    "parking_id": str(parking["_id"]),
                    "spot_id": str(parkingDetails["_id"]),
                    "parking_name": parking["name"],
                    "user_name": user["name"],
                    "vehicle_number": book.vehicle_number,
                    "booked_at": time.time
                }
            )
            return {
                "status": True,
                "message": "booked successfully"
            }
    else:
        raise HTTPException(401, error_schema("Unauthorized token"))

@book_routes.post("/getBookings", dependencies=[Depends(JWTBearer())])
def getBookings(book: GetBookings, request: Request):
    auth = request.headers.get('Authorization').split(" ")
    auth_key = ""
    if len(auth) >= 2:
        auth_key = auth[1]
    elif len(auth) == 0:
        auth_key = ""
    else:
        auth_key = auth[0]
    if decodeLoginJWT(auth_key) == 1:
        user = db["user_collection"].find_one({"_id": ObjectId(book.user_id)})
        if user == None:
            return HTTPException(404, error_schema("User not found"))
        else:
            bookings = get_bookings_schema(db[f"booking_{book.user_id}"].find())
            return {
                "status": True,
                "message": "booked successfully",
                "data": bookings
            }
    else:
        raise HTTPException(401, error_schema("Unauthorized token"))

@book_routes.post("/validate", dependencies=[Depends(JWTBearer())])
def getValidate(book: Validate, request: Request):
    auth = request.headers.get('Authorization').split(" ")
    auth_key = ""
    if len(auth) >= 2:
        auth_key = auth[1]
    elif len(auth) == 0:
        auth_key = ""
    else:
        auth_key = auth[0]
    if decodeLoginJWT(auth_key) == 1 or decodeLoginJWT(auth_key) == 0:
        user = db["user_collection"].find_one({"_id": ObjectId(book.user_id)})
        if user == None:
            return HTTPException(404, error_schema("User not found"))
        else:
            data: bool = db[f"booking_{book.user_id}"].find({"_id": ObjectId(book.id)})["is_active"]
            if data:
                db[f"booking_{book.user_id}"].find_one_and_update({"_id": ObjectId(book.id)}, {
                    "$set": {
                        "is_active": False
                    }
                })
                return {
                    "status": True,
                    "message": "Validated successfully"
                }
            else:
                return {
                    "status": False,
                    "message": "Not validated"
                }
    else:
        raise HTTPException(401, error_schema("Unauthorized token"))