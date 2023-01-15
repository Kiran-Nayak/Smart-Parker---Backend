from fastapi import FastAPI
from routes.user_routes import user_router
from routes.parking_routes import *
from routes.parking_spot_routes import *
from routes.booking_routes import *

app = FastAPI()

app.include_router(user_router)
app.include_router(api_routes)
app.include_router(api_router)
app.include_router(book_routes)
