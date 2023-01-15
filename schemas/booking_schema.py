def error_schema(msg: str):
    return {
        "status": False,
        "message": msg
    }
def get_booking_schema(booking):
    return {
        "id": str(booking["_id"]),
        "is_active": booking["is_active"],
        "user_id": booking["user_id"],
        "parking_id": booking["parking_id"],
        "spot_id": booking["spot_id"],
        "parking_name": booking["parking_name"],
        "vehicle_number": booking["vehicle_number"],
        "booked_at": booking["booked_at"]
    }

def get_bookings_schema(bookings):
    return [get_booking_schema(booking) for booking in bookings]