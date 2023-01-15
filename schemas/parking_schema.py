# error schema
def error_schema(msg: str):
    return {
        "status": False,
        "message": msg
    }

def inserted_parking_schema(msg: str, id: str):
    return {
        "status": True,
        "message": msg,
        "id": id
    }

def get_parking_schema(parking):
    return {
        "id": str(parking["_id"]),
        "name": parking["name"],
        "bike": parking["bike"],
        "car": parking["car"],
        "address": parking["address"],
        "latitude": parking["latitude"],
        "longitude": parking["longitude"]
    }

def get_parkings_schema(parkings):
    return [get_parking_schema(parking) for parking in parkings]

def response_schema(parkings):
    return {
        "status": True,
        "message": "Parking lists",
        "data": get_parkings_schema(parkings)
    }