from fastapi import APIRouter, Depends, Request, HTTPException
from auth.jwt_bearer import JWTBearer
from models.book_parking import *
from models.bookings import *
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
            count = count - 1
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
            collection = db[f"booking_{book.user_id}"]
            if collection == None:
                db.create_collection(name=f"booking_{book.user_id}").insert_one(
                    dict(Booking(is_active=True, user_id=str(user["_id"]), parking_id=str(parking["_id"]), spot_id=str(parkingDetails["_id"]),parking_name= parking["name"], user_name=user["name"],vehicle_number=book.vehicle_number, type=book.vehicle_type, latitude=float(parking["latitude"]), longitude=float(parking["longitude"])))
                )
            else:
                collection.insert_one(
                    dict(Booking(is_active=True, user_id=str(user["_id"]), parking_id=str(parking["_id"]), spot_id=str(parkingDetails["_id"]),parking_name= parking["name"], user_name=user["name"],vehicle_number=book.vehicle_number, type=book.vehicle_type, latitude=float(parking["latitude"]), longitude=float(parking["longitude"])))
                )
            return {
                "status": True,
                "message": "booked successfully"
            }
    else:
        raise HTTPException(401, error_schema("Unauthorized token"))

@book_routes.post("/getActiveBookings", dependencies=[Depends(JWTBearer())])
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
            bookings = get_bookings_schema(db[f"booking_{book.user_id}"].find({"is_active": True}))
            return {
                "status": True,
                "message": "Active booking list",
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
            data: bool = db[f"booking_{book.user_id}"].find_one({"_id": ObjectId(book.id)})["is_active"]
            if data:
                db[f"booking_{book.user_id}"].find_one_and_update({"_id": ObjectId(book.id)}, {
                    "$set": {
                        "is_active": False
                    }
                })
                parking_id = db[f"booking_{book.user_id}"].find_one({"_id": ObjectId(book.id)})["parking_id"]
                type = db[f"booking_{book.user_id}"].find_one({"_id": ObjectId(book.id)})["type"]
                print(parking_id)
                print(type)
                parkingCount = db["parkings"].find_one({"_id": ObjectId(parking_id)})[type]
                db["parkings"].find_one_and_update({"_id": ObjectId(parking_id)}, {
                    "$set": {
                        type: parkingCount + 1
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