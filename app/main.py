# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, cart, checkout, products

# Create the app instance
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the routers for the API endpoints
app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(cart.router)
# app.include_router(checkout.router)
app.include_router(products.router, prefix="/products", tags=["products"])

