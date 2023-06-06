# error schema
def error_schema(msg: str):
    return {
        "status": False,
        "message": msg
    }
def get_parking_spot_schema(parking):
    return {
        "id": str(parking["_id"]),
        "name": parking["name"],
        "is_occupied": parking["is_occupied"]
    }
def parking_spots_schema(dic):
    return [get_parking_spot_schema(parking) for parking in dic]

def response_schema(dic):
    return {
        "status": True,
        "message": "Parking lists",
        "data": parking_spots_schema(dic)
    }
def error_availability_schema():
    return {
        "status": False,
        "message": "Not available",
        "occupied": None
    }
def response_availability_schema(occupied):
    return {
        "status": True,
        "message": "Available",
        "occupied": occupied
    }